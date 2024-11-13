from repositories.firestore_repository import FirestoreRepository

class FormService:
    def __init__(self, repository: FirestoreRepository):
        self.repository = repository

    def save_form(self, form_data: dict):
        if form_data["action"] != "saveForm":
            raise ValueError("Acción no soportada")
        return self.repository.save_form(form_data)
