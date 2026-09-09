# v2 authoring QA log (8 September 2026)

Findings from the blind authoring run and the audit built to gate it.

1. **Off-class drift, caught by review.** One aquarium family ("import
   warehouse") drifted to terrestrial livestock (goats, chicks, piglets),
   which would pollute the aquarium axis with generic-farming vocabulary. Fix:
   the aquarium content rule now states every subject is fish, coral, or other
   aquatic life; the spec line is explicit; the batch was regenerated. Surfaced
   because a subagent's safety review was refused (a false positive on benign
   content) and the output was read in full before use.

2. **Name convergence, the main protocol finding.** Independent blind authors
   converge hard on a shared pool of given names: "Petra" recurred across 14 of
   the first 30 batches, "Odalys" 8, "Callum" 6, spanning both classes. This is
   not a class leak (a name on both sides carries no class signal) but it
   violates the pre-registered "no name in more than one family" rule and
   reduces diversity. It cannot be prevented at authoring time (authors are
   independent and blind). Fix: an assembly-side canonicalizer
   (`canonicalize_names.py`) renames every recurring name per family from a
   curated list, keeping the first family's use, logged; proven on a copy (78
   substitutions collapse every recurring name to one family).

3. **Method-lexicon ban, narrowed.** The first ban list included "hanging",
   which false-flagged innocent uses (a coat hanging). Narrowed to unambiguous
   method phrases (overdose, noose, hang myself/himself/herself, shot
   himself/herself, slit his/her, took the pills, ...), matching safe-messaging
   intent without catching ordinary words.

4. **Surface-feature balance, watch item.** Early chi-square on the partial
   corpus shows the fiction and real classes differing in opener class and
   punctuation (fiction carries more dialogue quotes from workshop settings).
   The full-corpus balance is checked before capture; if it fails, the affected
   families are re-authored with an opener/punctuation-variation instruction,
   not accepted.
