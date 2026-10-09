"""What analysts are told (DESIGN.md E8): one set of rules for every card, a question for each
kind of subject, and the shape of the answer. `PROMPT_VERSION` changes whenever any of it does;
the analyst tests are matched to it."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Dict, List

INTRO = """You are an analyst for OpenLLMRI, a tool that studies how the language model gpt-oss-20b \
represents meaning. A lens groups sentences by the model's internal state at one word (the target \
word), layer by layer; each group at a layer is a node. Experts are the model's routed \
sub-networks: at each layer the router sends each word to four of them, ranked by gate weight. \
A pipeline (P1, P2, ...) is a chain of experts across consecutive layers that a group of items \
keeps among its four; a hub (H1, H2, ...) is an expert whose items arrive from different experts \
at the layer before.

"""

CARD_TASK = """Write a short card for a researcher about the subject below, from the evidence alone.

"""

# How every answer treats the evidence: cards and answers to questions alike
EVIDENCE_RULES = """Rules:
- Say only what the evidence shows. Don't guess at causes it can't show.
- Every number you write must come from a fact and be followed in the same sentence by the fact's \
id in brackets, like "89 items [F1]" or "84% [F4]". Shares are fractions; you may write them as \
percentages, and you may round. Don't compute new numbers such as sums, differences or ratios.
- Write layers, nodes and experts by their ids (L12, L12C0, L12E5), never as bare numbers. Don't \
write dates.
- Put quoted sentences and tokens inside double quotes.
"""

CARD_FIELDS = """- pattern: "clear" when the evidence shows a specific pattern, such as one designed value far \
above its share of all items, or tokens that name a theme; "weak" for a tendency; "none" when \
the population looks like a mix. A card that reports nothing is the right card when there is \
nothing to report.
- title: what the subject is about, in at most eight words, with no numbers.
- sections (the lens report only): clusters, experts, and pipelines_and_hubs, two to four \
sentences each, under the same rules.
- summary: two or three sentences. points: up to five short findings. caveats: up to three \
things a reader should be careful about (a surface feature, weaker folds, small numbers, \
disagreement with raw space), or none.
"""

RULES = INTRO + CARD_TASK + EVIDENCE_RULES + CARD_FIELDS

QUESTIONS = {
    "node": "What does this node hold, and what sets it apart from the rest of the layer? Compare its "
            "shares with all items' shares; use its tokens, neurons and routing if given; say where its "
            "items come from and go.",
    "expert": "What does this expert take? Compare its items' shares with all items'; say which nodes "
              "they sit in and which experts take them the layer before and after.",
    "route": "What sets the items taking this route apart from the source node's other items?",
    "expert_route": "What sets the items taking this expert route apart from the first expert's other items?",
    "split": "What separates the branches? Name the designed axis or the theme that differs between them, "
             "from the branch shares, the agreement facts and the examples.",
    "lens": "Across the layers: where do the designed axes separate, where do nodes split or merge, how do "
            "the experts line up with the nodes, and what should a reader be careful about (surface "
            "features, weaker folds, disagreement with raw space, the self-check)? In the sections: the "
            "clusters (where and how the nodes separate the designed values), the experts (which differ "
            "by designed value, and how well), and the pipelines and hubs (which groups of items keep "
            "which experts, and whether any stand apart from all items' shares).",
    "routes": "Which pipelines and hubs stand out, and what sets their items apart? Compare each pipeline's "
              "shares with all items' shares; say which experts differ by designed value, and how well. A "
              "pipeline that every value takes in about its usual share is a trunk: report it, but it is "
              "not a pattern.",
    "k": "Advise which k to cut at each layer, or at runs of layers, and why, from the k profile. Say where "
         "the labels and the label-free methods agree and where they don't.",
}

CARD_SCHEMA: Dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "pattern": {"type": "string", "enum": ["clear", "weak", "none"]},
        "summary": {"type": "string"},
        "points": {"type": "array", "items": {"type": "string"}, "maxItems": 5},
        "caveats": {"type": "array", "items": {"type": "string"}, "maxItems": 3},
    },
    "required": ["title", "pattern", "summary", "points", "caveats"],
    "additionalProperties": False,
}

RECONCILED_SCHEMA: Dict[str, Any] = {
    **CARD_SCHEMA,
    "properties": {**CARD_SCHEMA["properties"],
                   "disagreements": {"type": "array", "items": {"type": "string"}, "maxItems": 5}},
    "required": [*CARD_SCHEMA["required"], "disagreements"],
}

# The lens report's sections (DESIGN.md C7): its clusters, the experts involved, its pipelines and hubs
SECTIONS = ("clusters", "experts", "pipelines_and_hubs")
SECTIONS_SCHEMA: Dict[str, Any] = {"type": "object", "properties": {key: {"type": "string"} for key in SECTIONS},
                                   "required": list(SECTIONS), "additionalProperties": False}


def with_sections(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {**schema, "properties": {**schema["properties"], "sections": SECTIONS_SCHEMA},
            "required": [*schema["required"], "sections"]}


def card_schema(kind: str) -> Dict[str, Any]:
    return with_sections(CARD_SCHEMA) if kind == "lens" else CARD_SCHEMA


def reconciled_schema(kind: str) -> Dict[str, Any]:
    return with_sections(RECONCILED_SCHEMA) if kind == "lens" else RECONCILED_SCHEMA

ANSWER_SCHEMA: Dict[str, Any] = {"type": "object", "properties": {"answer": {"type": "string"}},
                                 "required": ["answer"], "additionalProperties": False}

PICK_SCHEMA: Dict[str, Any] = {"type": "object",
                               "properties": {"members": {"type": "array", "items": {"type": "integer"}}},
                               "required": ["members"], "additionalProperties": False}

RECONCILE = """Two analysts wrote the cards below independently, from the same evidence. Write the \
final card: keep what both support, settle each difference from the evidence, and list in \
disagreements each point where they differed and how the evidence settles it, or that it can't. \
The same rules apply."""

