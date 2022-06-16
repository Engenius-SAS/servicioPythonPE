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

def generarPdf(idFormulario, consecutivo):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT A.Num_formulario,CONCAT(A.Dia,'/',A.Mes,'/',A.Año),D.Nombre_encuestado,D.Cedula_encuestado,J.U_vereda,J.U_municipio,J.U_latitud,J.U_longitud, D.`Telefono_celular_encuestado`, N.`rutaserver` FROM suncosurvey.encabezado A INNER JOIN suncosurvey.c_sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN suncosurvey.caracteristicas_predio C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN suncosurvey.consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN suncosurvey.datos_vivienda_I E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN suncosurvey.economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN suncosurvey.energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN suncosurvey.servicios_publicos H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN suncosurvey.tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN suncosurvey.ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN suncosurvey.URE K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN suncosurvey.porcentaje L ON A.Id_Encuesta = L.Id_Encuesta INNER JOIN suncosurvey.agua M ON A.Id_Encuesta = M.Id_Encuesta INNER JOIN suncosurvey.fotos_firma N ON A.Id_Encuesta = N.Id_Encuesta WHERE A.isdelete = 0 AND D.Nombre_beneficiario_usuario != 'null'AND L.Verificacion IS NOT NULL AND (L.IsAlert='0' OR L.IsAlert IS NULL) AND A.Id_Proyecto_Funcionario IN (SELECT `Id_Proyecto_Funcionario` FROM suncosurvey.proyectos_funcionarios WHERE `Id_Proyecto` = '2' AND `Num_formulario`= '"+idFormulario+"')")
              datos = cursor.fetchone()
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    fecha = dia +"/04/2022"
    can.drawString(118, 672, fecha)
    can.drawString(435, 672, consecutivo)
    can.drawString(90, 632, datos[2])
    can.drawString(60, 619, datos[3])
    can.drawString(330, 606, datos[4])
    can.drawString(60, 593, datos[5])
    can.drawString(410, 593, datos[6])
    can.drawString(60, 580, datos[7])
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
    can.drawString(93, 327, datos[2])
    can.drawString(93, 314, datos[3])
    can.drawString(103, 299, datos[8])
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