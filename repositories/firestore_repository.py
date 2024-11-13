import os
import json
from google.cloud import firestore
from google.oauth2 import service_account
from config import settings  # Cargamos las configuraciones de entorno desde config.py


class FirestoreRepository:
    def __init__(self):
        # Obtenemos las credenciales desde la variable de entorno
        cred_info = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
        if cred_info:
            try:
                # Convertimos el JSON de credenciales a un diccionario
                cred_dict = json.loads(cred_info)
                credentials = service_account.Credentials.from_service_account_info(cred_dict)

                # Especificamos el proyecto y la base de datos
                project_id = 'vmasideas-crm'
                database_id = 'vmi-collection-forms-data'  # La base de datos específica para nuestro proyecto

                # Conectamos con la base de datos en Firestore
                self.db = firestore.Client(project=project_id, credentials=credentials, database=database_id)
                self.collection = self.db.collection("forms")  # Nombre de la colección donde guardaremos los datos
                print(f"Connected to Firestore database: {database_id} in project: {project_id}")
            except Exception as e:
                print(f"Error initializing Firestore: {e}")
                self.db = None
        else:
            print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set")
            self.db = None

    def save_form(self, form_data: dict):
        if self.collection:
            # Agregamos los datos en la colección especificada
            doc_ref = self.collection.document()  # Crea un nuevo documento
            doc_ref.set(form_data)  # Guarda los datos en Firestore
            return doc_ref.id
        else:
            raise Exception("No connection to Firestore database")


# Ejemplo de cómo se inicializaría el repositorio
firebase_config = FirestoreRepository()
