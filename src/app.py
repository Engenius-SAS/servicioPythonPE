import datetime
from flask import Flask, request, send_file, make_response, Response, logging, jsonify
import io
import os 
import csv, operator
from flask_cors import CORS, cross_origin
from excel.generacionExcel import *
from pdf.pdfIPSE import *
from pdf.pdfActasMant import *
import json
from drive.drive import *
# from pdf.ejemploPdf import *
# from pdf.generacionPdf import *
# from pdf.pdfLineaColectoraDos import *
# from pdf.pdfLineaColectora import *
# from pdf.pdfDispower import *
# from pdf.pdfActasMant import *
# from pdf.pdfAOM import *
# from pdf.pdfAOMfotos import *
from fotos.ejemploFotos import *
# from fotos.fotosAOM import *
# from fotos.fotosAES import *
import PyPDF2 
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pyexcel as pe
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook

import xlsxwriter
def LoggingStart():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
CORS(app, support_credentials=True)

folder_url = 'https://drive.google.com/drive/folders/'

@app.route('/excelQuery', methods=['POST'])
def createExcelWhitQuery():
    query = request.json['query']
    print(query)

    #carpeta principal para los excel
    folderName="Excel Engenius"
    existingFolder = getFolderId(folder_name=folderName)

    if existingFolder:
        folder_id = existingFolder
        print(folder_id)
    else:
        folder_id = create_driver_folder(folderName=folderName)

    generarExcel(query=query, folderId=folder_id)

    urlExcelEngenius = folder_url + folder_id
    print(urlExcelEngenius)
    return urlExcelEngenius


    # return Response(
    #     save_virtual_workbook(generarExcel(query)),
    #     headers={
    #         'Content-Disposition': 'attachment; filename=sheet.xlsx',
    #         'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    #     }
    # )

@app.route('/excel', methods=['POST'])
def createExcel():
    idProyecto = request.json['idProyecto']
    return Response(
        save_virtual_workbook(generarExcelGrande(idProyecto)),
        headers={
            'Content-Disposition': 'attachment; filename=sheet.xlsx',
            'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    )

@app.route('/pdf', methods=['GET'])
def createPdfPrueba():
    return;
    # idEncuestas = request.json['idEncuentas']
    # print(idEncuestas)
    # generarVariosPdf(idEncuestas)
    # response = make_response()
    # response.headers['Content-Disposition'] = "attachment; filename='ejemplo.pdf"
    # response.mimetype = 'application/pdf'
    # return send_file('../destination.zip', as_attachment=True)
  
@app.route('/zip', methods=['GET'])
def createZipPrueba():
    generarVariosPdf(['21-1639680474344', '14-1638972378193'])
    response = make_response()
    response.headers['Content-Disposition'] = "attachment; filename='ejemplo.zip"
    response.mimetype = 'application/zip'
    return send_file('../destination.zip', as_attachment=True)

@app.route('/zip', methods=['POST'])
def createZipPdf():
    idEncuestas= request.json['idEncuestas']
    generarVariosPdf(idEncuestas)
    response = make_response()
    response.headers['Content-Disposition'] = "attachment; filename='ejemplo.zip"
    response.mimetype = 'application/zip'
    return send_file('../destination.zip', as_attachment=True)

@app.route('/fotosZip', methods=['POST'])
def createZipFotos():
    idFotos = request.json['idFotos']
    date = datetime.date.today()

    #fecha
    # Obtener el día y el año
    nombre_mes = date.strftime("%b")
    dia = date.strftime("%d")
    ano = date.strftime("%Y")
    concat = f"{nombre_mes} - {dia} - {ano}"

    #creamos la carpeta principal
    folder_name = f"Carpeta Imagenes finalesesas - {concat}"
    existingFolder = getFolderId(folder_name=folder_name)
    if existingFolder:
        folder_id = existingFolder
    else:
        folder_id = create_driver_folder(folderName=folder_name)
    print(folder_id)

    for id in idFotos:
        generarFotosCoordenadas(ids=id, folderId=folder_id)

    urlDriveImagenes = folder_url + folder_id
    return urlDriveImagenes

    # generarRarFotos(idFotos)
    # response = make_response()
    # response.headers['Content-Disposition'] = "attachment; filename='ejemplo.zip"
    # response.mimetype = 'application/zip'
    # return send_file('../imagenes.zip', as_attachment=True)

@app.route('/ActasMantenimiento', methods=['POST'])
def sendGoogleDrive():
    idEncuestas  = request.json.get('idEncuestas')   
    date = datetime.date.today()
    id = ', '.join(' ' + str(id) for id in idEncuestas)
    print(id)
    print(idEncuestas)
    
    #si 
    # Obtener el día y el año
    nombre_mes = date.strftime("%b")
    dia = date.strftime("%d")
    ano = date.strftime("%Y")
    concat = f"{nombre_mes} - {dia} - {ano}"


    #folder principal 
    folderName = f"Actas Mantenimiento - {concat}"
    existingFolder = getFolderId(folder_name=folderName)

    if existingFolder:
        folder_id = existingFolder
        print("carpeta ya existe: " + folder_id)
    else:
        folder_id = create_driver_folder(folderName=folderName)
        print("no existe creada: " + folder_id)
        
    #logica para crear carpetas y archivos 
    for id in idEncuestas:
        generarPdfId(id=str(id), folderId=folder_id)
    
    # Obtener el enlace de la carpeta
    folder_url = 'https://drive.google.com/drive/folders/'
    urlPdfMantenimiento = folder_url + folder_id

    return jsonify({"urlPdfMantenimiento": urlPdfMantenimiento})


@app.route('/deleteFolder', methods=['POST'])
def deleteFolder():
    folderName = request.json['folderName']
    print(folderName)

    # Obtener el ID de la carpeta
    # Eliminar la carpeta
    delete_folder(folderName)

    return "Carpeta eliminada"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
