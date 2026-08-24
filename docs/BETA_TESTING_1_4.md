# Ad Astra 1.4.0-beta.1 — Test Notebook

This is the private-beta test contract. Steam Workshop remains on 1.3.2.
Enable only `Ad Astra: Origins - Beta`; never enable it alongside Workshop.
While this local beta is installed, treat the Workshop copy as unusable and do
not load its saves with the beta.

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

- B00–B05 are core cards.
- B06–B10 are the space chain and must all pass before 1.4 can become a release candidate.
- B11–B13 are distributed by DLC and empire configuration; no tester needs to run every combination.
- B14 is optional multiplayer coverage.

Short cards target 5–15 minutes. B06 is split across sessions and creates the
natural checkpoint saves used by B07–B10.

## B00 — Install, origin and calendar

**Setup:** new Atomic game, no other mods.

1. Confirm the launcher shows `Ad Astra: Origins - Beta 1.4.0-beta.1` and no Workshop Ad Astra entry is active.
2. Start the game, finish the initial choices, then pause on the first day.
3. Record the visible date and inspect the game-setup calendar sliders.

**Pass:** origin selectable, initialization completes, game begins at vanilla date
**2200.01.01**, and vanilla calendar ranges remain intact.

**Fail:** missing origin, two Ad Astra copies enabled, non-vanilla date or a
visible initialization/localisation error.

## B01 — Atomic day-one economy

**Setup:** new Atomic game, Accelerated History, no other mods.

1. Pause on day one; record Beyond the Stars progress, energy and consumer goods.
2. Let exactly one monthly pulse pass without building.
3. Open Terra, resource bar, district list and construction window.

**Pass:** progress begins at **200/375**; capital and districts remain after the
pulse; no forced energy or consumer-goods collapse; displayed building slots are
usable; Archives are not placed for free.

**Fail:** a required district/building vanishes, an unavoidable deficit appears,
slots cannot be used, or a raw localisation key is visible.

## B02 — Renaissance deck and first completion

**Setup:** new Renaissance game, Accelerated History, no other mods.

1. Before choosing research, capture the three research decks and situation.
2. Let one monthly pulse pass, then select one period technology.
3. Let that technology finish naturally; inspect the deck and situation again.

**Pass:** progress begins at **100/375**; a valid Renaissance card is offered;
the technology moves to researched and adds exactly one point; it does not
return to the deck or cause an instant chain.

**Fail:** empty deck, invalid card, more than one progress point, instant custom
research, card returning after completion, or a research error.

## B03 — Stone prerequisite tree

**Setup:** new Stone game, Accelerated History, no other mods.

1. Inspect the offered cards in each field before choosing.
2. Complete one Stone technology naturally.
3. Inspect newly offered cards and their prerequisite tooltips.

**Pass:** initially available cards are rank-one possibilities; the completed
technology adds exactly one point; newly available cards name a completed Stone
prerequisite where applicable.

**Fail:** a later rank appears without its prerequisite, no valid card exists, a
stated prerequisite is already met but the card is blocked, or the situation
gains passive monthly progress.

## B04 — Technology, specialization and slots

**Setup:** new Renaissance or Steam game where Writing is already known.

1. Open Terra and find the Archives specialization.
2. Inspect its unlocking technology tooltip and its zone/building capacity.
3. Build it only if the stated technology and an open district slot exist.
4. Inspect any available telescope card.

**Pass:** the technology names the specialization it unlocks; Archives are a
player construction choice rather than free infrastructure; slot count matches
the development stage; every visible custom card has name, description, cost
and icon.

**Fail:** a specialization appears early, stays unavailable after its technology,
has the wrong number of slots, or shows a raw key such as
`building_core_observatory`.

## B05 — Situation approaches and pace

**Setup:** three fresh Atomic games, one per approach.

1. Select Continuity, Forced March, then Eyes on the Sky in separate games.
2. Record the same kind of research estimate and listed modifiers in each.
3. Let one month pass without completing research.

**Pass:** approaches display their stability/happiness/unity/research trade-off;
Forced March is faster than Continuity for comparable research; no passive
situation progress occurs.

**Fail:** approaches have identical effects, a listed modifier is absent, or the
bar advances without technology or milestone completion.

## B06 — Early Space: astronomy and satellite

**Setup:** new Early Space game, Accelerated History, no other mods.

1. Record the decks and situation: it must begin at **225/375**.
2. Research the 25 Early Space period technologies naturally over several sessions, keeping the same save.
3. Record every situation increase; inspect custom icons as cards appear.
4. Build observatory, radiotelescope and space telescope when their technologies and slots allow them.
5. Complete the satellite decision once it becomes available.

**Pass:** every period technology adds one point, none completes instantly, and
only completed astronomy research plus the satellite action advances the stage
to **250/375**.

**Fail:** blank or instant deck, absent telescope icon/localisation, stale
decision target, or a milestone that skips a stated requirement.

**Output:** share a natural post-satellite save named `B06-satellite-DATE`.

## B07 — Exploration and sublight survey

**Setup:** B06 post-satellite checkpoint.

1. Research the Exploration-stage foundations.
2. Enact the Space Exploration Program on Terra.
3. Confirm delivery of exactly one sublight science vessel.
4. In **system view**, right-click and survey every non-star body in the home system. Do not use the galaxy-map survey order.
5. Let one monthly pulse pass after the final survey.

**Pass:** decision cost/duration are visible; vessel is usable; every body can be
surveyed from system view; stage reaches **275/375** only after research,
decision and full survey.

**Fail:** no/duplicate vessel, impossible survey order, early stage advance, or
stalled stage after every body is surveyed.

**Output:** natural Construction checkpoint.

## B08 — Construction program

**Setup:** B07 Construction checkpoint.

1. Research all Construction-stage foundations.
2. Enact the construction decision and wait for its stated duration.
3. Find the delivered construction ship, then let a monthly pulse pass.

**Pass:** exactly one constructor arrives; it can receive normal construction
orders; no starbase is created by the decision; stage reaches **300/375** only
after research and delivery.

**Fail:** missing/duplicate constructor, automatic starbase, or premature stage
advance.

**Output:** natural Outpost checkpoint.

## B09 — Starbase before stations

**Setup:** B08 Outpost checkpoint.

1. Research Outpost-stage foundations.
2. Use the delivered constructor to build the first starbase in the home system through the normal Stellaris order.
3. Before completion, attempt a mining or research station on a surveyed deposit; repeat after the starbase exists.
4. Let a monthly pulse pass, then complete Orbital-stage research and build one valid mining or research station.

**Pass:** station construction is blocked before the player-built starbase and
available only after it plus normal technology requirements; milestones occur
in Outpost then Orbital order, reaching **325** then **350/375**.

**Fail:** station before starbase, constructor unable to build the starbase,
automatic base creation, or an unreactive situation after correct infrastructure.

**Output:** natural Hyperdrive checkpoint.

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

**Setup:** copy of a 1.3.2 or older 1.4-development save. Never overwrite it.

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

## Beta.1 exit rule

Any B00–B10 failure requires a new beta build. A release candidate requires all
B00–B10 cards passing on the same version, two successful B11/B12 configurations,
no unresolved critical log entry, and one natural B06–B10 run. B14 is strongly
preferred but does not block a single-player beta release.
