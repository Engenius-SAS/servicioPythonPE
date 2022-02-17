from flask import Flask, request, send_file, make_response, Response
import io
import os 
import csv, operator
from flask_cors import CORS, cross_origin
from excel.generacionExcel import *
from pdf.ejemploPdf import *
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

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/excel', methods=['POST'])
def createExcel():
    idProyecto = request.json['idProyecto']
    print(idProyecto)
    return Response(
        save_virtual_workbook(generarExcelGrande(idProyecto)),
        headers={
            'Content-Disposition': 'attachment; filename=sheet.xlsx',
            'Content-type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        }
    )
    #return { 'status ' : 'ok'}
@app.route('/excel', methods=['GET'])
def createExcelPrueba():
    return Response(
        save_virtual_workbook(generarPrueba()),
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
    response = make_response()
    response.headers['Content-Disposition'] = "attachment; filename='ejemplo.zip"
    response.mimetype = 'application/zip'
    return send_file('pdf\\a\\destination.zip', as_attachment=True)
    # with open(os.path.join('destinatio.zip'), 'rb') as f:
    #     data = f.readlines()
    # os.remove(os.path.join('destinatio.zip'))
    # return Response(data, headers={
    #     'Content-Type': 'application/zip',
    #     'Content-Disposition': 'attachment; filename=%s;' % 'destinatio.zip'
    # })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000, debug=True)