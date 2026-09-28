import json,re
from app.config import settings
def generate_story(req,outline):
    if settings.gemini_api_key:
        try:
            from google import genai
            client=genai.Client(api_key=settings.gemini_api_key)
            prompt=f"Write concise comic narration and dialogue for five panels. Story {req.prompt}; character {req.character_name}; tone {req.tone}. Outline: {json.dumps(outline)}. Return ONLY a JSON array of five objects with panel_number, caption, narration, dialogue."
            raw=client.models.generate_content(model=settings.gemini_story_model,contents=prompt).text or ""
            match=re.search(r"\[.*\]",raw,re.S); data=json.loads(match.group(0) if match else raw)
            if isinstance(data,list) and len(data)==5:return data
        except Exception:pass
    return [{"panel_number":p["panel_number"],"caption":p["scene_description"],"narration":f"{req.character_name} takes one step closer to the unknown. The moment calls for {req.tone}.","dialogue":"“I can do this,” they whisper." if i in (0,3) else ""} for i,p in enumerate(outline)]
