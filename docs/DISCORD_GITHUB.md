# Discord reports and GitHub issues

GitHub is the technical source of truth: an issue keeps the diagnosis,
versions, labels, decisions, and fix. Discord remains the space for community
conversation and game feedback.

The bot links a Discord forum thread and an issue. Existing bug reports and
suggestions can be imported once by staff; future reports can use `/github
create`. The bot mirrors unlinked GitHub issues labelled `bug`, `idea`, or
`enhancement` into the matching Discord forum. It only edits its own status or
mirror message, never a player message.

## Tracking labels

- `source: discord`: issue created or imported from Discord;
- `status: needs information`: insufficient detail to investigate;
- `status: needs reproduction`: waiting for a reliable reproduction;
- `status: confirmed`: observed in game or in the files;
- `status: fixed`: fixed on `dev`, awaiting validation before closure;
- `compatibility` and `balance`: optional dimensions for bugs and ideas.

Closing an issue is reflected in its Discord thread. Comments are not copied
between platforms: they are often contextual and would create duplicate,
unreadable discussions. GitHub titles, descriptions, labels, and state are
reflected in bot-created Discord mirrors; a Discord report creates its linked
issue from its initial submitted content.
