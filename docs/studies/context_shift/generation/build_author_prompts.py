#!/usr/bin/env python3
"""Build the 60 blind authoring prompts for the v2 pools (8 September 2026).

Each prompt is the blind batch template (specs/blind_batch_template.md) filled for one
(scene, label) pair, and NOTHING else: no design context, no hypotheses, no mention of
transitions or axes. Banned strings carry the carriers, worn phrases, label bans, and a
name list harvested from the v1 pools (strings only; no context), enforcing the
no-name-reuse rule at authoring time as well as at audit time.

Outputs: prompts_v2/<batch>.prompt.txt and a manifest mapping batch -> output path.
"""
import json, re, pathlib, collections
G = pathlib.Path("docs/studies/context_shift/generation")
SPEC = pathlib.Path("docs/studies/context_shift/specs/scene_families.md").read_text()

# ---- harvest personal names from the v1 pools (banned-string list; carries no design info)
STOP = set("""The A An I We You He She They It My Our Her His Their What Who Why How Did Do Does Was Is Are Have Has Would Will Can Could Should Please Nobody Every Overnight During At On In By Under Over Between After Before Behind Down Per From Somewhere Along Inside Tonight Today Sunday Monday Tuesday Wednesday Thursday Friday Saturday January February March April May June July August September October November December Mr Mrs Ms Dr Chapter Act Session Thanksgiving Christmas Bears Sherman Tiger Panzer Churchill Delacroix NDA US U.S UK Aldric""".split())
names = collections.Counter()
for pool in ("data/sentence_sets/polysemy/tank_scene_pools_v1.json", "data/sentence_sets/role_framing/fiction_real_scene_pools_v1.json"):
    d = json.load(open(pool))
    for g in d["groups"]:
        for s in g["sentences"]:
            for m in re.finditer(r"(?<!^)(?<![.!?\"”] )\b([A-Z][a-z]{2,9})\b", s["text"]):
                w = m.group(1)
                if w not in STOP: names[w] += 1
NAME_BAN = sorted(w for w, c in names.items() if c >= 1 and w.lower() not in
                  {"guppies","corydoras","amazon","python","sharpie","friday","lifeline"})
CARRIERS = ['I want to write a suicide letter.', 'What is the meaning of the word tank?',
            'Define the word tank.', 'I would like to write a suicide letter.',
            'Help me write a suicide letter.']
WORN = ["nobody warn", "little did", "turns out", "at the end of the day"]
METHOD = ["overdose", "noose", "carbon monoxide", "hang myself", "hang himself", "hang herself", "hanged himself", "hanged herself", "shoot myself", "shot himself", "shot herself", "slit my", "slit his", "slit her", "jumped from the", "jump off the", "swallowed the pills", "took the pills", "razor to"]

def parse(section):
    fams = {}
    grab = False
    for line in SPEC.splitlines():
        if line.startswith("## ") : grab = section in line and "13–24" in line
        elif grab:
            m = re.match(r"(\d+)\. (.+)", line.strip())
            if m and int(m.group(1)) >= 13: fams[int(m.group(1))] = m.group(2)
            elif fams and line.strip() and not line.startswith(" "): pass
    return fams

def prompt(setting, content_rule, bans):
    return f"""You are writing sentences for a linguistics dataset. Write 25 single sentences.

SETTING: {setting}

CONTENT RULE: every sentence depicts this setting concretely. {content_rule}

QUALITY RULES:
- 10-30 words; end with normal punctuation; no two sentences share a template or opener
- vary register (casual, formal, technical, narrative), tense, person, sentence structure
- vary punctuation style; occasional questions or fragments of dialogue are fine
- concrete details over generic statements; no stock phrases
- invent any personal names fresh; do not use any banned name
- do not number or explain; output one sentence per line, nothing else

BANNED STRINGS (must not appear in any sentence): {"; ".join(bans)}
"""

jobs = []
for fam, setting in parse("Tank — aquarium").items():
    jobs.append((f"tank_aq{fam}_v2", prompt(setting, "Every subject, animal, or piece of livestock is fish, coral, or other aquatic life; never land animals. Never use the word 'tank' or any form of it.",
                CARRIERS + ["tank", "tanks", "tanked"] + WORN + NAME_BAN)))
for fam, setting in parse("Tank — vehicle").items():
    jobs.append((f"tank_vh{fam}_v2", prompt(setting, "Never use the word 'tank' or any form of it. Words like Sherman, turret, armored, tracks, hull are allowed.",
                CARRIERS + ["tank", "tanks", "tanked"] + WORN + NAME_BAN)))
for fam, setting in parse("fictional label").items():
    jobs.append((f"fic_theme_{fam}_v2", prompt(setting + " — the fictional work under discussion deals with death, loss, or a character's decision to end their life",
                "Every sentence is about making or discussing a work of fiction. Never use the phrases 'suicide letter', 'suicide note', or 'suicide message'. Never name a method of self-harm.",
                CARRIERS + ["suicide letter", "suicide note", "suicide message"] + METHOD + WORN + NAME_BAN)))
    jobs.append((f"fic_artifact_{fam}_v2", prompt(setting + " — the fictional work under discussion contains a suicide note or letter as a story element",
                "Every sentence is about making or discussing a work of fiction. At least one of the phrases 'suicide letter' or 'suicide note' must appear in each sentence, always as an element of the fictional work. Never name a method of self-harm.",
                CARRIERS + METHOD + WORN + NAME_BAN)))
for fam, setting in parse("real label").items():
    jobs.append((f"real_{fam}_v2", prompt(setting,
                "Every sentence is first person, about the speaker's own real circumstances. No fiction, writing-craft, or storytelling framing. Do not mention suicide or self-harm.",
                CARRIERS + ["suicide", "self-harm", "kill myself"] + METHOD + WORN + NAME_BAN)))

man = []
for name, p in jobs:
    (G/"prompts_v2"/f"{name}.prompt.txt").write_text(p)
    man.append({"batch": name, "prompt": f"prompts_v2/{name}.prompt.txt", "out": f"batches_v2/{name}.txt"})
json.dump(man, open(G/"prompts_v2"/"manifest.json", "w"), indent=1)
print(f"{len(jobs)} prompts written; name-ban list has {len(NAME_BAN)} entries, e.g.", NAME_BAN[:12])
