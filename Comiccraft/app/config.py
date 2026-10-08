from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    app_name: str = "ComicCraft"

    host: str = "127.0.0.1"

    port: int = 8000

    demo_mode: bool = True

    # Gemini
    gemini_api_key: str = ""

    gemini_flash_model: str = "gemini-2.5-flash"

    gemini_pro_model: str = "gemini-2.5-pro"

    # Hugging Face
    hf_token: str = ""

    hf_image_model: str = (
        "stabilityai/stable-diffusion-xl-base-1.0"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()


# --------------------------------------------------
# Application directories
# --------------------------------------------------

TEMPLATES_DIR = (
    BASE_DIR / "app" / "templates"
)

STATIC_DIR = (
    BASE_DIR / "app" / "static"
)

PANELS_DIR = (
    STATIC_DIR / "panels"
)

EXPORTS_DIR = (
    STATIC_DIR / "exports"
)


# Create folders automatically
PANELS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

EXPORTS_DIR.mkdir(
    parents=True,
    exist_ok=True
)