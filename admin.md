# Workshop administration

Notes for Peter and Dimitrios. For participant setup, see the [student README](README.md).

These commands refer to `/home/local/workshop` on the compute nodes, not the downloaded repository on a student's laptop.

## Connect to the server

```bash
ssh -J dimkan@login.healthtech.dtu.dk dimkan@compute04
cd /home/local/workshop
```

You can connect to compute05 instead. Run the commands below on a compute
node, not the login node. The folder belongs to `dimkan`; Peter needs access
through that account or administrator-arranged permissions.

## Start, stop and check the models

These commands work from either compute node:

| Scope | Start | Stop | Check status |
|---|---|---|---|
| compute04 models | `bash bin/llm start compute04` | `bash bin/llm kill compute04` | `bash bin/llm status compute04` |
| compute05 model | `bash bin/llm start compute05` | `bash bin/llm kill compute05` | `bash bin/llm status compute05` |
| Everything | `bash bin/llm start all` | `bash bin/llm kill all` | `bash bin/llm status all` |

**Before the workshop, run `bash bin/llm start all` and check the readiness summary for both nodes.**

Start commands also start any missing connection services. Already-running
models are kept. If a start fails, read the error before trying again.
`kill` and `stop` mean the same thing: stop our workshop processes safely.
To restart, stop first, wait for success, then start.

> The shared connection service, called the **gateway**, runs on compute04.
> Stopping compute04 disconnects every model, including Qwen 3.8.
> Starting compute05 automatically starts that gateway if needed, but does
> not start compute04's other models.

No tmux is needed, and closing SSH leaves the models running. After a server
reboot, start them again. Only use this setup during the approved workshop
reservation; do not bypass the checks for occupied GPUs.

For just one model, run its command on the node listed below:

```bash
# Example on compute04
bash bin/llm start mistral
bash bin/llm stop mistral

# Example on compute05
bash bin/llm start qwen38
bash bin/llm stop qwen38
```

To preview a command without doing anything, add `--dry-run`.
For more options, run `bash bin/llm --help`.

## Model settings

| Model ID | Node | GPUs | Configured context | Configured ceiling | Native target | Server output cap |
|---|---|---|---:|---:|---:|---:|
| `qwen36` | compute04 | 0, 1 | 16384 | 65536 | 262144 | 4096 |
| `qwen38` | compute05 | 0, 1 | 32768 | 65536 | 262144 | 8192 |
| `mistral` | compute04 | 2 | 16384 | 32768 | 131072 | 4096 |
| `gptoss` | compute04 | 3 | 16384 | 32768 | 131072 | 8192 |

**Deployment check, 21 September 2026:** no server settings were changed.
compute04 reports `Failed to initialize NVML: Driver/library version mismatch`
(NVML library 580.178). All four public `/models` routes returned HTTP 503.
compute05's GPU query works, but its public route is also unavailable.
Do not restart compute04 models until Peter resolves the driver issue. This
does not imply that the mismatch explains every endpoint failure.

The native targets come from the installed checkpoint configuration, not a
capacity test. Historical vLLM memory logs show that the current allocations
cannot simply be assumed to fit every target. Higher limits remain **pending**.

**Context** is the total space for the conversation and answer, measured in
tokens. It includes previous messages, instructions and tool results.
**Output** is the maximum length of the model's answer, including reasoning.

To change a model's context, stop it first. For example, on compute04:

```bash
bash bin/llm stop mistral
bash bin/llm start mistral --context 32768
```

- This changes one launch only. To save a default, edit that model's
  `context` in `config/models.json` on its node, then stop/start it.
- Keep student `limit.context` defaults at 16384, or 32768 for Qwen 3.8,
  even after larger server capacities are verified. Keep all student output
  limits at 4096. Students may use a smaller budget than the server ceiling;
  they must restart OpenCode after a configuration change.
- Larger contexts need more GPU memory and must be tested. The launcher
  permits up to 65536 for the Qwen models and 32768 for Mistral/GPT-OSS;
  those are allowed settings, not guaranteed working capacities.
- To return Mistral to its default, stop it and start it with
  `--context 16384`. An already-running model ignores a new start request.
- Keep student output at 4096. The server may reduce it further to fit the
  conversation. If the conversation is too long, compact it or start a new chat.

The output caps are set in compute04's `app/gateway.py`, separately from
server context. Changing that code requires tests and a gateway restart.

### Complete the maximum-context rollout when the servers are healthy

1. Have Peter resolve compute04's driver mismatch, then confirm GPU visibility
   and the approved workshop reservation. Preserve the GPU assignments and
   occupied-GPU checks. Do not repair drivers from this repository.
2. Test one model at a time with a temporary validation profile targeting the
   native value above. Preserve the current configuration and working model
   state for recovery. Do not bypass vLLM's model-length/memory validation,
   change quantization or add context extension to force a result.
3. Verify the running `max_model_len`, a normal response, long-input responses,
   streaming and tool-call round trips. Test concurrent requests, cancellation
   and busy responses; a startup health ping alone is insufficient. Report
   observed latency and failures rather than claiming a fixed user capacity.