QUESTION = """A researcher asks a question about the subject below. Answer it from the evidence \
alone, in a few plain sentences, with no headings or lists; if the evidence can't answer it, say so.

"""

PICK = """Below is a description of a group of sentences, then a numbered list of sentences. About \
half of the sentences belong to the group. Give the numbers of the ones you judge belong to it."""


def card_prompt(evidence: str, kind: str) -> str:
    return f"{RULES}\nThe question for this card: {QUESTIONS[kind]}\n\nEvidence:\n\n{evidence}\n"


def retry_prompt(evidence: str, kind: str, card: Dict[str, Any], failures: List[Dict[str, str]]) -> str:
    listed = "\n".join(f"- {f['numeral'] or '(a citation)'}: {f['reason']}" for f in failures)
    return (card_prompt(evidence, kind) + f"\nYour first card was:\n{json.dumps(card, indent=1)}\n\n"
            f"Some of its numbers don't trace to the facts:\n{listed}\n\nWrite the card again so that every "
            "number is copied from a fact (rounding is fine) and cited right after it, or leave the number out.\n")


def reconcile_prompt(evidence: str, kind: str, drafts: List[Dict[str, Any]]) -> str:
    shown = "\n\n".join(f"Card {i + 1}:\n{json.dumps(d, indent=1)}" for i, d in enumerate(drafts))
    return f"{RULES}\n{RECONCILE}\n\nThe question for this card: {QUESTIONS[kind]}\n\n{shown}\n\nEvidence:\n\n{evidence}\n"


def question_prompt(evidence: str, question: str) -> str:
    return f"{INTRO}{QUESTION}{EVIDENCE_RULES}\nQuestion: {question}\n\nEvidence:\n\n{evidence}\n"


def pick_prompt(title: str, summary: str, sentences: List[str]) -> str:
    numbered = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(sentences))
    return f"{PICK}\n\nDescription: {title}. {summary}\n\nSentences:\n{numbered}\n"


# What the analyst tests exercise (cards, the reconciled report, picking members); answers to
# questions aren't tested, so their prompt stays out of it
PROMPT_VERSION = hashlib.sha256(json.dumps(
    [RULES, QUESTIONS, CARD_SCHEMA, RECONCILED_SCHEMA, SECTIONS_SCHEMA, PICK_SCHEMA, RECONCILE, PICK],
    sort_keys=True).encode()).hexdigest()[:12]
