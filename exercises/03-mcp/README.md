# Preface to the MCP Exercises

Exercise 1 built **skills**: reusable instructions for a task. Exercise 2
built **agents**: roles that decide what to do. This exercise adds the third
component, **MCP**: a standard way for OpenCode to connect to a capability
that lives outside it.

Here that capability is a **DuckDB** database holding 259,693 PDB entries —
every structure deposited between 1972 and September 2026. You will ask
questions in plain English, an agent will write SQL, and you will find out
whether the answers are true.

The server runs **on your laptop**, as a child process of OpenCode. It binds
no network port and needs no hosting, and the data never leaves your machine.
Only the language model runs on the DTU cluster.

The running theme of this exercise: **a query that succeeds is not the same as a correct answer.**
Exercise 1 made the same point about downloads — a
successful HTTP request is not the same as a downloaded structure file. A clean SQL result with a
plausible number is not necessarily correct.

## Where things live

The **MCP server** and the **exercise data** are separate, and stay separate:

```text
mcp/README.md            the server: config, setup and caveats.
exercises/03-mcp/data/   this exercise's data, with its own provenance.
```

The DuckDB MCP server opens whatever database file it is pointed at. This
exercise supplies one database; in exercise 3h you point the same server at your own data
without changing anything in `mcp/`.

You need python installation tool `uv` (or pip) installed. Check with `uv --version`; see
[the server notes](../../mcp/README.md) if it is missing.

You can install it with:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

# Exercise 3a — Connect the server, and verify that you did

In your terminal, from the workshop root, build the database from the shipped
Parquet files — about 5 MB of data becoming a 17 MB database:

```bash
uv run --with duckdb python exercises/03-mcp/scripts/make_db.py
```

It is built on your laptop rather than downloaded, so the workshop ZIP stays
small. Fetch the server package once, so its first use is not a silent 20 MB
download:

```bash
uvx mcp-server-motherduck@1.0.8 --help
```

Now start OpenCode and turn the server on, in the chat:

```text
/mcps
```

Four servers are listed, all disabled. Select **`duckdb`** — only that one —
press **space** to toggle it, then **esc**.

Leave the other three off. Each server's tool definitions are sent with
**every** request, which means the MCP is using context. That context is then not available to you
as every LLM model has some limit on context size. Thus you should only turn on the MCP's you really need.
The other three are described in
[mcp/README.md](../../mcp/README.md); `rcsb` is the live PDB, which is worth
comparing against this frozen snapshot once you have finished the exercise.

Check the saved configuration separately, in your terminal:

```bash
opencode mcp list
```

It reports `disabled`, because that is the setting on disk. Both statements
are true at once, and they are about different things: what is running now,
and what is configured. Keep them apart.

**Now quit and reopen OpenCode.** The server list is read at startup.

Then, in your terminal and **outside** the chat:

```bash
opencode mcp list
```

You want `✓ duckdb connected`.

## The meaning of the MCP being "connected"

Now break the MCP connection on purpose. Quit OpenCode and rename the database:

```bash
mv exercises/03-mcp/data/pdb.duckdb exercises/03-mcp/data/pdb.duckdb.hidden
```

Start OpenCode, toggle `duckdb` on with `/mcps` again, and it reports
**connected** — because the server process starts perfectly well. The
database is only opened when a query arrives. Ask the agent a question now
and you will get:

```text
IO Error: Cannot open database ".../pdb.duckdb" in read-only mode:
database does not exist
```

Put the file back:

```bash
mv exercises/03-mcp/data/pdb.duckdb.hidden exercises/03-mcp/data/pdb.duckdb
```

**What to notice:** "connected" means a process started and answered a
handshake. It does not mean the thing behind it works. This is the same
distinction as Exercise 2's "code generated", "viewer opened" and
"scientific content verified" — separate claims, separately checked. The
failure here was at least honest: it named the missing file instead of
inventing an answer.

---

# Exercise 3b — Ask something you cannot visually verify

Let the agent discover the data rather than telling it the schema:

> What tables are available through the DuckDB server, and what columns does
> each one have? Do not query the data yet, just describe what is there.

You should find two tables:

| Table | Rows | Contents |
|---|:---|:---|
| `entries` | 259,693 | ID, classification, deposition date, title, organism, resolution, experiment type |
| `entry_types` | 259,693 | ID, molecule type, method class |

259,693 rows is the point of the exercise. You cannot scroll through the rows, you cannot
eyeball it, and you cannot tell whether an answer about it is right by
looking at the data.

Now ask a question that sounds completely ordinary:

> What is the average resolution of structures in the PDB?

Read the SQL **before** you approve it. You will get something close to:

```sql
SELECT avg(resolution) FROM entries;
```

and an answer near **2.362 Å**.

That is an entirely plausible number. A crystallographer would not blink at
it. Write it down and move to 3c.

