from app.schemas import StoryPanel


def build_comic_layout(
    story: list[StoryPanel],
    image_paths: list[str],
) -> list[dict]:

    if len(story) != len(image_paths):

        raise ValueError(
            "Every story panel must "
            "have one image."
        )

    layout = []

    for panel, image_path in zip(
        story,
        image_paths,
    ):

        layout.append(
            {
                **panel.model_dump(),
                "image_path": image_path,
            }
        )

    return layout