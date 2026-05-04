from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from regles import evaluer_admission


app = FastAPI(title="Systeme expert d'admission a l'examen")
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": None,
            "form_data": None,
            "error_message": None,
        },
    )


@app.post("/evaluation", response_class=HTMLResponse)
async def evaluer(
    request: Request,
    nom: str = Form(""),
    nom_cours: str = Form(""),
    unite: str = Form(...),
    total_cours: float = Form(...),
    suivi: float = Form(...),
):
    data = {
        "nom": nom,
        "nom_cours": nom_cours,
        "unite": unite,
        "total_cours": total_cours,
        "suivi": suivi,
    }

    if suivi > total_cours:
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "request": request,
                "result": None,
                "form_data": data,
                "error_message": "Erreur: la participation saisie ne peut pas depasser le total des unites du cours.",
            },
            status_code=400,
        )

    result = evaluer_admission(data)
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "result": result,
            "form_data": data,
            "error_message": None,
        },
    )
