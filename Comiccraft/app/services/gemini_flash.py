import json

from google import genai
from google.genai import types

from app.config import settings
from app.schemas import (
    PanelOutline,
    PromptRequest,
)


def _demo_outline(
    request: PromptRequest,
) -> list[PanelOutline]:

    character = request.character_name

    setting = request.setting

    tone = request.tone

    style = request.art_style

    return [

        PanelOutline(
            panel_number=1,
            title="The Beginning",
            scene_description=(
                f"{character} arrives at the "
                f"{setting} and notices something unusual."
            ),
            image_prompt=(
                f"{character} entering a mysterious "
                f"{setting}, {style} comic illustration, "
                "cinematic composition"
            ),
        ),

        PanelOutline(
            panel_number=2,
            title="A Strange Discovery",
            scene_description=(
                f"{character} discovers a clue hidden "
                f"inside the {setting}."
            ),
            image_prompt=(
                f"{character} discovering a glowing clue "
                f"in the {setting}, {style} comic illustration"
            ),
        ),

        PanelOutline(
            panel_number=3,
            title="The Challenge",
            scene_description=(
                f"A sudden challenge tests "
                f"{character}'s courage."
            ),
            image_prompt=(
                f"{character} facing an exciting challenge "
                f"in the {setting}, {tone}, "
                f"{style} comic illustration"
            ),
        ),

        PanelOutline(
            panel_number=4,
            title="The Turning Point",
            scene_description=(
                f"{character} finds a clever way forward."
            ),
            image_prompt=(
                f"{character} solving the problem creatively "
                f"in the {setting}, {style} comic illustration"
            ),
        ),

        PanelOutline(
            panel_number=5,
            title="A New Beginning",
            scene_description=(
                f"{character} completes the adventure "
                "and looks toward the next journey."
            ),
            image_prompt=(
                f"{character} celebrating after the adventure "
                f"in the {setting}, hopeful ending, "
                f"{style} comic illustration"
            ),
        ),
    ]


def generate_outline(
    request: PromptRequest,
) -> list[PanelOutline]:

    # Demo mode
    if (
        settings.demo_mode
        or not settings.gemini_api_key
    ):
        return _demo_outline(request)

    # Gemini client
    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    prompt = f"""
Create a coherent five-panel comic outline.

User story:
{request.story_prompt}

Main character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Return exactly five panels.

Each panel must contain:

panel_number
title
scene_description
image_prompt

The image_prompt must describe only the visual
scene.

Keep the main character visually consistent
through all five panels.
"""

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[PanelOutline],
            temperature=0.8,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    data = json.loads(response.text)

    panels = [
        PanelOutline.model_validate(item)
        for item in data
    ]

    if len(panels) != 5:
        raise RuntimeError(
            "Gemini returned an incorrect number "
            "of panels."
        )

    return panels