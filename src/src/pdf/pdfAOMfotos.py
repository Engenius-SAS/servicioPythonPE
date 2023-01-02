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
              cursor.execute("SELECT B.`Id_Encuesta`, B.`Rutaserver`, A.Id_Encuesta, A.Nombre_Completo, A.Cedula FROM db_liwa.Fotos_AOM B INNER JOIN db_liwa.AOM A ON B.`Id_Encuesta` = A.`Id_Encuesta` WHERE A.Id_Encuesta IN ('"+id+"');")
              datos = cursor.fetchall()
    print("41aaaa",datos)
    varia = 760
    varia2 = 150
    lab = False
    packet = io.BytesIO()
    can= canvas.Canvas(packet, pagesize=A4)
    for i in datos:
        print(i[1])
        varia = varia - varia2
        print("Holas",varia)
        can.drawString(80, 795,"ID: "+i[2])
        can.drawString(80, 775,"Nombre: "+i[3])
        if (varia < 10 or lab == True ):
            var = varia + 900
            var = var - varia2
            lab = True
            print("Holas",var)
            can.drawImage("https://www.php.engenius.com.co"+i[1], 315, var, 200, 132 )
            
        else:

            can.drawImage("https://www.php.engenius.com.co"+i[1], 80, varia, 200, 132 )
            
    can.save()
    new_pdf = PyPDF2.PdfFileReader(packet)

    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/formatoAOM/PG-Blanco.pdf", "rb"))

    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

    # os.mkdir('pdfs/'+str(i[0]))
    outputStream = open("pdfs/"+str(i[0])+"_Fotos.pdf", "wb")
    output.write(outputStream)
    outputStream.close()






    

if __name__ == '__main__':
   generarPdfId('307-1605790991386')