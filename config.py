from pydantic_settings import BaseSettings,SettingsConfigDict
class Settings(BaseSettings):
    gemini_api_key:str=""
    gemini_outline_model:str="gemini-2.5-flash"
    gemini_story_model:str="gemini-2.5-flash"
    image_backend:str="placeholder"
    hf_api_key:str=""
    hf_model:str="stabilityai/stable-diffusion-xl-base-1.0"
    local_diffusion_model:str="runwayml/stable-diffusion-v1-5"
    image_width:int=768
    image_height:int=512
    model_config=SettingsConfigDict(env_file=".env",env_file_encoding="utf-8",extra="ignore")
settings=Settings()
