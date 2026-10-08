import os


# Force demo mode during tests
os.environ["DEMO_MODE"] = "true"


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text


def test_json_generation():

    response = client.post(

        "/generate-comic/json",

        json={

            "story_prompt":
                "A brave fox exploring "
                "an enchanted forest.",

            "character_name":
                "Ravi",

            "setting":
                "enchanted forest",

            "tone":
                "funny",

            "art_style":
                "comic book",
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert (
        data["success"]
        is True
    )


    assert (
        len(data["layout"])
        == 5
    )


    assert (
        data["pdf_url"]
        .endswith(".pdf")
    )


def test_image():

    response = client.post(

        "/test-image",

        json={

            "prompt":
                "A friendly fox "
                "in a forest"
        },
    )


    assert response.status_code == 200


    assert (
        response.json()["success"]
        is True
    )