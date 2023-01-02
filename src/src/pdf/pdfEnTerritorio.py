import PyPDF2 
import io
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import zipfile
import pymysql 
import tkinter as tk
from PIL import Image, ImageFont, ImageDraw
import  urllib
from io import StringIO, BytesIO
import random 

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
def obtener_conexion():
    return pymysql.connect(host='mysql.engenius.com.co',
                                user='infovisitas',
                                password='desarrollo2020'
                                )

def generarVariosPdf (ids):
    # generarPdfId()
    if os.path.exists("pdfs"):
        pdfsExistentes = ([arch.name for arch in os.scandir("pdfs") if arch.is_file()])
        for pdf in pdfsExistentes:
            os.remove("pdfs/"+pdf)
    if os.path.exists("destination.zip"):
        os.remove("destination.zip")
       # print(ids)
    i = 1
    for id in ids:
        try:
            if len(str(i)) == 1:
                consecutivo = '000'+str(i)
            elif len(str(i)) == 2:
                consecutivo = '00'+str(i)
            elif len(str(i)) == 3:
                consecutivo = '0'+str(i)
            else:
                consecutivo = str(i)
            generarPdf(id, consecutivo)
            i = i + 1
        except Exception as e: 
             print(str(id), 'No se pudo')
    zf = zipfile.ZipFile("destination.zip", mode="w")
    pdfsExistentes = ([arch.name for arch in os.scandir("pdfs") if arch.is_file()])
    try:
        for pdf in pdfsExistentes:
            zf.write("pdfs/"+pdf, compress_type=compression)
    finally:
        zf.close()

def generarPdf(idFormulario):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT *, (SELECT rutaserver from suncosurvey.fotos_firma B WHERE B.`Id_Encuesta`= A.`Id_Encuesta`) FROM suncosurvey.Users A Where `Id_Encuesta` = '"+idFormulario+"')")
              datos = cursor.fetchone()
    print(datos)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)
    #fecha de la visita
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    fecha = dia +"/04/2022"
    can.drawString(118, 672, fecha)
    #NoUsuario
    can.drawString(435, 672, datos[0])
    can.drawString(90, 632, datos[1])
    can.drawString(60, 619, datos[2])
    can.drawString(330, 606, datos[3])
    can.drawString(60, 593, datos[4])
    can.drawString(410, 593, datos[5])
    can.drawString(60, 580, datos[6])
    urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos[9],"ejemplo.jpg")
    filename = 'ejemplo.jpg'
    filename1 = 'fondoblanco.jpg'
    frontImage = Image.open(filename)
    background = Image.open(filename1)
    frontImage = frontImage.convert("RGBA")
    background = background.convert("RGBA")
    width = (background.width - frontImage.width) // 2
    height = (background.height - frontImage.height) // 2
    background.paste(frontImage, (width, height), frontImage)
    background.save("new.png", format="png")
    can.drawImage('new.png', 50, 353, 200, 40)
    can.drawString(93, 327, datos[1])
    can.drawString(93, 314, datos[2])
    can.drawString(103, 299, datos[7])
    can.save()
    new_pdf = PyPDF2.PdfFileReader(packet)
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/formatoEnTerritorio/FORMATO-SOCIALIZACIÓN-Y-REPLANTEO-DE-USUARIOS_DISPAC.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    outputStream = open("pdfs/"+datos[0]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()

if __name__ == '__main__':
    generarPdf()