# Ad Astra 1.4.0-beta.9 — Test Notebook

This is the public-beta test contract. Steam Workshop remains on 1.3.3.
Enable only `Ad Astra: Origins - Beta`; never enable it alongside Workshop.
While this local beta is installed, treat the Workshop copy as unusable and do
not load its saves with the beta.

**Beta.9** is the first build for **Stellaris 4.5 "Cygnus"**. It carries the
beta.8 content, merged again with the 4.5 game files, plus the outliner
notice and `ADASTRA DIAG` log lines. Stellaris 4.5 does not load 4.4 saves:
**no beta.8 save or checkpoint is valid**, and every card below must be run
again on beta.9. B20 and B22 remain **known failures**: rerun them to confirm
or refine the reports, not to discover them.

## Rules for every card

1. Use a new single-player game, a small galaxy and no extra mods unless the assigned card explicitly says otherwise.
2. Choose **Accelerated History** whenever research must complete. Do not use console commands, UI mods, save editing or external speed tools.
3. Run one card at a time. Stop on a failure; keep the save and copy `Documents/Paradox Interactive/Stellaris/logs/error.log` before restarting.
4. A shared checkpoint save is valid only when it was reached naturally with this beta. Name it with the completed card and in-game date.
5. Report both passes and failures. A pass proves only that card.

Use this report header:

```text
Beta tag / launcher version:
Card:
PASS, FAIL or UNCLEAR:
Starting age / approach / ascent pace / galaxy pace:
In-game date:
Enabled DLC and every other mod:
Observed result:
Expected result:
Save and error.log attached on failure: yes / no
```

Report any new `adastra`, `localization_reader`, invalid technology,
`unable to research`, `give_technology`, starbase or decision error. Do not
report unrelated vanilla warnings unless they prevent the card.

## Assignment and exit rule

**Beta.7 focus** (the occupied-sky build): surveying is manual again (the
invisible presence pulse is gone); star empires you detect stay unknown
(perpetual watch stage, no communications) until someone declares itself;
the occupant of your sky declares itself from the Atomic Age; Reclaim Our
Sky is a capital decision whose outcome follows the occupant's ethics
(cession, purchase, tributary status, or refusal granting a claim and a war
path); colony designations are locked to the era crest until emergence;
the Orbital Yard Programme returns if the Builder is lost.

- B00–B05 (install, early economies, prerequisite tree, slots, approaches)
  **passed in earlier betas and are retired**: their mechanics are unchanged
  in beta.7. Report a regression on any of them as a bug, not as a card.
- B06–B10 are the space chain and must all pass on beta.7 before 1.4 can
  become a release candidate.
- B11–B13 are distributed by DLC and empire configuration; no tester needs to
  run every combination.
- B14 is optional multiplayer coverage.
- B15–B17 cover the pre-FTL rework; B19 is observational.
- B18 (stage gauges) **is retired**: the gauge cards were removed in beta.7;
  stage requirements now live in the situation description.
- B20–B22 are new in beta.7: perception of star empires, the negotiation
  of the sky, and the outliner/sector diagnostic.

Short cards target 5–15 minutes. B06 is split across sessions and creates the
natural checkpoint saves used by B07–B10.

## B06 — Early Space: astronomy and first launch

**Setup:** new Early Space game, Accelerated History, no other mods.

1. Record the decks and situation: it must begin at **225/400**.
2. Research the Early Space period technologies naturally, keeping the same
   save. **Expect the deck to run dry twice**: the middle wave of technologies
   only enters the draw after a **radio telescope** is built, the last wave
   after the **space telescope**. The game must announce this rhythm at Space
   Age entry and remind you when the deck runs dry; the situation log must
   also state the rule. Astronomical Observation costs 100 influence +
   500 minerals and must grow **30% dearer** with each campaign.
3. Record every situation increase; inspect custom icons as cards appear.
4. Build each telescope tier when required. The construction list must only
   offer the **highest researched tier**, and the radio telescope must upgrade
   into the space telescope. Enact **Astronomical Observation**: its duration
   and cost must be visible, and the result must name one newly discovered
   system that appears on the map as known **with none of its bodies
   surveyed**.
