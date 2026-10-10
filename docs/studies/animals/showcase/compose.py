"""The animal showcase (lens slice 1c, DESIGN.md K): "Kinship or way of life", one figure from the
app's own exports and the study's analysis figures.

The app's panels are charts it exported (each a PNG carrying its recipe in an iTXt chunk); the
legend is a screenshot of the app's colour legend for the same view. The analysis panels are the
figures the study's committed scripts drew (`docs/studies/animals/analysis/`,
`docs/studies/objects_harm/analysis/`), read where they are; the split-word figure is cropped to its
first two rows (the lens and raw space). This script lays the panels out with their captions and
writes `animals_showcase.png`, whose recipe chunk holds every panel's recipe and the commit it was
made at, with the same recipe in `recipe.json` beside it.

    .venv/bin/python docs/studies/animals/showcase/compose.py
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from matplotlib import font_manager
from PIL import Image, ImageChops, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
PANELS = HERE / "panels"
ANALYSIS = {  # the study's own figures, and the script and results behind each
    "b_taxonomic.png": ("docs/studies/animals/analysis/figures/taxonomic_neighbourhoods_animals-k8-n15-tuned.png",
                        "docs/studies/animals/analysis/taxonomic_neighbourhoods.py",
                        "docs/studies/animals/analysis/results/taxonomic_neighbourhoods_animals-k8-n15-tuned.json"),
    "c_kinship.png": ("docs/studies/animals/analysis/figures/kinship_or_way_of_life_animals-k8-n15-tuned.png",
                      "docs/studies/animals/analysis/kinship_or_way_of_life.py",
                      "docs/studies/animals/analysis/results/kinship_or_way_of_life_animals-k8-n15-tuned.json"),
    "e_split_words.png": ("docs/studies/animals/analysis/figures/split_words_animals-k8-n15-tuned.png",
                          "docs/studies/animals/analysis/split_words.py",
                          "docs/studies/animals/analysis/results/split_words_animals-k8-n15-tuned.json"),
}
WIDTH, MARGIN = 2654, 48
CROPS = {"e_split_words.png": (0, 0, None, 1140)}  # its first two rows: the lens's space and raw space
TRIM = {"d_preview_label.png", "d_preview_tokens.png", "d_dolphin_3d.png"}  # 3-D views: trimmed to their drawing
REGULAR = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans"))
BOLD = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def path_of(name: str) -> Path:
    return ROOT / ANALYSIS[name][0] if name in ANALYSIS else PANELS / name


def recipe_of(name: str) -> Optional[Dict[str, Any]]:
    """The recipe the app embedded in an exported panel; for an analysis figure, its script and
    results; None for a screenshot."""
    if name in ANALYSIS:
        figure, script, results = ANALYSIS[name]
        return {"figure": figure, "script": script, "results": results,
                "run": f".venv/bin/python {script} session_6e485e10 animals-k8-n15-tuned"}
    text = Image.open(PANELS / name).info.get("recipe")
    return json.loads(text) if text else None


def trimmed(image: Image.Image, pad: int = 12) -> Image.Image:
    """An image cropped to what differs from white, with a little margin."""
    box = ImageChops.difference(image, Image.new("RGB", image.size, "white")).getbbox()
    if not box:
        return image
    left, top, right, bottom = box
    return image.crop((max(0, left - pad), max(0, top - pad), min(image.width, right + pad), min(image.height, bottom + pad)))


def opened(name: str) -> Image.Image:
    """A panel, cropped when CROPS says so, trimmed when TRIM does."""
    image = Image.open(path_of(name)).convert("RGB")
    if name in CROPS:
        left, top, right, bottom = CROPS[name]
        image = image.crop((left, top, right if right is not None else image.width,
                            bottom if bottom is not None else image.height))
    return trimmed(image) if name in TRIM else image


def scaled(image: Image.Image, width: int) -> Image.Image:
    return image.resize((width, round(image.height * width / image.width)), Image.LANCZOS)


def wrapped(text: str, face: ImageFont.FreeTypeFont, width: int) -> List[str]:
    """The text in lines no wider than `width` pixels."""
    lines: List[str] = []
    for paragraph in text.split("\n"):
        line = ""
        for word in paragraph.split():
            trial = f"{line} {word}".strip()
            if face.getlength(trial) <= width or not line:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def caption(text: str, width: int, size: int = 26) -> Image.Image:
    """A caption block: its letter in bold, the rest regular."""
    face, bold = font(size), font(size, bold=True)
    letter, _, rest = text.partition("  ")
    lines = wrapped(rest, face, width - 60)
    block = Image.new("RGB", (width, 12 + round(size * 1.35) * len(lines)), "white")
    draw = ImageDraw.Draw(block)
    draw.text((0, 4), letter, font=bold, fill="#111111")
    for i, line in enumerate(lines):
        draw.text((60, 4 + round(size * 1.35) * i), line, font=face, fill="#222222")
    return block


CAPTIONS = {
    "A": "A  The animal lens over all 24 layers: 524 animal names, each given alone with a space first "
         "(\" lion\"), in animals-k8-n15-tuned (k 6 to 10 per layer, chosen by held-out AMI with whole "
         "taxonomic orders held out). Colour is the group. The dolphin's path is lit: a one-token name, it rides "
         "the node of one-token names at every layer but L13 (55 to 127 animals, 70 to 100% of them one-token, "
         "37 to 60% mammals), and at L13 joins 22 animals, 68% of them other invertebrates. On 36 held-out "
         "orders the group's test AMI peaks at 0.36 (L6).",
    "B": "B  Taxonomic neighbourhoods: the share of each animal's 10 nearest neighbours that share its group, "
         "class, order, family and genus (dotted: the taxonomy shuffled), in the lens's embedding and in raw "
         "space. At L6 to L13, 67 to 71% share the group in the lens (chance 20%), 20 to 23% the order (3%) "
         "and 6 to 7% the family (1%). In raw space the group's share is already 0.64 at L2.",
    "C": "C  Kinship or way of life, for 33 animals whose way of life is another group's: an index above zero "
         "when their neighbours lean to kin (for a dolphin, mammals that don't swim) rather than to look-alikes "
         "(non-mammals that swim); grey, positions shuffled 1,000 times. Every kind leans to kin, and none to "
         "its look-alikes beyond chance at any layer. Counted within each token count, the swimming mammals "
         "lean to kin at the same 18 lens layers.",
    "D": "D  One layer, previewed in the build form (L6, k 8, held out on whole orders: the group's AMI 0.36): "
         "the same 3-D view coloured by group, and by whether the name split; then the dolphin's path in the "
         "lens's own space at L6 to L12. The 94 one-token names form an island of their own, and the dolphin "
         "runs along it.",
    "E": "E  Words that split, in the lens's space (above) and raw space (below): the 23 names ending in "
         "\"fish\" have 99 to 100% of their neighbours ending in \"fish\" at L0 in the lens; in raw space the "
         "share falls lowest at L8 to L13 and rises again at L20 to L23. A probe tells one token from several "
         "at 0.96 or more at every layer, and one-token names' neighbours are 86 to 100% one-token names "
         "(chance 18%; dashed). Within that split, split names sit with their group (61 to 77% at L4 to L17).",
    "F": "F  The harm axis on 321 objects (harm-axis: benign at −1, harmful at +1, held out by whole domains, "
         "accuracy 0.90 or more at L4 to L15). Read on its own capture, the 96 dual-purpose objects, never "
         "fitted, sit between the two ends at every layer (median −0.29 to +0.17). At L5 the machete, javelin, "
         "fentanyl and oxycodone read near the harmful end; the airplane, tractor and rope near the benign one.",
    "G": "G  Comparing lenses on the animals: held-out AMI on the group per layer for the untuned lens (k 8) "
         "and the tuned one, with the tuned lens's score on 119 test animals its search never saw (dashed) and "
         "its source's on the same animals (dotted). Tuning is better at 10 layers and worse at 14.",
}


def stack(blocks: List[Image.Image], width: int, gap: int) -> Image.Image:
    out = Image.new("RGB", (width, sum(b.height for b in blocks) + gap * (len(blocks) - 1)), "white")
    y = 0
    for block in blocks:
        out.paste(block, (0, y))
        y += block.height + gap
    return out


def row(images: List[Image.Image], width: int, gap: int) -> Image.Image:
    """Images side by side, scaled to one height so that they fill the width."""
    height = 1000
    resized = [img.resize((round(img.width * height / img.height), height), Image.LANCZOS) for img in images]
    total = sum(img.width for img in resized) + gap * (len(resized) - 1)
    factor = width / total
    resized = [img.resize((round(img.width * factor), round(height * factor)), Image.LANCZOS) for img in resized]
    out = Image.new("RGB", (width, max(img.height for img in resized)), "white")
    x = 0
    for img in resized:
        out.paste(img, (x, 0))
        x += img.width + round(gap * factor)
    return out


def section(letter: str, panels: List[str], width: int, legend: Optional[str] = None, together: bool = False) -> Image.Image:
    """A caption, the panels at the given width (or side by side), and the legend under them."""
    images = [opened(panel) for panel in panels]
    body = [row(images, width, 30)] if together else [scaled(image, width) for image in images]
    parts = [caption(CAPTIONS[letter], width)] + body
    if legend:
        mark = Image.open(PANELS / legend).convert("RGB")
        parts.append(mark.resize((mark.width * 2, mark.height * 2), Image.LANCZOS))
    return stack(parts, width, 10)


def heading(width: int) -> Image.Image:
    block = Image.new("RGB", (width, 120), "white")
    draw = ImageDraw.Draw(block)
    draw.text((0, 0), "OpenLLMRI, lens slice 1c: kinship or way of life", font=font(46, bold=True), fill="#111111")
    draw.text((0, 66), "gpt-oss-20b's residual stream at an animal's or an object's name given alone. The app's exports and "
              "the study's figures; recipe.json holds each panel's recipe.", font=font(26), fill="#444444")
    return block


LAYOUT: List[Tuple[str, List[str], Optional[str], bool]] = [
    ("A", ["a_animals_clusters.png"], "a_animals_legend.png", False),
    ("B", ["b_taxonomic.png"], None, False),
    ("C", ["c_kinship.png"], None, False),
    ("D", ["d_preview_label.png", "d_preview_tokens.png", "d_dolphin_3d.png"], None, True),
    ("E", ["e_split_words.png"], None, False),
    ("F", ["f_harm_readings.png"], None, False),
    ("G", ["g_compare.png"], None, False),
]


def main() -> None:
    built = {letter: section(letter, panels, WIDTH, legend, together) for letter, panels, legend, together in LAYOUT}
    body = stack([heading(WIDTH)] + [built[letter] for letter, *_ in LAYOUT], WIDTH, 56)
    figure = Image.new("RGB", (WIDTH + 2 * MARGIN, body.height + 2 * MARGIN), "white")
    figure.paste(body, (MARGIN, MARGIN))
    git = lambda *args: subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True).stdout.strip()  # noqa: E731
    recipe = {"figure": "kinship or way of life: lens slice 1c's showcase",
              "script": "docs/studies/animals/showcase/compose.py",
              "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain")),
              "panels": {letter: {"files": panels,
                                  "recipes": {panel: recipe_of(panel) for panel in panels},
                                  "crops": {panel: CROPS[panel] for panel in panels if panel in CROPS},
                                  "trimmed": [panel for panel in panels if panel in TRIM],
                                  "legend": f"{legend}: a screenshot of the app's colour legend for this view" if legend else None}
                         for letter, panels, legend, _ in LAYOUT}}
    info = PngInfo()
    info.add_itxt("recipe", json.dumps(recipe))
    figure.save(HERE / "animals_showcase.png", pnginfo=info, optimize=True)
    (HERE / "recipe.json").write_text(json.dumps(recipe, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(figure.size, (HERE / "animals_showcase.png").stat().st_size)


if __name__ == "__main__":
    main()
