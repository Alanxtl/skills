---
name: codex-sidebar-history-recovery
description: Diagnose and restore Codex Desktop thread history when the sidebar only shows the current conversation, search/list_threads cannot find older conversations, or recovered ~/.codex sessions exist but are not visible in the Desktop UI. Use for Codex Desktop, app-server, session_index.jsonl, state_*.sqlite, ~/.codex/sessions, archived_sessions, and remote host sidebar history issues.
---

# Codex Sidebar History Recovery

## Purpose

Recover visibility of existing Codex conversations in Codex Desktop's sidebar. Treat this as an index/cache/app-server problem unless evidence shows raw session files are missing.

## Safety Rules

- Do not delete, move, truncate, or rewrite `~/.codex/sessions`, `~/.codex/archived_sessions`, or `rollout-*.jsonl`.
- Before modifying any Codex state file, create timestamped backups of `~/.codex/state_*.sqlite` and `~/.codex/session_index.jsonl`.
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
