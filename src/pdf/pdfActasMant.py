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
        cursor.execute("SELECT A.Id_Encuesta, A.fecha, B.Maintenance_Type, C.UserName, A.Id_Proyecto, A.Id_Seccional, A.nombre, D.NUI, A.tipoDoc, A.numeroDoc, A.telefono, A.email, A.usopredio, A.propio, A.estrato, A.depto, A.municipio, A.codmuni, A.vereda, A.Latitud, A.Longitud, A.tipo, A.medidor, A.marcaM, A.serialM, A.instalaciones, A.fotovoltaico, A.estadoGabinete, A.paneles, A.puestaTierra, A.inversor, A.bateria, A.protecciones, A.mppt, A.soporte, A.observacionesF FROM db_liwa.Tecnico A INNER JOIN db_liwa.Maintenance_new B ON A.instalMant = B.Id_Maintenance INNER JOIN db_liwa.User C ON A.Id_Encuestador = C.Id_User INNER JOIN db_liwa.AOM D ON B.Id_Beneficiario = D.Id_Encuesta  WHERE A.Id_Encuesta IN ('"+id+"');")
        datos = cursor.fetchone()
    print(datos)
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 10)
    if str(datos[0]) == None:
        can.drawString(439, 664, "-")#ID encuesta
    else:
        can.drawString(439, 664, str(datos[0]))#ID encuesta
    if str(datos[1]) == None:
        can.drawString(478, 642, "-")# Fecha
    else:
        can.drawString(478, 642, str(datos[1]))# Fecha

    if str(datos[2]) == None:
        can.drawString(169, 616, "-")
    else:
        can.drawString(169, 616, str(datos[2]))# Tipo de matenimiento
    if str(datos[3]) == None:
        can.drawString(380, 616, "-")
    else:
        can.drawString(380, 616, str(datos[3]))# Nom. tecnico
    if str(datos[4]) == None:
        can.drawString(169, 603, "-")
    else:
        can.drawString(169, 603, str(datos[4]))# Proyecto
    if str(datos[5]) == None:
        can.drawString(380, 603, "-")
    else:
        can.drawString(380, 603, str(datos[5]))# Seccional
    
    if str(datos[6]) == None:
        can.drawString(200, 565, "-")
    else:
        can.drawString(200, 565, str(datos[6]))# Nombre
    if str(datos[7]) == None:
        can.drawString(458, 565, "-")
    else:
        can.drawString(458, 565, str(datos[7]))# NUI
    
    if str(datos[8]) == "RC":
        can.drawString(100, 552, "X")# Tipo Doc
    elif str(datos[8]) == "TI":
        can.drawString(125, 552, "X")# Tipo Doc
    elif str(datos[8]) == "CC":
        can.drawString(155, 552, "X")# Tipo Doc
    elif str(datos[8]) == "CE":
        can.drawString(180, 552, "X")# Tipo Doc
    elif str(datos[8]) == None:
        can.drawString(190, 552, ".")# Tipo Doc

    if str(datos[9]) == None:
        can.drawString(310, 552, "-")
    else:
        can.drawString(310, 552, str(datos[9]))#  N Documento
    
    if str(datos[10]) == None:
        can.drawString(458, 552, "-")
    else:
        can.drawString(458, 552, str(datos[10]))#  N telefono
    if str(datos[11]) == None:
        can.drawString(205, 539, "-")
    else:
        can.drawString(205, 539, str(datos[11]))#  correo

    if str(datos[12]) == None:
        can.drawString(150, 525, "-")
    else:
        can.drawString(150, 525, str(datos[12]))#  UsoPredio

    if str(datos[13]) == None:
        can.drawString(399, 525, "-")
    else:
        can.drawString(399, 525, str(datos[13]))#  Predio propio
    
    if str(datos[14]) == None:
        can.drawString(486, 525, "-")
    else:
        can.drawString(486, 525, str(datos[14]))#  estrato
    
    if str(datos[15]) == None:
        can.drawString(163, 486, "-")
    else:
        can.drawString(163, 486, str(datos[15]))#  Departamento

    if str(datos[16]) == None:
        can.drawString(313, 486, "-")
    else:
        can.drawString(313, 486, str(datos[16]))#  Municipio
    if str(datos[17]) == None:
        can.drawString(480, 486, "-")
    else:
        can.drawString(480, 486, str(datos[17]))#  Cod. Municipio

    if str(datos[18]) == None:
        can.drawString(163, 473, "-")
    else:
        can.drawString(163, 473, str(datos[18]))#  Vereda

    if str(datos[19]) == None:
        can.drawString(313, 473, "-")
    else:
        can.drawString(313, 473, str(datos[19]))#  latitud
    
    if str(datos[20]) == None:
        can.drawString(464, 473, "-")
    else:
        can.drawString(464, 473, str(datos[20]))#  Longitud

    if str(datos[21]) == None:
        can.drawString(156, 434, "-")
    else:
         can.drawString(156, 434, str(datos[21]))#  Tipo_Insta

    if str(datos[22]) == "Si":
        can.drawString(155, 421, "X")#  Tipo_Insta
    elif str(datos[22]) == "No":
        can.drawString(180, 421, "X")#  Tipo_Insta
    elif str(datos[22]) == None:
        can.drawString(190, 421, ".")#  Tipo_Insta

    if str(datos[23]) == None:
        can.drawString(297, 421, "-")
    else:
        can.drawString(297, 421, str(datos[23]))#  Marca

    if str(datos[24]) == None:
        can.drawString(464, 421, "-")
    else:
        can.drawString(464, 421, str(datos[24]))#  Serial Me

    if str(datos[24]) == None:
        can.drawString(155, 408, "-")
    else:
        can.drawString(155, 408, str(datos[25]))#  Instalacion

    if str(datos[24]) == None:
        can.drawString(399, 408, "-")
    else:
        can.drawString(399, 408, str(datos[26]))#  Fotovoltaica
    

    if str(datos[27]) == None:
        can.drawString(155, 369, "-")
    else:
        can.drawString(155, 369, str(datos[27]))#  Gibnete
    
    if str(datos[28]) == None:
        can.drawString(270, 369, "-")
    else:
        can.drawString(270, 369, str(datos[28]))# Paneles
    
    if str(datos[29]) == None:
        can.drawString(380, 369, "-")
    else:
        can.drawString(380, 369, str(datos[29]))# Puesta_t
    
    if str(datos[30]) == None:
        can.drawString(486, 369, "-")
    else:
        can.drawString(486, 369, str(datos[30]))# inveror
    
    if str(datos[31]) == None:
        can.drawString(155, 356, "-")
    else:
        can.drawString(155, 356, str(datos[31]))# Bateria
    
    if str(datos[32]) == None:
        can.drawString(270, 356, "-")
    else:
        can.drawString(270, 356, str(datos[32]))# Proyeccion
    
    if str(datos[33]) == None:
        can.drawString(380, 356, "-")
    else:
        can.drawString(380, 356, str(datos[33]))# Mppt
    
    if str(datos[34]) == None:
        can.drawString(486, 356, "-")
    else:
        can.drawString(486, 356, str(datos[34]))# Soporte
    
    if str(datos[35]) == None:
        can.drawString(100, 331, "-")
    else:
        can.drawString(100, 331, str(datos[35]))# Observaciones
    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = 'MF2'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        print(fotos1) 
        if fotos1 ==  None or fotos1 ==  'None':
            can.drawString(110, 216, "No Registra Fotografia")
        else:            
            can.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 216, 170, 80 )
    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = 'MF3'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone() 
        if fotos1 ==  None :
            can.drawString(338, 216, "No Registra Fotografia")
        else:
            can.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 216, 170, 80 )
    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = 'MF1'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone() 
        if fotos1 ==  None :
            can.drawString(110, 102, "No Registra Fotografia")
        else:
            can.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 102, 170, 84 )
    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.fotos_firma WHERE Id_Formulario = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None :
            urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
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
            can.drawImage('new.png', 338, 102, 170, 84)
        elif str(fotos1[4]) != "NO ENCONTRADO ARCHIVO LOCAL" and str(fotos1[4]) != "null" :   
            urllib.request.urlretrieve("https://www.php.engenius.com.co"+fotos1[4],"ejemplo.jpg")
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
            can.drawImage('new.png', 338, 102, 170, 84 )
        else:
            urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
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
            can.drawImage('new.png', 338, 102,170, 84)

    can.save()
    packet1 = io.BytesIO()
    can1 = canvas.Canvas(packet1, pagesize=A4)
    can1.setFont("Helvetica", 10)
    can1.drawString(600, 700, ".")

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '1'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(110, 580, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 580, 170, 80 )
    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '1f'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(338, 580, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 580, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '2'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(110, 460, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 460, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '2f'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(338, 460, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 460, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '3'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(110, 340, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 340, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '3f'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(338, 340, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 340, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '4'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(110, 225, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 225, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '4f'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(338, 225, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 225, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '5'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(110, 110, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 110, 110, 170, 80 )

    with bd.cursor() as cursor:
        cursor.execute("SELECT * FROM db_liwa.Fotos_Tecnico WHERE Estado = '5f'  AND Id_Encuesta = '"+id+"';")
        fotos1 = cursor.fetchone()
        if fotos1 ==  None or fotos1 ==  'None':
            can1.drawString(338, 110, "No Registra Fotografia")
        else:
            can1.drawImage("https://www.php.engenius.com.co"+fotos1[4], 338, 110, 170, 80 )
    can1.save()     
    # if datos : 
    #     print("41aaaa",id,datos)
    #     varia = 760
    #     varia2 = 150
    #     lab = False
    #     packet = io.BytesIO()
    #     can= canvas.Canvas(packet, pagesize=A4)
    #     can.drawImage("./Dispower.png", 350, 750, 200, 90 )
    #     for i in datos:
    #         can.drawString(80, 800,"ID: "+i[2])
    #         can.drawString(80, 780,"Nombre: "+str(i[3]))
    #         can.drawString(80, 760,"Documento: "+str(i[4]))
    #         can.drawString(80, 740,"Coordenadas: "+str(i[5]) +"|"+ str(i[6]))
    #         can.drawString(80, 720,"Medidor: "+str(i[7]))
    #         can.drawString(80, 700,"Marca Medidor: "+str(i[8]))
    #         can.drawString(80, 680,"Serial Medidor: "+str(i[9]))
    #         can.drawString(80, 660,"Tipo de módulo fotovoltaico: "+str(i[10]))
    #         can.drawString(80, 640,"Estado del Gabinete: "+str(i[11]))
    #         can.drawString(80, 620,"Estado paneles: "+str(i[12]))
    #         can.drawString(80, 600,"Estado puesta a tierra(SPT): "+str(i[13]))
    #         can.drawString(80, 580,"Estado porta tarjeta NFC: "+str(i[14]))
    #         can.drawString(80, 560,"Estado inversor: "+str(i[15]))
    #         can.drawString(80, 540,"Estado Controladore de carga (MPPT): "+str(i[16]))
    #         can.drawString(80, 520,"Estado de la Bateria: "+str(i[17]))
    #         can.drawString(80, 500,"Estado de Protecciones (Tacos/Breakeirs): "+str(i[18]))
    #         can.drawString(80, 480,"Estado instalaciones General: "+str(i[19]))
    #         can.drawString(80, 460,"Estado soporte de paneles: "+str(i[20]))
    #         can.drawString(80, 440,"Tarjeta NFC: "+str(i[21]))
    #         can.drawString(80, 380,"Referencia: "+str(i[24]))
    #         can.drawString(80, 360,"Numero: "+str(i[25]))
    #         can.drawString(80, 340,"Recarga: "+str(i[26]))
    #         can.drawString(80, 320,"Localizacion: "+str(i[27]))
    #         can.drawString(80, 300,"Observaciones: "+str(i[28]))
    #         can.drawString(80, 280,"Equipos: "+str(i[29]))
    #         can.drawString(80, 260,"Falla: "+str(i[31]))
    #         can.drawString(80, 240,"Labores: "+str(i[32]))
    #         can.drawString(80, 220,"Tecnicos: "+str(i[33]))
    #         can.drawString(80, 200,"Externos: "+str(i[34]))
    #         can.drawString(80, 180,"Observaciones: "+str(i[35]))

    #         with bd.cursor() as cursor:
    #                 cursor.execute("Select rutaserver from db_liwa.fotos_firma where Id_Formulario = '"+id+"';")
    #                 datos2 = cursor.fetchone()
    #         if datos2 ==  None :
    #             print(datos2,"asd")
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")
    #         elif str(datos2[0]) != "NO ENCONTRADO ARCHIVO LOCAL" and str(datos2[0]) != "null" :   
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos2[0],"ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")
    #         else:
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")

                
    #     can.save()
    #     packet1 = io.BytesIO()
    #     can1= canvas.Canvas(packet1, pagesize=A4)
    #     can1.drawImage("./Dispower.png", 350, 750, 200, 90 )
    #     for i in datos:
    #         print(i[1])
    #         varia = varia - varia2
    #         print("Holas",varia)
    #         can1.drawString(80, 800,"ID: "+i[2])
    #         can1.drawString(80, 788,"Nombre: "+i[3])
    #         can1.drawString(80, 775,"Coordenadas: "+i[5] + i[6])
    #         if (varia < 10 or lab == True ):
    #             var = varia + 900
    #             var = var - varia2
    #             lab = True
    #             print("Holas",var)
    #             can1.drawImage("https://www.php.engenius.com.co"+i[1], 315, var, 200, 132 )
                
    #         else:

    #             can1.drawImage("https://www.php.engenius.com.co"+i[1], 80, varia, 200, 132 )
    # else:
    #     with bd.cursor() as cursor:
    #         cursor.execute("SELECT A.Id_Encuesta, A.nombre, A.numeroDoc, A.Latitud, A.Longitud,A.medidor,A.marcaM,A.serialM,A.fotovoltaico,A.estadoGabinete,A.paneles,A.puestaTierra,A.portaT,A.inversor,A.mppt,A.bateria,A.protecciones,A.instalaciones,A.soporte,A.nfc,A.instalMant,A.marcame,A.referencia,A.numero,A.recarga,A.localizacion,A.observacionesF,A.equipos,A.cuales,A.falla,A.labores,A.tecnicos,A.externos,A.observaciones FROM db_liwa.Tecnico A  WHERE A.IsDelete = 0 AND  A.Id_Encuesta IN ('"+id+"');")
    #         datos = cursor.fetchall()
    #     print("41aaaa",id,datos)
    #     varia = 760
    #     varia2 = 150
    #     lab = False
    #     packet = io.BytesIO()
    #     can= canvas.Canvas(packet, pagesize=A4)
    #     can.drawImage("./Dispower.png", 350, 750, 200, 90 )
    #     for i in datos:
    #         can.drawString(80, 800,"ID: "+i[0])
    #         can.drawString(80, 780,"Nombre: "+str(i[1]))
    #         can.drawString(80, 760,"Documento: "+str(i[2]))
    #         can.drawString(80, 740,"Coordenadas: "+str(i[3]) +"|"+ str(i[4]))
    #         can.drawString(80, 720,"Medidor: "+str(i[6]))
    #         can.drawString(80, 700,"Marca Medidor: "+str(i[7]))
    #         can.drawString(80, 680,"Serial Medidor: "+str(i[8]))
    #         can.drawString(80, 660,"Tipo de módulo fotovoltaico: "+str(i[9]))
    #         can.drawString(80, 640,"Estado del Gabinete: "+str(i[10]))
    #         can.drawString(80, 620,"Estado paneles: "+str(i[11]))
    #         can.drawString(80, 600,"Estado puesta a tierra(SPT): "+str(i[12]))
    #         can.drawString(80, 580,"Estado porta tarjeta NFC: "+str(i[13]))
    #         can.drawString(80, 560,"Estado inversor: "+str(i[14]))
    #         can.drawString(80, 540,"Estado Controladore de carga (MPPT): "+str(i[15]))
    #         can.drawString(80, 520,"Estado de la Bateria: "+str(i[16]))
    #         can.drawString(80, 500,"Estado de Protecciones (Tacos/Breakeirs): "+str(i[17]))
    #         can.drawString(80, 480,"Estado instalaciones General: "+str(i[18]))
    #         can.drawString(80, 460,"Estado soporte de paneles: "+str(i[19]))
    #         can.drawString(80, 440,"Tarjeta NFC: "+str(i[20]))
    #         can.drawString(80, 380,"Referencia: "+str(i[22]))
    #         can.drawString(80, 360,"Numero: "+str(i[23]))
    #         can.drawString(80, 340,"Recarga: "+str(i[24]))
    #         can.drawString(80, 320,"Localizacion: "+str(i[25]))
    #         can.drawString(80, 300,"Observaciones: "+str(i[26]))
    #         can.drawString(80, 280,"Equipos: "+str(i[27]))
    #         can.drawString(80, 260,"Falla: "+str(i[29]))
    #         can.drawString(80, 240,"Labores: "+str(i[30]))
    #         can.drawString(80, 220,"Tecnicos: "+str(i[31]))
    #         can.drawString(80, 200,"Externos: "+str(i[32]))
    #         can.drawString(80, 180,"Observaciones: "+str(i[33]))
            
    #         with bd.cursor() as cursor:
    #                 cursor.execute("Select rutaserver from db_liwa.fotos_firma where Id_Formulario = '"+id+"';")
    #                 datos2 = cursor.fetchone()
    #         if datos2 ==  None :
    #             print(datos2,"asd")
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")
    #         elif str(datos2[0]) != "NO ENCONTRADO ARCHIVO LOCAL" and str(datos2[0]) != "null" :   
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos2[0],"ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")
    #         else:
    #             urllib.request.urlretrieve("https://www.php.engenius.com.co/Fotos_IPSE_AE/Fotos_firma/29-1637588696115.jpg","ejemplo.jpg")
    #             filename = 'ejemplo.jpg'
    #             filename1 = 'fondoblanco.jpg'
    #             frontImage = Image.open(filename)
    #             background = Image.open(filename1)
    #             frontImage = frontImage.convert("RGBA")
    #             background = background.convert("RGBA")
    #             width = (background.width - frontImage.width) // 2
    #             height = (background.height - frontImage.height) // 2
    #             background.paste(frontImage, (width, height), frontImage)
    #             background.save("new.png", format="png")
    #             can.drawImage('new.png', 80, 100, 175, 75 )
    #             can.drawString(80, 90,"Firma")
            
    #     can.save()
    #     packet1 = io.BytesIO()
    #     can1= canvas.Canvas(packet1, pagesize=A4)
    #     can1.drawImage("./Dispower.png", 350, 750, 200, 90 )
    #     for i in datos:
    #         print(i[1])
    #         varia = varia - varia2
    #         print("Holas",varia)
    #         can1.drawString(80, 800,"ID: "+i[0])
    #         can1.drawString(80, 788,"Nombre: "+i[1])
    #         can1.drawString(80, 775,"Coordenadas: "+i[3] + i[4])
    #         can1.drawString(80, 705,"No cuenta con fotos registradas en el sistema!")
            
    # can1.save()

    new_pdf = PyPDF2.PdfFileReader(packet)
    new_pdf1 = PyPDF2.PdfFileReader(packet1)

    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/actas/ActaDeMantenimientos-1.pdf", "rb"))
    existing_pdf1 = PyPDF2.PdfFileReader(open("src/pdf/actas/ActaDeMantenimientos-2.pdf", "rb"))

    output = PyPDF2.PdfFileWriter()

    page = existing_pdf.getPage(0)
    page1 = existing_pdf1.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page1.mergePage(new_pdf1.getPage(0))
    output.addPage(page)
    output.addPage(page1)

    # os.mkdir('pdfs/'+str(i[0]))
    outputStream = open("pdfs/"+str(datos[6])+"_Acta.pdf", "wb")
    output.write(outputStream)
    outputStream.close()


if __name__ == '__main__':
   generarPdfId('307-1605790991386')