5. Complete **First Suborbital Launch** once the situation instructs you to do
   so. If it fails, retry only after recording the visible failure; if it
   succeeds, confirm it disappears.

**Pass:** every period technology adds one point, none completes instantly, and
the stage reaches **250/400** only after all 25 period technologies. A successful
First Suborbital Launch then reaches **275/400** and opens the Exploration
Program. The satellite is a separate, one-time historical milestone and does
not replace this launch.

**Fail:** blank or instant deck, absent telescope icon/localisation, stale
decision target, or a milestone that skips a stated requirement.

**Output:** share a natural post-launch save named `B06-first-launch-DATE`.

## B07 — Exploration and sublight survey

**Setup:** B06 post-launch checkpoint.

1. Research the Exploration-stage foundations.
2. Enact the Space Exploration Program on Terra.
3. Confirm delivery of exactly one sublight science vessel.
4. Survey the home system's bodies **by explicit order** (right-click →
   Survey). Nothing may survey itself: no body may flip to surveyed without
   your ship working on it (the old presence pulse is removed in beta.7).
5. If another empire has claimed the home system, survey orders must be
   refused until **Remote Sensing** is researched, and accepted after it.
6. Let one monthly pulse pass after the final body is surveyed.

**Pass:** decision cost/duration are visible; vessel is usable; every body is
surveyed by order only; stage reaches **300/400** only after research,
decision and full survey.

**Fail:** no/duplicate vessel, impossible survey order, early stage advance, or
stalled stage after every body is surveyed.

**Output:** natural Construction checkpoint at 300/400.

## B08 — Construction program

**Setup:** B07 Construction checkpoint.

1. Research all Construction-stage foundations.
2. Enact the construction decision and wait for its stated duration.
3. Find the delivered construction ship, then let a monthly pulse pass.

**Pass:** exactly one constructor arrives; it can receive normal construction
orders; no starbase is created by the decision; stage reaches **325/400** only
after research and delivery.

**Fail:** missing/duplicate constructor, automatic starbase, or premature stage
advance.

**Output:** natural Outpost checkpoint at 325/400.

## B09 — Starbase before stations

**Setup:** B08 Outpost checkpoint.

1. Research Outpost-stage foundations.
2. Use the delivered constructor to build the first starbase in the home system through the normal Stellaris order.
3. Before completion, attempt a mining or research station on a surveyed deposit; repeat after the starbase exists.
4. Let a monthly pulse pass, then complete Orbital-stage research and build one valid mining or research station.

**Pass:** station construction is blocked before the player-built starbase and
available only after it plus normal technology requirements; milestones occur
in Outpost then Orbital order, reaching **350/400** then **375/400**.

**Fail:** station before starbase, constructor unable to build the starbase,
automatic base creation, or an unreactive situation after correct infrastructure.

**Output:** natural Hyperdrive checkpoint at 375/400.

## B10 — Hyperdrive and emergence

**Setup:** B09 Hyperdrive checkpoint. One lead tester must also run B06–B10
naturally without a checkpoint load.

1. Research remaining foundations and enact the Hyperspace Program.
2. Research Hyperdrive naturally in Physics.
3. Read every emergence event and record whether the home system is free or occupied.
4. Confirm normal technology access, FTL civilian ships, Legacy of the Ascent and the free government reform.
5. Use the reform once, then confirm it is not repeatedly free.

**Pass:** Hyperdrive is the final trigger; situation completes once; outcome is
coherent; FTL ships and usable home-system ownership exist; one free reform is
offered; pre-FTL restrictions are removed.

**Fail:** early/duplicate emergence, no FTL refit, unusable home system, repeated
reform, broken normal-tech deck, or missing Legacy.

## B15 — True pre-FTL status *(new in beta.5)*

**Setup:** new game, any pre-Space age, Accelerated History, several AI empires.

1. Open the homeworld: its designation must carry the **era crest** of the
   current age, and follow age transitions.
2. From the Machine Age onward, confirm the era hardship blockers (decrepit
   dwellings, failing infrastructure) appear once on the capital.
3. Play until a foreign empire takes interest: an **observation post** built by
   an AI above the homeworld is now possible and must not break the game.
