# Testing the public beta

The beta is an experimental local build, published as a **GitHub
pre-release**. Steam Workshop remains the stable channel (1.3.3) and never
receives beta builds.

## Installation

1. Download the beta `.zip` attached to the latest pre-release on the
   project's GitHub **Releases** page, for example `beta-1.4.0-beta.9`.
2. If an older beta is installed, **delete** `mod/adastra_beta` and
   `mod/adastra_beta.mod` first. Extracting a new beta over an old one keeps
   files that the new version removed.
3. Extract the archive directly into your Stellaris user folder:
   `Documents/Paradox Interactive/Stellaris/`.
4. Open the Stellaris launcher and enable **Ad Astra: Origins - Beta**.
5. Disable the Steam Workshop version of Ad Astra. Never enable both copies in
   the same playset, and do not load Workshop saves with the beta.
6. Start a new game unless that beta release explicitly says otherwise.
7. Read the **Known issues** in the release notes, then open `TEST_PLAN.md`
   from the archive if you want to run structured test cards.

On Windows, if the launcher lists the mod but the game does not load its
content, check that the path of your Stellaris user folder contains no
accented character; if it does, move the extracted `adastra_beta` folder to a
path without accents and update `path=` in `mod/adastra_beta.mod`.

To return to the stable release, disable the beta entry and re-enable the
Workshop entry. Delete `mod/adastra_beta` and `mod/adastra_beta.mod` if you no
longer want it installed.

## Reporting a beta problem

Open an issue on GitHub or a thread in the Discord bug-report forum. Include
the beta tag, the mod version shown by the launcher, the test card if any,
starting age, current game date, active mods, a save if possible, and
`error.log`.

Beta saves are not guaranteed to remain compatible with later beta or stable
versions. The beta is covered by the project license: personal use is
allowed, redistribution and re-uploads are not.

## Maintainers

Run the **beta release** GitHub Actions workflow manually on the `beta`
branch. Its tag must use the form `beta-MAJOR.MINOR.PATCH-beta.N`, for example
`beta-1.4.0-beta.9`, and must match the descriptor version. The `beta-` prefix
is mandatory: `release.yml` publishes to the Workshop on any `v*` tag.

The workflow runs the full checks, builds the beta archive, and creates a
GitHub **pre-release** with that archive and the release notes taken from the
first `CHANGELOG.md` section. It never receives Steam secrets and never
publishes to the Workshop. A published beta is never replaced: a fix becomes
the next beta number.
