import PyPDF2 
import io
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
# from reportlab.lib.pagesizes import letter
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
def llenarCampos(can, x, y, dato, distanciaX):
    for letra in dato:
        can.drawString(x, y, letra)
        x = x + distanciaX
def generarVariosPdf (ids):
    for id in ids:
        try:
            generarPdfId(id)
        except Exception as e: 
             print(str(id), 'No se pudo', e)


def generarPdfId(id):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT A.Id, A.Id_Encuesta, A.Nombre_Completo, A.Cedula, A.TipoDoc,(SELECT DISTINCT rutaserver from db_liwa.fotos_firma B WHERE B.Id_Formulario = A.Id_Encuesta GROUP BY B.Id_Formulario) FROM db_liwa.AOM A WHERE A.Id_Encuesta = '"+id+"';")
              datos = cursor.fetchone()
    print(datos)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)
    can.drawString(600, 700, ".")
    can.save()
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=A4)
    can2.setFont("Helvetica", 10)
    can2.drawString(600, 700, ".")
    can2.save()
    packet3 = io.BytesIO()
    can3 = canvas.Canvas(packet3, pagesize=A4)
    can3.setFont("Helvetica", 10)
    can3.drawString(600, 700, ".")
    can3.save()
    packet4 = io.BytesIO()
    can4 = canvas.Canvas(packet4, pagesize=A4)
    can4.setFont("Helvetica", 10)
    can4.drawString(600, 700, ".")
    can4.save()
    packet5 = io.BytesIO()
    can5 = canvas.Canvas(packet5, pagesize=A4)
    can5.setFont("Helvetica", 10)
    can5.drawString(600, 700, ".")
    can5.save()
    packet6 = io.BytesIO()
    can6 = canvas.Canvas(packet6, pagesize=A4)
    can6.setFont("Helvetica", 10)
    can6.drawString(600, 700, ".")
    can6.save()
    packet7 = io.BytesIO()
    can7 = canvas.Canvas(packet7, pagesize=A4)
    can7.setFont("Helvetica", 10)
    can7.drawString(600, 700, ".")
    can7.save()
    packet8 = io.BytesIO()
    can8 = canvas.Canvas(packet8, pagesize=A4)
    can8.setFont("Helvetica", 10)
    can8.drawString(600, 700, ".")
    can8.save()
    packet9 = io.BytesIO()
    can9 = canvas.Canvas(packet9, pagesize=A4)
    can9.setFont("Helvetica", 10)
    can9.drawString(600, 700, ".")
    can9.save()
    packet10 = io.BytesIO()
    can10 = canvas.Canvas(packet10, pagesize=A4)
    can10.setFont("Helvetica", 10)
    can10.drawString(600, 700, ".")
    can10.save()
    packet11 = io.BytesIO()
    can11 = canvas.Canvas(packet11, pagesize=A4)
    can11.setFont("Helvetica", 10)
    can11.drawString(600, 700, ".")
    can11.save()
    packet12 = io.BytesIO()
    can12 = canvas.Canvas(packet12, pagesize=A4)
    can12.setFont("Helvetica", 10)
    can12.drawString(600, 700, ".")
    can12.save()
    packet13 = io.BytesIO()
    can13 = canvas.Canvas(packet13, pagesize=A4)
    can13.setFont("Helvetica", 10)
    can13.drawString(600, 700, ".")
    can13.save()
    packet14 = io.BytesIO()
    can14 = canvas.Canvas(packet14, pagesize=A4)
    can14.setFont("Helvetica", 10)
    can14.drawString(600, 700, ".")
    can14.save()
    packet15 = io.BytesIO()
    can15 = canvas.Canvas(packet15, pagesize=A4)
    can15.setFont("Helvetica", 10)
    can15.drawString(600, 700, ".")
    can15.save()
    packet16 = io.BytesIO()
    can16 = canvas.Canvas(packet16, pagesize=A4)
    can16.setFont("Helvetica", 10)
    can16.drawString(600, 700, ".")
    can16.save()
    packet17 = io.BytesIO()
    can17 = canvas.Canvas(packet17, pagesize=A4)
    can17.setFont("Helvetica", 10) 
    can17.drawString(600, 700, ".") 
    can17.save() 
    packet18 = io.BytesIO()
    can18 = canvas.Canvas(packet18, pagesize=A4)
    can18.setFont("Helvetica", 10)
    can18.drawString(600, 700, ".")
    can18.save()

    packet19 = io.BytesIO()
    can19 = canvas.Canvas(packet19, pagesize=A4)
    can19.setFont("Helvetica", 10)
    can19.drawString(600, 700, ".")
    can19.save()

    packet20 = io.BytesIO()
    can20 = canvas.Canvas(packet20, pagesize=A4)
    can20.setFont("Helvetica", 10)
    can20.drawString(600, 700, ".")
    can20.save()
    
    packet21 = io.BytesIO()
    can21 = canvas.Canvas(packet21, pagesize=A4)
    can21.setFont("Helvetica", 10)
    can21.drawString(600, 700, ".")
    can21.save()
    

    packet22 = io.BytesIO()
    can22= canvas.Canvas(packet22, pagesize=A4)
    can22.setFont("Helvetica", 10)
    #NoUsuario
    can22.drawString(176, 268, str(datos[2]))
    can22.drawString(110, 254, str(datos[3]))
    urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos[5],"ejemplo.jpg")
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
    can22.drawImage('new.png', 95, 285, 175, 75 )
    can22.save()

    packet23 = io.BytesIO()
    can23 = canvas.Canvas(packet23, pagesize=A4)
    can23.setFont("Helvetica", 10)
    can23.drawString(600, 700, ".")
    can23.save()

    new_pdf = PyPDF2.PdfFileReader(packet)
    new_pdf2 = PyPDF2.PdfFileReader(packet2)
    new_pdf3 = PyPDF2.PdfFileReader(packet3)
    new_pdf4 = PyPDF2.PdfFileReader(packet4)
    new_pdf5 = PyPDF2.PdfFileReader(packet5)
    new_pdf6 = PyPDF2.PdfFileReader(packet6)
    new_pdf7 = PyPDF2.PdfFileReader(packet7)
    new_pdf8 = PyPDF2.PdfFileReader(packet8)
    new_pdf9 = PyPDF2.PdfFileReader(packet9)
    new_pdf10 = PyPDF2.PdfFileReader(packet10)
    new_pdf11 = PyPDF2.PdfFileReader(packet11)
    new_pdf12 = PyPDF2.PdfFileReader(packet12)
    new_pdf13 = PyPDF2.PdfFileReader(packet13)
    new_pdf14 = PyPDF2.PdfFileReader(packet14)
    new_pdf15 = PyPDF2.PdfFileReader(packet15)
    new_pdf16 = PyPDF2.PdfFileReader(packet16)
    new_pdf17 = PyPDF2.PdfFileReader(packet17)
    new_pdf18 = PyPDF2.PdfFileReader(packet18)
    new_pdf19 = PyPDF2.PdfFileReader(packet19)
    new_pdf20 = PyPDF2.PdfFileReader(packet20)
    new_pdf21 = PyPDF2.PdfFileReader(packet21)
    new_pdf22 = PyPDF2.PdfFileReader(packet22)
    new_pdf23 = PyPDF2.PdfFileReader(packet23)
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-1.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-2.pdf", "rb"))
    existing_pdf3 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-3.pdf", "rb"))
    existing_pdf4 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-4.pdf", "rb"))
    existing_pdf5 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-5.pdf", "rb"))
    existing_pdf6 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-6.pdf", "rb"))
    existing_pdf7 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-7.pdf", "rb"))
    existing_pdf8 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-8.pdf", "rb"))
    existing_pdf9 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-9.pdf", "rb"))
    existing_pdf10 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-10.pdf", "rb"))
    existing_pdf11 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-11.pdf", "rb"))
    existing_pdf12 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-12.pdf", "rb"))
    existing_pdf13 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-13.pdf", "rb"))
    existing_pdf14 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-14.pdf", "rb"))
    existing_pdf15 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-15.pdf", "rb"))
    existing_pdf16 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-16.pdf", "rb"))
    existing_pdf17 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-17.pdf", "rb"))
    existing_pdf18 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-18.pdf", "rb"))
    existing_pdf19 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-19.pdf", "rb"))
    existing_pdf20 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-20.pdf", "rb"))
    existing_pdf21 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-21.pdf", "rb"))
    existing_pdf22 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-22.pdf", "rb"))
    existing_pdf23 = PyPDF2.PdfFileReader(open("src/pdf/CUUDIS/CCU DISPOWER-23.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page2 = existing_pdf2.getPage(0)
    page3 = existing_pdf3.getPage(0)
    page4 = existing_pdf4.getPage(0)
    page5 = existing_pdf5.getPage(0)
    page6 = existing_pdf6.getPage(0)
    page7 = existing_pdf7.getPage(0)
    page8 = existing_pdf8.getPage(0)
    page9 = existing_pdf9.getPage(0)
    page10 = existing_pdf10.getPage(0)
    page11 = existing_pdf11.getPage(0)
    page12 = existing_pdf12.getPage(0)
    page13 = existing_pdf13.getPage(0)
    page14 = existing_pdf14.getPage(0)
    page15 = existing_pdf15.getPage(0)
    page16 = existing_pdf16.getPage(0)
    page17 = existing_pdf17.getPage(0)
    page18 = existing_pdf18.getPage(0)
    page19 = existing_pdf19.getPage(0)
    page20 = existing_pdf20.getPage(0)
    page21 = existing_pdf21.getPage(0)
    page22 = existing_pdf22.getPage(0)
    page23 = existing_pdf23.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page2.mergePage(new_pdf2.getPage(0))
    page3.mergePage(new_pdf3.getPage(0))
    page4.mergePage(new_pdf4.getPage(0))
    page5.mergePage(new_pdf5.getPage(0))
    page6.mergePage(new_pdf6.getPage(0))
    page7.mergePage(new_pdf7.getPage(0))
    page8.mergePage(new_pdf8.getPage(0))
    page9.mergePage(new_pdf9.getPage(0))
    page10.mergePage(new_pdf10.getPage(0))
    page11.mergePage(new_pdf11.getPage(0))
    page12.mergePage(new_pdf12.getPage(0))
    page13.mergePage(new_pdf13.getPage(0))
    page14.mergePage(new_pdf14.getPage(0))
    page15.mergePage(new_pdf15.getPage(0))
    page16.mergePage(new_pdf16.getPage(0))
    page17.mergePage(new_pdf17.getPage(0))
    page18.mergePage(new_pdf18.getPage(0))
    page19.mergePage(new_pdf19.getPage(0))
    page20.mergePage(new_pdf20.getPage(0))
    page21.mergePage(new_pdf21.getPage(0))
    page22.mergePage(new_pdf22.getPage(0))
    page23.mergePage(new_pdf23.getPage(0))
    output.addPage(page)
    output.addPage(page2)
    output.addPage(page3)
    output.addPage(page4)
    output.addPage(page5)
    output.addPage(page6)
    output.addPage(page7)
    output.addPage(page8)
    output.addPage(page9)
    output.addPage(page10)
    output.addPage(page11)
    output.addPage(page12)
    output.addPage(page13)
    output.addPage(page14)
    output.addPage(page15)
    output.addPage(page16)
    output.addPage(page17)
    output.addPage(page18)
    output.addPage(page19)
    output.addPage(page20)
    output.addPage(page21)
    output.addPage(page22)
    output.addPage(page23)
    outputStream = open("pdfs/"+str(datos[0])+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()



if __name__ == '__main__':
   generarPdfId('307-1605790991386')