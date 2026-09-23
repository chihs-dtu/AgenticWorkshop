# Workshop administration

Operating notes for Peter and Dimitrios. For participant setup see the
[student README](README.md).

All paths below are `/home/local/workshop` on the compute nodes, not the
repository on a laptop.

## Connect

```bash
ssh -J dimkan@login.healthtech.dtu.dk dimkan@compute04
cd /home/local/workshop
```

compute05 works the same way. Run everything on a compute node, not the login
node.

## Start, stop and check

Either node can drive both.

| Scope | Start | Stop | Status |
|---|---|---|---|
| compute04 models | `bash bin/llm start compute04` | `bash bin/llm kill compute04` | `bash bin/llm status compute04` |
| compute05 model | `bash bin/llm start compute05` | `bash bin/llm kill compute05` | `bash bin/llm status compute05` |
| Everything | `bash bin/llm start all` | `bash bin/llm kill all` | `bash bin/llm status all` |

**Before the workshop: `bash bin/llm start all`, then check the readiness
summary for both nodes.**

A start also brings up any missing connection services and leaves
already-running models alone. `kill` and `stop` are the same command. To
restart, stop, wait for success, then start.

> The **gateway** is the shared connection service and runs on compute04.
> Stopping compute04 disconnects every model, Qwen 3.8 included. Starting
> compute05 brings the gateway up if needed, but does not start compute04's
> other models.

No tmux needed; closing SSH leaves the models running. Start them again after
a reboot. Use the setup only during the approved reservation, and do not
bypass the occupied-GPU checks.

Single models run on their own node:

```bash
bash bin/llm start mistral      # compute04
bash bin/llm stop  mistral
bash bin/llm start qwen38       # compute05
bash bin/llm stop  qwen38
```

Add `--dry-run` to preview. `bash bin/llm --help` for the rest.

## Model settings

| Model ID | Node | GPUs | Configured context | Launcher ceiling | Checkpoint maximum | Output cap |
|---|---|---|---:|---:|---:|---:|
| `qwen36` | compute04 | 0, 1 | 16384 | 65536 | 262144 | 4096 |
| `qwen38` | compute05 | 0, 1 | 32768 | 65536 | 262144 | 8192 |
| `mistral` | compute04 | 2 | 16384 | 32768 | 131072 | 4096 |
| `gptoss` | compute04 | 3 | 16384 | 32768 | 131072 | 8192 |

The checkpoint maximum is what the model supports, not what the current GPU
allocation fits. The launcher ceiling is what it will accept without testing.

**Context** is the whole conversation plus the answer, in tokens, including
instructions and tool results. **Output** is the answer alone.

Change a model's context by stopping it first:

```bash
bash bin/llm stop mistral
bash bin/llm start mistral --context 32768
```

- That changes one launch. For a persistent default, edit `context` in the
  node's `config/models.json`, then stop and start.
- A running model ignores a new start request. Revert with
  `bash bin/llm stop mistral` then `bash bin/llm start mistral --context 16384`.
- Student `limit.context` defaults stay at 16384, 32768 for Qwen 3.8, with
  output 4096. Students restart OpenCode after a config change.
- Output caps live in compute04's `app/gateway.py`, separate from server
  context. Changing them needs tests and a gateway restart.

### Raising the context limits

1. Confirm GPU visibility and the reservation. Keep the GPU assignments and
   occupied-GPU checks.
2. Test one model at a time against its checkpoint maximum, using a temporary
   profile and keeping the working configuration for recovery. Do not bypass
   vLLM's length and memory validation, change quantization, or add context
   extension.
3. Check the running `max_model_len`, a normal response, a long input,
   streaming, and a tool-call round trip. Then concurrent requests,
   cancellation and busy responses.
4. The gateway and model endpoints cap request bodies at 2 MiB. If that blocks
   valid input, raise the application caps to 8 MiB and have Peter match the
   HTTPS-proxy limit. Keep answer caps as they are.
5. Once a target passes, persist `context` and `max_context` in that node's
   `config/models.json`, synchronise Qwen 3.8's profile on both nodes, and
   check the public endpoint after the restart. If it fails, restore the
   previous profile.
6. Update the student defaults only if you intend students to use more.
   Budgets above 32768 need organiser approval.

## Checks and troubleshooting

The launcher waits up to five minutes per node, checks gateway and model
health, then sends a test message through each public URL. A model is
**READY** only once it returns text. Models are checked independently, and the
summary lists each as READY or NOT READY with a reason. Check both nodes.

Re-running the start command repeats the checks without reloading running
models.

**Isolation warning (checked 23 September 2026):** the shared gateway's
`/health` and `/models` handlers probe every configured backend, including
compute05. A compute04-only start's normal readiness checks can therefore
contact compute05. Do not use those checks when compute05 must be completely
untouched. Test a selected compute04 model with a direct chat request instead;
do not stop the shared gateway while compute05 is in use.

From anywhere with access to the teaching URL:

```bash
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/health
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/models
```

Swap `mistral` for another model ID. `available: true` is the one to look for;
`max_model_len` shows the running context size.

On the node:

```bash
bash bin/llm status all
tail -n 60 logs/direct-mistral.log
```

Also `direct-qwen36.log`, `direct-qwen38.log`, `direct-gptoss.log`, and
`logs/direct-gateway.log` on compute04 for connection-service errors.

Gateway only, on compute04:

```bash
bash bin/llm stop gateway
bash bin/llm start gateway
```

That interrupts connections briefly and leaves the models loaded.

## Files and ports

| Location | Purpose |
|---|---|
| `bin/llm.py` | Start, stop and status |
| `app/` | Connection handling and model requests |
| `config/models.json` | Model settings and server addresses |
| `config/model-endpoints.json`, `config/reverse-proxy.json` | Public-connection settings |
| `config/access-policy.json` | Whether students need an API key |
| `models/`, `envs/`, `runtime/` | Models and installed software. Leave in place |
| `logs/`, `run/`, `cache/`, `tmp/` | Logs and working files. Do not clear while running |

vLLM 0.19.0 runs the models. Peter's HTTPS server forwards each public model
URL to its HTTP address.

## Endpoints

| Model ID | Public Base URL | HTTP upstream | Node |
|---|---|---|---|
| `qwen36` | `https://teaching.healthtech.dtu.dk/workshop/qwen36` | `http://10.57.11.104:28102` | compute04 |
| `qwen38` | `https://teaching.healthtech.dtu.dk/workshop/qwen38` | `http://10.57.11.105:28101` | compute05 |
| `mistral` | `https://teaching.healthtech.dtu.dk/workshop/mistral` | `http://10.57.11.104:28103` | compute04 |
| `gptoss` | `https://teaching.healthtech.dtu.dk/workshop/gptoss` | `http://10.57.11.104:28104` | compute04 |

Use the public Base URLs exactly as shown and **do not append `/v1`**.
OpenCode appends `/chat/completions`; health and listing use `/health` and
`/models`. Preserve that suffix when forwarding. TLS is handled by the HTTPS
proxy, so the upstreams are HTTP.

The gateway is on compute04 port 28100 and must reach Qwen 3.8's service on
compute05 port 28201.

Student API keys are disabled.

## Tests

On compute04:

```bash
source bin/workshop-env.sh
PYTHONPATH=/home/local/workshop envs/manage/bin/python -m unittest discover -s tests -p 'test_*.py'
```
