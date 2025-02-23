from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.exception import AppwriteException
from appwrite.query import Query
from config import APPWRITE_ENDPOINT, APPWRITE_PROJECT_ID, APPWRITE_API_KEY, APPWRITE_DATABASE_ID


client = Client()
client.set_endpoint(APPWRITE_ENDPOINT)
client.set_project(APPWRITE_PROJECT_ID)
client.set_key(APPWRITE_API_KEY)
db = Databases(client)

def create_document(collection_id: str, data: dict, document_id: str = "unique()"):
    try:
        return db.create_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id,
            data=data,
            permissions=["read(\"any\")", "write(\"any\")"]
        )
    except AppwriteException as e:
        
        error_message = e.message if hasattr(e, 'message') else str(e)
        print(f"Appwrite error: {error_message}")
        raise Exception(f"Failed to create document: {error_message}")

def get_document(collection_id: str, document_id: str):
    try:
        return db.get_document(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=collection_id,
            document_id=document_id
        )
    except AppwriteException as e:
        error_message = e.message if hasattr(e, 'message') else str(e)
        print(f"Appwrite error: {error_message}")
        raise Exception(f"Failed to get document: {error_message}")

def list_documents(collection_id: str, queries: list = None):
    try:
        return db.list_documents(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=collection_id,
            queries=queries
        )
    except AppwriteException as e:
        error_message = e.message if hasattr(e, 'message') else str(e)
        print(f"Appwrite error: {error_message}")
        raise Exception(f"Failed to list documents: {error_message}")