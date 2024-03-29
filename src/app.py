from flask import Flask, request, send_file, make_response, Response, logging
import io
import os 
import csv, operator
from flask_cors import CORS, cross_origin
from excel.generacionExcel import *
from pdf.pdfIPSE import *
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


@app.route('/excelQuery', methods=['POST'])
def createExcelWhitQuery():
    query = request.json['query']
    return Response(
        save_virtual_workbook(generarExcel(query)),
        headers={
            'Content-Disposition': 'attachment; filename=sheet.xlsx',
            'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    )

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
    # response = make_response()
    # response.headers['Content-Disposition'] = "attachment; filename='ejemplo.pdf"
    # response.mimetype = 'application/pdf'
    # return send_file(generarPdfEjemplo(), as_attachment=True)
    generarPdfId()
    return "aaa"
  
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
    idFotos= request.json['idFotos']
    generarRarFotos(idFotos)
    response = make_response()
    response.headers['Content-Disposition'] = "attachment; filename='ejemplo.zip"
    response.mimetype = 'application/zip'
    return send_file('../imagenes.zip', as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)