import json,re
from app.config import settings
def _fallback_outline(req):
    beats=[("A Curious Beginning","notices an unusual clue","wide establishing shot"),("The First Challenge","faces a surprising obstacle","dynamic action scene"),("A Hidden Discovery","finds a secret that changes everything","dramatic close-up"),("The Brave Choice","makes a difficult, generous choice","heroic composition"),("A New Dawn","ends the adventure with new hope","uplifting final scene")]
    return [{"panel_number":i+1,"title":t,"scene_description":f"{req.character_name} {d} in {req.setting}.","image_prompt":f"{req.art_style} illustration, {visual}, {req.character_name} in {req.setting}; consistent character design, expressive, no lettering"} for i,(t,d,visual) in enumerate(beats)]
def generate_outline(req):
    if not settings.gemini_api_key:return _fallback_outline(req)
    try:
        from google import genai
        client=genai.Client(api_key=settings.gemini_api_key)
        prompt=f"Create exactly 5 coherent comic panels for: {req.prompt}. Character: {req.character_name}; setting: {req.setting}; tone: {req.tone}; style: {req.art_style}. Return ONLY a JSON array of objects with panel_number, title, scene_description, image_prompt. Story arc: beginning, conflict, discovery, choice, ending. No lettering in image prompts."
        raw=client.models.generate_content(model=settings.gemini_outline_model,contents=prompt).text or ""
        match=re.search(r"\[.*\]",raw,re.S); data=json.loads(match.group(0) if match else raw)
        if not isinstance(data,list) or len(data)!=5:raise ValueError("Expected five panels")
        return data
    except Exception:return _fallback_outline(req)
