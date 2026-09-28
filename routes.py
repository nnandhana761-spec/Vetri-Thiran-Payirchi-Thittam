from pathlib import Path
from fastapi import APIRouter,Request,Form,HTTPException
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates
from app.schemas import PromptRequest
from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf
BASE=Path(__file__).resolve().parent.parent; templates=Jinja2Templates(directory=str(BASE/"templates"));router=APIRouter()
def create_comic(req):
    outline=generate_outline(req);story=generate_story(req,outline)
    images=[generate_image(p["image_prompt"]) for p in outline]
    layout=build_comic_layout(outline,story,images);return layout,save_pdf(layout)
@router.get("/",response_class=HTMLResponse)
async def home(request:Request):return templates.TemplateResponse(request=request,name="index.html",context={})
@router.post("/generate",response_class=HTMLResponse)
async def generate(request:Request,prompt:str=Form(...),character_name:str=Form("Alex"),setting:str=Form("enchanted forest"),tone:str=Form("adventurous"),art_style:str=Form("comic book")):
    try:
        layout,pdf_path=create_comic(PromptRequest(prompt=prompt,character_name=character_name,setting=setting,tone=tone,art_style=art_style))
        return templates.TemplateResponse(request=request,name="comic_preview.html",context={"layout":layout,"pdf_path":pdf_path})
    except Exception as exc:return templates.TemplateResponse(request=request,name="index.html",context={"error":str(exc),"prompt":prompt},status_code=500)
@router.post("/generate-comic/json")
async def generate_json(req:PromptRequest):
    try:
        layout,pdf_path=create_comic(req);return {"layout":layout,"pdf_path":pdf_path,"download_url":pdf_path}
    except Exception as exc:raise HTTPException(status_code=500,detail=str(exc))
@router.post("/test-image")
async def test_image(prompt:str=Form(...)):
    try:return {"image_path":generate_image(prompt)}
    except Exception as exc:raise HTTPException(status_code=500,detail=str(exc))
@router.get("/export-success",response_class=HTMLResponse)
async def export_success(request:Request,pdf_path:str):
    if not pdf_path.startswith("/static/exports/") or ".." in pdf_path:raise HTTPException(status_code=400,detail="Invalid export path")
    return templates.TemplateResponse(request=request,name="export_success.html",context={"pdf_path":pdf_path})
@router.get("/download")
async def download(pdf_path:str):
    if not pdf_path.startswith("/static/exports/") or ".." in pdf_path:raise HTTPException(status_code=400,detail="Invalid export path")
    path=BASE/pdf_path.lstrip("/")
    if not path.is_file():raise HTTPException(status_code=404,detail="PDF not found")
    return FileResponse(path,media_type="application/pdf",filename=path.name)
