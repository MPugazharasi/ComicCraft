import json

from google import genai
from google.genai import types

from app.config import settings

from app.schemas import (
    PanelOutline,
    PromptRequest,
    StoryPanel,
)


def _demo_story(
    request: PromptRequest,
    outline: list[PanelOutline],
) -> list[StoryPanel]:

    result = []

    for panel in outline:

        result.append(
            StoryPanel(

                panel_number=panel.panel_number,

                title=panel.title,

                scene_description=(
                    panel.scene_description
                ),

                image_prompt=(
                    panel.image_prompt
                ),

                caption=(
                    f"Meanwhile, in the "
                    f"{request.setting}..."
                ),

                narration=(
                    f"{request.character_name} "
                    "takes a deep breath and "
                    "moves forward. The adventure "
                    "becomes more exciting with "
                    "every step."
                ),

                dialogue=(
                    f'"We can do this!" says '
                    f'{request.character_name}.'
                ),
            )
        )

    return result


def generate_story(
    request: PromptRequest,
    outline: list[PanelOutline],
) -> list[StoryPanel]:

    if (
        settings.demo_mode
        or not settings.gemini_api_key
    ):
        return _demo_story(
            request,
            outline
        )

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    outline_json = json.dumps(
        [
            panel.model_dump()
            for panel in outline
        ],
        ensure_ascii=False,
    )

    prompt = f"""
Turn this five-panel comic outline
into a polished comic script.

Original story:
{request.story_prompt}

Character:
{request.character_name}

Setting:
{request.setting}

Tone:
{request.tone}

Art style:
{request.art_style}

Outline:
{outline_json}

Return exactly five objects containing:

panel_number
title
scene_description
image_prompt
caption
narration
dialogue

Keep the narration concise enough
for a comic page.

Maintain character and visual
continuity.
"""

    response = client.models.generate_content(
        model=settings.gemini_pro_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=list[StoryPanel],
            temperature=0.9,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty story."
        )

    data = json.loads(response.text)

    panels = [
        StoryPanel.model_validate(item)
        for item in data
    ]

    if len(panels) != 5:
        raise RuntimeError(
            "Gemini returned an incorrect "
            "number of story panels."
        )

    return panels