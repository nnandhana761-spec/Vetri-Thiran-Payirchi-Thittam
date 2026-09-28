def build_comic_layout(outline,story,image_paths):
    by_num={int(x.get("panel_number",i+1)):x for i,x in enumerate(story)}
    return [{"panel_number":int(p.get("panel_number",i+1)),"title":p.get("title",f"Panel {i+1}"),"scene_description":p.get("scene_description",""),"image_prompt":p.get("image_prompt",""),"image_path":image_paths[i],"caption":by_num.get(int(p.get("panel_number",i+1)),{}).get("caption",""),"narration":by_num.get(int(p.get("panel_number",i+1)),{}).get("narration",""),"dialogue":by_num.get(int(p.get("panel_number",i+1)),{}).get("dialogue","")} for i,p in enumerate(outline)]
