from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from config import APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, APPWRITE_API_KEY

# appwrite client
client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
db = Databases(client)

def create_document(collection_id: str, data: dict, document_id: str = "unique()"):
    try:
        return db.create_document(
            collection_id=collection_id,
            document_id=document_id,
            data=data,
            permissions=["read('any')", "write('any')"]
        )
    except AppwriteException as e:
        raise Exception(f"Failed to create document: {str(e)}")

def get_document(collection_id: str, document_id: str):
    try:
        return db.get_document(collection_id, document_id)
    except AppwriteException as e:
        raise Exception(f"Failed to get document: {str(e)}")

def list_documents(collection_id: str, filters: list = None):
    try:
        return db.list_documents(collection_id, filters=filters)
    except AppwriteException as e:
        raise Exception(f"Failed to list documents: {str(e)}")