4. If an observation post exists and the pre-FTL builds a construction ship
   later: confirm any observation post it builds on the homeworld itself is
   dismantled with a refund event.

**Pass:** the era designation is present from day one and follows every age
transition without manual selection; no modern-era blockers exist at a
pre-Industrial start; hardships appear once at Machine Age (no duplicates);
foreign observation is survivable; self-observation is refused narratively.

**Fail:** missing crest, repeated hardship stacking, crash or dead game state
around observation posts.

## B16 — Awareness told from the ground *(new in beta.5)*

**Setup:** continue any game where at least one foreign empire is active near
the home system.

1. Observation-flavour events (lights, abductions, signals, debris) must fire
   **only** when a foreign fleet is in the home system or an observation post
   exists — never in an empty sky.
2. Awareness chapter events (Commission → Schism → Answer? → We Know) must
   fire one per awareness threshold, never repeat, and their choices must show
   their effects on the buttons.
3. The "A Distant Sky" modifier must be present for the whole confinement
   (it no longer falls at High awareness) and vanish at emergence.

**Pass:** no event without an observer; one chapter per threshold; slowdown
present until emergence, then gone.

**Fail:** event spam, chapters out of order, modifier surviving emergence.

## B17 — Deep probe economics *(new in beta.5)*

**Setup:** B06 checkpoint or any Space Age save before the probe.

1. The probe requires the lunar landing **only if the home system has a
   moon**; with no moon it opens directly after the crewed flight (galaxy
   re-roll may be needed to test the no-moon branch; report which branch you
   tested).
2. Launch the probe: the event must name the body and its deposits must be
   revealed for us.
3. Launch it again: it must stay available while unknown bodies remain, and
   each launch must cost **35% more** than the last.
4. Hover the decision and every milestone confirmation button: rewards and
   openings must be summarised on the button itself.

**Pass:** correct moon branch, visible deposits, growing cost, informative
buttons.

**Fail:** probe dead-end without a moon, invisible results, flat cost.

## B18 — Stage gauges *(retired in beta.7)*

The gauge cards were removed at the mod author's request. Stage requirements
are enumerated in the situation description. Report a missing or wrong
requirement listing there as a bug, not as a card.

## B19 — Occupied home system *(exploratory, new in beta.5)*

**Setup:** play until a foreign empire claims the home system with a starbase.
This card records behaviour; some outcomes are known issues, not failures.

1. Confirm your surveys display as **yours** (probe results, ordered
   surveys) even under a foreign flag, and that the occupant's own surveys
   do **not** show as yours or grey out your survey orders.
2. With Remote Sensing researched, confirm the survey order works on the
   home system under a foreign flag.
3. Record the known issue if it occurs: homeworld missing from the outliner
   while the system is claimed. Attach the save **and**
   `Documents/Paradox Interactive/Stellaris/logs/game.log` — the beta logs
   an `ADASTRA DIAG` line each time it tries to recreate the sector, and
   those lines are the evidence the fix needs.

**Pass:** survey truthfulness holds; the rest is observational.

**Fail (hard):** crash, or surveys attributed to the wrong empire again.

## B11 — Civic, ethic and trait configuration

**Setup:** assigned non-gestalt authority, ethics, civics and traits; earliest
age relevant to any required building.

1. Inspect day one, the first monthly pulse and each relevant technology.
2. Watch for missing mandatory infrastructure, anachronistic upkeep or locked required mechanics.
3. At emergence, take the free reform and inspect normal civic selection.

**Pass:** selected content stays playable; deferred civic infrastructure appears
only when its age, resource and free slot allow it; no permanent loss of the
civic mechanic.

**Fail:** selectable setup creates a dead end, demands a missing building, or
loses its intended mechanic permanently.

## B12 — DLC presence and absence

**Setup:** assigned DLC test pair.

1. Run B01 or B02 with the relevant DLC enabled.
2. Repeat without it, or compare with a tester who does not own it.
3. Inspect DLC buildings, civics, authorities and origin screens used by the assigned empire.

**Pass:** both games launch and remain playable; DLC content disappears cleanly
when unavailable; no missing asset, raw key or forced DLC dependency appears.

