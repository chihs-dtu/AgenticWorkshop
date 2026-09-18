# MCP servers

Notes on the MCP servers this project configures. **This folder holds
documentation only** — there is no server code here, and nothing to install
from it.

| Server | Connects to | Used by |
|---|---|---|
| `duckdb` | any DuckDB database file | [Exercise 3](../exercises/03-mcp/README.md) |

## Where a server actually lives

Three separate things, in three places, none of them this folder:

| Part | Where it is |
|---|---|
| The program | A PyPI package. `uvx` downloads it into `~/.cache/uv/` on first use. |
| The configuration | The `mcp.duckdb` block in `opencode.json`, at the project root. |
| The data it opens | Whoever owns it. For `duckdb`, `exercises/03-mcp/data/`. |

OpenCode starts the program as a **child process on your laptop** and talks to
it over stdin and stdout: it writes a JSON line to the child's stdin and reads
one back from its stdout. The server binds no network port, needs no hosting,
and exits when that pipe closes. Only the language model runs on the DTU
cluster.

Someone does host the *file*: PyPI serves the package from
`files.pythonhosted.org`, published by MotherDuck. `uvx` downloads it once,
into `~/.cache/uv`. Nobody hosts a running instance of it.

**One outbound request to be aware of.** The FastMCP framework the server is
built on checks PyPI for a newer version of itself
(`GET https://pypi.org/pypi/fastmcp/json`, 2-second timeout, cached). It sends
no query, no data and no identifiers, and the server works offline without it.
Your database contents never leave your machine, but the process is not
completely silent, and saying so is more useful than claiming it is.

Creating a folder does not connect a server, and neither does a permission rule.

## Servers here, data elsewhere

A server is a **capability**; a dataset is **someone's material**. They have
different owners and lifetimes, so they stay apart. The DuckDB server has no
knowledge of the PDB: Exercise 3 supplies a PDB database for it to open, and
changing one `--db-path` line points the same server at anything else. If a
server ever *is* specific to one dataset, name it for that pairing rather than
hiding the coupling.

---

# The `duckdb` server

Lets an agent query a DuckDB database by writing SQL.

## Setup

**1. Build a database.** This server does not create one. For Exercise 3:

```bash
uv run --with duckdb python exercises/03-mcp/scripts/make_db.py
```

**2. Warm the package** once, so its first use is not a silent 20 MB download:

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

**3. Turn it on** with OpenCode's built-in command, in the chat:

```text
/mcps          then press space on "duckdb"
```

No restart, nothing to edit. You need `uv`
(`curl -LsSf https://astral.sh/uv/install.sh | sh`) and Python 3.10+.
WSL2 users: install `uv` **inside** WSL2, where OpenCode runs.

## `/mcps` is a session toggle, not a saved setting

Measured against the running OpenCode server: toggling `duckdb` on took its
status from `disabled` to `connected` immediately, and afterwards
`opencode.json` was **byte-for-byte unchanged** and nothing was written to
OpenCode's state directory. The toggle takes effect at once, lasts for that
OpenCode run only, and never edits your configuration.

That is why this project ships `"enabled": false`. A student doing Exercises 1
and 2 never meets a server they have not set up, never pays ~780 tokens of
tool definitions in every request, and turning it on for Exercise 3 changes
nothing on disk. Set `"enabled": true` by hand if you want it on by default —
that is the setting `/mcps` deliberately does not touch.

On the command line, `opencode mcp` offers `add`, `list`, `auth`, `logout` and
`debug`, but no enable or disable. `opencode mcp list` reports the saved
configuration, not what is running.

## The configuration

```json
"duckdb": {
  "type": "local",
  "enabled": false,
  "command": [
    "uvx", "mcp-server-motherduck@1.0.8",
    "--db-path", "exercises/03-mcp/data/pdb.duckdb",
    "--max-rows", "100",
    "--max-chars", "8000"
  ],
  "timeout": 60000
}
```