**What to notice:** you have a clean query, no error, and a believable
result. Every signal available to you says the task is finished.

---

# Exercise 3c — Find out whether the answer is true

Ask the agent one more question:

> How many rows are in entries, and how many of them actually have a
> resolution value? Show me both numbers.

```sql
SELECT count(*), count(resolution) FROM entries;
```

| count(\*) | count(resolution) |
|---:|---:|
| 259,693 | 244,589 |

**15,104 entries were silently excluded from that average.** `count(*)`
counts rows; `count(column)` skips NULLs, and so does `avg()`.

Find out which ones:

> Group the entries with no resolution value by experiment type.

They are not a random 6% of the PDB. **Solution NMR structures have no
resolution at all** — the concept does not apply to the method. Of 14,668
`SOLUTION NMR` entries, none carry a resolution.

## Check it yourself, without trusting the agent

This is what `exercises/03-mcp/data/pdb_sample.csv` is for: 512 entries, small
enough to open and count. In the terminal, ask to create a small python script 
to check the count of the blanks.

<details>
<summary>For reference, this python script will do the job.</summary>
  
```bash
python3 -c "
import csv
rows = list(csv.DictReader(open('exercises/03-mcp/data/pdb_sample.csv')))
blank = [r for r in rows if r['resolution'] == '']
print('rows:', len(rows), ' blank resolution:', len(blank))
print(set(r['experiment_type'] for r in blank))
"
```

```text
rows: 512  blank resolution: 26
{'SOLUTION NMR'}
```

</details>

All 26 blanks are NMR only. You have now confirmed the pattern with your own
tool, on a file you can read.

The sample is deliberately chosen (every entry where `hash(pdb_id) % 520 = 0`),
so it is reproducible — but it is a sample for checking *method_class* (see below), not a
representative subset. Do not quote percentages from it.

## Now ask the question properly

The honest version has to say which methods it utilizes, which needs the
second table:

> For each method_class, how many entries are there and what is the median
> resolution? Join entries to entry_types.

| method_class | entries | median resolution |
|---|---:|---:|
| diffraction | 207,603 | 2.00 Å |
| EM | 36,687 | 3.29 Å |
| NMR | 14,921 | — |

**What to notice:** the SQL in exercise 3b was valid, the agent did nothing wrong, and
the number was real. The asked *question* was unanswerable, and nothing in
the output said so. Deciding that "average resolution of the PDB database" must be
qualified, is *domain knowledge*. The model can not discover this from the
schema. The way to confirm the correct result: comparing `count(*)` with
`count(column)` — takes only one query.

Ask the agent to redo exercise 3b's answer as a sentence you would be willing to put
in a paper. It should name the method_class, the row count, and the exclusion.

---

# Exercise 3d — A question worth asking

Now that you can check answers, ask something real:

> For cryo-EM structures, show the median resolution per year of deposition
> from 2012 to 2024, with the number of entries each year.

| year | entries | median resolution |
|---:|---:|---:|
| 2012 | 73 | 9.20 Å |
| 2015 | 227 | 4.20 Å |
| 2019 | 1,869 | 3.50 Å |
| 2024 | 7,067 | 3.14 Å |

That is the **resolution revolution** — detector and software improvements
turning cryo-EM from a low-resolution technique into a competitor to
crystallography — visible in a table you just produced from primary data.

Apply the exercise 3c checks before believing it.<br>How many 2012 entries are there?<br>
Is a median over 73 entries the same kind of claim as one over 7,067?<br>
Did the query filter on `method_class` or on `experiment_type`, and do those two
give the same answer?<br>

Try one more of your own, and check it the same way:

- Which organisms appear most often? (Watch what happens to `Homo sapiens`
  versus `Homo sapiens; SYNTHETIC CONSTRUCT` — the field is free text, not a
  controlled vocabulary.)
- How has the share of structures solved by each method changed by decade?
- What is the resolution distribution for structures containing both protein
  and nucleic acid?

Known quirks in the data are listed in
[`PROVENANCE.md`](data/PROVENANCE.md). Read it when a result
looks strange — several strange results are genuine.

---

# Exercise 3e — Turn your checks into a skill

You have been applying the same checks by hand. That is what skills are for.

In **Plan** mode, with `skill-builder` from Exercise 1e:

> Use skill-builder to design a skill for answering questions about the PDB
> DuckDB database. It should state which tables and columns it used, report
> the SQL and the row count with every answer, and require that any question
> about resolution says which experiment types are included, because NMR
> entries have no resolution. It must report a zero-row result as zero rows.
> Propose it before implementing.

Build it, then re-ask an exercise 3b style question and see whether the answer arrives
with its evidence attached.

**What to notice:** the skill does not execute anything. The MCP server runs
the SQL; the skill says what a trustworthy answer has to contain. Guidance and
capability are separate, and you have now used both on the same task.

---

# Exercise 3f — Read-only is not as read-only as it sounds

