import PyPDF2 
import io
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import zipfile
import pymysql 
import tkinter as tk
from PIL import Image, ImageFont, ImageDraw, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
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
    # generarPdfId()
    
    if os.path.exists("pdfs"):
        pdfsExistentes = ([arch.name for arch in os.scandir("pdfs") if arch.is_file()])
        for pdf in pdfsExistentes:
            os.remove("pdfs/"+pdf)
    if os.path.exists("destination.zip"):
        os.remove("destination.zip")
       # print(ids)
    for id in ids:
        generarPdfId(id)
    zf = zipfile.ZipFile("destination.zip", mode="w")
    pdfsExistentes = ([arch.name for arch in os.scandir("pdfs") if arch.is_file()])
    try:
        for pdf in pdfsExistentes:
            zf.write("pdfs/"+pdf, compress_type=compression)
    finally:
        zf.close()
   
def generarPdfId(id):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
            cursor.execute("SELECT B.`Id_Encuesta`, B.`Rutaserver`, A.Id_Encuesta, A.Nombre_Completo, A.Cedula, A.Latitud, A.Longitud,A.Medidor,A.MarcaM,A.SerialM,A.Fotovoltaico,A.Gabinete,A.Paneles,A.SPT,A.PortaT,A.Inversor,A.MPPT,A.Bateria,A.Protecciones,A.Instalaciones,A.Soporte,A.NFC,A.Percepcion,A.TelefonoIn,A.Celulares,A.Internet,A.Lavadora,A.Nevera,A.Licuadora,A.Ventilador,A.AireAcondicionado,A.Sanduchera,A.Ducha,A.Cercas,A.NumLED,A.NumIncand,A.TV,A.Otras FROM db_liwa.Fotos_AOM B INNER JOIN db_liwa.AOM A ON B.`Id_Encuesta` = A.`Id_Encuesta` WHERE B.IsDelete = 0 AND  A.Id_Encuesta IN ('"+id+"');")
            datos = cursor.fetchall()
    if datos : 
        print("41aaaa",id,datos)
        varia = 760
        varia2 = 150
        lab = False
        packet = io.BytesIO()
        can= canvas.Canvas(packet, pagesize=A4)
        can.drawImage("./Dispower.png", 350, 750, 200, 90 )
        for i in datos:
            can.drawString(80, 800,"ID: "+i[2])
            can.drawString(80, 780,"Nombre: "+i[3])
            can.drawString(80, 760,"Documento: "+i[4])
            can.drawString(80, 740,"Coordenadas: "+i[5] + i[6])
            can.drawString(80, 720,"Medidor: "+i[7])
            can.drawString(80, 700,"Marca Medidor: "+i[8])
            can.drawString(80, 680,"Serial Medidor: "+i[9])
            can.drawString(80, 660,"Tipo de módulo fotovoltaico: "+i[10])
            can.drawString(80, 640,"Estado del Gabinete: "+i[11])
            can.drawString(80, 620,"Estado paneles: "+i[12])
            can.drawString(80, 600,"Estado puesta a tierra(SPT): "+i[13])
            can.drawString(80, 580,"Estado porta tarjeta NFC: "+i[14])
            can.drawString(80, 560,"Estado inversor: "+i[15])
            can.drawString(80, 540,"Estado Controladore de carga (MPPT): "+i[16])
            can.drawString(80, 520,"Estado de la Bateria: "+i[17])
            can.drawString(80, 500,"Estado de Protecciones (Tacos/Breakeirs): "+i[18])
            can.drawString(80, 480,"Estado instalaciones General: "+i[19])
            can.drawString(80, 460,"Estado soporte de paneles: "+i[20])
            can.drawString(80, 440,"Tarjeta NFC: "+i[21])
            can.drawString(80, 420,"Persepcíon del servicio: "+i[22])
            can.drawString(80, 400,"Telefono Inalambrico: "+i[23])
            can.drawString(80, 380,"Celulares: "+str(i[24]))
            can.drawString(80, 360,"Internet Wi-Fi: "+i[25])
            can.drawString(80, 340,"Lavadora: "+i[26])
            can.drawString(80, 320,"Nevera: "+i[27])
            can.drawString(80, 300,"Licuadora: "+i[28])
            can.drawString(80, 280,"Ventilador: "+i[29])
            can.drawString(80, 260,"Aire Acondicionado: "+i[30])
            can.drawString(80, 240,"Sanduchera: "+i[31])
            can.drawString(80, 220,"Ducha Eléctrica: "+i[32])
            can.drawString(80, 200,"Cercas Eléctricas: "+i[33])
            can.drawString(80, 180,"Numero de Bombillas LED: "+str(i[34]))
            can.drawString(80, 160,"Nuero de Bombillas Incandesentes: "+str(i[35]))
            can.drawString(80, 140,"TV: "+i[36])
            can.drawString(80, 120,"Otros: "+i[37])
                
        can.save()
        packet1 = io.BytesIO()
        can1= canvas.Canvas(packet1, pagesize=A4)
        can1.drawImage("./Dispower.png", 350, 750, 200, 90 )
        for i in datos:
            print(i[1])
            varia = varia - varia2
            print("Holas",varia)
            can1.drawString(80, 800,"ID: "+i[2])
            can1.drawString(80, 788,"Nombre: "+i[3])
            can1.drawString(80, 775,"Coordenadas: "+i[5] + i[6])
            if (varia < 10 or lab == True ):
                var = varia + 900
                var = var - varia2
                lab = True
                print("Holas",var)
                can1.drawImage("https://www.php.engenius.com.co"+i[1], 315, var, 200, 132 )
                
            else:

                can1.drawImage("https://www.php.engenius.com.co"+i[1], 80, varia, 200, 132 )
    else:
        with bd.cursor() as cursor:
            cursor.execute("SELECT A.Id_Encuesta, A.Nombre_Completo, A.Cedula, A.Latitud, A.Longitud,A.Medidor,A.MarcaM,A.SerialM,A.Fotovoltaico,A.Gabinete,A.Paneles,A.SPT,A.PortaT,A.Inversor,A.MPPT,A.Bateria,A.Protecciones,A.Instalaciones,A.Soporte,A.NFC,A.Percepcion,A.TelefonoIn,A.Celulares,A.Internet,A.Lavadora,A.Nevera,A.Licuadora,A.Ventilador,A.AireAcondicionado,A.Sanduchera,A.Ducha,A.Cercas,A.NumLED,A.NumIncand,A.TV,A.Otras FROM db_liwa.AOM A WHERE A.Id_Encuesta IN ('"+id+"');")
            datos = cursor.fetchall()
        print("41aaaa",id,datos)
        varia = 760
        varia2 = 150
        lab = False
        packet = io.BytesIO()
        can= canvas.Canvas(packet, pagesize=A4)
        can.drawImage("./Dispower.png", 350, 750, 200, 90 )
        for i in datos:
            can.drawString(80, 800,"ID: "+i[0])
            can.drawString(80, 780,"Nombre: "+i[1])
            can.drawString(80, 760,"Documento: "+i[2])
            can.drawString(80, 740,"Coordenadas: "+i[3] + i[4])
            can.drawString(80, 720,"Medidor: "+i[5])
            can.drawString(80, 700,"Marca Medidor: "+i[6])
            can.drawString(80, 680,"Serial Medidor: "+i[7])
            can.drawString(80, 660,"Tipo de módulo fotovoltaico: "+i[8])
            can.drawString(80, 640,"Estado del Gabinete: "+i[9])
            can.drawString(80, 620,"Estado paneles: "+i[10])
            can.drawString(80, 600,"Estado puesta a tierra(SPT): "+i[11])
            can.drawString(80, 580,"Estado porta tarjeta NFC: "+i[12])
            can.drawString(80, 560,"Estado inversor: "+i[13])
            can.drawString(80, 540,"Estado Controladore de carga (MPPT): "+i[14])
            can.drawString(80, 520,"Estado de la Bateria: "+i[15])
            can.drawString(80, 500,"Estado de Protecciones (Tacos/Breakeirs): "+i[16])
            can.drawString(80, 480,"Estado instalaciones General: "+i[17])
            can.drawString(80, 460,"Estado soporte de paneles: "+i[18])
            can.drawString(80, 440,"Tarjeta NFC: "+i[19])
            can.drawString(80, 420,"Persepcíon del servicio: "+i[20])
            can.drawString(80, 400,"Telefono Inalambrico: "+i[21])
            can.drawString(80, 380,"Celulares: "+str(i[22]))
            can.drawString(80, 360,"Internet Wi-Fi: "+i[23])
            can.drawString(80, 340,"Lavadora: "+i[24])
            can.drawString(80, 320,"Nevera: "+i[25])
            can.drawString(80, 300,"Licuadora: "+i[26])
            can.drawString(80, 280,"Ventilador: "+i[27])
            can.drawString(80, 260,"Aire Acondicionado: "+i[28])
            can.drawString(80, 240,"Sanduchera: "+i[29])
            can.drawString(80, 220,"Ducha Eléctrica: "+i[30])
            can.drawString(80, 200,"Cercas Eléctricas: "+i[31])
            can.drawString(80, 180,"Numero de Bombillas LED: "+str(i[32]))
            can.drawString(80, 160,"Nuero de Bombillas Incandesentes: "+str(i[33]))
            can.drawString(80, 140,"TV: "+i[34])
            can.drawString(80, 120,"Otros: "+i[35])
            
        can.save()
        packet1 = io.BytesIO()
        can1= canvas.Canvas(packet1, pagesize=A4)
        can1.drawImage("./Dispower.png", 350, 750, 200, 90 )
        for i in datos:
            print(i[1])
            varia = varia - varia2
            print("Holas",varia)
            can1.drawString(80, 800,"ID: "+i[0])
            can1.drawString(80, 788,"Nombre: "+i[1])
            can1.drawString(80, 775,"Coordenadas: "+i[3] + i[4])
            can1.drawString(80, 705,"No cuenta con fotos registradas en el sistema!")
            
    can1.save()
    new_pdf = PyPDF2.PdfFileReader(packet)
    new_pdf1 = PyPDF2.PdfFileReader(packet1)

    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/formatoAOM/PG-Blanco.pdf", "rb"))
    existing_pdf1 = PyPDF2.PdfFileReader(open("src/pdf/formatoAOM/PG-Blanco.pdf", "rb"))

    output = PyPDF2.PdfFileWriter()

    page = existing_pdf.getPage(0)
    page1 = existing_pdf1.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page1.mergePage(new_pdf1.getPage(0))
    output.addPage(page)
    output.addPage(page1)

    # os.mkdir('pdfs/'+str(i[0]))
    outputStream = open("pdfs/"+str(i[0])+"_Fotos.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    

if __name__ == '__main__':
   generarPdfId('307-1605790991386')