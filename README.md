# Ad Astra — Origins

**A pre-FTL origin for Stellaris.**

[![Version](https://img.shields.io/badge/version-1.4.0--beta.1-orange)](CHANGELOG.md)
[![Stellaris](https://img.shields.io/badge/Stellaris-v4.4%20Pegasus-orange)](https://www.stellaris.com/)
[![DLC](https://img.shields.io/badge/DLC-none%20required-green)](#)
[![Languages](https://img.shields.io/badge/in--game%20languages-English%20%C2%B7%20French-lightgrey)](#)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

*Per aspera ad astra — through hardship, to the stars.*

Everyone else starts with a fleet. You start with a planet, and a very long way to go.

Ad Astra lets you begin Stellaris as a civilization confined to its homeworld. Choose one of ten historical starting ages, build your society through them, create a space program from nothing, and emerge into a galaxy that did not wait for you.

[Steam Workshop](https://steamcommunity.com/sharedfiles/filedetails/?id=3781408257) · [GitHub beta builds](https://github.com/ampynjord/ad-astra-stellaris/releases) · [Discord](https://discord.gg/nKP4TfNzNX) · [Bug reports and ideas](https://github.com/ampynjord/ad-astra-stellaris/issues/new/choose)
Steam Workshop is the stable channel. Experimental builds are GitHub
pre-releases: install them as a separate local mod and never enable the beta
and Workshop copies together. See [Testing the GitHub beta](docs/BETA.md).

## 1.3.2 — Progression and Economy Hotfix

Version 1.3.2 completes the focused hotfix line for the blocking 1.3.0
progression and early-economy regressions.

- Age technologies stay researchable after an age transition, including Bronze and Renaissance.
- Advanced starts receive their historical technologies and infrastructure immediately.
- Pre-Steam consumer-goods upkeep no longer creates an unavoidable deficit.
- Early buildings and district specializations unlock through their relevant historical technologies.
- The fix is deliberately focused: it does not add 1.4 content or change the intended pace of an age.

**Start a new game after updating.** Please report any remaining progression issue with the starting age, ascent pace, game date, mod version, active mods, and `error.log`.

## What you play

### Day one

Choose an age from Stone to Early Space. Starting earlier is harder, but improves the final **Legacy of the Ascent**. You also choose an ascent pace and whether the rest of the galaxy develops normally or waits for your emergence.

### The ascent

The **Beyond the Stars** situation tracks the journey through ten ages. Each age contains period technologies across the three research fields. Completing the relevant research advances the ascent; prerequisites keep discoveries in a coherent historical order.

Choose an approach for the current age: careful continuity for stability, a forced march for speed at a social cost, or eyes on the sky for research at the expense of unity.

### An economy that arrives with history

Resources appear only once your civilization can make use of them. Alloys arrive with bronze, consumer goods with steam, and energy with electricity. Period capitals and buildings take your world from a ring of stones to modern ministries, while exploitation campaigns offer short-term gains with real trade-offs.

### The road to space

In the Space Age, base-game founding technologies must be researched instead of being granted automatically. They appear only when the gameplay they support exists. Your programs then provide sublight exploration, a starbase yard, an optional orbital fleet, and finally the path to Hyperdrive.

The sublight science ship surveys by presence: it maps one body per month while in a system, including a home system another empire has claimed.

### Emergence

Research **Hyperdrive** to complete the ascent. Your fleet is refitted for FTL travel, the normal technology tree opens, and the Legacy of the Ascent becomes a permanent bonus. If another empire occupies your home system, emergence is negotiated rather than ignored.

## Compatibility and support

| Item | Status |
| --- | --- |
| Stellaris | 4.4.x “Pegasus” |
| DLC | None required |
| Languages in game | English and French |
| New game | Required after updates |
| Achievements | Disabled, as with any mod |

The mod overrides starting and early-tier technologies, selected civilian ship sizes, scripted triggers such as `is_regular_empire`, several casus belli and war goals, and focus cards. Those are the most likely conflict points.

Known incompatibilities under investigation: **Gigastructural Engineering & More** can leave the starting colony without a city district, and **Ethics and Civics Classic** can interfere with the capital chain. Please include a complete load order when reporting compatibility problems.

## Roadmap — the Ad Astra collection

The roadmap is direction, not a release calendar. A version is released only
after its targeted in-game tests pass. The current mod will remain a complete
experience throughout 1.4. The collection restructuring begins in **1.5**;
Origins will not be split in the middle of 1.4 development.

- **Ad Astra: Origins** — the flagship of the collection and its original
  pre-FTL, planetary origin. It covers the ten historical ages, the first
  space program and emergence into the galaxy.
  **1.4 “Galileo”** remains its immediate priority: research-led progression,
  astronomy, the path from first launch to a player-built starbase, and an art
  pass for custom content. Stellaris' vanilla start and end dates remain
  unchanged.
- **Ad Astra: Core** — the shared, non-playable foundation planned for **1.5**:
  common scripts,
  technology rules, assets and compatibility interfaces for every Ad Astra
  module. It will be extracted only after Origins is stable enough to make the
  shared contract dependable.
- **Ad Astra: Ark** — a separate pre-FTL origin aboard a nomadic ark. Its
  population, economy, movement and survival problems are fundamentally
  different from a homeworld origin.
- **Ad Astra: Frontier** — post-emergence frontier development: non-habitable
  outposts and biodomes, staged terraforming, asteroid and deep-space stations,
  and the supporting spatial mechanics.
- **Ad Astra: Millenium** — generation and cryogenic ships that establish a
  distant independent colony, then create a later reunion, integration or
  independence story after emergence.
- **Ad Astra: Nations** — the planetary macro layer: countries, factions,
  institutions, political legitimacy, economic competition and planetary
  warfare leading to unification.

These modules will be released as separate Workshop items in an **Ad Astra
Collection**, with Origins as its flagship and Core as an explicit shared
requirement where needed.
Gestalt authorities and a galaxy where every empire starts pre-FTL remain
separate-project territory.

## Contributing

Bug reports, play reports, balance observations, writing help, translations, and ideas are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or a pull request.

## Credits

Created by **ampynjord**. Released under the [MIT License](LICENSE).