**Fail:** load failure, required missing DLC, or a DLC-specific economy/slot break.

## B13 — Save migration

**Setup:** copy of a 1.3.3 save made on Stellaris 4.5. Never overwrite it.

1. Load it with only the beta enabled and let one monthly pulse pass.
2. Inspect situation, research decks, capital districts and resource bar.
3. Save under a new name, reload, then inspect the same items once more.

**Pass:** progression recalibrates once; technologies/decks remain valid; capital
economy stays coherent after reload.

**Fail:** reset to Stone, repeated monthly jumps, lost technologies, invalid cards
or missing infrastructure.

## B14 — Multiplayer smoke test (optional)

**Setup:** two players, exact same beta archive, no other mods.

1. Host a small galaxy with Stone or Atomic Ad Astra; guest uses assigned empire.
2. Play to first contact or named space decision, then wait three monthly pulses while both watch the situation log.

**Pass:** same result for both players; no duplicate event, loop, mismatch or desync.

**Fail:** duplicate contact/target text, stuck event or desync. Attach host and
guest logs and saves separately.

## B20 — The unknown stays unknown *(new in beta.7)*

**Setup:** new game, any age, several AI empires; play until foreign ships
are detected near the home system.

1. When a first-contact site opens toward a star empire, an era-flavoured
   perception window must fire (omens → scholarly dispute → unidentified
   objects → "a foreign civilization exists"), and the site must settle into
   a **watch stage** ("our instruments keep the object under study").
2. The site must **never conclude** and never establish communications: the
   empire's name, borders and capital stay hidden. No hidden event spam in
   the log.
3. From the Atomic Age, an empire holding a starbase **or an observation
   post** in the home system must declare itself once: communications with
   that empire only, with the "They Declare Themselves" window.
4. At emergence, watched sites must resume the normal vanilla first-contact
   chain and become completable.

**Pass:** no magic reveals; exactly one declaration; watch sites resume at
emergence.

**Fail:** communications from a watched site, unknown-empire intel leaking,
window spam, or a site stuck after emergence.

## B21 — Reclaim Our Sky *(new in beta.7)*

**Setup:** play until a foreign empire holds a starbase in the home system;
reach the Orbital Yard Programme stage and wait for the occupant's
declaration.

1. The **Reclaim Our Sky** decision must exist on the capital only from the
   Orbital Yard stage onward, and only once the occupant has declared
   itself; its tooltip must list the four ethic outcomes.
2. Enact it and record the occupant's ethics and the outcome: free cession
   (pacifist/xenophile), purchase at 1500 energy + 500 alloys
   (megacorp/materialist/egalitarian), tributary status (authoritarian), or
   refusal (xenophobe/militarist).
3. On any cession: the starbase changes flag, the occupant's mining and
   research stations are dismantled, its survey data is wiped (bodies become
   surveyable again), and the homeworld should return to the outliner.
4. On a refusal: a **claim** on the home system must appear, and declaring
   war on the occupant must become possible.
5. Re-enacting must be blocked for two years, with a visible reason.

**Pass:** outcome matches ethics; cession delivers all three transfers; the
claim opens the war path.

**Fail:** decision visible too early, outcome mismatching ethics, a ceded
starbase destroyed by the safety guard, or no claim on refusal.

## B22 — Outliner and sector diagnostic *(observational, new in beta.7)*

**Setup:** any game; check at three moments — day one, while the home system
is claimed by another empire, and after reclaiming it.

1. Note whether the homeworld appears in the outliner at each moment.
2. After each session, copy the `ADASTRA DIAG` lines from
   `Documents/Paradox Interactive/Stellaris/logs/game.log` into the report.

**Pass:** observational — every report with its DIAG lines is a pass.

**Fail (hard):** crash only.

## Beta.7 exit rule

Any B06–B10, B15–B17 or B20–B21 failure requires a new beta build. A release
candidate requires all B06–B10, B15–B17 and B20–B21 cards passing on the
same version, two successful B11/B12 configurations, no unresolved critical
log entry, and one natural B06–B10 run. B14 is strongly preferred but does
not block a single-player beta release; B19 and B22 record behaviour and only
block on a crash.
