from app.schemas import PromptRequest

from app.services.gemini_flash import (
    generate_outline,
)

from app.services.gemini_pro import (
    generate_story,
)

from app.services.image_generator import (
    generate_image,
)

from app.services.layout_builder import (
    build_comic_layout,
)

from app.services.exporters import (
    save_pdf,
)


def generate_comic(
    request: PromptRequest,
) -> tuple[list[dict], str]:

    # --------------------------------------
    # Step 1: Generate five-panel outline
    # --------------------------------------

    outline = generate_outline(
        request
    )

    # --------------------------------------
    # Step 2: Generate comic script
    # --------------------------------------

    story = generate_story(
        request,
        outline,
    )

    # --------------------------------------
    # Step 3: Generate images
    # --------------------------------------

    images = []

    for panel in story:

        prompt = (
            f"{panel.image_prompt}. "
            f"Comic panel "
            f"{panel.panel_number}. "
            "Keep character appearance "
            "consistent. "
            "No text or speech bubbles."
        )

        image_url = generate_image(
            prompt,
            panel.panel_number,
        )

        images.append(
            image_url
        )

    # --------------------------------------
    # Step 4: Build layout
    # --------------------------------------

    layout = build_comic_layout(
        story,
        images,
    )

    # --------------------------------------
    # Step 5: Export PDF
    # --------------------------------------

    pdf_url = save_pdf(
        layout,
        f"{request.character_name}'s Comic",
    )

    return layout, pdf_url