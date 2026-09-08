# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Read and write only within this directory.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

New PM on **Rook Dispatch**, started 31 Aug 2026, succeeding Priya Raghunathan (departed 21 Aug after 14 months). Full source material lives in `00-rook/` — see file map at the bottom.

### The company

Rook Industries builds coordination software for the protective-response sector: independently-operating masked responders and the handlers/quartermasters who support them (Rook does not employ responders). Founded 2014, ~241 employees, mostly remote (HQ "Site Aleph" only reachable twice weekly). Ships monthly on a 4.x release train.

**Confidentiality is contractual, not a preference:** Rook never stores a mapping from a responder's cover identity to a legal identity, and never tries to work one out. Don't design anything that assumes that mapping exists — see Security Policy 4.1 before touching responder records.

### The two products

| | Rook Dispatch | Rook Supply |
|---|---|---|
| Does | Responder coordination: availability, routing, callout offers, acceptance | Gear provisioning: requisitions, maintenance, failure reports |
| Users | Handlers (web console), responders (mobile) | Handlers, quartermasters |
| I own | **This one** | — |

**Dispatch flow:** incident arrives → Dispatch ranks available responders → callout offer goes to the top-ranked responder's phone → they accept/decline/timeout → on no, it moves to the next responder. Headline metric is **acceptance rate**; also watched: **time-to-accept**, **coverage gap**.

**How Supply connects:** Supply reads the **Responder Availability Record** (written by Dispatch, Supply never writes to it) to schedule maintenance around callout load. A change to how Dispatch calculates that record flows into Supply automatically — worth a heads-up to Supply's PM before shipping one, per `availability.py`.

**Routing mechanics** (`00-rook/code/dispatch-routing/`, owned by Wen Li): each available responder gets a score = proximity (weight 0.60) + recent-acceptance (0.25) + capability match (0.15), highest offered first. Recent-acceptance is a running 0–1 score, +0.08 on accept, **−0.12 on decline *or* timeout — the code treats a timeout exactly like an active decline.**

### Vocabulary

- **Callout** — a request for a responder to attend an incident; **callout offer** — that request live on one responder's phone; **callout timeout** — how long it stays live (currently 60s) before moving on.
- **Capability tag** — labeled competency (flight, structural-entry, hazmat-tolerant, cold-weather, aquatic, crowd-management, de-escalation) matched against incident requirements.
- **Routing priority** — the ranking score above.
- **Mutual aid** — responders covering across regions; not built yet, Q4 exploration.
- Full glossary: `00-rook/company/glossary.docx`.

### The people

| Name | Role | Notes |
|---|---|---|
| Helen Achebe | Director of Product (Dispatch & Supply) | Owns roadmap/commitments |
| Marcus Oyelaran | Eng Manager, Dispatch | First stop for anything unsure; can pull numbers |
| Wen Li | Staff Eng, routing | Built it; no design doc exists, ask her directly |
| Sofia Marino | Product Designer, Dispatch | Currently running console redesign research |
| Nadia Hoffmann | Support Lead (both surfaces) | Tracks ticket trends, based in Berlin |
| Ravi Menon | Data Analyst (both surfaces) | Weekly acceptance-rate numbers, requests via #data |

### Where things stand

**4.2 shipped 12 Aug 2026** and rebalanced routing weight toward proximity and away from recent-acceptance, and cut the offer timeout 90s→60s. Both were deliberate, long-requested changes — not framed internally as something to revert.

Since then, acceptance is down and tickets are up (~3x normal), splitting into two recurring complaints: "my phone never goes off" and "it buzzed and was already gone." Priya's handoff read this as mostly seasonal and left it for a fresh look in September.

