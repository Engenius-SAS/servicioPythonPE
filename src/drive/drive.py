#google drive auth
import os
import io
import tempfile
from google.auth import impersonated_credentials
from googleapiclient.http import MediaIoBaseUpload
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import openpyxl

# ruta al json de las credenciales de google 
credentials_file = os.path.join(os.path.dirname(__file__), 'drive_secrets.json')

scopes = ['https://www.googleapis.com/auth/drive']

permissions = {
        'type': 'user',
        'role': 'reader',
        'emailAddress': 'camilo.mendoza@sunpoweresp.co'# Reemplaza con tu dirección de correo electrónico
}

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

    service.permissions().create(fileId=folder_id, body=permissions).execute()
    print('Añadido como visualizador de la carpeta')

    return folder_id

def create_sub_folders(folder_id, subfolder_names):
    #actualizar las credenciales si han expirado
    if credentials.expired:
        credentials.refresh(Request())
    
    #construir el servicio del api 
    service = build('drive', 'v3', credentials=credentials)

    #crea la carpeta de google drive
    folder_metadata = {
        'name': subfolder_names,
        "parents": [folder_id],
        'mimeType': 'application/vnd.google-apps.folder',
    }
    folder = service.files().create(body=folder_metadata).execute()
    folder_id = folder['id']
    print(f'Carpeta creada con éxito. ID de carpeta: {folder_id}')

    # Obtener enlace de la carpeta
    folder_url = 'https://drive.google.com/drive/folders/' + folder_id
    print('Enlace de la carpeta:', folder_url)

    service.permissions().create(fileId=folder_id, body=permissions).execute()
    print('Añadido como visualizador de la carpeta')

    return folder_id

    
def sendFiles(file_path, folder_id):
    file_name = os.path.basename(file_path)
    file_extension = os.path.splitext(file_path)[-1]

    # Verificar si el archivo existe en la ruta proporcionada
    if not os.path.isfile(file_path):
        print(f'El archivo no existe en la ruta especificada: {file_path}')
        return

    # Abrir el archivo en modo de lectura binaria
    with open(file_path, 'rb') as file_obj:

            #evalua el tipo de archivo para enviarlo a la carpeta
        if file_extension == '.pdf':
            media = MediaIoBaseUpload(file_obj, mimetype='application/pdf')
            print('entro pdf')
        elif file_extension == '.jpeg' or file_extension == '.jpg':
            media = MediaIoBaseUpload(file_obj, mimetype='image/jpeg')
            print("entro imagen")
        elif file_extension == '.xlsx':
                media = MediaIoBaseUpload(file_obj, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                print("entro excel")
        else:
            print(f'tipo de archivo no compatible {file_extension}')


        # Crear los metadatos del archivo
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }

        # Subir el archivo a Google Drive
        uploaded_file = service.files().create(body=file_metadata, media_body=media).execute()

        # Obtener el ID del archivo subido
        file_id = uploaded_file.get('id')


        # Obtener la URL del archivo subido
        file_url = f'https://drive.google.com/file/d/{file_id}/view'

        # Imprimir la URL del archivo
        print(f'URL del archivo: {file_url}')

        # Imprimir el nombre y la extensión del archivo
        print(f'Archivo subido: {file_name}')
        print(f'Extensión del archivo: {file_extension}')


    

def getFolderId(folder_name):
    # Realiza una consulta a la API de Google Drive para buscar la carpeta por su nombre
    results = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'").execute()
    folders = results.get('files', [])
    
    # Si se encontró una carpeta con el nombre dado, devuelve el ID de la primera coincidencia
    if folders:
        return folders[0]['id']
    
    # Si no se encontró ninguna carpeta, devuelve None
    return None