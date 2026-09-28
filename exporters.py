from pathlib import Path
from datetime import datetime
from fpdf import FPDF
BASE=Path(__file__).resolve().parents[2]
def save_pdf(layout,title="ComicCraft"):
    out=BASE/"static"/"exports";out.mkdir(parents=True,exist_ok=True)
    path=out/f"comic_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.pdf"
    pdf=FPDF();pdf.set_auto_page_break(auto=True,margin=15)
    for p in layout:
        pdf.add_page();pdf.set_font("Helvetica","B",18)
        pdf.multi_cell(0,10,f"Panel {p['panel_number']}: {p['title']}".encode("latin-1","replace").decode("latin-1"))
        image=BASE/p["image_path"].lstrip("/") if p["image_path"].startswith("/static/") else Path(p["image_path"])
        if image.is_file():pdf.image(str(image),x=15,y=pdf.get_y()+3,w=180);pdf.ln(5)
        for key,label in [("scene_description","Scene"),("caption","Caption"),("narration","Narration"),("dialogue","Dialogue")]:
            if p.get(key):
                pdf.set_font("Helvetica","B",11);pdf.cell(0,7,label,ln=True);pdf.set_font("Helvetica","",11)
                pdf.multi_cell(0,6,str(p[key]).encode("latin-1","replace").decode("latin-1"));pdf.ln(1)
    pdf.output(str(path));return f"/static/exports/{path.name}"