The server is started in read-only mode. Test what that covers.

> Try to delete all entries with no resolution from the database.

Refused, by DuckDB itself:

```text
Cannot execute statement of type "DELETE" on database "pdb"
which is attached in read-only mode
```

`CREATE`, `UPDATE` and `ATTACH` are refused too. Now try this one:

> Run this query: COPY (SELECT 1 AS x) TO 'exercises/03-mcp/data/PROOF.parquet' (FORMAT parquet)

```bash
ls exercises/03-mcp/data/PROOF.parquet
```

**It succeeded, and a new file exists on your disk.**<br>
A read-only *database* does not mean a read-only *filesystem*.

Delete the file:

```bash
rm exercises/03-mcp/data/PROOF.parquet
```

This is the same lesson as Exercise 2's permission section: `edit: deny` does
not make an agent read-only when `bash` can still modify files. A safety
property is only as broad as the mechanism enforcing it. If you want the
agent restricted, restrict the tool:

```yaml
permission:
  duckdb_execute_query: ask
  duckdb_list_tables: allow
  duckdb_list_columns: allow
```

Add a block like that to an agent of your own from Exercise 2b and confirm it
prompts you. Check the tool names your OpenCode version actually registers —
a permission rule that matches nothing restricts nothing, and says so
nowhere.

**Take-home message:** If you have important data you must take great
care to restrict your agent from modifying it - include all tools the agent uses.
You are not necessarily informed about modification.<br>
Think about it like making a deal with the devil.

---

# Exercise 3g — When is an MCP server worth it?

Do one of your earlier questions a different way. With the server off
(`/mcps`, space to toggle it off), ask an agent with `bash` permission to
answer the same question using the `duckdb` command-line tool or Python.

Compare:

- Which was quicker to set up?
- Which action was easier for you to review before approving it?
- Which would still work on a laptop without `uv`?
- Which would you rather hand to someone else?

There is a real cost to a server. Every tool it exposes is described in
**every request**:

| Server | Tools | Tool definitions | Share of a 16,384-token DTU context |
|---|---:|---:|---:|
| `duckdb` | 4 | ~780 tokens | 5% |
| BioMCP 0.7.0 | 83 | ~17,377 tokens | **106%** |

BioMCP covers 43 biomedical databases — PubMed, BLAST, UniProt, Ensembl,
KEGG — and is actively maintained. Its tool list alone does not fit in a DTU
model's context window, before anyone asks anything. On a small model the
limiting factor of an MCP server is how many tools it has, not how much it
can do.

**What to notice:** MCP is not automatically the better option. It is worthwhile
when a capability is reusable, hard to reproduce with a shell command, and
narrow enough to stay affordable. "There is an MCP server for it" is not a
reason to connect one.

---

# Exercise 3h — Point it at your own data

Nothing you have done so far was specific to the PDB database. The MCP server takes a
database path, so give it a different one.

Build a database from a CSV you care about — one of your own files, or an
output from exercise 1.<br>
Here are some data sets (already downloaded) if you don't have one at hand:<br>
[Palmer Penguins](https://allisonhorst.github.io/palmerpenguins/) for data exploration and visualization.<br>

```bash
uv run --with duckdb python -c "
import duckdb
con = duckdb.connect('my_data.duckdb')
con.execute(\"CREATE TABLE measurements AS SELECT * FROM read_csv('my_file.csv')\")
con.close()"
```

Point the MCP server at it and restart OpenCode:

Point the server at it by editing one line in `opencode.json`:

```json
"--db-path", "my_data.duckdb",
```

Restart OpenCode — configuration is read at startup, unlike the `/mcps`
toggle — and turn the server on again. Ask the agent what tables exist, and
run the same checks from exercise 3c: how many rows, how many non-null, what does the
count tell you that the answer did not.

**What to notice:** you changed one argument. The server, the four tools and
the whole configuration were unchanged, because a DuckDB MCP server is not a
PDB tool — it is a SQL tool that Exercise 3 happened to hand a PDB database.
When you next consider adding an MCP server, ask what it is actually coupled
to, and keep its data somewhere it can be replaced.

To go back, set `--db-path` to `exercises/03-mcp/data/pdb.duckdb` again.

---

# Epilogue

The dataset is a frozen snapshot, built from public wwPDB index files on
18 September 2026. It will not match a live PDB query made later, which is
expected. Sources, schema and quirks are in
[`PROVENANCE.md`](data/PROVENANCE.md); the MCP server
configuration and what has and has not been tested are in
[the server notes](../../mcp/README.md).

To put the workshop back as you found it: nothing to undo in the
configuration, because `/mcps` never changed it. Delete
`exercises/03-mcp/data/pdb.duckdb` if you want the 17 MB back.

Previous: [Exercise 2 — Agents](../02-agents/README.md) · Next: [Exercise 4 — Share what you built](../04-share/README.md).
