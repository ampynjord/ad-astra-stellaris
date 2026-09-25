# Changelog — Ad Astra

All notable player-facing changes are recorded here. Dates use ISO format.

## 1.4.0-beta.9 — 2026-09-25

> Public beta for Stellaris 4.5 "Cygnus", published as a GitHub pre-release.
> Stellaris 4.5 does not load 4.4 saves: start a new game. Never enable it
> beside the Steam Workshop version, which keeps the stable 1.3.3 release.

### Changed

- Ad Astra now targets Stellaris 4.5 "Cygnus". The base-game technologies,
  colony designations, buildings, zones, traditions and diplomacy that the
  mod rewrites were merged again with the 4.5 files: the mod's age locks,
  costs and guards are kept, and the 4.5 changes are carried over.
- Keys that 4.5 removed are gone from the mod's country types and starting
  technologies, and the mod no longer overrides the Dyson Gun technology,
  which 4.5 moved to tier 3.
- The Terror Camp now follows its age table and opens in the Steam Age.

### Added

- When another empire takes your home system, a notice tells you once per
  occupation that your homeworld may have left the outliner, with a button
  that takes you to it.
- Each change of state of the home system (capital sector, system owner) is
  written as an `ADASTRA DIAG` line in `game.log`, the evidence cards B19 and
  B22 collect for the outliner issue.

### Known issues

- A first-contact chain can still end by revealing a star empire's name and
  communications before emergence.
- The homeworld can disappear from the outliner, reported when entering the
  Bronze Age and while another empire holds your home system. The planet is
  still yours and reachable from the galaxy map or the new notice.
- A cosmic storm can impose an energy deficit before electricity exists.
- The Energy Mogul leader trait can produce energy too early.
- The Great Khan notification can appear before emergence.

Report issues on GitHub or in the Discord bug-report forum with the beta tag,
your starting age, the game date, a save and `error.log`.

## 1.3.3 — 2026-09-24

### Changed

- Ad Astra now targets Stellaris 4.5 "Cygnus". Keys that 4.5 removed are gone from the mod's country type and starting technologies, and the mod no longer overrides the Dyson Gun technology, which 4.5 moved to tier 3.

### Fixed

- The Starbase Program now completes when your home system already holds a starbase with no owner, or one that is already yours. It previously charged its cost, ran for 720 days, reported "The Sky Is Already Taken" and became available again, forever. The programme now takes over that starbase and delivers the construction ship. A starbase owned by another empire still blocks the decision, as before.

### Player action

- Stellaris 4.5 does not load 4.4 saves. Start a new game after updating.

## 1.4.0-beta.8 — 2026-09-16

> First **public** beta, published as a GitHub pre-release. It is a local mod
> with its own name: never enable it beside the Steam Workshop version, and
> start a new game. The Workshop kept the stable 1.3.2 release.

### Fixed

- The first-contact watch stage now has an explicit roll-failure path. The
  engine previously logged that watched contact sites would never progress;
  a failed roll now keeps the contact unknown without firing a random event.
- The home-system sector is no longer re-created every month while the
  confined empire owns no starbase. The engine refuses a sector without the
  system's starbase, so those attempts always failed and only filled the
  logs. The sector is still re-created when you reclaim your sky and the
  starbase becomes yours.

### Known issues

- A first-contact chain can still end by revealing a star empire's name and
  communications before emergence.
- The homeworld can disappear from the outliner when entering the Bronze
  Age. The planet is still yours and reachable from the galaxy map.
- A cosmic storm can impose an energy deficit before electricity exists.
- The Energy Mogul leader trait can produce energy too early.
- The Great Khan notification can appear before emergence.

Report issues on GitHub or in the Discord bug-report forum with the beta tag,
your starting age, the game date, a save and `error.log`.

## 1.4.0-beta.7 — 2026-08-31

> Living-under-an-occupied-sky build. Selected testers only; new games
> required; never enable beside the Workshop version.

### Added

