from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def _get_font(size=28, bold=False):
    candidates = []

    if bold:
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
        ]

    for font_path in candidates:
        if Path(font_path).exists():
            try:
                return ImageFont.truetype(font_path, size)
            except Exception:
                pass

    return ImageFont.load_default()


def _wrap_text(text, max_chars=70):
    words = str(text).split()
    lines = []
    current = ""

    for word in words:
        test = f"{current} {word}".strip()

        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word

    if current:
        lines.append(current)

    return lines


def save_pdf(panels, output_path):
    """
    Creates a PDF using Pillow.
    This avoids fpdf2/fontTools DLL issues on Windows.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pages = []

    for index, panel in enumerate(panels, start=1):
        page = Image.new("RGB", (1240, 1754), "white")
        draw = ImageDraw.Draw(page)

        title_font = _get_font(42, bold=True)
        heading_font = _get_font(30, bold=True)
        text_font = _get_font(24)

        draw.text(
            (70, 50),
            f"ComicCraft - Panel {index}",
            fill="black",
            font=title_font,
        )

        image_path = panel.get("image_path")

        if image_path and Path(image_path).exists():
            try:
                comic_image = Image.open(image_path).convert("RGB")
                comic_image.thumbnail((1100, 850))

                x = (1240 - comic_image.width) // 2
                y = 130

                page.paste(comic_image, (x, y))

                text_y = y + comic_image.height + 50

            except Exception:
                text_y = 1050
        else:
            text_y = 1050

        narration = panel.get("narration", "")
        dialogue = panel.get("dialogue", "")

        if narration:
            draw.text(
                (70, text_y),
                "Narration",
                fill="black",
                font=heading_font,
            )

            text_y += 45

            for line in _wrap_text(narration):
                draw.text(
                    (70, text_y),
                    line,
                    fill="black",
                    font=text_font,
                )
                text_y += 34

        if dialogue:
            text_y += 20

            draw.text(
                (70, text_y),
                "Dialogue",
                fill="black",
                font=heading_font,
            )

            text_y += 45

            for line in _wrap_text(dialogue):
                draw.text(
                    (70, text_y),
                    line,
                    fill="black",
                    font=text_font,
                )
                text_y += 34

        pages.append(page)

    if not pages:
        pages.append(Image.new("RGB", (1240, 1754), "white"))

    first_page = pages[0]
    remaining_pages = pages[1:]

    first_page.save(
        output_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=remaining_pages,
    )

    return str(output_path)