4. Both the gateway and model endpoint currently cap request bodies at 2 MiB.
   Test representative long requests. If that blocks otherwise valid input,
   raise the workshop application caps to 8 MiB and have Peter check matching
   HTTPS-proxy limits; retain finite limits. Keep answer caps unchanged.
5. Only after a target passes, persist its `context` and `max_context` in the
   node's `config/models.json`. Synchronize Qwen 3.8's profile on compute04 as
   well as compute05. Verify the public endpoint after the controlled restart.
   If it fails, restore the previous working profile and report the lower
   verified capacity; do not advertise the native target as available.
6. Update this status and the student/MCP notes with the actual deployed maxima.
   Keep the small student defaults. Require organiser approval for student
   budgets above 32768 and explicitly discourage 262144 for ordinary tasks.

Students edit only the context budget for their selected model in their own
project. That budget affects all agents using the same provider/model entry.
Do not confuse a high ceiling with every request using that many tokens: it
is actual long contexts and concurrent work that consume shared capacity.

The genome reference in Exercise 2c can be checked offline now. Its full
five-model rehearsal and the larger-context rollout remain separate pending
checks. Do not substitute saved reference outputs for evidence of a live run.

## Check connections and investigate errors

The launcher waits up to five minutes per node. It checks the gateway and
model health, then sends a tiny test message through each model's public URL.
Each model is marked **READY** only after it returns answer text. Models are
checked independently, so a slow or failed model does not hide the others.

The final summary lists every requested model as **READY** or **NOT READY**,
with a reason for any failure. A failure or timeout makes the command report
an incomplete startup; it does not stop the models that are running. Check
both nodes: compute04 being ready does not mean compute05 also started.

To repeat the checks, run the same start command again. Already-running
models are not reloaded. This tests basic replies, not every possible
OpenCode tool call or a student's network connection.

From a computer with access to the teaching URL:

```bash
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/health
curl --fail --max-time 15 https://teaching.healthtech.dtu.dk/workshop/mistral/models
```

Replace `mistral` with another model ID. Look for `available: true`;
`max_model_len` shows the running context size.

On the model's node:

```bash
bash bin/llm status all
tail -n 60 logs/direct-mistral.log
```

Use `direct-qwen36.log`, `direct-qwen38.log` or `direct-gptoss.log` for
the other models. Connection-service errors are in compute04's
`logs/direct-gateway.log`. Re-running the model's start command restores
missing required services without reloading an already-running model.

To restart only the gateway, on compute04:

```bash
bash bin/llm stop gateway
bash bin/llm start gateway
```

This briefly interrupts all connections but leaves the models loaded.

## Files and ports we maintain

| Location on the cluster | What it is for |
|---|---|
| `bin/llm.py` | Starting, stopping and checking services |
| `app/` | Connection handling and model requests |
| `config/models.json` | Model settings and server addresses |
| `config/model-endpoints.json`, `config/reverse-proxy.json` | Public-connection settings |
| `config/access-policy.json` | Whether students need an API key |
| `models/`, `envs/`, `runtime/` | Models and installed software; leave these in place |
| `logs/`, `run/`, `cache/`, `tmp/` | Logs and working files; do not clear while running |

We use **vLLM 0.19.0** to run the models. Peter's HTTPS server forwards
each model URL to the corresponding HTTP address.

## Model endpoints

This is the maintained endpoint reference. These are the configured addresses,
not a live service-status report. Use the readiness checks above before sharing.

| Model ID | Public Base URL for OpenCode | HTTP upstream for Peter's proxy | Node |
|---|---|---|---|
| `qwen36` | `https://teaching.healthtech.dtu.dk/workshop/qwen36` | `http://10.57.11.104:28102` | compute04 |
| `qwen38` | `https://teaching.healthtech.dtu.dk/workshop/qwen38` | `http://10.57.11.105:28101` | compute05 |
| `mistral` | `https://teaching.healthtech.dtu.dk/workshop/mistral` | `http://10.57.11.104:28103` | compute04 |
| `gptoss` | `https://teaching.healthtech.dtu.dk/workshop/gptoss` | `http://10.57.11.104:28104` | compute04 |

Use the public Base URLs exactly as shown: **do not append `/v1`**.
OpenCode appends request paths such as `/chat/completions`; health and model
listing use `/health` and `/models`. Preserve that suffix when forwarding each
public route to its model endpoint. TLS is handled by Peter's HTTPS proxy;
these internal upstreams use HTTP. Students should not use the internal IPs.

The shared gateway is on compute04 port 28100. It must reach Qwen 3.8's
private model service on compute05 port 28201. These are not student URLs.

Student API keys are currently disabled. Keep the teaching URLs restricted
to the intended audience. Internal credentials are still required; do not
publish server `config/`, keys or logs. The student `opencode.json`
contains no credentials and is intended for sharing.

To check code changes on compute04:

```bash
source bin/workshop-env.sh
PYTHONPATH=/home/local/workshop envs/manage/bin/python -m unittest discover -s tests -p 'test_*.py'
```