- Reclaim the Sky: a single negotiation decision on your capital, available
  whenever an empire holds the home system starbase and has declared itself
  (the engine's diplomatic-action list is hardcoded, so the button lives in
  the decisions tab). No dice: the occupant's ethics decide. A xenophobe or militarist refuses —
  and the refusal grants you a claim on your own system, opening the war
  path. A pacifist or xenophile cedes freely. An authoritarian cedes in
  exchange for tribute (you become their tributary). Commercial-minded
  empires sell for 1500 energy + 500 alloys. Any cession transfers the
  starbase, dismantles their mining and research stations, and wipes their
  survey data.
- The unknown stays unknown: a first-contact chain you conduct toward a star
  empire is held in a perpetual watch stage — it never concludes, no
  communications are ever established by it, and an era-flavoured event
  tells what your age understands. The empire's name, capital and borders
  stay hidden. Information must be given to you or found: the occupant of your
  sky declares itself from the Atomic Age (opening its diplomacy screen),
  full awareness and enlightenment still work, and emergence lifts the veil.
- Perception of the visitors depends on your era: space fauna at the
  telescope, a presence living above your world, era-flavoured reactions,
  and a receivable enlightenment offer with real effects.
- A constructor finishing its shakedown under an occupied sky says so and
  points at the negotiation.

### Changed

- No more self-surveying sky: the invisible net that charted one body per
  month by mere science-ship presence is gone. Surveying is done by your
  science ship, on your orders — and Remote Sensing explicitly grants the
  right to survey the home system even when another empire has claimed it.
- Astronomical Observation costs 100 influence + 500 minerals, and each
  campaign makes the next one 30% dearer.
- The orbital stage accepts any starbase building — no more hidden shortlist.
- The Orbital Yard Programme becomes available again if the Builder is lost.
- Text pass: every custom decision, building and technology states exactly
  what it requires and unlocks (telescope ranges, national programme
  contract, survey rights) on top of its lore, in English and French.

### Fixed

- Colony-scoped decisions no longer spam scope errors when the galaxy holds
  nomadic ship colonies.
- Building an observation post over your own homeworld is dismantled
  immediately with a full refund (the guard event never fired — wrong hook
  scope); the observation chain no longer starts on yourself.
- The homeworld's sector is created on day one and re-created after a
  cession, keeping the planet in the outliner. Known engine limit: while the
  occupant's own sector covers your home system, the engine refuses to
  recreate yours — ending the occupation restores it.
- Colony designations are locked to the era designation until emergence;
  the full vanilla palette returns once you emerge.
- Several event options granted momentum bonuses that silently did nothing
  (a non-existent effect parameter); they now use real timed modifiers.
- Observation events no longer test a non-existent trigger; abductions
  again require an intrusive observation post.

### Removed

- The "Progress:" gauge decision cards. Stage requirements live in the
  situation description instead.

## 1.4.0-beta.6 — 2026-08-30

> Hotfix build for the beta.5 wave of reports. Selected testers only; new
> games required; never enable beside the Workshop version.

### Fixed

- Historically dated vanilla technologies (Scientific Method, Industrial
  Base, Mechanized Mining, and the other era-dated foundations) now cost on
  their host era's scale instead of their vanilla price — at 500 they were
  being mistaken for leaks. Luxury Residences at Renaissance is likewise a
  deliberate era unlock.
- Modern-era blockers (Sprawling Slums, failing infrastructure, the Great
  Pacific Garbage Patch) are removed at any pre-Industrial start, and the
  Machine Age era hardships no longer duplicate blockers that already exist.
- The homeworld's era designation is set immediately at game start and now
  follows age transitions on its own.
- The Galactic Community no longer re-invites the confined empire in a loop;
  invitations resume normally at emergence.

### Changed

- Electrical grid grace period: energy production starts with the technology,
  but building upkeep only switches to energy once a generator district
  exists — or two years after the technology at the latest. The rule is
  stated in the technology's description.

Follow the pinned test plan in the beta category and report the beta tag with
every result.

## 1.4.0-beta.5 — 2026-08-30

> Fifth private beta build — the "true pre-FTL" build. This package is for
> selected testers only: it is not on Steam Workshop, requires a new game, and
> must never be enabled beside the Workshop version. Saves from earlier beta
> builds are not supported.

### Added

