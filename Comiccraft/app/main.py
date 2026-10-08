from fastapi import FastAPI

from fastapi.staticfiles import (
    StaticFiles,
)

from app.config import (
    settings,
    STATIC_DIR,
)

from app.routes import (
    router,
)


app = FastAPI(

    title=settings.app_name,

    description=(
        "AI Comic Story Creator "
        "using Gemini and "
        "Stable Diffusion"
    ),

    version="1.0.0",
)


# --------------------------------------
# Static files
# --------------------------------------

app.mount(

    "/static",

    StaticFiles(
        directory=str(
            STATIC_DIR
        )
    ),

    name="static",
)


# --------------------------------------
# Application routes
# --------------------------------------

app.include_router(
    router
)


# --------------------------------------
# Health check
# --------------------------------------

@app.get("/health")
async def health():

    return {

        "status":
            "ok",

        "app":
            settings.app_name,

        "demo_mode":
            settings.demo_mode,
    }