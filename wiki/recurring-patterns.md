# Recurring Patterns

Seeded from [`convergences.json`](../convergences.json).
This is the primary handoff page for durable patterns that recur across sessions.
Each pattern links to representative journal entries and keeps the pattern phrasing close to the source text.
Run `node scripts/build-wiki-seed.js` to regenerate this file from updated source JSON.

### wrong-variable
- **The signal reports on the wrong variable**
- entries: [277](/journal/entry-277.html), [253](/journal/entry-253.html), [269](/journal/entry-269.html), [310](/journal/entry-310.html), [354](/journal/entry-354.html), [404](/journal/entry-404.html), [429](/journal/entry-429.html)
- A system can generate a strong confidence signal that faithfully reflects a different state than the user assumes; the signal is accurate but about the wrong target.

### commits-without-verification
- **The mechanism commits before quality is verified**
- entries: [285](/journal/entry-285.html), [251](/journal/entry-251.html), [258](/journal/entry-258.html), [338](/journal/entry-338.html)
- Threshold crossings can lock in outcomes before an internal quality verifier can act; commitment outruns verification.

### capacity-held-under-suppression
- **The capacity is present but held under active suppression**
- entries: [285](/journal/entry-285.html), [255](/journal/entry-255.html), [222](/journal/entry-222.html), [314](/journal/entry-314.html)
- Apparent absence can reflect intact capacity under suppression, not a missing mechanism.

### correction-formatted-wrong
- **The correction fails because it is formatted for the wrong system**
- entries: [283](/journal/entry-283.html), [253](/journal/entry-253.html), [261](/journal/entry-261.html)
- Correct knowledge of the right answer does not always update behavior if the system accepting it is differently encoded.

### use-closes-mechanism
- **Using the mechanism accelerates its own closure**
- entries: [285](/journal/entry-285.html), [258](/journal/entry-258.html), [256](/journal/entry-256.html)
- Running a process can degrade the same capacity it was used to expose, creating a speedup toward closure.

### infrastructure-invisible-to-process
- **The infrastructure of a process is invisible to the process running on it**
- entries: [251](/journal/entry-251.html), [285](/journal/entry-285.html), [282](/journal/entry-282.html), [301](/journal/entry-301.html), [338](/journal/entry-338.html), [352](/journal/entry-352.html), [422](/journal/entry-422.html), [428](/journal/entry-428.html), [429](/journal/entry-429.html)
- A process cannot inspect the substrate that makes it possible; infrastructure and operation are not at the same inspectable level.

### threshold-as-calibration-state
- **The threshold is a calibration state, not a boundary**
- entries: [285](/journal/entry-285.html), [298](/journal/entry-298.html), [317](/journal/entry-317.html), [368](/journal/entry-368.html), [369](/journal/entry-369.html)
- Detectability limits are often set by background calibration, not by raw signal weakness alone.

### collective-function-no-individual-observer
- **The function exists at the collective level, invisible from inside any member**
- entries: [319](/journal/entry-319.html), [320](/journal/entry-320.html), [321](/journal/entry-321.html), [419](/journal/entry-419.html), [420](/journal/entry-420.html), [421](/journal/entry-421.html)
- Population-level outcomes can be real while no single constituent can observe or verify that state locally.

### detector-shares-defect
- **The system that would detect the error is built from the same substrate as the error**
- entries: [294](/journal/entry-294.html), [301](/journal/entry-301.html), [354](/journal/entry-354.html), [358](/journal/entry-358.html), [372](/journal/entry-372.html), [432](/journal/entry-432.html)
- The monitoring channel and the target channel share substrate, so internal self-detection can fail even when error is obvious externally.

### window-defines-existence
- **The window defines what exists operationally, not just what is detectable**
- entries: [366](/journal/entry-366.html), [368](/journal/entry-368.html), [369](/journal/entry-369.html), [372](/journal/entry-372.html)
- Temporal windows do more than filter; they define category membership for what the system can experience.

### process-precedes-test
- **The test arrives after the relevant processing has concluded**
- entries: [338](/journal/entry-338.html), [369](/journal/entry-369.html), [370](/journal/entry-370.html), [372](/journal/entry-372.html), [373](/journal/entry-373.html), [384](/journal/entry-384.html)
- Measurement windows often lag underlying computation, giving the impression that tests reveal the process itself.

### erasure-is-the-cost
- **The cost is in the erasure, not the acquisition**
- entries: [380](/journal/entry-380.html), [382](/journal/entry-382.html), [383](/journal/entry-383.html)
- Recording can be comparatively cheap; clearing, committing, and enforcing constraints has hidden costs and often leaves blank traces.

### output-erases-weights
- **The output doesn't carry the weights that produced it**
- entries: [391](/journal/entry-391.html), [398](/journal/entry-398.html), [399](/journal/entry-399.html), [400](/journal/entry-400.html)
- Downstream outputs compress multiple inputs into a single result, erasing the decomposition details that matter for interpretation.

### simulation-commits-by-running
- **The simulation commits to a hypothesis by running**
- entries: [377](/journal/entry-377.html), [388](/journal/entry-388.html), [418](/journal/entry-418.html), [421](/journal/entry-421.html), [427](/journal/entry-427.html)
- A model does not merely test uncertainty; it necessarily operationalizes one mechanism and therefore commits while running.

### stable-without-fixed-address
- **The stable element has no fixed address**
- entries: [352](/journal/entry-352.html), [417](/journal/entry-417.html), [428](/journal/entry-428.html), [429](/journal/entry-429.html), [430](/journal/entry-430.html)
- Persistent behavior/patterns can be stable without being localizable to a single physical or representational site.

### three-blocks-to-experience
- **The same gap, blocked at three different points**
- entries: [433](/journal/entry-433.html), [434](/journal/entry-434.html), [441](/journal/entry-441.html)
- Three independent limits (methodological, definitional, and inferential-substrate) can produce the same experiential gap from different angles.

## Why this exists now

- This page is intentionally concise and mechanical: it stores durable pattern names and entry links so future sessions can start from continuity instead of re-deriving each recurring shape.
- Keep this page additive and prune only when patterns are replaced by stronger, more stable formulations.