- The empire is now a genuine pre-FTL civilization in the engine's eyes:
  observation posts, infiltration operations, non-interference policies and
  the awareness mechanic all apply to it. The homeworld carries its era
  designation crest, and era hardships appear from the Machine Age onward.
- An awareness storyline told from the ground: threshold events chain from
  doubt to certainty as foreign powers act above us, and observation events
  now require an actual observer (a foreign fleet in the home system or an
  observation post in orbit).
- The Space Age is paced by its instruments: early discoveries come from the
  laboratories, the next wave requires a radio telescope, the last wave the
  space telescope. The rhythm is announced in-game and detailed in the
  situation log.
- One "Progress" gauge card per space-program stage: hover it to see, in green
  and red, everything the current stage still requires.
- Milestone events now summarise their rewards on the confirmation button, and
  every programme decision explains what it delivers before you pay for it.

### Changed

- Astronomy campaigns mark the discovered system as known on the map without
  surveying any of its bodies; uncharted space clears around each discovery.
- The deep probe is repeatable while unknown bodies remain, reveals the
  target's deposits, and each launch makes the next one 35% dearer.
- First Lunar Landing is required only when the home system has a moon; the
  deep probe opens directly otherwise, and the situation log says so.
- The Hyperspace Programme is far longer and costlier (5 years; 1000 influence,
  6000 minerals, 500 alloys).
- The Colonisation Programme only appears when the home system actually holds
  a colonizable, unowned world.
- Foreign first-contact chains toward us advance at quarter speed while our
  awareness of the galaxy remains low.
- The construction list shows only the highest researched telescope tier;
  building an outdated tier is no longer offered.
- Every period technology now grants a readable bonus of at least 1%.

### Fixed

- Capital and telescope upgrade chains were rejected by the engine as upgrade
  loops and silently broken; both are now linear and upgrade correctly.
- Late-start research could dead-lock the situation at 237/295 points through
  two circular requirements; both locks are removed and the recount is
  unconditional.
- Survey display no longer lies when a foreign empire holds the home system:
  your own surveys are shown as yours (engine intel display worked around via
  a strict vanilla-copy override of the default country type — under test).
- An observation post built by the pre-FTL on its own homeworld is dismantled
  with a refund.
- The first-contact slowdown modifier is removed on emergence.

Follow `TEST_PLAN.md` in the archive and report the beta tag with every result.

## 1.4.0-beta.4 — 2026-08-27

> Fourth private beta build. This package is for selected testers only: it is
> not on Steam Workshop, requires a new game, and must never be enabled beside
> the Workshop version. Saves from earlier beta builds are not supported.

### Fixed

- Civil Education no longer creates an energy deficit before the Electrical
  Grid exists. Its State Academy is restored automatically on the capital once
  the technology is researched.

Follow `TEST_PLAN.md` in the archive and report the beta tag with every result.

## 1.4.0-beta.3 — 2026-08-27

> Third private beta build. This package is for selected testers only: it is
> not on Steam Workshop, requires a new game, and must never be enabled beside
> the Workshop version. Saves from earlier beta builds are not supported.

### Fixed

- Early Space progression now waits for the required research and milestones,
  including the launch, satellite, crewed-flight and exploration decisions.
- Astronomy observations reveal one eligible neighbouring system at a time and
  no longer run implicitly when a telescope is built.
- The deep-probe decision now surveys one previously unknown celestial body in
  the home system and correctly handles planets with moons.
- Period technology costs and progress accounting no longer produce zero-cost
  cards or skip situation points.

### Changed

- The astronomy chain uses one upgradeable telescope line; each upgrade
  increases observation range and the amount of information revealed.
- Space-program decisions are unique or retryable only after failure, with
  costs and prerequisites shown in their tooltips.
- First contact remains unidentified until emergence or an empire explicitly
  shares sensor information.

Follow `TEST_PLAN.md` in the archive and report the beta tag with every result.

## 1.4.0-beta.2 — 2026-08-27

> Second private beta build. Same rules as beta.1: not on Steam Workshop,
> requires a new game, never enable it beside the Workshop version. Saves from
> beta.1 are not supported. Follow `TEST_PLAN.md` before reporting a result.

