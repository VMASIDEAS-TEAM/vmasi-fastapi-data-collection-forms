from fastapi import FastAPI, HTTPException, Depends
from schemas import FormData
from services.form_service import FormService
from repositories.firestore_repository import FirestoreRepository

app = FastAPI()

# Dependencia para inyectar el servicio en el endpoint
def get_form_service():
    repository = FirestoreRepository()
    return FormService(repository)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/submit_form")
async def submit_form(data: FormData, form_service: FormService = Depends(get_form_service)):
    try:
        form_id = form_service.save_form(data.dict())
        return {"message": "Formulario guardado con éxito", "form_id": form_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")
