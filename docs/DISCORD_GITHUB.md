# Discord reports and GitHub issues

GitHub is the technical source of truth: an issue keeps the diagnosis, version,
labels, decisions and fix. Discord remains the place for community conversation and
the first report in the format players find easiest.

## Scope and safety

Only the `bug-reports`, `suggestions` and private `beta-bug-reports` forums are
synchronised. A new player post there creates a matching GitHub issue. The bot writes
only its own status card and comment mirrors; it never edits, deletes or moves a
player's post, thread, screenshot or conversation.

Free discussion in a report stays on Discord. A player or staff member can use
`/github reply` to send a deliberate follow-up to the linked issue. GitHub comments
are mirrored back into the matching Discord thread. This prevents accidental copying,
noise and feedback loops while keeping the investigation visible on both sides.

## Labels

- `bug` or `idea`: issue kind;
- `source: discord` or `source: github`: original intake;
- `release: beta`: private beta report, never the Workshop live build;
- `status: needs information`: context is insufficient to investigate;
- `status: needs reproduction`: waiting for a reliable reproduction;
- `status: confirmed`: observed in game or in source files;
- `status: fixed`: fixed on `dev`, awaiting validation before closure;
- `compatibility` and `balance`: optional cross-cutting dimensions.

The GitHub templates use the same language as Discord: version, starting age,
in-game date, DLC/mod list, expected result, observed result, reproduction and
evidence. Do not open the same report in both places.

## Operations

The bot uses SQLite on its persistent Docker volume and a signed GitHub webhook;
delivery IDs are retained to make retries idempotent. A slow reconciliation remains
as a safety net. The operational setup, secret variables and health check live in
`C:\Users\Public\AdAstra\discord-bot\LIEN_GITHUB.md` and are intentionally not
stored in this mod repository.