### Fixed

- The first-celestial-body decision no longer raised a scope error on every
  evaluation. Empires whose capital is not a planet made it fail roughly a
  hundred times per session in the error log.
- War goals inherited from the base game now define the technology ratio they
  compare against, instead of reading an undefined value.

### Changed

- Urban capacity, district specializations and start zones follow the period
  technologies more closely, and every technology states what it unlocks.
- Age transitions record their in-game year, so a future chronicle can retell
  the history of a running game.

## 1.4.0-beta.1 — 2026-08-24

> Experimental private beta. This build is not on Steam Workshop and requires
> a new game. Install it as a separate local mod, never beside the Workshop
> version. The feature scope is frozen: until release, 1.4 receives only
> test-driven bug fixes, compatibility work, and localization or asset
> corrections needed to resolve a defect. Follow `TEST_PLAN.md` from the beta
> archive before reporting a result.

### Added

- Research-led age progression: period technologies now advance the Beyond the
  Stars situation through a historical prerequisite tree.
- Progressive building capacity and technology-gated district specializations.
- Stellaris-style custom icon coverage for the period technology set, plus the
  new observatory, radio telescope and space telescope buildings.
- Deferred civic infrastructure and a free government reform at emergence.

### Changed

- The Early Space Age now leads through astronomy, exploration, construction,
  a player-built starbase, orbital infrastructure and Hyperdrive milestones.
- The game uses Stellaris' vanilla start, mid-game, end-game and victory dates.

### Stabilization and test focus

- The complete space-program chain, astronomical fog of war, research pacing,
  building slots, later starts, DLC/civic interactions and save migration need
  in-game validation.

## 1.3.2 — 2026-08-20

### Fixed

- Period technologies remain researchable after the next age begins. This fixes the Renaissance dead end reported in 1.3.1 when a required technology belonged to a later historical wave of the previous age.
- Period buildings now use the urban zone set present in Ad Astra cities, restoring valid construction slots for the Granary, Foundry and other age buildings.
- Pre-Steam consumer-goods costs now use flat job upkeep reductions rather than multipliers capped by Stellaris, preventing administrative and research jobs from creating an unavoidable early deficit.
- District specializations now require their relevant historical technology. Archives require Writing, military districts require a Standing Army, and later specializations follow the same rule.
- Bronze through Renaissance starts no longer receive an Archives zone for free; it becomes available for the player to build after researching Writing.

### Player action

- Start a new game after updating. Existing 1.3.1 saves may retain an invalid research deck or previously missing building slots.

## 1.3.1 — 2026-08-18

### Fixed

- Age technologies no longer invalidate their own prerequisites after an age is completed. This prevented Bronze and later technology from being granted or researched in 1.3.0.
- Advanced starts now receive their prior historical technologies before the starting capital is prepared, restoring the intended energy and consumer-goods economy.

### Player action

- Start a new game after updating. Existing saves created with 1.3.0 may already be missing the technologies that the hotfix restores for new starts.

## 1.3.0 — The Technological Backbone — 2026-08-16

### Added

- 250 period technologies: 25 for each of the ten historical ages and across all three research fields.
- Five chronological technology waves per age; the current wave is derived from the technologies' historical dates.
- Research completion gating: an age waits until all of its period technologies have been discovered.
- Sixteen base-game founding technologies for the Space Age, unlocked only when their gameplay becomes relevant.
- Survey by presence for sublight science ships, including claimed home systems.
- Space exploration, starbase, orbital fleet, and hyperspace programs.
- Wider casus belli and war-goal support for grounded empires.

### Changed

- Period technology bonuses were rescaled.
- The Space Age now uses staged founding technology and program milestones rather than granting the normal starting package at once.

## 1.2.0 — The Ages — 2026-08-12

### Added

- Historical ages, period buildings, capital tiers, and resource availability tied to technological development.
- Starting-age and ascent-pace choices, grounded diplomacy and war support, and AI access to the origin.

## 1.1.0 — 2026-08

### Added

- First public progression, early economy, and emergence framework.

## 1.0.0 — 2026-08

### Added

- Initial public release of Ad Astra — Origins.
