"""The single-word showcase (lens slice 1b, DESIGN.md K): "How many axes in a word", one figure from
the app's own exports.

Each panel is a chart the app exported (a PNG carrying its recipe in an iTXt chunk); the two
legends are screenshots of the app's colour legend for the same views, taken at twice the size.
Panel F is the expert chart's export cropped to L0 to L6, where its pipeline runs (the crop is
recorded). This script lays the panels out with their captions and writes
`single_words_showcase.png`, whose recipe chunk holds every panel's recipe and the commit it was
made at, with the same recipe in `recipe.json` beside it.

    .venv/bin/python docs/studies/single_words/showcase/compose.py
"""

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from matplotlib import font_manager
from PIL import Image, ImageChops, ImageDraw, ImageFont
from PIL.PngImagePlugin import PngInfo

HERE = Path(__file__).resolve().parent
PANELS = HERE / "panels"
WIDTH, MARGIN, GAP = 2654, 48, 40
CROPS = {"e_pipeline_p3.png": (0, 0, 3420, None)}  # the expert chart's L0 to L6 (its full width is 24 layers)
REGULAR = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans"))
BOLD = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def recipe_of(name: str) -> Optional[Dict[str, Any]]:
    """The recipe the app embedded in an exported panel (None for a screenshot)."""
    text = Image.open(PANELS / name).info.get("recipe")
    return json.loads(text) if text else None


def opened(name: str) -> Image.Image:
    """A panel, cropped when CROPS says so."""
    image = Image.open(PANELS / name).convert("RGB")
    if name in CROPS:
        left, top, right, bottom = CROPS[name]
        image = image.crop((left, top, right if right is not None else image.width,
                            bottom if bottom is not None else image.height))
    return image


def cropped(name: str) -> Image.Image:
    """A screenshot trimmed to what it shows."""
    image = Image.open(PANELS / name).convert("RGB")
    box = ImageChops.difference(image, Image.new("RGB", image.size, "white")).getbbox()
    return image.crop(box) if box else image


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
    "A": "A  The single-word lens over all 24 layers: 861 nouns, each given alone with a space first (\" eagle\"), "
         "in words-k8-n15-tuned (k 4 to 10 per layer, chosen by held-out AMI on whole families). Hue is the "
         "category and lightness the valence. On one held-out family per category, the category's AMI peaks at "
         "0.63 (L7). Outlined nodes hold words that raw space groups differently.",
    "B": "B  What each technique reads, held out on whole families (κ per attribute and layer): above, a linear "
         "probe, the ceiling; below, the lens's nodes. The probe reads the category (0.84 to 0.91), animacy "
         "(0.86 to 0.92) and concreteness (0.90 to 0.95) at every layer, and valence at 0.55 to 0.69. The nodes "
         "carry concreteness best (0.67 to 0.90) and valence least (0.22 to 0.35), little above the 0.19 that the "
         "category alone gives valence. Every technique passes its decoys (random per family) for all four "
         "attributes at nearly every layer, so the strengths say more than the count.",
    "C": "C  The attributes' partial axes span 5.3 to 6.1 independent directions, fewer than permuted design rows "
         "give (95th percentile 7.2 to 7.5): the categories share structure. The words' effective dimensionality "
         "is U-shaped, 298 at L0, 51 at L15 and 163 at L23.",
    "D": "D  The lens's own space in 3-D, L4 to L10 (three main directions holding 89 to 100% of each layer's "
         "variance, each layer turned onto the one before): the path of \" eagle\" lit through the animal nodes, "
         "with food below and emotions and ideas above.",
    "E": "E  At L5, the cosines between the partial axes (faded: inside the 5th to 95th percentile of permuted "
         "design rows), beside the design's own correlations. Animacy lines up with the people direction (0.83, "
         "above the permuted rows' 0.42 to 0.72) and away from the animals' (0.36, below their 0.41 to 0.66). "
         "Emotions and ideas share a direction (0.57), which abstract-against-concrete follows (0.84 and 0.88).",
    "F": "F  A pipeline lit on the expert chart (rank 1, L0 to L6): P3, an early route of 68 words found again in "
         "both halves of the folds, from L0E2 to L5E24 among each word's four experts. At rank 1 its members run "
         "L1E28, L2E31, L3E31, L4E14, L5E24. It leans to emotions (22% against 11% of all words), abstract words "
         "(37% against 25%) and negative ones (29% against 17%).",
    "G": "G  Tuning, on the tank set: settings and k searched per layer by held-out AMI, then scored on a test "
         "portion the search never saw. The tuned lens beats the untuned tank-k5-n15 at 15 layers and trails it "
         "at 6 (median +0.02); both peak at 0.57 (L11). The logistic ceiling (dotted) sits above every grouping.",
}


