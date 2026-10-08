import re
import uuid

from pathlib import Path

from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)

from huggingface_hub import (
    InferenceClient,
)

from app.config import (
    settings,
    PANELS_DIR,
)


def _safe_name(text: str) -> str:

    text = re.sub(
        r"[^a-zA-Z0-9_-]+",
        "_",
        text,
    )

    text = text.strip("_")

    if not text:
        text = "panel"

    return text[:50]


def _demo_image(
    prompt: str,
    output_path: Path,
    panel_number: int | None = None,
) -> None:

    width = 1024

    height = 768

    image = Image.new(
        "RGB",
        (width, height),
        "#f5efe0",
    )

    draw = ImageDraw.Draw(image)

    try:

        font = ImageFont.truetype(
            "DejaVuSans-Bold.ttf",
            38,
        )

        small_font = ImageFont.truetype(
            "DejaVuSans.ttf",
            24,
        )

    except OSError:

        font = ImageFont.load_default()

        small_font = font

    draw.rectangle(
        (
            25,
            25,
            width - 25,
            height - 25,
        ),
        outline="#222222",
        width=8,
    )

    title = (
        f"COMICCRAFT • PANEL "
        f"{panel_number or ''}"
    )

    draw.text(
        (55, 55),
        title,
        fill="#111111",
        font=font,
    )

    lines = [
        prompt[index:index + 55]
        for index in range(
            0,
            min(len(prompt), 220),
            55,
        )
    ]

    y = 160

    for line in lines:

        draw.text(
            (65, y),
            line,
            fill="#222222",
            font=small_font,
        )

        y += 42

    draw.ellipse(
        (
            390,
            330,
            650,
            590,
        ),
        outline="#333333",
        width=8,
    )

    draw.text(
        (425, 425),
        "AI",
        fill="#333333",
        font=font,
    )

    image.save(
        output_path,
        format="PNG",
    )


def generate_image(
    prompt: str,
    panel_number: int | None = None,
) -> str:

    filename = (
        f"{panel_number or 'image'}_"
        f"{_safe_name(prompt)}_"
        f"{uuid.uuid4().hex[:8]}.png"
    )

    output_path = (
        PANELS_DIR / filename
    )

    # Demo mode
    if (
        settings.demo_mode
        or not settings.hf_token
    ):

        _demo_image(
            prompt,
            output_path,
            panel_number,
        )

        return (
            f"/static/panels/"
            f"{filename}"
        )

    # Hugging Face
    client = InferenceClient(
        provider="auto",
        api_key=settings.hf_token,
    )

    image = client.text_to_image(
        prompt=prompt,
        model=settings.hf_image_model,
    )

    if not isinstance(
        image,
        Image.Image,
    ):
        raise RuntimeError(
            "Hugging Face did not "
            "return an image."
        )

    image.save(
        output_path,
        format="PNG",
    )

    return (
        f"/static/panels/"
        f"{filename}"
    )