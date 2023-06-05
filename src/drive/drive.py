#google drive auth
import os
import io
from google.auth import impersonated_credentials
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


# ruta al json de las credenciales de google 
credentials_file = os.path.join(os.path.dirname(__file__), 'drive_secrets.json')

scopes = ['https://www.googleapis.com/auth/drive']

#carga las credenciales del servicio
credentials = service_account.Credentials.from_service_account_file(
    credentials_file,
    scopes=scopes
)

#construir el servicio del api 
service = build('drive', 'v3', credentials=credentials)

def create_driver_folder(folderName):
    
    #actualizar las credenciales si han expirado
    if credentials.expired:
        credentials.refresh(Request())
    
    #construir el servicio del api 
    service = build('drive', 'v3', credentials=credentials)

    #crea la carpeta de google drive
    folder_metadata = {
        'name': folderName,
        'mimeType': 'application/vnd.google-apps.folder',
    }
    folder = service.files().create(body=folder_metadata).execute()
    folder_id = folder['id']
    print(f'Carpeta creada con éxito. ID de carpeta: {folder_id}')

    # Obtener enlace de la carpeta
    folder_url = 'https://drive.google.com/drive/folders/' + folder_id
    print('Enlace de la carpeta:', folder_url)

    # Añadir como visualizador
    permission = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': 'camilo.mendoza@sunpoweresp.co'  # Reemplaza con tu dirección de correo electrónico
    }
    service.permissions().create(fileId=folder_id, body=permission).execute()
    print('Añadido como visualizador de la carpeta')

    return folder_id

def create_sub_folders(folder_id, subfolder_names):
    subfolder_ids = []
    for subfolder_name in subfolder_names:
        subfolder_metadata = {
            'name': subfolder_name,
            'parents': [folder_id],
            'mimeType': 'application/vnd.google-apps.folder'
        }
        subfolder = service.files().create(body=subfolder_metadata).execute()
        subfolder_id = subfolder.get('id')
        subfolder_ids.append(subfolder_id)
    return subfolder_ids


    

def sendFiles(file, folder_id):
    file_name, file_extension = os.path.splitext(file.filename)
    file_metadata = {
        'name': file.filename,
        'parents': [folder_id]
    }

    # Verificar el contenido de file_metadata
    print("file_metadata:", file_metadata)

    # Crear el objeto de carga de medios para el archivo binario
    media = MediaIoBaseUpload(io.BytesIO(file.read()), mimetype=file.content_type)

    # Subir el archivo a Google Drive
    uploaded_file = service.files().create(body=file_metadata, media_body=media).execute()

    # Imprimir el nombre y la extensión del archivo
    print(f'Archivo subido: {file.filename}')
    print(f'Extensión del archivo: {file_extension}')

    # Obtener el ID del archivo subido
    file_id = uploaded_file.get('id')
    print(f'ID del archivo: {file_id}')

    

def getFolderId(folder_name):
    # Realiza una consulta a la API de Google Drive para buscar la carpeta por su nombre
    results = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'").execute()
    folders = results.get('files', [])
    
    # Si se encontró una carpeta con el nombre dado, devuelve el ID de la primera coincidencia
    if folders:
        return folders[0]['id']
    
    # Si no se encontró ninguna carpeta, devuelve None
    return None