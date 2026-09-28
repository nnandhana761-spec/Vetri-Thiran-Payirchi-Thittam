from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router
BASE=Path(__file__).resolve().parent.parent
for folder in ("static/panels","static/exports"): (BASE/folder).mkdir(parents=True,exist_ok=True)
app=FastAPI(title="ComicCraft – AI Comic Story Creator",version="1.0.0")
app.mount("/static",StaticFiles(directory=str(BASE/"static")),name="static")
app.include_router(router)
@app.get("/health")
def health(): return {"status":"ok"}
