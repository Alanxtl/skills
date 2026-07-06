---
name: codex-sidebar-history-recovery
description: Diagnose and restore Codex Desktop thread history when the sidebar only shows the current conversation, search/list_threads cannot find older conversations, or recovered ~/.codex sessions exist but are not visible in the Desktop UI. Use for Codex Desktop, app-server, session_index.jsonl, state_*.sqlite, ~/.codex/sessions, archived_sessions, and remote host sidebar history issues.
---

# Codex Sidebar History Recovery

## Purpose

Recover visibility of existing Codex conversations in Codex Desktop's sidebar. Treat this as a provider-metadata/index/cache/app-server problem unless evidence shows raw session files are missing.

## Safety Rules

- Do not delete, move, truncate, or rewrite message content in `~/.codex/sessions`, `~/.codex/archived_sessions`, or `rollout-*.jsonl`.
- Provider metadata repair may rewrite only the first `session_meta` line in `rollout-*.jsonl`; never edit conversation event lines.
- Before modifying any Codex state file, create timestamped backups of `~/.codex/state_*.sqlite`, `~/.codex/sqlite/state_*.sqlite`, `~/.codex/session_index.jsonl`, and `.codex-global-state.json` when present.
- Prefer read-only inspection first. Restart app-server only after confirming the session records exist.
- If multiple users have app-server processes on a shared host, only touch the current user's processes and files.
- Warn the user that app-server restart may refresh/reconnect the Desktop host but should not affect repository files.

## Diagnosis Workflow

1. Confirm the raw history exists:

```bash
find ~/.codex/sessions ~/.codex/archived_sessions -type f -name 'rollout-*.jsonl' 2>/dev/null | wc -l
find ~/.codex/sessions ~/.codex/archived_sessions -type f -name 'rollout-*.jsonl' 2>/dev/null | sort | tail -20
```

2. Inspect the Codex state database:

```bash
sqlite3 ~/.codex/state_5.sqlite "PRAGMA table_info(threads);"
sqlite3 ~/.codex/state_5.sqlite "SELECT COUNT(*), SUM(archived), SUM(has_user_event) FROM threads;"
sqlite3 ~/.codex/state_5.sqlite "SELECT id, substr(title,1,80), archived, has_user_event, cwd, source, thread_source FROM threads ORDER BY updated_at DESC LIMIT 20;"
```

If the host has a differently numbered state DB, use the newest `~/.codex/state_*.sqlite`.

3. Compare list visibility with direct thread readability:

- Use the Codex app thread tools when available.
- If `read_thread(threadId, hostId=...)` can open a thread but `list_threads` or sidebar search cannot find it, the content exists and the list index/cache is stale.

4. Check `session_index.jsonl`:

```bash
wc -l ~/.codex/session_index.jsonl
head -3 ~/.codex/session_index.jsonl
```

If `threads` has many more rows than `session_index.jsonl`, rebuild the index from the DB.

## Provider Metadata Sync First

Before rebuilding `session_index.jsonl`, synchronize Codex provider visibility metadata when history exists but the sidebar or `/resume` is filtered to the wrong provider. This addresses mismatches among rollout metadata, SQLite thread metadata, and Codex Desktop project-root cache.

1. Determine the current provider:

- Read the root-level `model_provider` from `~/.codex/config.toml`.
- If no root-level `model_provider` is present before the first TOML table, treat the current provider as Codex's implicit default: `openai`.

2. Create a timestamped backup before any write:

```bash
backup="$HOME/.codex/backups_state/sidebar-history-recovery/$(date +%Y%m%dT%H%M%S)"
mkdir -p "$backup"
cp -a ~/.codex/session_index.jsonl "$backup/" 2>/dev/null || true
cp -a ~/.codex/.codex-global-state.json "$backup/" 2>/dev/null || true
cp -a ~/.codex/.codex-global-state.json.bak "$backup/" 2>/dev/null || true
cp -a ~/.codex/state_*.sqlite* "$backup/" 2>/dev/null || true
mkdir -p "$backup/sqlite"
cp -a ~/.codex/sqlite/state_*.sqlite* "$backup/sqlite/" 2>/dev/null || true
```

3. Synchronize rollout provider metadata:

