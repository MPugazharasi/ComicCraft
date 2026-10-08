from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from app.config import (
    TEMPLATES_DIR,
)

from app.schemas import (
    PromptRequest,
    ImageRequest,
)

from app.services.comic_service import (
    generate_comic,
)

from app.services.image_generator import (
    generate_image,
)


router = APIRouter()

templates = Jinja2Templates(
    directory=str(
        TEMPLATES_DIR
    )
)


# --------------------------------------
# Home page
# --------------------------------------

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": "ComicCraft",
        },
    )


# --------------------------------------
# Web form generation
# --------------------------------------

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    form = {

        "story_prompt":
            story_prompt,

        "character_name":
            character_name,

        "setting":
            setting,

        "tone":
            tone,

        "art_style":
            art_style,
    }

    try:

        data = PromptRequest(
            **form
        )

        layout, pdf_url = (
            generate_comic(data)
        )

        return templates.TemplateResponse(
            request=request,

            name="comic_preview.html",

            context={

                "app_name":
                    "ComicCraft",

                "layout":
                    layout,

                "pdf_url":
                    pdf_url,

                "character_name":
                    data.character_name,
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={

                "app_name":
                    "ComicCraft",

                "error":
                    str(exc),

                "form":
                    form,
            },

            status_code=500,
        )


# --------------------------------------
# JSON API
# --------------------------------------

@router.post(
    "/generate-comic/json"
)
async def generate_comic_json(
    payload: PromptRequest,
):

    try:

        layout, pdf_url = (
            generate_comic(
                payload
            )
        )

        return {

            "success":
                True,

            "title":
                f"{payload.character_name}'s Comic",

            "layout":
                layout,

            "pdf_url":
                pdf_url,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------
# Image testing API
# --------------------------------------

@router.post(
    "/test-image"
)
async def test_image(
    payload: ImageRequest,
):

    try:

        image_url = generate_image(
            payload.prompt
        )

        return {

            "success":
                True,

            "image_url":
                image_url,
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# --------------------------------------
# Export success page
# --------------------------------------

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_url: str = "",
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={

            "app_name":
                "ComicCraft",

            "pdf_url":
                pdf_url,
        },
    )