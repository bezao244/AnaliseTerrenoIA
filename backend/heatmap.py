import base64
import io
from typing import Tuple
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from schemas import TerrainAnalysis


TERRAIN_COLORS = {
    "água": (0, 119, 190),
    "water": (0, 119, 190),
    "vegetação": (34, 139, 34),
    "vegetation": (34, 139, 34),
    "solo": (139, 69, 19),
    "soil": (139, 69, 19),
    "solo exposto": (139, 69, 19),
    "rocha": (128, 128, 128),
    "rock": (128, 128, 128),
    "areia": (244, 164, 96),
    "sand": (244, 164, 96),
    "árvores": (0, 100, 0),
    "trees": (0, 100, 0),
    "floresta": (0, 100, 0),
    "forest": (0, 100, 0),
    "pastagem": (124, 185, 82),
    "grass": (124, 185, 82),
    "urbano": (169, 169, 169),
    "urban": (169, 169, 169),
}

DEFAULT_COLORS = [
    (34, 139, 34),
    (139, 69, 19),
    (0, 119, 190),
    (128, 128, 128),
    (244, 164, 96),
    (0, 100, 0),
    (169, 169, 169),
    (255, 165, 0),
]


def _get_color_for_component(name: str, hex_color: str, index: int) -> Tuple[int, int, int]:
    name_lower = name.lower()
    for key, color in TERRAIN_COLORS.items():
        if key in name_lower:
            return color

    if hex_color and hex_color.startswith("#") and len(hex_color) == 7:
        try:
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            return (r, g, b)
        except ValueError:
            pass

    return DEFAULT_COLORS[index % len(DEFAULT_COLORS)]


def generate_heatmap(image_bytes: bytes, analysis: TerrainAnalysis) -> str:
    original = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
    width, height = original.size

    legend_height = max(80, 30 + len(analysis.components) * 25)
    total_height = height + legend_height

    result = Image.new("RGBA", (width, total_height), (255, 255, 255, 255))
    result.paste(original, (0, 0))

    if analysis.components:
        overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        num_components = len(analysis.components)
        strip_width = width // max(num_components, 1)

        for i, component in enumerate(analysis.components):
            color = _get_color_for_component(component.name, component.color, i)
            alpha = int(120 * (component.percentage / 100.0) + 40)
            alpha = min(180, max(40, alpha))

            x0 = i * strip_width
            x1 = x0 + strip_width if i < num_components - 1 else width

            blend_height = int(height * (component.percentage / 100.0))
            blend_height = max(blend_height, 10)
            y0 = max(0, (height - blend_height) // 2)
            y1 = min(height, y0 + blend_height)

            draw.rectangle([x0, y0, x1, y1], fill=(*color, alpha))

        result.paste(Image.alpha_composite(original, overlay), (0, 0))

    legend_area = ImageDraw.Draw(result)
    legend_area.rectangle(
        [0, height, width, total_height],
        fill=(240, 240, 240, 255)
    )
    legend_area.line([0, height, width, height], fill=(200, 200, 200), width=2)

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
        title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
    except (IOError, OSError):
        font = ImageFont.load_default()
        title_font = font

    legend_area.text((10, height + 8), "Legenda:", fill=(50, 50, 50), font=title_font)

    x_pos = 10
    y_pos = height + 28
    for i, component in enumerate(analysis.components):
        color = _get_color_for_component(component.name, component.color, i)
        legend_area.rectangle(
            [x_pos, y_pos, x_pos + 16, y_pos + 16],
            fill=(*color, 255)
        )
        label = f"{component.name} ({component.percentage:.1f}%)"
        legend_area.text((x_pos + 22, y_pos), label, fill=(50, 50, 50), font=font)
        x_pos += 180
        if x_pos + 180 > width:
            x_pos = 10
            y_pos += 22

    result_rgb = result.convert("RGB")
    buffer = io.BytesIO()
    result_rgb.save(buffer, format="PNG", optimize=True)
    buffer.seek(0)

    return base64.b64encode(buffer.getvalue()).decode("utf-8")
