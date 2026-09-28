from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health():assert client.get("/health").json()=={"status":"ok"}
def test_homepage():
    r=client.get("/");assert r.status_code==200 and "ComicCraft" in r.text
def test_json_generation():
    r=client.post("/generate-comic/json",json={"prompt":"A brave fox explores an enchanted forest","character_name":"Pip","setting":"forest","tone":"funny","art_style":"comic book"})
    assert r.status_code==200,r.text
    data=r.json();assert len(data["layout"])==5
    assert client.get(data["pdf_path"]).status_code==200
def test_image_endpoint():
    r=client.post("/test-image",data={"prompt":"a comic fox"})
    assert r.status_code==200 and r.json()["image_path"].startswith("/static/panels/")
