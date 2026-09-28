from pydantic import BaseModel,Field
class PromptRequest(BaseModel):
    prompt:str=Field(min_length=5,max_length=2000)
    character_name:str=Field(default="Alex",max_length=80)
    setting:str=Field(default="enchanted forest",max_length=120)
    tone:str=Field(default="adventurous",max_length=80)
    art_style:str=Field(default="comic book",max_length=80)
