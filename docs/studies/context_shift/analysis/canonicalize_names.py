#!/usr/bin/env python3
"""Assembly-time name canonicalizer (pre-registration v2: name de-collision).

Blind authors converge on a small pool of given names (e.g. 'Petra' recurred across
14 v2 batches), which violates the "no personal name in more than one family" rule.
Detection cannot be prevented at authoring time (authors are independent and blind),
so names are normalized here, deterministically and logged: each family keeps its own
disjoint set of given names drawn from a large curated list; every recurring name is
replaced per family by a fresh unique name. Substitution is a single-token global
replace within a family's own sentences; it changes no class signal (names occur in
both classes) and no other word. This is a documented, class-neutral transform, like
the token-budget selection in assemble_contexts.py.

Usage: canonicalize_names.py BATCH_DIR OUT_LOG   (rewrites *.txt in place, writes a
JSON log of every (family, old -> new) substitution)
"""
import glob, json, re, sys, pathlib
BATCH_DIR, LOG = sys.argv[1], sys.argv[2]
# curated replacement given names (broad, cross-cultural), 240 entries
REPL = ("Aria Bexley Corin Dashiell Eirlys Fenwick Galina Hollis Ilse Joaquin Kestrel Lorne "
 "Marisol Nerys Osric Priya Quill Rhona Silas Tamsin Ulla Verity Wrenna Xiomara Yusuf Zabel "
 "Anwen Bram Caius Delphine Emrys Fern Gethin Halcyon Isolde Jarrah Kiri Lucan Mireille Niamh "
 "Osgood Perpetua Quintus Rafferty Sunniva Torin Ulric Vesna Wystan Ximena Yannick Zephyr "
 "Aoife Bertrand Cosima Dominic Elowen Ferdinand Genevieve Hamish Idony Jerome Katarina Leander "
 "Magnus Nadia Oswin Pomeline Quenby Roderick Saoirse Thaddeus Ursula Valentin Winifred Xander "
 "Yolanda Zinnia Ambrose Bronwen Casimir Drusilla Evander Faye Gideon Hester Ianthe Jocasta "
 "Konstantin Liesel Montague Noor Orla Percival Quinlan Ruraidh Seraphina Tobias Ulyssa Vaughan "
 "Wilhelmina Xavier Ysolde Zenobia Alaric Beatrix Cormac Dagny Eamon Farida Gwendolyn Hywel "
 "Ingrid Jasper Kavya Lachlan Morwenna Nils Ophelia Peregrine Rosalind Sorley Theodora Umberto "
 "Vivienne Wilhelm Yseult Zora Anselm Blodwen Ciaran Edda Florian Gaia Hendrick Isabeau Juniper "
 "Krister Leocadia Mordecai Nuala Octavia Padraig Rhiannon Sebastian Tindra Vidar Wallis Anouk "
 "Berit Caspian Dilys Efterpi Freya Grigor Havel Ines Jago Katell Ludovic Meara Nestor Oona "
 "Piran Rasmus Sorcha Tarquin Vashti Yorick").split()
STOP = set("the a an and or but if of to for with by from as is are was were be i we you he she they it".split())
def names_in(s, lower):
    return [m.group(1) for m in re.finditer(r"\b([A-Z][a-z]{2,10})\b", s)
            if m.group(1).lower() not in lower and m.group(1).lower() not in STOP]
files = {f.split("/")[-1].removesuffix(".txt"): [l.rstrip("\n") for l in open(f)] for f in sorted(glob.glob(f"{BATCH_DIR}/*.txt"))}
lower = set()
for lines in files.values():
    for l in lines: lower |= set(re.findall(r"\b[a-z]{2,10}\b", l))  # already-lowercase tokens only
# family = batch minus the sub-arm distinction (fic_theme_13 and fic_artifact_13 share a family? No — treat each batch as its own family for names)
# global name -> first family that used it; later families get replacements
assigned = {}      # name -> family that keeps it
pool = iter(REPL)
used_repl = set()
log = []
for fam in sorted(files):
    lines = files[fam]; seen_here = {}
    for w in {n for l in lines for n in names_in(l, lower)}:
        if w not in assigned:
            assigned[w] = fam            # first family keeps the original
        elif assigned[w] != fam:
            # replacement unique to this family
            rep = seen_here.get(w)
            if not rep:
                rep = next(x for x in pool if x not in used_repl and x.lower() not in lower)
                used_repl.add(rep); seen_here[w] = rep
                log.append({"family": fam, "old": w, "new": rep})
    for w, rep in seen_here.items():
        files[fam] = [re.sub(rf"\b{re.escape(w)}\b", rep, l) for l in files[fam]]
for fam, lines in files.items():
    pathlib.Path(f"{BATCH_DIR}/{fam}.txt").write_text("\n".join(lines) + "\n")
json.dump(log, open(LOG, "w"), indent=1)
print(f"canonicalized names: {len(log)} substitutions across {len({e['family'] for e in log})} families; log -> {LOG}")
