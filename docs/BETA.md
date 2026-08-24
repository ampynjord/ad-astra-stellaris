# Testing the GitHub beta

GitHub beta releases are experimental local builds. Steam Workshop remains the
stable channel.

## Installation

1. Download the beta `.zip` attached in the private Discord beta channel, for
   example `v1.4.0-beta.1`. Access is granted manually through the **Beta
   Tester** role.
2. Extract it directly into your Stellaris user folder:
   `Documents/Paradox Interactive/Stellaris/`.
3. Open the Stellaris launcher and enable **Ad Astra: Origins - Beta**.
4. Disable the Steam Workshop version of Ad Astra. While the local beta is
   installed, treat the Workshop copy as unusable: never enable both copies in
   the same playset, and do not use Workshop saves with the beta.
5. Start a new game unless that beta release explicitly says otherwise.
6. Open `TEST_PLAN.md` from the archive and run only the assigned test cards.

To return to the stable release, disable the beta entry and re-enable the
Workshop entry. Delete `mod/adastra_beta` and `mod/adastra_beta.mod` if you no
longer want it installed.

## Reporting a beta problem

Include the beta tag, the mod version shown by the launcher, assigned test
card, starting age, current game date, active mods, a save if possible, and
`error.log`.

Beta saves are not guaranteed to remain compatible with later beta or stable
versions. Do not redistribute the archive, its attachment link, saves or test
material outside the selected beta group.

## Maintainers

Run the **private beta validation** GitHub Actions workflow manually from `dev`, a
`release/*` branch, or a `hotfix/*` branch. Its tag must use SemVer prerelease
format: `vMAJOR.MINOR.PATCH-beta.N`, for example `v1.4.0-beta.1`. The workflow
requires the descriptor version to match that tag exactly. It creates neither
a GitHub release nor a public artifact, and never receives Steam secrets or
publishes to the Workshop. After it is green, build locally and attach the
archive through `discord-bot/publish-private-beta.js` in the role-gated Discord
channel.