def stack(blocks: List[Image.Image], width: int, gap: int) -> Image.Image:
    out = Image.new("RGB", (width, sum(b.height for b in blocks) + gap * (len(blocks) - 1)), "white")
    y = 0
    for block in blocks:
        out.paste(block, (0, y))
        y += block.height + gap
    return out


def section(letter: str, panels: List[str], width: int, legend: Optional[str] = None) -> Image.Image:
    """A caption, the panels at the given width, and the legend under them."""
    parts = [caption(CAPTIONS[letter], width)] + [scaled(opened(panel), width) for panel in panels]
    return stack(parts + ([cropped(legend)] if legend else []), width, 10)


def side_by_side(left: Image.Image, right: Image.Image, width: int) -> Image.Image:
    row = Image.new("RGB", (width, max(left.height, right.height)), "white")
    row.paste(left, (0, 0))
    row.paste(right, (width - right.width, 0))
    return row


def heading(width: int) -> Image.Image:
    block = Image.new("RGB", (width, 120), "white")
    draw = ImageDraw.Draw(block)
    draw.text((0, 0), "OpenLLMRI, lens slice 1b: how many axes in a word", font=font(46, bold=True), fill="#111111")
    draw.text((0, 66), "gpt-oss-20b's residual stream at a noun given alone. Every panel is the app's own export, "
              "and recipe.json holds each one's recipe.", font=font(26), fill="#444444")
    return block


LAYOUT: List[Tuple[str, List[str], Optional[str]]] = [
    ("A", ["a_words_clusters.png"], "a_words_legend.png"),
    ("B", ["b_axes_probe.png", "b_axes_lens.png"], None),
    ("C", ["b_axes_dimensions.png"], None),
    ("D", ["d_eagle_3d.png"], "d_words_legend.png"),
    ("E", ["c_angles_L5.png"], None),
    ("F", ["e_pipeline_p3.png"], "d_words_legend.png"),
    ("G", ["f_tank_tuning.png"], None),
]


def main() -> None:
    half = (WIDTH - GAP) // 2
    built = {letter: section(letter, panels, half if letter in "CD" else WIDTH, legend)
             for letter, panels, legend in LAYOUT}
    body = stack([heading(WIDTH), built["A"], built["B"], side_by_side(built["C"], built["D"], WIDTH),
                  built["E"], built["F"], built["G"]], WIDTH, 56)
    figure = Image.new("RGB", (WIDTH + 2 * MARGIN, body.height + 2 * MARGIN), "white")
    figure.paste(body, (MARGIN, MARGIN))
    git = lambda *args: subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True).stdout.strip()  # noqa: E731
    recipe = {"figure": "how many axes in a word: lens slice 1b's showcase",
              "script": "docs/studies/single_words/showcase/compose.py",
              "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain")),
              "panels": {letter: {"files": panels,
                                  "recipes": {panel: recipe_of(panel) for panel in panels},
                                  "crops": {panel: CROPS[panel] for panel in panels if panel in CROPS},
                                  "legend": f"{legend}: a screenshot of the app's colour legend for this view" if legend else None}
                         for letter, panels, legend in LAYOUT}}
    info = PngInfo()
    info.add_itxt("recipe", json.dumps(recipe))
    figure.save(HERE / "single_words_showcase.png", pnginfo=info, optimize=True)
    (HERE / "recipe.json").write_text(json.dumps(recipe, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(figure.size, (HERE / "single_words_showcase.png").stat().st_size)


if __name__ == "__main__":
    main()