- Scan `~/.codex/sessions/**/rollout-*.jsonl` and `~/.codex/archived_sessions/**/rollout-*.jsonl`.
- For each file, parse only the first line when it is `{"type":"session_meta", ...}`.
- If `payload.model_provider` differs from the current provider, rewrite only that first line to the current provider.
- Preserve all following conversation event lines exactly.
- While scanning, collect:
  - `payload.id` as the thread id.
  - `payload.cwd` as the thread working directory.
  - Whether any line contains a user message.
  - Whether the file contains `encrypted_content`.

4. Synchronize SQLite thread metadata:

- Open each existing state database candidate:
  - `~/.codex/sqlite/state_5.sqlite`
  - `~/.codex/state_5.sqlite`
  - any `sqlite_home` configured in `config.toml`
  - any `CODEX_SQLITE_HOME` override
- In one transaction per database:
  - Set `threads.model_provider` to the current provider when it differs.
  - Set `threads.has_user_event = 1` for thread ids where rollout scanning found a user message.
  - Set `threads.cwd` from rollout `session_meta.payload.cwd` when the database row differs.

5. Normalize Codex Desktop project-root cache:

- If `~/.codex/.codex-global-state.json` exists, normalize project path entries in:
  - `electron-saved-workspace-roots`
  - `project-order`
  - `active-workspace-roots`
  - `electron-workspace-root-labels`
  - `open-in-target-preferences.perPath`
- On Windows, convert extended paths such as `\\?\C:\...` and `\\?\UNC\...` to the Desktop-visible form.

6. Warn about encrypted content:

- Visibility repair does not re-encrypt `encrypted_content`.
- Old sessions may become visible but still fail when continued or compacted across a different provider/account.
- If rollout files or SQLite are locked, close Codex Desktop/app-server and retry.

## Rebuild session_index.jsonl

Back up first:

```bash
cp ~/.codex/session_index.jsonl ~/.codex/session_index.jsonl.backup-$(date +%Y%m%dT%H%M%S)
cp ~/.codex/state_5.sqlite ~/.codex/state_5.sqlite.backup-$(date +%Y%m%dT%H%M%S)
```

Then rebuild a minimal index from `threads`:

```bash
sqlite3 -json ~/.codex/state_5.sqlite \
  "SELECT id, COALESCE(NULLIF(title,''), NULLIF(preview,''), 'Untitled') AS thread_name, datetime(updated_at, 'unixepoch') || 'Z' AS updated_at FROM threads ORDER BY updated_at;" \
  | jq -c '.[]' > ~/.codex/session_index.jsonl
```

Validate:

```bash
jq -c . ~/.codex/session_index.jsonl >/dev/null
wc -l ~/.codex/session_index.jsonl
```

## Refresh app-server

If raw sessions and DB rows exist but Desktop still only shows the current conversation, refresh the remote/local app-server.

1. Inspect processes:

```bash
ps -ef | rg 'codex app-server|app-server proxy' | rg -v rg
```

2. Prefer managed daemon restart:

```bash
codex app-server daemon restart
```

3. If restart reports that the app-server is running but not managed by the daemon, terminate only the current user's old `codex app-server --listen unix://` process with `SIGTERM`. Do not kill other users' processes.

```bash
kill -TERM <node-wrapper-pid> <codex-binary-pid>
```

After this, Codex Desktop should reconnect and start a fresh app-server/proxy. Recheck the sidebar. If it does not reconnect automatically, ask the user to refresh/reopen the host connection in Codex Desktop.

## Interpretation

Common root cause: conversation data is intact, but Codex Desktop's sidebar list is reading a stale host-side thread index or an old long-running app-server cache. Direct thread reads may still work by ID because they bypass the stale list path.

Successful recovery usually has these signals:

- `threads` table contains the expected conversations.
- `read_thread` can open old threads by ID.
- `session_index.jsonl` count roughly matches `threads`.
- Restarting the stale app-server makes the Desktop sidebar list repopulate.

## Optional Transcript Export

If the UI still does not recover quickly, export readable Markdown from `rollout-*.jsonl` or `threads.rollout_path` into `~/.codex/recovered_transcripts/` as a fallback for the user. Keep this as a fallback; the primary goal is to restore sidebar visibility.
