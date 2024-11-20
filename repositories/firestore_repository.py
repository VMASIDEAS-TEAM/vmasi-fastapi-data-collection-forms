import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
from config import settings

class FirestoreRepository:
    def __init__(self):
        cred_info = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_info:
            try:
                cred_dict = json.loads(cred_info)
                credentials = service_account.Credentials.from_service_account_info(cred_dict)
                project_id = 'vmasideas-crm'
                database_id = 'vmi-collection-forms-data'
                self.db = firestore.Client(project=project_id, credentials=credentials, database=database_id)
                self.collection = self.db.collection("forms")
                print(f"Connected to Firestore database: {database_id} in project: {project_id}")
            except Exception as e:
                print(f"Error initializing Firestore: {e}")
                self.db = None
        else:
            print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            self.db = None

    def save_form(self, form_data: dict):
        if self.collection:
            doc_ref = self.collection.document()
            doc_ref.set(form_data)
            return doc_ref.id
        else:
            raise Exception("No connection to Firestore database")

    def get_all_forms(self):
        if self.collection:
            try:
                # Obtiene todos los documentos de la colección
                docs = self.collection.stream()
                forms = [doc.to_dict() for doc in docs]
                return forms
            except Exception as e:
                print(f"Error al recuperar los datos de Firestore: {e}")
                return []
        else:
            raise Exception("No connection to Firestore database")

firebase_config = FirestoreRepository()
