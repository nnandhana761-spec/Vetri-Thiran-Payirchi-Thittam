import uuid
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from app.config import settings
BASE=Path(__file__).resolve().parents[2]; PANELS=BASE/"static"/"panels"; PANELS.mkdir(parents=True,exist_ok=True)
def _placeholder(prompt,path):
    w,h=settings.image_width,settings.image_height
    im=Image.new("RGB",(w,h),(239,224,196)); d=ImageDraw.Draw(im)
    d.rectangle((12,12,w-12,h-12),outline=(37,31,29),width=8)
    d.ellipse((w*.68,40,w*.86,220),fill=(247,184,78),outline=(37,31,29),width=4)
    d.polygon([(0,h*.8),(w*.3,h*.45),(w*.55,h*.8)],fill=(94,133,104))
    d.polygon([(w*.35,h),(w*.6,h*.55),(w*.85,h)],fill=(61,100,78))
    try:font=ImageFont.truetype("DejaVuSans.ttf",20)
    except OSError:font=ImageFont.load_default()
    d.rounded_rectangle((25,h-90,w-25,h-25),radius=12,fill=(255,250,235),outline=(37,31,29),width=2)
    d.text((40,h-75),prompt[:90],font=font,fill=(37,31,29)); im.save(path)
def generate_image(prompt):
    path=PANELS/f"{uuid.uuid4().hex}.png"
    if settings.image_backend=="hf":
        if not settings.hf_api_key:raise RuntimeError("HF_API_KEY required for image_backend=hf")
        import requests
        r=requests.post(f"https://router.huggingface.co/hf-inference/models/{settings.hf_model}",headers={"Authorization":f"Bearer {settings.hf_api_key}"},json={"inputs":prompt},timeout=180);r.raise_for_status();path.write_bytes(r.content)
    elif settings.image_backend=="diffusers":
        import torch
        from diffusers import StableDiffusionPipeline
        dtype=torch.float16 if torch.cuda.is_available() else torch.float32
        pipe=StableDiffusionPipeline.from_pretrained(settings.local_diffusion_model,torch_dtype=dtype)
        if torch.cuda.is_available():pipe=pipe.to("cuda")
        pipe(prompt,width=settings.image_width,height=settings.image_height).images[0].save(path)
    else:_placeholder(prompt,path)
    return f"/static/panels/{path.name}"
