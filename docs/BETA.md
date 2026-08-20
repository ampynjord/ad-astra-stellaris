# Testing the GitHub beta

GitHub beta releases are experimental local builds. Steam Workshop remains the
stable channel.

## Installation

1. Download the beta `.zip` from the matching GitHub pre-release.
2. Extract it directly into your Stellaris user folder:
   `Documents/Paradox Interactive/Stellaris/`.
3. Open the Stellaris launcher and enable **Ad Astra: Origins - Beta**.
4. Disable the Steam Workshop version of Ad Astra. Never enable both copies in
   the same playset.
5. Start a new game unless that beta release explicitly says otherwise.

To return to the stable release, disable the beta entry and re-enable the
Workshop entry. Delete `mod/adastra_beta` and `mod/adastra_beta.mod` if you no
longer want it installed.

## Reporting a beta problem

Include the beta tag, the mod version shown by the launcher, starting age,
current game date, active mods, a save if possible, and `error.log`.

Beta saves are not guaranteed to remain compatible with later beta or stable
versions.

## Maintainers

Run the **beta release** GitHub Actions workflow manually from `dev`, a
`release/*` branch, or a `hotfix/*` branch. Its tag must start with `beta-`.
The workflow creates a GitHub pre-release and never receives Steam secrets or
publishes to the Workshop.