**Confirmed against `00-rook/data/callout-history.csv` (weekly pings sent/taken per responder, late Jun–end of Aug):** these are two different problems, one transient and one not.
- System-wide acceptance dropped 78%→54% the week 4.2 shipped, then recovered to ~73% by 31 Aug — consistent with the timeout cut (90s→60s) causing a one-time wave of near-misses that's fading as people adapt. Explains the "lost it fast" tickets (Vantage, Falkirk, Longcast, Cindermark).
- Separately, and **not recovering**: four responders — Vesper, Farlight, The Undertow, Meteor Mite — have had weekly offer volume collapse toward zero (e.g. Farlight: 12→10→3→1→0 over the last five weeks) while a different group (Nightwell, The Gale, Stormwrack, Vantage, Falkirk) is absorbing more offers each week. All 16 responders took the same bad week when 4.2 shipped; only these four never recovered. Matches `history.py`: a timeout scores exactly like a decline (−0.12), the score never regenerates on its own (Wen's 2019 TODO, still open), and it only updates when someone is actually offered a callout — so one bad week plus the lower recent-acceptance weight (0.40→0.25) and harder proximity cutoff (0.60 weight, hard zero past 45 min) was enough to knock a few responders below the threshold where they get reached at all, with no mechanism to climb back. Kip's interview independently corroborates this (Meteor Mite dead quiet, The Gale nonstop, same handler, same week, same city).
- **Ticket volume is a misleading proxy here.** Nightwell and Ironvale generated the most "gone quiet" tickets, but their actual offer volume is flat-to-rising in the data. Vesper and Meteor Mite — two of the four actually collapsing to zero — never filed a ticket at all; they only surfaced via Sofia's console-redesign interviews.
- Not yet available anywhere in the source material: time-to-accept and coverage-gap data (the other two headline metrics), and any geographic/proximity data to directly confirm the horizon-cutoff theory rather than infer it from timing + code. Worth asking Ravi for both, and Marcus flagged mid-August that the numbers he could pull fast "won't be the real weekly numbers" — worth confirming with him whether this CSV is that rough pull or Ravi's official report before quoting exact figures externally.

**Q3 roadmap** (`00-rook/company/roadmap-q3.pdf`, owner Helen): committed for 4.2 — the routing/timeout changes above and "Availability Confidence" (a confidence score next to stated availability, driven by support escalations — not yet shipped, worth checking status). Committed for 4.3 — Supply's requisition approval chains (Halloran's interview flags this queue as broken today: one FIFO queue regardless of priority flag). Q4 exploring: handler phone app (Supply), shared cover between responders (Dispatch).

**Other open threads from research/tickets, not yet triaged:** console dark mode (repeatedly requested — Kip), filter persistence occasionally reverting without warning (Ambrose), larger status-badge text (Ambrose, Aunt Dot), per-responder alert sounds for handlers managing multiple responders (Kip), Supply's failure-report and catalog-search complaints (Halloran) — Supply-side, not mine to fix but worth relaying.

### Open loops to close

- **Marcus asked Wen the exact right question on 14 Aug** (Slack, `company/notes/dispatch-slack-thread.txt`) — does the 4.2 config distinguish responders who've been declining/timing out from everyone else when reweighting who gets pinged. Wen went on PTO before answering and it was never picked back up. This is the mechanism question behind the four-responder collapse above — worth forwarding her the thread plus what the data shows now.
- **No quartermaster-voice research exists.** All four of Sofia's interviews are handlers; Supply's 4.3 commitment (requisition approval chains) is about a quartermaster-side bottleneck, but the only account of it on file (Halloran's) is from the requester side, not the approver side.
- **"Shared cover between responders" (roadmap-q3.pdf, Dispatch, Q4/Exploring) and "Mutual aid" (glossary.docx) read like the same initiative under two different names** — same status, same quarter, same description. Worth confirming with Helen they're one thing, not two.
- **`who-does-what.xlsx` doesn't list me** despite being dated "last updated 2 September 2026" — Priya's row is still there with no successor. The team directory is stale on its most PM-relevant entry; worth getting fixed rather than assuming it's current elsewhere too.

### File map

- `company/` — about-rook, product one-pagers, release history, Q3 roadmap, glossary, team directory (`who-does-what.xlsx`), handoff doc, Slack export
- `code/dispatch-routing/` — the actual routing/offer/history logic referenced above
- `feedback/tickets/` — 25 support tickets, mostly Aug–Sep 2026, both handler- and responder-filed
- `feedback/interviews/` — 4 console-redesign research transcripts (Sofia Marino)
- `data/callout-history.csv` — weekly pings-sent vs. pings-taken per responder, back to late June 2026
