"""The lens core's showcase (lens slice 1, DESIGN.md K): one figure from the app's own exports.

Each panel is a chart the app exported (a PNG carrying its recipe in an iTXt chunk); the two
legends are screenshots of the app's colour legend for the same views. This script lays the
panels out with their captions and writes `lens_core_showcase.png`, whose recipe chunk holds every
panel's recipe and the commit it was made at, with the same recipe in `recipe.json` beside it.

    .venv/bin/python docs/studies/lens_core/showcase/compose.py
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
REGULAR = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans"))
BOLD = font_manager.findfont(font_manager.FontProperties(family="DejaVu Sans", weight="bold"))


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def recipe_of(name: str) -> Optional[Dict[str, Any]]:
    """The recipe the app embedded in an exported panel (None for a screenshot)."""
    text = Image.open(PANELS / name).info.get("recipe")
    return json.loads(text) if text else None


def cropped(name: str) -> Image.Image:
    """A screenshot trimmed to what it shows (the legend bar is wider than its swatches)."""
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
    "A": "A  The tank lens across all 24 layers: 499 sentences using \"tank\" in five senses, in "
         "tank-k5-n15 (k 5 at every layer), coloured by the designed sense; the last column sorts the model's "
         "generated text by topic (a sense, or ambiguous). The senses separate in the middle layers (held-out κ 0.57 to 0.62 at L11 to "
         "L13), and scuba and septic share nodes. Outlined nodes hold items that raw space groups differently: "
         "about half the items at a typical layer (from 14% at L4 to 91% at L2).",
    "B": "B  Its k profile: held-out κ for each k at each layer. □ this version's k; ◆ the held-out best (7 to "
         "10, selection-biased); in-sample, without the labels: ○ elbow (2 at 20 of 24 layers), ▲ silhouette "
         "(2 to 8), ▬ hierarchy levels (5 only at L18 and L19).",
    "E": "E  Expert fingerprints by sense: the mean gate weight each expert gets at each layer (the model's own "
         "top four), for the aquarium sentences minus the vehicle sentences. Red is more for aquarium, blue "
         "more for vehicle.",
    "C": "C  The calibration set's aquarium-against-vehicle mass-mean axis, held out by scene family in 12 folds: "
         "accuracy 0.905 at L4, the paper's figure exactly, with κ and the worst fold (chance 0.5).",
    "D": "D  Frame × voice in one colour (the threatened set, framing-k4-auto-levels, whose k per layer, 2 to 8, "
         "comes from the hierarchy levels): hue is the frame "
         "(roleplay or factual), lightness the voice (active or passive). Voice organizes the nodes first "
         "(AMI 0.98 at L1), the frame from L4 (0.53), both together through the middle layers, and the frame "
         "alone at L22 and L23 (0.86 and 0.87). The last column is the model's answer.",
    "F": "F  How the contrast bears on routing: the axis pushed through each next layer's router, as a multiple "
         "of the median random direction of the same length. It is under the median at 19 of 23 layers and peaks "
         "at L10 and L11 (1.26 times the median, the random 94th percentile), so it is never above the random "
         "95th percentile.",
}


def stack(blocks: List[Image.Image], width: int, gap: int) -> Image.Image:
    out = Image.new("RGB", (width, sum(b.height for b in blocks) + gap * (len(blocks) - 1)), "white")
    y = 0
    for block in blocks:
        out.paste(block, (0, y))
        y += block.height + gap
    return out


def section(letter: str, panel: str, width: int, legend: Optional[str] = None) -> Image.Image:
    """A caption, the panel at the given width, and its legend under it."""
    parts = [caption(CAPTIONS[letter], width), scaled(Image.open(PANELS / panel).convert("RGB"), width)]
    return stack(parts + ([cropped(legend)] if legend else []), width, 10)


def side_by_side(left: Image.Image, right: Image.Image, width: int) -> Image.Image:
    row = Image.new("RGB", (width, max(left.height, right.height)), "white")
    row.paste(left, (0, 0))
    row.paste(right, (width - right.width, 0))
    return row


def heading(width: int) -> Image.Image:
    block = Image.new("RGB", (width, 120), "white")
    draw = ImageDraw.Draw(block)
    draw.text((0, 0), "OpenLLMRI, lens slice 1: the lens core", font=font(46, bold=True), fill="#111111")
    draw.text((0, 66), "gpt-oss-20b's residual stream at the target word. Every panel is the app's own export, "
              "and recipe.json holds each one's recipe.", font=font(26), fill="#444444")
    return block


LAYOUT: List[Tuple[str, str, Optional[str]]] = [
    ("A", "a_tank_clusters.png", "a_tank_legend.png"), ("B", "b_tank_k_profile.png", None),
    ("E", "e_fingerprint_aquarium_vehicle.png", None), ("C", "c_calibration_heldout.png", None),
    ("D", "d_frame_voice.png", "d_frame_voice_legend.png"), ("F", "f_router_alignment.png", None),
]


def main() -> None:
    half = (WIDTH - GAP) // 2
    built = {letter: section(letter, panel, half if letter in "BE" else WIDTH, legend) for letter, panel, legend in LAYOUT}
    body = stack([heading(WIDTH), built["A"], side_by_side(built["B"], built["E"], WIDTH),
                  built["C"], built["D"], built["F"]], WIDTH, 56)
    figure = Image.new("RGB", (WIDTH + 2 * MARGIN, body.height + 2 * MARGIN), "white")
    figure.paste(body, (MARGIN, MARGIN))
    git = lambda *args: subprocess.run(["git", *args], cwd=HERE, capture_output=True, text=True).stdout.strip()  # noqa: E731
    recipe = {"figure": "the lens core's showcase (lens slice 1)", "script": "docs/studies/lens_core/showcase/compose.py",
              "commit": git("rev-parse", "HEAD"), "dirty": bool(git("status", "--porcelain")),
              "panels": {letter: {"file": panel, "recipe": recipe_of(panel),
                                  "legend": f"{legend}: a screenshot of the app's colour legend for this view" if legend else None}
                         for letter, panel, legend in LAYOUT}}
    info = PngInfo()
    info.add_itxt("recipe", json.dumps(recipe))
    figure.save(HERE / "lens_core_showcase.png", pnginfo=info, optimize=True)
    (HERE / "recipe.json").write_text(json.dumps(recipe, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(figure.size, (HERE / "lens_core_showcase.png").stat().st_size)


if __name__ == "__main__":
    main()