| Choice | Reason |
|---|---|
| `@1.0.8` | Pinned. An upstream release cannot change behaviour on the morning of the workshop. |
| a file, not `:memory:` | The server refuses `:memory:` unless you also pass `--read-write`, because in-memory databases are always writable. A file gives real read-only access. |
| relative path | OpenCode starts the server in the project root, so no per-laptop absolute paths. |
| `--max-rows 100` | The DTU models hold 16,384 tokens. The default cap is 1024 rows; one careless `SELECT *` would fill the conversation. |
| `--max-chars 8000` | The same, for wide text columns. |

To serve a different database, change `--db-path` and restart OpenCode.
Configuration is read at startup, unlike the `/mcps` toggle.

## What it exposes

Four tools: `execute_query` (argument `sql`), `list_tables`, `list_columns`
(argument `table`) and `list_databases`. Their definitions cost about **780
tokens in every request** — roughly 5% of a DTU model's context before any
data comes back.

`switch_database_connection` is **not** exposed, because
`--allow-switch-databases` is not set. The agent cannot repoint the server.

## Two results that matter

**Read-only does block database writes.** `CREATE TABLE`, `UPDATE`, `DELETE`
and `ATTACH` are all refused:
`Cannot execute statement of type "..." on database "..." which is attached in read-only mode`.

**Read-only does not stop the server writing files.** This **succeeds**
against the read-only server and creates a file on disk:

```sql
COPY (SELECT 1 AS x) TO 'PROOF.parquet' (FORMAT parquet)
```

Reading is equally open: `read_csv('...')` will open any file the server
process can reach. "Read-only" describes the *database*, not the *filesystem*
— the same distinction the agent exercises make about `edit: deny` not making
an agent read-only when it can still run shell commands. Restrict the tool,
and keep approval prompts on:

```yaml
permission:
  duckdb_execute_query: ask
  duckdb_list_tables: allow
  duckdb_list_columns: allow
```

OpenCode names MCP tools `servername_toolname`. Verify the names your version
registers before relying on a rule — one that matches nothing restricts
nothing, silently.

## Verified on 18 September 2026

macOS, OpenCode 1.18.30, `mcp-server-motherduck` 1.0.8, DuckDB 1.5.5.

- With `enabled: false`, `POST /mcp/duckdb/connect` (what `/mcps` calls) moved
  the status from `disabled` to `connected` with no restart, leaving
  `opencode.json` and OpenCode's state directory unchanged.
- With `enabled: true`, `opencode mcp list` reports `duckdb connected`.
- A missing database still reports `connected`, because DuckDB opens the file
  lazily; the failure appears per query as
  `Cannot open database ... in read-only mode: database does not exist`.
- A missing `uv` reports `duckdb failed — Executable not found in $PATH`.
- Pointing `--db-path` at an unrelated database served that schema instead,
  confirming the server is not tied to the PDB data.
- `list_tables` finds the tables; `list_columns` returns the documented types.
- Database writes refused; a `COPY ... TO` file write is not.
- `--max-rows` truncation triggers and is reported in the result.

### Not yet verified

- **A live DTU model.** All four endpoints returned HTTP 503 during this work,
  so no model has used these tools. Whether a 12B-20B model reliably writes
  correct SQL is untested, and is the first thing to check once the models run.
- **The exact permission key strings.** MCP tools attach at session time, so
  `duckdb_execute_query` follows OpenCode's documented pattern but was not
  observed directly.
- **Windows/WSL2 and Linux.** Checked on macOS only.

---

## Adding another server

Register it under `mcp` in `opencode.json` with `"enabled": false`, and add a
section to this file. Give it a folder of its own only when it needs files of
its own — documentation alone belongs here.

Check its tool count first. Every tool is described in **every** request:

| Server | Tools | Tool definitions | Share of a 16,384-token DTU context |
|---|---:|---:|---:|
| `duckdb` | 4 | ~780 tokens | 5% |
| [BioMCP](https://pypi.org/project/biomcp-server/) 0.7.0 | 83 | ~17,377 tokens | **106%** |

BioMCP covers 43 biomedical databases and is actively maintained, but its tool
list alone does not fit in a DTU model's context window, before anyone asks a
question. On small models the binding constraint is tool count, not features.
