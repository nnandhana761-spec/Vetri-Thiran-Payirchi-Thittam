# ComicCraft — AI Comic Story Creator

A FastAPI + Jinja2 app implementing the uploaded brief's workflow: five-panel outline → narration/dialogue → illustrations → layout → PDF.

## Requirements
Python 3.10+ (3.11 recommended), VS Code and the Python extension. Gemini and image services are optional for local smoke testing.

## Windows PowerShell
```powershell
cd comiccraft
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
Copy-Item .env.example .env
python -m uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000; API docs at http://127.0.0.1:8000/docs; health at http://127.0.0.1:8000/health.

## macOS/Linux
```bash
cd comiccraft
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload
```

## AI configuration
Edit `.env`. Add `GEMINI_API_KEY` for Gemini text generation. Default `IMAGE_BACKEND=placeholder` produces local development illustrations without a GPU or token. For hosted images, set `IMAGE_BACKEND=hf` and `HF_API_KEY`. For local generation, set `IMAGE_BACKEND=diffusers`, install a PyTorch build compatible with your hardware plus `diffusers`, `transformers`, and `accelerate`; model weights can be large. Gemini uses the current `google-genai` SDK and falls back to deterministic story content if unavailable.

## Test
```bash
pip install pytest httpx
pytest
```
Create a comic in the browser and verify five panels and the PDF download. JSON API example:
```bash
curl -X POST http://127.0.0.1:8000/generate-comic/json -H "Content-Type: application/json" -d "{\"prompt\":\"A brave fox explores an enchanted forest\",\"character_name\":\"Pip\",\"setting\":\"forest\",\"tone\":\"funny\",\"art_style\":\"comic book\"}"
```
