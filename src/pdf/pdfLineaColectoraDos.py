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
              cursor.execute("SELECT A.*,B.*,C.*,D.*,E.*,F.*,G.*,H.*,N.*,I.*,J.*,K.*,M.* FROM aes2021.Encabezado A INNER JOIN aes2021.Sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN aes2021.Caracteristicas C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN aes2021.Consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN aes2021.Datos E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN aes2021.Economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN aes2021.Energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN aes2021.Servicios H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN aes2021.Tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN aes2021.Ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN aes2021.Sociales K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN aes2021.Agua N ON A.Id_Encuesta = N.Id_Encuesta INNER JOIN aes2021.Proyectos_funcionarios L ON A.Id_Proyecto_Funcionario = L.Id_Proyecto_Funcionario INNER JOIN aes2021.Funcionarios M ON M.Id_Funcionario = L.Id_Funcionario INNER JOIN aes2021.Porcentaje O ON A.Id_Encuesta = O.Id_Encuesta INNER JOIN aes2021.Encuestadores P ON A.Id_Encuesta = P.Id_Encuesta WHERE A.isdelete = 0 AND A.Id_Encuesta = '"+id+"';")
              datos = cursor.fetchone()
    print(id)

    #pagina 1
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)

    can.drawString(392, 813, datos[3])# num Formulario
    llenarCampos(can, 396, 802, datos[4],10)# Dia
    llenarCampos(can, 435, 802, datos[5],10)# Mes
    llenarCampos(can, 485, 802, datos[6],10)# Año
    
    # coordenadas  latitud
    latitudUnidad = datos[370].split('.')[0]
    latitudDecimales = datos[370].split('.')[1]
    can.drawString(240, 425, latitudUnidad)
    llenarCampos(can, 290, 425, latitudDecimales, 24)
    # coordenadas  longitud
    longitudUnidad = datos[371].split('.')[0]
    longitudDecimales = datos[371].split('.')[1]
    can.drawString(237, 388, longitudUnidad)
    llenarCampos(can, 290, 388, longitudDecimales, 24)
    # coordenadas  altitud
    if datos[372] == 'null':
        altitud = '-'
    else:
        altitud = round(float(datos[372]))
    llenarCampos(can, 233, 350, str(altitud), 30)
    #nombre departamento
    llenarCampos(can, 124, 293, datos[374], 16)
    #codigo departamento
    llenarCampos(can, 124, 262, datos[375], 16)
    #nombre municipio
    llenarCampos(can, 124, 240, datos[376], 16)
    #codigo municipio
    llenarCampos(can, 124, 215, datos[377], 16)    
    #nombre vereda
    llenarCampos(can, 124, 191, datos[378], 16)  
    #nombre corregimiento
    llenarCampos(can, 124, 162, datos[379], 16)

    can.save()

    #pagina2
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=A4)
    
    can2.setFont("Helvetica", 9)

    can2.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can2, 396, 786, datos[4],10)# Dia
    llenarCampos(can2, 435, 786, datos[5],10)# Mes
    llenarCampos(can2, 485, 786, datos[6],10)# Año

    if datos[359] == 'Si':
        can2.drawString(318, 707, "X")
    else:
        can2.drawString(318, 697, "X")
    if datos[360] == 'Vivienda': 
        can2.drawString(318, 623, "X")
    else:
        can2.drawString(318, 613, "X")
    if datos[363] == 'Permanente': 
        can2.drawString(318, 538, "X")
    elif datos[363] == 'Temporal':
        can2.drawString(318, 526, "X")
    if datos[162] == 'Si': 
        can2.drawString(320, 280, "X")
    else:
        can2.drawString(368, 280, "X")

    fuente = datos[185]
    if fuente == 'Gas Propano': 
        can2.drawString(368, 168, datos[163])
        can2.drawString(458, 168, datos[174])
    else:
        can2.drawString(368, 168, "0")
        can2.drawString(458, 168, "0")
    if fuente == 'Gas Natural':
        can2.drawString(368, 156, datos[164])
        can2.drawString(458, 156, datos[175])
    else:
        can2.drawString(368, 156, "0")
        can2.drawString(458, 156, "0")
    if fuente == 'Gasolina':
        can2.drawString(368, 144, datos[165])
        can2.drawString(458, 144, datos[176])
    else:
        can2.drawString(368, 144, "0")
        can2.drawString(458, 144, "0")
    if fuente == 'Kerosene':
        can2.drawString(368, 132, datos[166])
        can2.drawString(458, 132, datos[177])
    else:
        can2.drawString(368, 132, "0")
        can2.drawString(458, 132, "0")
    if fuente == 'Petróleo':
        can2.drawString(368, 120, datos[167])
        can2.drawString(458, 120, datos[178])
    else:
        can2.drawString(368, 120, "0")
        can2.drawString(458, 120, "0")
    if fuente == 'Alcohol':
        can2.drawString(368, 108, datos[168])
        can2.drawString(458, 108, datos[179])
    else:
        can2.drawString(368, 108, "0")
        can2.drawString(458, 108, "0")
    if fuente == 'Carbón Mineral':
        can2.drawString(368, 96, datos[169])
        can2.drawString(458, 96, datos[180])
    else:
        can2.drawString(368, 96, "0")
        can2.drawString(458, 96, "0")
    if fuente == 'Leña Comprada':
        can2.drawString(368, 84, datos[170])
        can2.drawString(458, 84, datos[181])
    else:
        can2.drawString(368, 84, "0")
        can2.drawString(458, 84, "0")
    if fuente == 'Leña Auto Apropiada':
        can2.drawString(368, 72, datos[171])
        can2.drawString(458, 72, datos[182])
    else:
        can2.drawString(368, 72, "0")
        can2.drawString(458, 72, "0")
    if fuente == 'Residuos del Agro':
        can2.drawString(368, 60, datos[172])
        can2.drawString(458, 60, datos[183])
    else:
        can2.drawString(368, 60, "0")
        can2.drawString(458, 60, "0")
    if fuente == 'Otro':
        can2.drawString(150, 48, datos[186])
        can2.drawString(260, 48, "kg")
        can2.drawString(368, 44, datos[173])
        can2.drawString(458, 44, datos[184])
    else:
        can2.drawString(150, 48, datos[186])
        can2.drawString(260, 48, "kg")
        can2.drawString(368, 44, datos[173])
        can2.drawString(458, 44, datos[184])

    can2.save()
    #hoja 3 del pdf
    packet3 = io.BytesIO()
    # create a new PDF with Reportlab
    can3 = canvas.Canvas(packet3, pagesize=A4)
    can3.setFont("Helvetica", 9)

    can3.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can3, 396, 786, datos[4],10)# Dia
    llenarCampos(can3, 435, 786, datos[5],10)# Mes
    llenarCampos(can3, 485, 786, datos[6],10)# Año

    can3.drawString(372, 759, datos[187] + "  horas")
    #pilas baterias


       #Queman residuos
    if datos[188] == 'Si':
        can3.drawString(315, 690, "x")
    else:
        can3.drawString(315, 677, "x")

    #gas propano
    if datos[211] == "Gas Propano":
        can3.drawString(365, 575, datos[189])
        can3.drawString(462, 575, datos[200])
    else:
        can3.drawString(365, 575, "0")
        can3.drawString(462, 575, "0")
    #gas natural
    if datos[211] == "Gas Natural":
        can3.drawString(365, 563, datos[190])
        can3.drawString(462, 563, datos[201])
    else:
        can3.drawString(365, 563, "0")
        can3.drawString(462, 563, "0")
    #gasolina
    if datos[211] == "Gasolina":
        can3.drawString(365, 551, datos[191])
        can3.drawString(462, 551, datos[202])
    else:
        can3.drawString(365, 551, "0")
        can3.drawString(462, 551, "0")
    #
    if datos[211] == "Kerosene":
        can3.drawString(365, 539, datos[192])
        can3.drawString(462, 539, datos[203])
    else:
        can3.drawString(365, 539, "0")
        can3.drawString(462, 539, "0")
    #Petroleo
    if datos[211] == "Petróleo":
        can3.drawString(365, 527, datos[193])
        can3.drawString(462, 527, datos[204])
    else:
        can3.drawString(365, 527, "0")
        can3.drawString(462, 527, "0")
    #Carbon mineral
    if datos[211] == "Alcohol":
        can3.drawString(365, 515, datos[194])
        can3.drawString(462, 515, datos[205])
    else:
        can3.drawString(365, 515, "0")
        can3.drawString(462, 515, "0")
    #Leña comprada
    if datos[211] == "Carbón Mineral":
        can3.drawString(365, 503, datos[195])
        can3.drawString(462, 503, datos[206])
    else:
        can3.drawString(365, 503, "0")
        can3.drawString(462, 503, "0")
    #Leña autoapropiada
    if datos[211] == "Leña Comprada":
        can3.drawString(365, 491, datos[196])
        can3.drawString(462, 491, datos[207])
    else:
        can3.drawString(365, 491, "0")
        can3.drawString(462, 491, "0")
    #gas propano
    if datos[211] == "Leña Auto Apropiada":
        can3.drawString(365, 479, datos[197])
        can3.drawString(462, 479, datos[208])
    else:
        can3.drawString(365, 479, "0")
        can3.drawString(462, 479, "0")
    #residuos del agro
    if datos[211] == "Residuos del Agro":
        can3.drawString(365, 467, datos[198])
        can3.drawString(462, 467, datos[209])
    else:
        can3.drawString(365, 467, "0")
        can3.drawString(462, 467, "0")
    #Otro
    if datos[211] == "Otro": 
        can3.drawString(150, 455, datos[212])
        can3.drawString(260, 455, " ")
        can3.drawString(365, 452, datos[199])
        can3.drawString(462, 452, datos[210])
    else:
        can3.drawString(150, 455, datos[212])
        can3.drawString(260, 455, " ")
        can3.drawString(365, 452, datos[199])
        can3.drawString(462, 452, datos[210])


    if datos[239] == 'Baterias':
        can3.drawString(285, 317, datos[214])
        can3.drawString(345, 317, datos[222])
        if datos[230] == 'Cabecera municipal':
            can3.drawString(417, 317, 'x')
        elif datos[230] == 'Vereda':
            can3.drawString(460, 317, 'x')
        elif datos[230] == 'Domicilio':  
            can3.drawString(502, 317, 'x')
    else:
        can3.drawString(285, 317, "0")
        can3.drawString(345, 317, "0")

    #gasolina
    if datos[239] == 'Planta eléctrica a gasolina':
        can3.drawString(285, 305, datos[215])
        can3.drawString(345, 305, datos[223])
        if datos[231] == 'Cabecera municipal':
            can3.drawString(417, 305, 'x')
        elif datos[231] == 'Vereda':
            can3.drawString(460, 305, 'x')
        elif datos[231] == 'Domicilio':
            can3.drawString(502, 305, 'x')
    else:
        can3.drawString(285, 305, "0")
        can3.drawString(345, 305, "0")
    #Kerosene
    if datos[239] == 'Kerosene':
        can3.drawString(285, 293, datos[216])
        can3.drawString(345, 293, datos[224])
        if datos[232] == 'Cabecera municipal':
            can3.drawString(417, 293, 'x')
        elif datos[232] == 'Vereda':
            can3.drawString(460, 293, 'x')
        elif datos[232] == 'Domicilio':
            can3.drawString(502, 293, 'x')
    else:
        can3.drawString(285, 293, "0")
        can3.drawString(345, 293, "0")
    #Petroleo
    if datos[239] == 'Petróleo':
        can3.drawString(285, 281, datos[217])
        can3.drawString(345, 281, datos[225])
        if datos[233] == 'Cabecera municipal':
            can3.drawString(417, 281, 'x')
        elif datos[233] == 'Vereda':
            can3.drawString(460, 281, 'x')
        elif datos[233] == 'Domicilio':
            can3.drawString(502, 281, 'x')
    else:
        can3.drawString(285, 281, "0")
        can3.drawString(345, 281, "0")
    #Alcohol
    if datos[239] == 'Alcohol':
        can3.drawString(285, 269, datos[218])
        can3.drawString(345, 269, datos[226])
        if datos[234] == 'Cabecera municipal':
            can3.drawString(417, 269, 'x')
        elif datos[234] == 'Vereda':
            can3.drawString(460, 269, 'x')
        elif datos[234] == 'Domicilio':
            can3.drawString(502, 269, 'x')
    else:
        can3.drawString(285, 269, "0")
        can3.drawString(345, 269, "0")
    #Diesel
    if datos[239] == 'Planta eléctrica diesel':
        can3.drawString(285, 257, datos[219])
        can3.drawString(345, 257, datos[227])
        if datos[235] == 'Cabecera municipal':
            can3.drawString(417, 257, 'x')
        elif datos[235] == 'Vereda':
            can3.drawString(460, 257, 'x')
        elif datos[235] == 'Domicilio':
            can3.drawString(502, 257, 'x')
    else:
        can3.drawString(285, 257, "0")
        can3.drawString(345, 257, "0")
    #Velas
    if datos[239] == 'Velas':
        can3.drawString(285, 245, datos[220])
        can3.drawString(345, 245, datos[228])
        if datos[236] == 'Cabecera municipal':
            can3.drawString(417, 245, 'x')
        elif datos[236] == 'Vereda':
            can3.drawString(460, 245, 'x')
        elif datos[236] == 'Domicilio':
            can3.drawString(502, 245, 'x')
    else:
        can3.drawString(285, 245, "0")
        can3.drawString(345, 245, "0")
    #Otro
    if datos[239] == 'Otro':
        can3.drawString(120, 233, datos[238])
        can3.drawString(230, 233, " ")
        can3.drawString(285, 233, datos[221])
        can3.drawString(345, 233, datos[229])
        if datos[237] == 'Cabecera municipal':
            can3.drawString(417, 233, 'x')
        elif datos[237] == 'Vereda':
            can3.drawString(460, 233, 'x')
        elif datos[237] == 'Domicilio':
            can3.drawString(502, 233, 'x')
    else:
        can3.drawString(120, 233, datos[239])
        can3.drawString(230, 233, " ")
        can3.drawString(285, 233, "0")
        can3.drawString(345, 233, "0")
     #Horas al dia utiliza
    # can3.drawString(410, 612, datos[240])
 
    if datos[276] == 'Si':
        can3.drawString(320, 138, "x")
    else:
        can3.drawString(320, 124, "x")


    if datos[277] == "null":
        can3.drawString(90, 80, "$ 0")
    else:
        can3.drawString(90, 80, "$"+datos[277])


    #cuantas horas al dia utiliza para ilumminar 
    # can3.drawString(350, 305, datos[213])
    #contaminacion 
    #exceso de ruido
    # if datos[274] == 'Si':
    #     can3.drawString(385, 210, "x")
    # else:
    #     can3.drawString(430, 210, "x")
    #malos oloress
    # uso del predio

    can3.save()
    #hoja 4 del pdf
    packet4 = io.BytesIO()
    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet4, pagesize=A4)
    can4.setFont("Helvetica", 9)

    can4.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can4, 396, 786, datos[4],10)# Dia
    llenarCampos(can4, 435, 786, datos[5],10)# Mes
    llenarCampos(can4, 485, 786, datos[6],10)# Año
    #estrato del predio

    if datos[241] == "null" or datos[241] == "false":
        can4.drawString(345, 712, "0")
    else:
        can4.drawString(345, 712, "1")
    if datos[256] == "null"  or datos[256] == "false":
        can4.drawString(445, 712, "0")
    else:
        can4.drawString(445, 712, "1")
    if datos[242] == "null" or datos[242] == "false" :
        can4.drawString(345, 700, "0")
    else:
        can4.drawString(345, 700, "1")
    if datos[257] == "null"  or datos[257] == "false":
        can4.drawString(445, 700, "0")
    else:
        can4.drawString(445, 700, "1")
    if datos[243] == "null" or datos[243] == "false":
        can4.drawString(345, 688, "0")
    else:
        can4.drawString(345, 688, "1")
    if datos[258] == "null"  or datos[258] == "false":
        can4.drawString(445, 688, "0")
    else:
        can4.drawString(445, 688, "1")
    if datos[244] == "null" or datos[244] == "false" :
        can4.drawString(345, 676, "0")
    else:
        can4.drawString(345, 676, "1")
    if  datos[259] == "null"  or datos[259] == "false":
        can4.drawString(445, 676, "0")
    else:
        can4.drawString(445, 676, "1")
    if datos[245] == "null" or datos[245] == "false" :
        can4.drawString(345, 664, "0")
    else:
        can4.drawString(345, 664, "1")
    if  datos[260] == "null"  or datos[260] == "false":
        can4.drawString(445, 664, "0")
    else:
        can4.drawString(445, 664, "1")
    if datos[246] == "null" or datos[246] == "false" :
        can4.drawString(345, 652, "0")
    else:
        can4.drawString(345, 652, "1")
    if  datos[261] == "null"  or datos[261] == "false":
        can4.drawString(445, 652, "0")
    else:
        can4.drawString(445, 652, "1")
    if datos[247] == "null" or datos[247] == "false":
        can4.drawString(345, 640, "0")
    else:
        can4.drawString(345, 640, "1")
    if datos[262] == "null"  or datos[262] == "false":
        can4.drawString(445, 640, "0")
    else:
        can4.drawString(445, 640, "1")
    if datos[248] == "null" or datos[248] == "false":
        can4.drawString(345, 628, "0")
    else:
        can4.drawString(345, 628, "1")
    if datos[263] == "null"  or datos[263] == "false":
        can4.drawString(445, 628, "0")
    else:
        can4.drawString(445, 628, "1")
    if datos[249] == "null" or datos[249] == "false" :
        can4.drawString(345, 616, "0")
    else:
        can4.drawString(345, 616, "1") 
    if datos[264] == "null"  or datos[264] == "false":
        can4.drawString(445, 616, "0")
    else:
        can4.drawString(445, 616, "1")    
    if datos[250] == "null" or datos[250] == "false":
        can4.drawString(345, 604, "0")
    else:
        can4.drawString(345, 604, "1")
    if  datos[265] == "null"  or datos[265] == "false":
        can4.drawString(445, 604, "0")
    else:
        can4.drawString(445, 604, "1")   
    if datos[251] == "null" or datos[251] == "false":
        can4.drawString(345, 592, "0")
    else:
        can4.drawString(345, 592, "1") 
    if datos[266] == "null"  or datos[266] == "false":
        can4.drawString(445, 592, "0")
    else:
        can4.drawString(445, 592, "1") 
    if datos[252] == "null" or datos[252] == "false":
        can4.drawString(345, 580, "0")
    else:
        can4.drawString(345, 580, "1") 
    if datos[267] == "null"  or datos[267] == "false":
        can4.drawString(445, 580, "0")
    else:
        can4.drawString(445, 580, "1")  
    if datos[253] == "null" or datos[253] == "false" :
        can4.drawString(345, 568, "0")
    else:
        can4.drawString(345, 568, "1")
    if datos[268] == "null"  or datos[268] == "false":
        can4.drawString(445, 568, "0")
    else:
        can4.drawString(445, 568, "1")
    if datos[254] == "null" or datos[254] == "false":
        can4.drawString(345, 556, "0")
    else:
        can4.drawString(345, 556, "1")
    if datos[254] == "null" or datos[254] == "false":
        can4.drawString(445, 556, "0")
    else:
        can4.drawString(445, 556, "1") 
    if datos[255] == "null" or datos[255] == "false":
        can4.drawString(345, 542, " ")
    else:
        can4.drawString(345, 542, "1")
    if datos[270] == "null"  or datos[270] == "false":
        can4.drawString(445, 542, " ")
    else:
        can4.drawString(445, 542, "1")     

    if datos[271] == 'Si':
        can4.drawString(385, 469, "x")
    else:
        can4.drawString(430, 469, "x")

    if datos[272] == 'Si':
        can4.drawString(385, 456, "x")
    else:
        can4.drawString(430, 456, "x")

    if datos[273] == 'No':
        can4.drawString(320, 398, "x")
    else:
        can4.drawString(320, 384, "x")

    can4.drawString(90, 343, datos[274])

    if datos[272] == 'Si':
        can4.drawString(324, 254, "x")
        can4.drawString(368, 254, "x")
    else:
        can4.drawString(324, 254, "x")
        can4.drawString(368, 254, "x")

    #residencial
    if datos[73] == 'Residencial':
        can4.drawString(415, 150, "x")
    #negocio
    elif datos[73] == 'Negocio':
        can4.drawString(415, 136, "x")
    #mixto
    elif datos[73] == 'Mixto':
        can4.drawString(415, 120, "x")
    #institucional
    elif datos[73] == 'Institución':
        can4.drawString(415, 106, "x")

    print(datos[74])
    if datos[74] == 'Estrato 1':
        can4.drawString(255, 43, "x")
    #2
    elif datos[74] == 'Estrato 2':
        can4.drawString(280, 43, "x")
    #3
    elif datos[74] == 'Estrato 3':
        can4.drawString(305, 43, "x")
    #4
    elif datos[74] == 'Estrato 4':
        can4.drawString(330, 43, "x")
    #5
    elif datos[74] == 'Estrato 5':
        can4.drawString(350, 43, "x")
    #6
    elif datos[74] == 'Estrato 6':
        can4.drawString(375, 43, "x")
    #Nombre de la comunidad
    # can4.drawString(90, 670, datos[103])
    #personas en la comunidad 
    # llenarCampos(can4, 315, 598, datos[116], 30)
    #la vivienda se encuentra ubicada al interior de 
    #caserio
    # if datos[104] == 'Caserío':
    #     can4.drawString(405, 536, "x")
    # #resguardo indigena
    # elif datos[104] == 'Resguardo indígena':
    #     can4.drawString(405, 523, "x")
    # #parcialidad
    # elif datos[104] == 'Parcialidad o asentamiento indígena fuera del resguardo':
    #     can4.drawString(405, 510, "x")
    # #territorio colectivo
    # elif datos[104] == 'Territorio colectivo de comunidad negra':
    #     can4.drawString(405, 497, "x")
    # #territorio de comunidad
    # elif datos[104] == 'Territorio de comunidad negra no titulada':
    #     can4.drawString(405, 484, "x")
    # #territorio ancestral
    # elif datos[104] == 'Territorio ancestral raizal del Archipiélago de San Andrés, Providencia y Santa Catalina':
    #     can4.drawString(405, 471, "x")
    # #reancheria
    # elif datos[104] == 'Ranchería - Guajira':
    #     can4.drawString(405, 458, "x")
    # #territorio palenquero
    # elif datos[104] == 'Territorio Palenquero de San Basilio':
    #     can4.drawString(405, 445, "x")
    # #territorio gitano
    # elif datos[104] == 'Territorio Gitano - ROM':
    #     can4.drawString(405, 432, "x")
    # #zona rural
    # elif datos[104] == 'Zona rural':
    #     can4.drawString(405, 419, "x")
    # #tenencia de la vivenda
    # if datos[105] == 'Propia':
    #     can4.drawString(350, 351, "x")
    # elif datos[105] == 'Arriendo':
    #     can4.drawString(350, 339, "x")
    # elif datos[105] == 'Colectiva':
    #     can4.drawString(350, 327, "x")
    # hogares en la vivienda
    # llenarCampos(can4, 342, 267 , datos[106], 30)
    #personas en la vivienda
    # llenarCampos(can4, 342, 222 , datos[107], 30)
    #material predominante en la vivienda
    #bloque
    # if datos[108] == 'Bloque, ladrillo, piedra, madera pulida':
    #     can4.drawString(420, 152, "x")
    # #concreto
    # elif datos[108] == 'Concreto':
    #     can4.drawString(420, 140, "x")
    # #tapia
    # elif datos[108] == 'Tapia pisada, bahareque, adobe':
    #     can4.drawString(420, 128, "x")
    # #madera
    # elif datos[108] == 'Madera burda, tabla, tablón':
    #     can4.drawString(420, 116, "x")
    # #prefabricado
    # elif datos[108] == 'Material prefabricado':
    #     can4.drawString(420, 104, "x")
    # #guadua
    # elif datos[108] == 'Guadua, caña, esterilla, otros vegetales':
    #     can4.drawString(420, 92, "x")
    # #desechos
    # elif datos[108] == 'Materiales de desecho (zinc, tela, cartón, latas, plásticos, otros)':
    #     can4.drawString(420, 80, "x")
    # #no tiene
    # elif datos[108] == 'No tiene paredes':
    #     can4.drawString(420, 68, "x")
    can4.save()
    #hoja 5 del pdf
    packet5 = io.BytesIO()
    # create a new PDF with Reportlab
    can5 = canvas.Canvas(packet5, pagesize=A4)
    can5.setFont("Helvetica", 9)

    can5.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can5, 396, 786, datos[4],10)# Dia
    llenarCampos(can5, 435, 786, datos[5],10)# Mes
    llenarCampos(can5, 485, 786, datos[6],10)# Año

    #Nombre de la comunidad
    can5.drawString(90, 712, datos[103])

        #personas en la comunidad 
    llenarCampos(can5, 260, 648, datos[116], 30)


    #caserio
    if datos[104] == 'Caserío':
        can5.drawString(405, 586, "x")
    #resguardo indigena
    elif datos[104] == 'Resguardo indígena':
        can5.drawString(405, 573, "x")
    #parcialidad
    elif datos[104] == 'Parcialidad o asentamiento indígena fuera del resguardo':
        can5.drawString(405, 558, "x")
    #territorio colectivo
    elif datos[104] == 'Territorio colectivo de comunidad negra':
        can5.drawString(405, 548, "x")
    #territorio de comunidad
    elif datos[104] == 'Territorio de comunidad negra no titulada':
        can5.drawString(405, 534, "x")
    #territorio ancestral
    elif datos[104] == 'Territorio ancestral raizal del Archipiélago de San Andrés, Providencia y Santa Catalina':
        can5.drawString(405, 520, "x")
    #reancheria
    elif datos[104] == 'Ranchería - Guajira':
        can5.drawString(405, 506, "x")
    #territorio palenquero
    elif datos[104] == 'Territorio Palenquero de San Basilio':
        can5.drawString(405, 490, "x")
    #territorio gitano
    elif datos[104] == 'Territorio Gitano - ROM':
        can5.drawString(405, 478, "x")
    #zona rural
    elif datos[104] == 'Zona rural':
        can5.drawString(405, 466, "x")
    #tenencia de la vivenda
    if datos[105] == 'Propia':
        can5.drawString(350, 410, "x")
    elif datos[105] == 'Arriendo':
        can5.drawString(350, 396, "x")
    elif datos[105] == 'Colectiva':
        can5.drawString(350, 382, "x")

            # hogares en la vivienda
    llenarCampos(can5, 342, 325, datos[106], 30)

        #personas en la vivienda
    llenarCampos(can5, 342, 280 , datos[107], 30)

        #bloque
    if datos[108] == 'Bloque, ladrillo, piedra, madera pulida':
        can5.drawString(420, 230, "x")
    #concreto
    elif datos[108] == 'Concreto':
        can5.drawString(420, 218, "x")
    #tapia
    elif datos[108] == 'Tapia pisada, bahareque, adobe':
        can5.drawString(420, 202, "x")
    #madera
    elif datos[108] == 'Madera burda, tabla, tablón':
        can5.drawString(420, 188, "x")
    #prefabricado
    elif datos[108] == 'Material prefabricado':
        can5.drawString(420, 176, "x")
    #guadua
    elif datos[108] == 'Guadua, caña, esterilla, otros vegetales':
        can5.drawString(420, 165, "x")
    #desechos
    elif datos[108] == 'Materiales de desecho (zinc, tela, cartón, latas, plásticos, otros)':
        can5.drawString(420, 154, "x")
    #no tiee
    elif datos[108] == 'No tiene paredes':
        can5.drawString(420, 142, "x")

    if datos[109] == 'Paja, palma y otros vegetales':
        can5.drawString(420, 85, "x")
    elif datos[109] == 'Plancha de cemento, concreto y hormigón':
        can5.drawString(420, 73, "x")
    elif datos[109] == 'Tejas (barro, asbesto - cemento, metálica o lámina de zinc, plástica)': 
        can5.drawString(420, 58, "x")
    elif datos[109] == 'Material de desecho (tela, cartón, latas, plástico, otros)':    
        can5.drawString(420, 30, "x")


    # #vivienda ha sido afectada
    # if datos[111] == 'Si':
    #     can5.drawString(385, 523, "x")
    # else:
    #     can5.drawString(432, 523, "x")
    # if datos[112] == 'Si':
    #     can5.drawString(385, 511, "x")
    # else:
    #     can5.drawString(432, 511, "x")
    # if datos[113] == 'Si':
    #     can5.drawString(385, 499, "x")
    # else:
    #     can5.drawString(432, 499, "x")
    # if datos[114] == 'Si':
    #     can5.drawString(385, 487, "x")
    # else:
    #     can5.drawString(432, 487, "x")
    # if datos[114] == 'Si':
    #     can5.drawString(385, 475, "x")
    # else:
    #     can5.drawString(432, 475, "x")
    # #area de construccion
    # llenarCampos(can5, 300, 417, datos[115],30)
    # #la vivienda cuenta con servicios
    # if datos[284] == 'true':
    #     can5.drawString(400, 304, "x")
    # if datos[285] == 'true':
    #     can5.drawString(400, 292, "x")
    # if datos[286] == 'true':
    #     can5.drawString(400, 280, "x")
    # if datos[287] == 'true':
    #     can5.drawString(400, 268, "x")
    # if datos[288] == 'true':
    #     can5.drawString(400, 256, "x")
    # if datos[289] == 'true':    
    #     can5.drawString(400, 244, "x")
    # #obtencion de agua
    # if datos[291] == 'true':
    #     can5.drawString(295, 167, "x")
    # if datos[292] == 'true':
    #     can5.drawString(295, 153, "x")
    # if datos[293] == 'true':
    #     can5.drawString(295, 141, "x")
    # if datos[294] == 'true':
    #     can5.drawString(295, 129, "x")
    # if datos[295] == 'true':
    #     can5.drawString(295, 117, "x")
    # if datos[296] == 'true':
    #     can5.drawString(295, 105, "x")
    # if datos[297] == 'true':
    #     can5.drawString(295, 93, "x")
    # if datos[298] == 'true':
    #     can5.drawString(295, 81, "x")
    # #tiene medidor de agua
    # if datos[290] == 'true':
    #     can5.drawString(465, 167, "x")
    # else:
    #     can5.drawString(500, 167, "x")
    can5.save()
    #hoja 6 del pdf
    packet6 = io.BytesIO()
    # create a new PDF with Reportlab
    can6 = canvas.Canvas(packet6, pagesize=A4)
    can6.setFont("Helvetica", 9)

    can6.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can6, 396, 786, datos[4],10)# Dia
    llenarCampos(can6, 435, 786, datos[5],10)# Mes
    llenarCampos(can6, 485, 786, datos[6],10)# Año


        #material predominante en piso
    if datos[110] == 'Alfombra o tapete de pared a pared':
        can6.drawString(410, 726, "x")
    if datos[110] == 'Mármol, parqué, madera pulida y lacada':
        can6.drawString(410, 716, "x")
    if datos[110] == 'Baldosa, vinilo, tableta, ladrillo, laminado':
        can6.drawString(410, 704, "x")
    if datos[110] == 'Cemento, gravilla':
        can6.drawString(410, 555, "x")
    if datos[110] == 'Madera burda, tabla, tablón, otro vegetal':
        can6.drawString(410, 682, "x")
    if datos[110] == 'Tierra, arena, barro':
        can6.drawString(410, 670, "x")

    # #vivienda ha sido afectada
    if datos[111] == 'Si':
        can6.drawString(385, 623, "x")
    else:
        can6.drawString(432, 623, "x")
    if datos[112] == 'Si':
        can6.drawString(385, 611, "x")
    else:
        can6.drawString(432, 611, "x")
    if datos[113] == 'Si':
        can6.drawString(385, 599, "x")
    else:
        can6.drawString(432, 599, "x")
    if datos[114] == 'Si':
        can6.drawString(385, 587, "x")
    else:
        can6.drawString(432, 587, "x")

        #area de construccion
    llenarCampos(can6, 320, 536, datos[115],30)
    #la vivienda cuenta con servicios
    if datos[284] == 'true':
        can6.drawString(400, 446, "x")
    if datos[285] == 'true':
        can6.drawString(400, 435, "x")
    if datos[286] == 'true':
        can6.drawString(400, 422, "x")
    if datos[287] == 'true':
        can6.drawString(400, 409, "x")
    if datos[288] == 'true':
        can6.drawString(400, 398, "x")
    if datos[289] == 'true':    
        can6.drawString(400, 390, "x")

    #obtencion de agua
    if datos[291] == 'true':
        can6.drawString(295, 318, "x")
    if datos[292] == 'true':
        can6.drawString(295, 308, "x")
    if datos[293] == 'true':
        can6.drawString(295, 292, "x")
    if datos[294] == 'true':
        can6.drawString(295, 286, "x")
    if datos[295] == 'true':
        can6.drawString(295, 276, "x")
    if datos[296] == 'true':
        can6.drawString(295, 260, "x")
    if datos[297] == 'true':
        can6.drawString(295, 246, "x")
    if datos[298] == 'true':
        can6.drawString(295, 230, "x")
    #tiene medidor de agua
    if datos[290] == 'true':
        can6.drawString(465, 318, "x")
    else:
        can6.drawString(500, 318, "x")

    #Servicio sanitario
    print('sanitariop', datos[299])
    if datos[299] == 'true':
        can6.drawString(400, 172, "x")
    if datos[300] == 'true':
        can6.drawString(400, 160, "x")
    if datos[301] == 'true':
        can6.drawString(400, 154, "x")
    if datos[302] == 'true':
        can6.drawString(400, 138, "x")
    if datos[303] == 'true':
        can6.drawString(400, 126, "x")
    if datos[304] == 'true':
        can6.drawString(230, 248, datos[304])
        can6.drawString(400, 112, "x")
    # tiene acceso a gas
    if datos[305] == 'Pipeta / Cilindro':
        can6.drawString(320, 66, "x")
    elif datos[305] == 'Gasoducto':
        can6.drawString(320, 58, "x")
    elif datos[305] == 'No tiene servicio de gas':
        can6.drawString(320, 38, "x")
    #tiene acceso al agua
    # if datos[312] == 'Si':
    #     can6.drawString(320, 68, "x")
    # elif datos[312] == 'No':
    #     can6.drawString(320, 54, "x")
    # #que cantidad de agua puede obtener
    # can6.drawString(100, 430, datos[313])
    # #promedio cantidad de agua
    # can6.drawString(400, 395, datos[314])
    # #fuente principal de abastesimiento de agua
    # if datos[315] == 'Jagüey':
    #     can6.drawString(400, 313, "x")
    # elif datos[315] == 'Pozo':
    #     can6.drawString(400, 301, "x")
    # elif datos[315] == 'Molino':
    #     can6.drawString(400, 289, "x")
    # elif datos[315] == 'Carrotanques':
    #     can6.drawString(400, 277, "x")
    # elif datos[315] == 'Aguas lluvias':
    #     can6.drawString(400, 265, "x")
    # elif datos[315] == 'Ríos':
    #     can6.drawString(400, 253, "x")
    # elif datos[315] == 'Arroyos':
    #     can6.drawString(400, 241, "x")
    # elif datos[315] == 'Quebradas':
    #     can6.drawString(400, 228, "x")
    # elif datos[315] == 'Otro':
    #     can6.drawString(400, 216, "x")
    # #la casimba es comunitaria
    # if datos[319] == 'Si':
    #     can6.drawString(320, 147, "x")
    # elif datos[319] == 'No':    
    #     can6.drawString(320, 135, "x")
    # #cual
    # can6.drawString(120, 110, datos[318])
    can6.save()
    #hoja 7 del pdf
    packet7 = io.BytesIO()
    # create a new PDF with Reportlab
    can7 = canvas.Canvas(packet7, pagesize=A4)
    can7.setFont("Helvetica", 9)

    can7.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can7, 396, 786, datos[4],10)# Dia
    llenarCampos(can7, 435, 786, datos[5],10)# Mes
    llenarCampos(can7, 485, 786, datos[6],10)# Año

        #tiene acceso al agua
    if datos[312] == 'Si':
        can7.drawString(320, 702, "x")
    elif datos[312] == 'No':
        can7.drawString(372, 702, "x")


    if datos[313] == "1-10":
        can7.drawString(395,636, "x")
    elif datos[313] == "11-20":
        can7.drawString(395,624, "x")
    elif datos[313] == "21-25":
        can7.drawString(395,612, "x")
    elif datos[313] == "25":
        can7.drawString(395,602, "x")


    #fuente principal de abastesimiento de agua
    if datos[315] == 'Jagüey':
        can7.drawString(395, 540, "x")


    elif datos[315] == 'Pozo':
        can7.drawString(395, 531, "x")
    elif datos[315] == 'Molino':
        can7.drawString(395, 519, "x")
    elif datos[315] == 'Carrotanques':
        can7.drawString(395, 507, "x")
    elif datos[315] == 'Aguas lluvias':
        can7.drawString(395, 495, "x")
    elif datos[315] == 'Ríos':
        can7.drawString(395, 483, "x")
    elif datos[315] == 'Arroyos':
        can7.drawString(395, 471, "x")
    elif datos[315] == 'Quebradas':
        can7.drawString(395, 458, "x")
    elif datos[315] == 'Otro':
        can7.drawString(395, 442, "x")


    if datos[317] == 'Si':
        can7.drawString(290, 372, "x")
    elif datos[317] == 'No':
        can7.drawString(290, 352, "x")

  #cual
    can7.drawString(262,  330, datos[319])

    can7.drawString(280,  300, datos[320])

    can7.drawString(280,  270, datos[322])
        # #cuanto dura el agua que recolect
    if datos[323]== "null":
        can7.drawString(330, 240, " ")
    elif datos[323]== "1":
        can7.drawString(330, 240, "Menos de 1 hora")
    elif datos[323]== "1-3":
        can7.drawString(330, 240, '1 a 3 horas')
    elif datos[323]== "4-6":
        can7.drawString(330, 240, '4 a 6 horas')
    elif datos[323]== "7-9":
        can7.drawString(330, 240, '7 a 9 horas')
    elif datos[323]== "No sabe":
        can7.drawString(330, 240, datos[323])
    
        # #cantidad destinada higiene
    if datos[324] == "null":
        can7.drawString(410, 210, " ")
    elif datos[324] == "50":
        can7.drawString(410, 210, "Más de 50 litros")
    else:
        can7.drawString(410, 210, datos[324]+" litros")

    if datos[325] =="null":
        can7.drawString(300, 183, " ")
    elif datos[325] == "-1":
        can7.drawString(300, 183,'Menos de 1 km')
    else:
        can7.drawString(300, 183,datos[325]+" Kílotmetro")

    if datos[326] =="null":
        can7.drawString(100, 147, " ")
    elif datos[326] == "7":
        can7.drawString(100, 147,'Más de 7 horas')
    elif datos[326] == "No sabe":
        can7.drawString(100, 147,datos[326])
    else:
        can7.drawString(100, 147,datos[326]+" horas")

    if datos[327] == "null":
        can7.drawString(380, 116," ")
    else:
        can7.drawString(380, 116,datos[327])

    can7.drawString(340, 90,datos[329])

    can7.drawString(320, 60,datos[334])
    print (datos[335])
    if datos[335] == "None" or datos[335] == None:
        can7.drawString(300, 30, " ")
    else:
        can7.drawString(300, 30,datos[335])
     #uso del agua que obtienen
    # usosAgua = datos[320].split(',')  
    # if 'Cocinar' in usosAgua:
    #     can7.drawString(405, 744, "x")
    # if 'Higiene' in usosAgua:
    #     can7.drawString(405, 732, "x")
    # if 'Actividades agropecuarias' in usosAgua:
    #     can7.drawString(405, 720, "x")
    # if 'Actividades de ganadería' in usosAgua:
    #     can7.drawString(405, 708, "x")
    # if 'Otro' in usosAgua:
    #     can7.drawString(405, 696, "x")
    # # va al puesto de agua todos los dias
    # if datos[322] == 'Si':
    #     can7.drawString(320, 626, "x")
    # elif datos[322] == 'No':
    #     can7.drawString(320, 614, "x")
    # else:
    #     can7.drawString(320, 602, "x")
    # #cuanto dura el agua que recolecta
    # can7.drawString(300, 573, datos[323])
    # #cantidad destinada higiene
    # can7.drawString(100, 528, datos[324])
    # #distancia para obtener agua
    # can7.drawString(300, 495, datos[325])
    # #ti3mpo destina a la recoleccion de agua
    # can7.drawString(100, 450, datos[326])
    # #medio de transporte para el agua
    # if datos[327] == 'Moto':
    #     can7.drawString(405, 377, "x")
    # elif datos[327] == 'Transporte animal':    
    #     can7.drawString(405, 365, "x")
    # elif datos[327] == 'Caminando':
    #     can7.drawString(405, 353, "x")
    # elif datos[327] == 'Bicicleta':
    #     can7.drawString(405, 341, "x")
    # elif datos[327] == 'Otro':
    #     can7.drawString(405, 329, "x")
    #     can7.drawString(250, 329, datos[328])
    # #adquiere agua de otra fuente
    # if datos[329] == 'Si':
    #     can7.drawString(320, 260, "x")
    # elif datos[329] == 'No':
    #     can7.drawString(320, 248, "x")
    # #cuanta agua adquiere de esa fuente
    # can7.drawString(360, 220, datos[330])
    # #cual es la otra fuente
    # if datos[331] == 'Galón/pimpina':
    #     can7.drawString(405, 145, "x")
    # elif datos[331] == 'Carrotanque':
    #     can7.drawString(405, 134, "x")
    # elif datos[331] == 'Botellón':
    #     can7.drawString(405, 122, "x")
    # elif datos[331] == 'Pozo':
    #     can7.drawString(405, 111, "x")
    can7.save()
    #hoja 8 del pdf
    packet8 = io.BytesIO()
    # create a new PDF with Reportlab
    can8 = canvas.Canvas(packet8, pagesize=A4)
    can8.setFont("Helvetica", 9)

    can8.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can8, 396, 786, datos[4],10)# Dia
    llenarCampos(can8, 435, 786, datos[5],10)# Mes
    llenarCampos(can8, 485, 786, datos[6],10)# Año

    can8.drawString(110, 758, datos[336]);

    if datos[337] == "None" or datos[337] == None:
       can8.drawString(320, 720, " ")
    else:
        can8.drawString(320, 720, datos[337]);
    # can8.drawString(320, 720, datos[337]);
    if datos[338] == "None" or datos[338] == None:
        can8.drawString(438, 695," ")
    else:
        can8.drawString(438, 695, datos[338]);
    # can8.drawString(438, 695, datos[338]);
    if datos[339] == "None" or datos[339] == None:
        can8.drawString(356, 651," ")
    else:
        can8.drawString(356, 651, datos[339]);
    # can8.drawString(356, 651, datos[339]);

    can8.drawString(360, 625, datos[340]);

    can8.drawString(360, 595, datos[341]);

    can8.drawString(360, 567, datos[342]);

    can8.drawString(378, 540, datos[343]);

    can8.drawString(380, 505, datos[344]);
    
    can8.drawString(360, 478, datos[346]);

    can8.drawString(385, 450, datos[348]);

    can8.drawString(340, 423, datos[350]);

    can8.drawString(360, 390, datos[351]);

    can8.drawString(360, 365, datos[352]);
    
    if datos[13] == "None" or datos[13] == None:
         can8.drawString(97 , 204," ")
    else:
        familia = (json.loads(datos[13]))
        for i in range(len(familia)):
            integrante = dict(familia[i])
            if integrante['Parentesco'] == 'Jefe (a) de hogar':
                can8.drawString(97 , 204, 'x')
                can8.drawString(195, 204, integrante['Genero'])
                can8.drawString(244, 204, str(integrante['Edad']))
                can8.drawString(288, 204, integrante['Registro'])
                can8.drawString(324, 204, integrante['Escolaridad'])
                can8.drawString(434, 204, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Pareja, Esposo(a), cónyuge, compañero(a)':
                can8.drawString(97 , 185, 'x')
                can8.drawString(195, 185, integrante['Genero'])
                can8.drawString(244, 185, str(integrante['Edad']))
                can8.drawString(288, 185, integrante['Registro'])
                can8.drawString(324, 185, integrante['Escolaridad'])
                can8.drawString(434, 185, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)':
                can8.drawString(97 , 171, 'x')
                can8.drawString(195, 171, integrante['Genero'])
                can8.drawString(244, 171, str(integrante['Edad']))
                can8.drawString(288, 171, integrante['Registro'])
                can8.drawString(324, 171, integrante['Escolaridad'])
                can8.drawString(434, 171, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 2':
                can8.drawString(97 , 159, 'x')
                can8.drawString(195, 159, integrante['Genero'])
                can8.drawString(244, 159, str(integrante['Edad']))
                can8.drawString(288, 159, integrante['Registro'])
                can8.drawString(324, 159, integrante['Escolaridad'])
                can8.drawString(434, 159, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 3':
                can8.drawString(97 , 147, 'x')
                can8.drawString(195, 147, integrante['Genero'])
                can8.drawString(244, 147, str(integrante['Edad']))
                can8.drawString(288, 147, integrante['Registro'])
                can8.drawString(324, 147, integrante['Escolaridad'])
                can8.drawString(434, 147, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 4':
                can8.drawString(97 , 132, 'x')
                can8.drawString(195, 132, integrante['Genero'])
                can8.drawString(244, 132, str(integrante['Edad']))
                can8.drawString(288, 132, integrante['Registro'])
                can8.drawString(324, 132, integrante['Escolaridad'])
                can8.drawString(434, 132, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 5':
                can8.drawString(97 , 119, 'x')
                can8.drawString(195, 119, integrante['Genero'])
                can8.drawString(244, 119, str(integrante['Edad']))
                can8.drawString(288, 119, integrante['Registro'])
                can8.drawString(324, 119, integrante['Escolaridad'])
                can8.drawString(434, 119, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Nieto(a)':
                can8.drawString(97 , 106, 'x')
                can8.drawString(195, 106, integrante['Genero'])
                can8.drawString(244, 106, str(integrante['Edad']))
                can8.drawString(288, 106, integrante['Registro'])
                can8.drawString(324, 106, integrante['Escolaridad'])
                can8.drawString(434, 106, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Suegro(a)':
                can8.drawString(97 , 94, 'x')
                can8.drawString(195, 94, integrante['Genero'])
                can8.drawString(244, 94, str(integrante['Edad']))
                can8.drawString(288, 94, integrante['Registro'])
                can8.drawString(324, 94, integrante['Escolaridad'])
                can8.drawString(434, 94, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Tios(as)':
                can8.drawString(97 , 81, 'x')
                can8.drawString(195, 81, integrante['Genero'])
                can8.drawString(244, 81, str(integrante['Edad']))
                can8.drawString(288, 81, integrante['Registro'])
                can8.drawString(324, 81, integrante['Escolaridad'])
                can8.drawString(434, 81, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Yerno, nuera':
                can8.drawString(97 , 69, 'x')
                can8.drawString(195, 69, integrante['Genero'])
                can8.drawString(244, 69, str(integrante['Edad']))
                can8.drawString(288, 69, integrante['Registro'])
                can8.drawString(324, 69, integrante['Escolaridad'])
                can8.drawString(434, 69, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Otro (a) pariente del (de la) jefe (a)':
                can8.drawString(97 , 53, 'x')
                can8.drawString(195, 53, integrante['Genero'])
                can8.drawString(244, 53, str(integrante['Edad']))
                can8.drawString(288, 53, integrante['Registro'])
                can8.drawString(324, 53, integrante['Escolaridad'])
                can8.drawString(434, 53, integrante['Ocupacion'])
            elif integrante['Parentesco'] == 'Otro (a) no pariente':
                can8.drawString(97 , 39, 'x')
                can8.drawString(195, 39, integrante['Genero'])
                can8.drawString(244, 39, str(integrante['Edad']))
                can8.drawString(288, 39, integrante['Registro'])
                can8.drawString(324, 39, integrante['Escolaridad'])
                can8.drawString(434, 39, integrante['Ocupacion'])
            elif integrante['Parentesco'] == " " or integrante['Parentesco'] == None:
                can8.drawString(97 , 39, " ")
                can8.drawString(195, 39, " ")
                can8.drawString(244, 39, " ")
                can8.drawString(288, 39, " ")
                can8.drawString(324, 39, " ")
                can8.drawString(434, 39, " ")
    # if datos[332] == 'Si':
    #     can8.drawString(320, 743, 'x')
    # elif datos[332] == 'No':
    #     can8.drawString(320, 730, 'x')
    # #cuanto debe pagar
    # can8.drawString(200, 712, datos[333])
    # #tratamiento del agua
    # if datos[334] == 'Filtrarla':
    #     can8.drawString(404,637,'x')
    # elif datos[334] == 'Calentarla':
    #     can8.drawString(404,625,'x')
    # elif datos[334] == 'Pastillas de Cloro':
    #     can8.drawString(404,613,'x')
    # elif datos[334] == 'Ninguno':
    #     can8.drawString(404,601,'x')
    # elif datos[334] == 'Otro':
    #     can8.drawString(404,591,'x')
    #     can8.drawString(250,589,datos[335])
    # #espacio de almacenamiento de agua
    # if datos[336] == 'Si':
    #     can8.drawString(320, 510, 'x')
    # elif datos[336] == 'No':
    #     can8.drawString(320, 498, 'x')
    # #capacidad promedio
    # can8.drawString(310, 480, datos[337])
    # #se utilizan los almacenamientos para otras actividades 
    # if datos[338] == 'Si':
    #     can8.drawString(320, 405, 'x')
    # elif datos[338] == 'No':
    #     can8.drawString(320, 393, 'x')
    # #se realizan procedimientos de limpieza
    # if datos[339] == 'Si':
    #     can8.drawString(320, 315, 'x')
    # elif datos[339] == 'No':
    #     can8.drawString(320, 303, 'x')
    # elif datos[339] == 'No sabe':
    #     can8.drawString(320, 291, 'x')
    # #tiene sitio para las basuras
    # if datos[340] == 'Si':
    #     can8.drawString(320, 224, 'x')
    # elif datos[340] == 'No':
    #     can8.drawString(320, 212, 'x')
    # #cuenta con servicio de recoleccion
    # if datos[341] == 'Municipal':
    #     can8.drawString(320, 140, 'x')
    # elif datos[341]== 'Veredal':
    #     can8.drawString(320, 128, 'x')
    # elif datos[341] == 'No Tiene':
    #     can8.drawString(320, 116, 'x')
    can8.save()
    #hoja 9 del pdf
    packet9 = io.BytesIO()
    # create a new PDF with Reportlab
    can9 = canvas.Canvas(packet9, pagesize=A4)
    can9.setFont("Helvetica", 9)

    can9.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can9, 396, 786, datos[4],10)# Dia
    llenarCampos(can9, 435, 786, datos[5],10)# Mes
    llenarCampos(can9, 485, 786, datos[6],10)# Año

    if datos[15] == "Permanente":
        can9.drawString(392,710, "x")
    elif datos[15] == "Temporal":
        can9.drawString(392, 696, "x")


    if datos[317] == 'Si':
        can9.drawString(325, 628, "x")
    elif datos[317] == 'No':
        can9.drawString(372, 628, "x")

    if datos[20]=='Indígena':
        can9.drawString(408, 548, "x")
    elif datos[20]=='Gitano (a)(ROM)':
        can9.drawString(408, 536, "x")
    elif datos[20]=='Raizal de San Andrés, Providencia, Santa Catalina':
        can9.drawString(408, 522, "x")
    elif datos[20]=='Palenquero (a)':
        can9.drawString(408, 510, "x")
    elif datos[20]=='Negro (a), afrodescendiente, afrocolombiano (a)':
        can9.drawString(408, 498, "x")
    elif datos[20]=='Ninguno de los anteriores':   
        can9.drawString(408, 486, "x")

    if datos[22] == 'Si':
        can9.drawString(320, 412, "x")
    elif datos[22] == 'No':
        can9.drawString(320, 400, "x")

    can9.drawString(70, 355, datos[23])

    if datos[24] == 'Si':
        can9.drawString(323, 258, "x")
    elif datos[24] == 'No':
        can9.drawString(368, 258, "x")
    if datos[25] == 'Si':
        can9.drawString(320, 176, "x")
    elif datos[25] == 'No':
        can9.drawString(320, 168, "x")
    #cual organizacion pertenece
    can9.drawString(70, 100, datos[26])
    

    can9.save()
    #hoja 10 del pdf
    packet10 = io.BytesIO()
    # create a new PDF with Reportlab
    can10 = canvas.Canvas(packet10, pagesize=A4)
    can10.setFont("Helvetica", 9)

    can10.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can10, 396, 786, datos[4],10)# Dia
    llenarCampos(can10, 435, 786, datos[5],10)# Mes
    llenarCampos(can10, 485, 786, datos[6],10)# Año

    #domesticas
    if datos[27] == 'true':
        can10.drawString(364, 692, "x")
    if datos[37] == 'true':
        can10.drawString(404, 692, "x")
    if datos[47] == 'true':
        can10.drawString(444, 692, "x")
    if datos[57] == 'true':
        can10.drawString(484, 692, "x")
        #pagos
    if datos[28] == 'true':
        can10.drawString(364, 679, "x")
    if datos[38] == 'true':
        can10.drawString(404, 679, "x")
    if datos[48] == 'true':
        can10.drawString(444, 679, "x")
    if datos[58] == 'true':
        can10.drawString(484, 679, "x")
        #finca
    if datos[29] == 'true':
        can10.drawString(364, 666, "x")
    if datos[39] == 'true':
        can10.drawString(404, 666, "x")
    if datos[49] == 'true':
        can10.drawString(444, 666, "x")
    if datos[59] == 'true':
        can10.drawString(484, 666, "x")
        #Transporte
    if datos[30] == 'true':
        can10.drawString(364, 653, "x")
    if datos[40] == 'true':
        can10.drawString(404, 653, "x")
    if datos[50] == 'true':
        can10.drawString(444, 653, "x")
    if datos[60] == 'true':
        can10.drawString(484, 653, "x")
        #admin finca
    if datos[31] == 'true':
        can10.drawString(364, 640, "x")
    if datos[41] == 'true':
        can10.drawString(404, 640, "x")
    if datos[51] == 'true':
        can10.drawString(444, 640, "x")
    if datos[61] == 'true':
        can10.drawString(484, 640, "x")
        #comercia
    if datos[32] == 'true':
        can10.drawString(364, 627, "x")
    if datos[42] == 'true':
        can10.drawString(404, 627, "x")
    if datos[52] == 'true':
        can10.drawString(444, 627, "x")
    if datos[62] == 'true':
        can10.drawString(484, 627, "x")
        #Estudia
    if datos[33] == 'true':
        can10.drawString(364, 614, "x")
    if datos[43] == 'true':
        can10.drawString(404, 614, "x")
    if datos[53] == 'true':
        can10.drawString(444, 614, "x")
    if datos[63] == 'true':
        can10.drawString(484, 614, "x")
        # fORMACION HIJOS
    if datos[34] == 'true':
        can10.drawString(364, 601, "x")
    if datos[44] == 'true':
        can10.drawString(404, 601, "x")
    if datos[54] == 'true':
        can10.drawString(444, 601, "x")
    if datos[64] == 'true':
        can10.drawString(484, 601, "x")
        #Cuidado adultos
    if datos[35] == 'true':
        can10.drawString(364, 588, "x")
    if datos[45] == 'true':
        can10.drawString(404, 588, "x")
    if datos[55] == 'true':
        can10.drawString(444, 588, "x")
    if datos[65] == 'true':
        can10.drawString(484, 588, "x")
        #Otro
    if datos[36] == 'true':
        can10.drawString(364, 575, "x")
    if datos[46] == 'true':
        can10.drawString(404, 575, "x")
    if datos[56] == 'true':
        can10.drawString(444, 575, "x")
    if datos[66] == 'true':
        can10.drawString(160, 575, "Otro")
        can10.drawString(484, 575, "x")
    #fuentes de ingtreso en l hogar
    if datos[123] == 'true':
        can10.drawString(402, 407, "x")
    if datos[124] == 'true':
        can10.drawString(402, 394, "x")
    if datos[125] == 'true':
        can10.drawString(402, 381, "x")
    if datos[126] == 'true':
        can10.drawString(402, 368, "x")
    if datos[127] == 'true':
        can10.drawString(402, 355, "x")
    if datos[128] == 'true':
        can10.drawString(402, 342, "x")
    if datos[129] == 'true':
        can10.drawString(402, 329, "x")
    if datos[130] == 'true':
        can10.drawString(402, 316, "x")
    if datos[131] == 'true':
        can10.drawString(402, 303, "x")
    if datos[132] == 'true':
        can10.drawString(402, 290, "x")
    if datos[133] == 'true':
        can10.drawString(402, 277, "x")
    if datos[134] == 'true':
        can10.drawString(402, 264, "x")
    if datos[135] == 'true':
        can10.drawString(402, 251, "x")
    if datos[136] == 'true':
        can10.drawString(402, 238, "x")
    if datos[137] == 'true':
        can10.drawString(402, 225, "x")
        can10.drawString(242, 225, datos[137])

    if datos[138] == "null":
        can10.drawString(142, 169, "No registra")
    else:    
        can10.drawString(142, 169, datos[138])
    if datos[139] == "null":
        can10.drawString(142, 156, "No registra")
    else:
        can10.drawString(142, 156, datos[139])  
    if datos[140] == "null":
        can10.drawString(142, 143, "No registra")
    else:
        can10.drawString(142, 143, datos[140])
    if datos[141] == "null":
        can10.drawString(142, 130, "No registra")
    else: 
        can10.drawString(142, 130, datos[141])
        
        

    


    can10.save()
    #hoja 11 del pdf
    packet11 = io.BytesIO()
    # create a new PDF with Reportlab
    can11 = canvas.Canvas(packet11, pagesize=A4)
    can11.setFont("Helvetica", 9)

    can11.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can11, 396, 786, datos[4],10)# Dia
    llenarCampos(can11, 435, 786, datos[5],10)# Mes
    llenarCampos(can11, 485, 786, datos[6],10)# Año


    can11.drawString(350, 710, datos[142])
    can11.drawString(350, 697, datos[143])
    can11.drawString(350, 684, datos[144])
    can11.drawString(350, 671, datos[145])
    can11.drawString(350, 658, datos[146])
    can11.drawString(350, 647, datos[147])
    can11.drawString(350, 635, datos[148])
    can11.drawString(350, 622, datos[149])
    can11.drawString(350, 610, datos[150])
    can11.drawString(350, 596, datos[151])
    can11.drawString(350, 583, datos[152])
    can11.drawString(350, 574, datos[153])
    can11.drawString(242, 562, datos[155])
    can11.drawString(350, 562, datos[154]) 

    if datos[387] == 'Si':
        can11.drawString(320, 440, "x")
    elif datos[387] == 'No':
        can11.drawString(320, 428, "x")

    can11.drawString(340, 390, datos[388])
    can11.drawString(318, 410, datos[389])

    can11.drawString(320, 359, datos[390])
    can11.drawString(280, 342, datos[392])
    can11.drawString(320, 299, datos[393])
    can11.drawString(320, 275, datos[394])
    can11.drawString(320, 246, datos[395])
    can11.drawString(320, 218, datos[396])




    can11.save()
    #hoja 12 del pdf
    packet12 = io.BytesIO()
    # create a new PDF with Reportlab
    can12 = canvas.Canvas(packet12, pagesize=A4)
    can12.setFont("Helvetica", 9)

    can12.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can12, 396, 786, datos[4],10)# Dia
    llenarCampos(can12, 435, 786, datos[5],10)# Mes
    llenarCampos(can12, 485, 786, datos[6],10)# Año 
    #nombre

    can12.drawString(110, 670, datos[81])

    can12.drawString(110, 595, datos[81])
    #telefono c
    can12.drawString(310, 602, datos[83])
    #telefono f
    if datos[84] == "None" or datos[84] == None:
        can12.drawString(310, 575," ")
    else:
        can12.drawString(310, 575, datos[84])
    
    #correo 
    if datos[86] == "None" or datos[86] == None:
        can12.drawString(310, 555," ")
    else:
        can12.drawString(310, 555, datos[86])
    
    # No ID
    can12.drawString(110, 546, datos[85])
    can12.drawString(310, 138, datos[85])
    # firma

    if datos[87] == "true" :
        can12.drawString(420, 425, "x")
    else :
        can12.drawString(485, 425, "x")

    if datos[88] == "true" :
        can12.drawString(420, 405, "x")
    else :
        can12.drawString(485, 405, "x")
 
    if datos[89] == "true" :
        can12.drawString(420, 375, "x")
    else :
        can12.drawString(485, 375, "x")

    if datos[90] == "true" :
        can12.drawString(420, 350, "x")
    else :
        can12.drawString(485, 350, "x")

    if datos[91] == "true" :
        can12.drawString(420, 324, "x")
    else :
        can12.drawString(485, 324, "x")

    #firmaaa
    with bd.cursor() as cursor:
              cursor.execute("Select rutaserver from aes2021.Fotos_firma where Id_Encuesta = '"+id+"';")
              datos2 = cursor.fetchone()
    urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos2[0],"ejemplo.jpg")
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

    can12.drawImage('new.png', 75, 135, 200, 99)
    can12.drawImage('blanco.JPG', 69, 10, 458, 20)

    can12.save()
    packet13 = io.BytesIO()
    # create a new PDF with Reportlab
    can13 = canvas.Canvas(packet13, pagesize=A4)
    can13.setFont("Helvetica", 9)

    can13.drawString(403, 802, datos[3])# num Formulario
    llenarCampos(can13, 396, 778, datos[4],10)# Dia
    llenarCampos(can13, 435, 778, datos[5],10)# Mes
    llenarCampos(can13, 485, 778, datos[6],10)# Año 

    can13.drawString(110, 700, datos[401])
    can13.drawString(340, 725, datos[408])

    can13.drawString(340, 689, datos[409])
    can13.drawString(110, 650, datos[410])
    can13.drawString(340, 650, datos[411])

    if datos[95] == "Propositivo" :
        can13.drawString(325, 586, "x")
    elif datos[95] == "Reactivo " :
        can13.drawString(325, 572, "x")

    if datos[96] == "Desconfiado" :
        can13.drawString(325, 515, "x")
    elif datos[96] == "Motivado" :
        can13.drawString(325, 502, "x")
    elif datos[96] == "Indiferente" :
        can13.drawString(325, 490, "x")

    can13.drawString(100, 450, datos[94])    

    can13.save()



    #move to the beginning of the StringIO buffer
    packet.seek(0)
    packet2.seek(0)
    packet3.seek(0)
    packet4.seek(0)
    packet5.seek(0)
    packet6.seek(0)
    packet7.seek(0)
    packet8.seek(0)
    packet9.seek(0)
    packet10.seek(0)
    packet11.seek(0)
    packet12.seek(0)
    packet13.seek(0)
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

    # read your existing PDF
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-1.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-2.pdf", "rb"))
    existing_pdf3 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-3.pdf", "rb"))
    existing_pdf4 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-4.pdf", "rb"))
    existing_pdf5 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-5.pdf", "rb"))
    existing_pdf6 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-6.pdf", "rb"))
    existing_pdf7 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-7-2.pdf", "rb"))
    existing_pdf8 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-8-2.pdf", "rb"))
    existing_pdf9 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-9.pdf", "rb"))
    existing_pdf10 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-10.pdf", "rb"))
    existing_pdf11 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-11.pdf", "rb"))
    existing_pdf12 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-12.pdf", "rb"))
    existing_pdf13 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-13-1.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
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
    os.mkdir('pdfs/'+id)
    outputStream = open("pdfs/"+id+"/"+id+"-replanteo.pdf", "wb")
    output.write(outputStream)
    outputStream.close()






# def generarPdfId(id):
#     bd = obtener_conexion()
#     with bd.cursor() as cursor:
#               cursor.execute("SELECT A.*,B.*,C.*,D.*,E.*,F.*,G.*,H.*,I.*,J.*,K.*,M.*, N.* FROM suncosurvey.encabezado A INNER JOIN suncosurvey.c_sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN suncosurvey.caracteristicas_predio C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN suncosurvey.consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN suncosurvey.datos_vivienda_I E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN suncosurvey.economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN suncosurvey.energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN suncosurvey.servicios_publicos H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN suncosurvey.tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN suncosurvey.ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN suncosurvey.URE K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN suncosurvey.proyectos_funcionarios L ON A.Id_Proyecto_Funcionario = L.Id_Proyecto_Funcionario INNER JOIN suncosurvey.funcionarios M ON M.Id_Funcionario = L.Id_Funcionario INNER JOIN suncosurvey.agua N ON A.Id_Encuesta = N.Id_Encuesta WHERE A.isdelete = 0 AND A.Id_Encuesta = '"+id+"';")
#               datos = cursor.fetchone()
#     print(id)
#     packet = io.BytesIO()
#     # create a new PDF with Reportlab
#     can = canvas.Canvas(packet, pagesize=A4)
#     #pagina 1
#     can.setFont("Helvetica", 8)
#     #numero de formulario 
#     can.drawString(410, 802, datos[3])
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can, 398, 790, dia, 10)
#     #mes
#     llenarCampos(can, 440, 790, '04', 10)
#     #anio
#     llenarCampos(can, 488, 790, '2022', 10)
#     can.drawImage('encabezadoPP.JPG', 69, 725, 458, 60)
#     can.drawImage('blanco.JPG', 69, 660, 458, 20)
#     # coordenadas  latitud
#     latitudUnidad = datos[323].split('.')[0]
#     latitudDecimales = datos[323].split('.')[1]
#     can.drawString(220, 396, latitudUnidad)
#     llenarCampos(can, 265, 396, latitudDecimales, 24)
#     # coordenadas  longitud
#     longitudUnidad = datos[324].split('.')[0]
#     longitudDecimales = datos[324].split('.')[1]
#     can.drawString(205, 359, longitudUnidad)
#     llenarCampos(can, 265, 359, longitudDecimales, 24)
#     # coordenadas  altitud
#     if datos[325] == 'null':
#         altitud = '-'
#     else:
#         altitud = round(float(datos[325]))
#     llenarCampos(can, 205, 322, str(altitud), 30)
#     #nombre departamento
#     llenarCampos(can, 128, 255, datos[326], 16)
#     #codigo departamento
#     llenarCampos(can, 128, 228, datos[327], 16)
#     #nombre municipio
#     llenarCampos(can, 128, 205, datos[328], 16)
#     #codigo municipio
#     llenarCampos(can, 128, 175, datos[329], 16)    
#     #nombre vereda
#     llenarCampos(can, 128, 155, datos[330], 16)  
#     #nombre corregimiento
#     llenarCampos(can, 128, 127, datos[331], 16)
#     can.save()
#     #pagina2
#     packet2 = io.BytesIO()
#     # create a new PDF with Reportlab
#     can2 = canvas.Canvas(packet2, pagesize=A4)
#     can2.setFont("Helvetica", 8)
#     can2.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #numero de formulario 
#     can2.drawString(410, 815, datos[3])
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can2, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can2, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can2, 488, 800, '2022', 10)
#     #autoriza la encuesta
#     if datos[312] == 'Si':
#         can2.drawString(315, 722, "X")
#     else:
#         can2.drawString(315, 710, "X")
#     #uso de vivienda
#     if datos[316] == 'Permanente': 
#         can2.drawString(320, 633, "X")
#     elif datos[316] == 'Temporal':
#         can2.drawString(320, 620, "X")
#     #cuenta con energia elcetrica
#     if datos[162] == 'Si': 
#         can2.drawString(320, 368, "X")
#     elif datos[162] == 'No':
#         can2.drawString(370, 368, "X")
#     #que fuente utiliza
#     can2.drawString(335, 290, datos[163])
#     can2.drawString(450, 290, datos[174])
#     can2.drawString(335, 276, datos[164])
#     can2.drawString(450, 276, datos[175])
#     can2.drawString(335, 264, datos[165])
#     can2.drawString(450, 264, datos[176])
#     can2.drawString(335, 250, datos[166])
#     can2.drawString(450, 250, datos[177])
#     can2.drawString(335, 238, datos[167])
#     can2.drawString(450, 238, datos[178])
#     can2.drawString(335, 226, datos[168])
#     can2.drawString(450, 226, datos[179])
#     can2.drawString(335, 214, datos[169])
#     can2.drawString(450, 214, datos[180])
#     can2.drawString(335, 202, datos[170])
#     can2.drawString(450, 202, datos[181])
#     can2.drawString(335, 190, datos[171])
#     can2.drawString(450, 190, datos[182])
#     can2.drawString(335, 178, datos[172])
#     can2.drawString(450, 178, datos[183])
#     can2.drawString(335, 164, datos[173])
#     can2.drawString(450, 164, datos[184])
#     #cuantas horas utiliza para cocinar
#     if datos[187] == None:
#         can2.drawString(350, 140, '-')
#     else:
#         can2.drawString(350, 140, datos[187])

#     can2.save()
#     packet3 = io.BytesIO()
#     # create a new PDF with Reportlab
#     can3 = canvas.Canvas(packet3, pagesize=A4)
#     can3.setFont("Helvetica", 8)
#     can3.drawString(410, 815, datos[3])
#     can3.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can3, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can3, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can3, 488, 800, '2022', 10)
#     #fuente para iluminarse
#     #pilas baterias
#     can3.drawString(280, 740, datos[214])
#     can3.drawString(340, 740, datos[222])
#     if datos[230] == "Cabecera municipal":
#         can3.drawString(420, 740, 'x')
#     elif datos[230] == "Vereda":
#         can3.drawString(462, 740, 'x')
#     elif datos[230] == "Domicilio":
#         can3.drawString(505, 740, 'x')
#     #gasolina
#     can3.drawString(280, 728, datos[215])
#     can3.drawString(340, 728, datos[223])
#     if datos[231] == "Cabecera municipal":
#         can3.drawString(420, 728, 'x')
#     elif datos[231] == "Vereda":
#         can3.drawString(462, 728, 'x')
#     elif datos[231] == "Domicilio":
#         can3.drawString(505, 728, 'x')
#     #Kerosene
#     can3.drawString(280, 716, datos[216])
#     can3.drawString(340, 716, datos[224])
#     if datos[232] == "Cabecera municipal":
#         can3.drawString(420, 716, 'x')
#     elif datos[232] == "Vereda":
#         can3.drawString(462, 716, 'x')
#     elif datos[232] == "Domicilio":
#         can3.drawString(505, 716, 'x')
#     #Petroleo
#     can3.drawString(280, 702, datos[217])
#     can3.drawString(340, 702, datos[225])
#     if datos[233] == "Cabecera municipal":
#         can3.drawString(420, 702, 'x')
#     elif datos[233] == "Vereda":
#         can3.drawString(462, 702, 'x')
#     elif datos[233] == "Domicilio":
#         can3.drawString(505, 702, 'x')
#     #Alcohol
#     can3.drawString(280, 692, datos[218])
#     can3.drawString(340, 692, datos[226])
#     if datos[234] == "Cabecera municipal":
#         can3.drawString(420, 692, 'x')
#     elif datos[234] == "Vereda":
#         can3.drawString(462, 692, 'x')
#     elif datos[234] == "Domicilio":
#         can3.drawString(505, 692, 'x')
#     #Diesel
#     can3.drawString(280, 680, datos[219])
#     can3.drawString(340, 680, datos[227])
#     if datos[235] == "Cabecera municipal":
#         can3.drawString(420, 680, 'x')
#     elif datos[235] == "Vereda":
#         can3.drawString(462, 680, 'x')
#     elif datos[235] == "Domicilio":
#         can3.drawString(505, 680, 'x')
#     #Velas
#     can3.drawString(280, 668, datos[220])
#     can3.drawString(340, 668, datos[228])
#     if datos[236] == "Cabecera municipal":
#         can3.drawString(420, 668, 'x')
#     elif datos[236] == "Vereda":
#         can3.drawString(462, 668, 'x')
#     elif datos[236] == "Domicilio":
#         can3.drawString(505, 668, 'x')
#     #Otro
#     can3.drawString(120, 652, datos[238])
#     can3.drawString(230, 652, "-")
#     can3.drawString(280, 652, datos[221])
#     can3.drawString(340, 652, datos[229])
#     if datos[237] == "Cabecera municipal":
#         can3.drawString(420, 652, 'x')
#     elif datos[237] == "Vereda":
#         can3.drawString(462, 652, 'x')
#     elif datos[237] == "Domicilio":
#         can3.drawString(505, 652, 'x')
#      #Horas al dia utiliza
#     if datos[240] == None:
#         can3.drawString(410, 612, '-')
#     else:
#         can3.drawString(410, 612, datos[240])
#     #Queman residuos
#     if datos[188]=='Si':
#         can3.drawString(320, 544, "x")
#     else:
#         can3.drawString(370, 544, "x")
#     #Fuente quema residuos
#     #gas propano
#     can3.drawString(340, 455, datos[189])
#     can3.drawString(442, 455, datos[200])
#     #gas natural
#     can3.drawString(340, 442, datos[190])
#     can3.drawString(442, 442, datos[201])
#     #gasolina
#     can3.drawString(340, 430, datos[191])
#     can3.drawString(442, 430, datos[202])
#     #Kerosene
#     can3.drawString(340, 417, datos[192])
#     can3.drawString(442, 417, datos[203])
#     #Petroleo
#     can3.drawString(340, 404, datos[193])
#     can3.drawString(442, 404, datos[204])
#     #Alcohol
#     #Carbon mineral
#     can3.drawString(340, 391, datos[194])
#     can3.drawString(442, 391, datos[205])
#     #Leña comprada
#     can3.drawString(340, 378, datos[195])
#     can3.drawString(442, 378, datos[206])
#     #Leña autoapropiada
#     can3.drawString(340, 367, datos[196])
#     can3.drawString(442, 367, datos[207])
#     #gas propano
#     can3.drawString(340, 354, datos[197])
#     can3.drawString(442, 354, datos[208])
#     #residuos del agro
#     can3.drawString(340, 343, datos[198])
#     can3.drawString(442, 343, datos[209])
#     #Otro
#     if datos[212] == None:
#         can3.drawString(150, 333, '-')
#     else:
#         can3.drawString(150, 333, datos[212])
#     can3.drawString(260, 333, "-")
#     can3.drawString(340, 330, datos[199])
    
#     #cuantas horas al dia utiliza para ilumminar
#     if datos[210] == None:
#         can3.drawString(350, 305, '-')
#     else:
#         can3.drawString(442, 330, datos[210])
#         can3.drawString(350, 305, datos[210])
#     #contaminacion 
#     #exceso de ruido
#     if datos[271]=='Si':
#         can3.drawString(385, 210, "x")
#     else:
#         can3.drawString(430, 210, "x")
#     #malos oloress
#     if datos[272] =='Si':
#         can3.drawString(385, 195, "x")
#     else:
#         can3.drawString(430, 195, "x")
#     # uso del predio
#     #residencial
#     if datos[74] == 'Residencial':
#         can3.drawString(415, 92, "x")
#     #negocio
#     elif datos[74] == 'Negocio':
#         can3.drawString(415, 80, "x")
#     #mixto
#     elif datos[74] == 'Mixto':
#         can3.drawString(415, 68, "x")
#     #institucional
#     elif datos[74] == 'Institucional':
#         can3.drawString(415, 56, "x")
#     can3.save()
#     packet4 = io.BytesIO()
#     # create a new PDF with Reportlab
#     can4 = canvas.Canvas(packet4, pagesize=A4)
#     can4.setFont("Helvetica", 8)
#     can4.drawString(410, 815, datos[3])
#     #fecha de formulario
#     can4.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can4, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can4, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can4, 488, 800, '2022', 10)
#     #estrato del predio
#     if datos[73] == "Estrato 1":
#         can4.drawString(255, 748, "x")
#     elif datos[73] == "Estrato 2":
#         can4.drawString(280, 748, "x")
#     elif datos[73] == "Estrato 3":
#         can4.drawString(305, 748, "x")
#     elif datos[73] == "Estrato 4":
#         can4.drawString(330, 748, "x")
#     elif datos[73] == "Estrato 5":
#         can4.drawString(350, 748, "x")
#     elif datos[73] == "Estrato 6":
#         can4.drawString(375, 748, "x")
#     #Nombre de la comunidad
#     can4.drawString(90, 670, datos[103])
#     #personas en la comunidad 
#     llenarCampos(can4, 315, 598, datos[116], 30)
#     #la vivienda se encuentra ubicada al interior de 
#     if datos[104]=='Caserío' :
#         can4.drawString(405, 536, "x")
#     elif datos[104]=='Resguardo indígena' :
#         can4.drawString(405, 523, "x")
#     #parcialidad
#     elif datos[104]=='Parcialidad o asentamiento indígena fuera del resguardo' :
#         can4.drawString(405, 510, "x")
#     elif datos[104]=='Territorio colectivo de comunidad negra' :
#         can4.drawString(405, 497, "x")
#     #territorio de comunidad
#     elif datos[104]=='Territorio de comunidad negra no titulada' :
#         can4.drawString(405, 484, "x")
#     #territorio ancestral
#     elif datos[104]=='Territorio ancestral raiza del Archipiélago de Sán Andrés, Providencia y Santa Catalina' :
#         can4.drawString(405, 471, "x")
#     #reancheria
#     elif datos[104]=='Ranchería - Guajira' :
#         can4.drawString(405, 458, "x")
#     #territorio palenquero
#     elif datos[104]=='Territorio Palenquero de San Basilio' :
#         can4.drawString(405, 445, "x")
#     #territorio gitano
#     elif datos[104]=='Territorio Gitano - ROOM' :
#         can4.drawString(405, 432, "x")
#     #zona rural
#     elif datos[104]=='Zona rural' :
#         can4.drawString(405, 419, "x")
#     #tenencia de la vivenda
#     if datos[105] == 'Propia':
#         can4.drawString(350, 351, "x")
#     #tenencia de la vivenda
#     elif datos[105] == 'Arriendo':
#         can4.drawString(350, 339, "x")
#     #tenencia de la vivenda
#     elif datos[105] == 'Colectiva':
#         can4.drawString(350, 327, "x")
#     # hogares en la vivienda
#     llenarCampos(can4, 342, 267 , datos[106], 30)
#     #personas en la vivienda
#     llenarCampos(can4, 342, 222 , datos[107], 30)
#     #material predominante en la vivienda
#     if datos[108] == 'Bloque, ladrillo, piedra, madera pulida' :
#         can4.drawString(420, 152, "x")
#     elif datos[108] == 'Concreto' :
#         can4.drawString(420, 140, "x")
#     elif datos[108] == 'Tapia pisada, adobe, bahareque' :
#         can4.drawString(420, 128, "x")
#     elif datos[108] == 'Madera burda, tabla, tablón' :
#         can4.drawString(420, 116, "x")
#     elif datos[108] == 'Material prefabricado' :
#         can4.drawString(420, 104, "x")
#     elif datos[108] == 'Guadua, caña, esterilla, otros vegetales' :
#         can4.drawString(420, 92, "x")
#     elif datos[108] == 'Materiales de desecho (zinc, tela, cartón, latas, plásticos, otros)' :
#         can4.drawString(420, 80, "x")
#     elif datos[108] == 'No tiene paredes' :
#         can4.drawString(420, 68, "x")
#     can4.save()

#     #hoja 5 del pdf
#     packet5 = io.BytesIO()
#     can5 = canvas.Canvas(packet5, pagesize=A4)
#     can5.setFont("Helvetica", 8)
#     can5.drawString(410, 815, datos[3])
#     can5.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can5, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can5, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can5, 488, 800, '2022', 10)
#     #material predominante techo
#     if datos[109] == 'Paja, palma y otros vegetales':
#         can5.drawString(420, 742, "x")
#     elif datos[109] == 'Plancha de cemento, concreto y hormigón':
#         can5.drawString(420, 730, "x")
#     elif datos[109] == 'Tejas (barro, asbesto – cemento, metálica o lámina de zinc, plástica)':
#         can5.drawString(420, 718, "x")
#     elif datos[109] == 'Material de desecho (tela, cartón, latas, plástico, otros)':    
#         can5.drawString(420, 706, "x")
#     #material predominante en piso
#     if datos[110] == 'Alfombra o tapete de pared a pared':
#         can5.drawString(410, 640, "x")
#     if datos[110] == 'Mármol, parqué, madera pulida y lacada':
#         can5.drawString(410, 628, "x")
#     if datos[110] == 'Baldosa, vinilo, tableta, ladrillo, laminado':
#         can5.drawString(410, 616, "x")
#     if datos[110] == 'Cemento, gravilla':
#         can5.drawString(410, 604, "x")
#     if datos[110] == 'Madera burda, tabla, tablón, otro vegetal':
#         can5.drawString(410, 592, "x")
#     if datos[110] == 'Tierra, arena, barro':
#         can5.drawString(410, 580, "x")
#     #vivienda ha sido afectada
#     if datos[111] == 'Si':
#         can5.drawString(385, 523, "x")
#     else:
#         can5.drawString(432, 523, "x")
#     if datos[112] == 'Si':
#         can5.drawString(385, 511, "x")
#     else:
#         can5.drawString(432, 511, "x")
#     if datos[113] == 'Si':
#         can5.drawString(385, 499, "x")
#     else:
#         can5.drawString(432, 499, "x")
#     if datos[114] == 'Si':
#         can5.drawString(385, 487, "x")
#     else:
#         can5.drawString(432, 487, "x")
#     if datos[114] == 'Si':
#         can5.drawString(385, 475, "x")
#     else:
#         can5.drawString(432, 475, "x")
#     #area de construccion
#     # area = datos[115].split('x')
#     can5.drawString(300, 417,  datos[115])
#     # can5.drawString(330, 417, 'X')
#     # can5.drawString(360, 417, area[1])
    
#     #la vivienda cuenta con servicios
#     if datos[284] == 'true':
#         can5.drawString(400, 304, "x")
#     if datos[285] == 'true':
#         can5.drawString(400, 292, "x")
#     if datos[286] == 'true':
#         can5.drawString(400, 280, "x")
#     if datos[287] == 'true':
#         can5.drawString(400, 268, "x")
#     if datos[288] == 'true':
#         can5.drawString(400, 256, "x")
#     if datos[289] == 'true':    
#         can5.drawString(400, 244, "x")
#     #obtencion de agua
#     if datos[289] == 'true':
#         can5.drawString(295, 167, "x")
#     if datos[292] == 'true':
#         can5.drawString(295, 153, "x")
#     if datos[293] == 'true':
#         can5.drawString(295, 141, "x")
#     if datos[294] == 'true':
#         can5.drawString(295, 129, "x")
#     if datos[295] == 'true':
#         can5.drawString(295, 117, "x")
#     if datos[296] == 'true':
#         can5.drawString(295, 105, "x")
#     if datos[297] == 'true':
#         can5.drawString(295, 93, "x")
#     if datos[298] == 'true':
#         can5.drawString(295, 81, "x")
#     #tiene medidor de agua
#     if datos[291] == 'true':
#         can5.drawString(465, 167, "x")
#     else:
#         can5.drawString(500, 167, "x")
#     can5.save()
#      #hoja 6 del pdf
#     packet6 = io.BytesIO()
#     can6 = canvas.Canvas(packet6, pagesize=A4)
#     can6.setFont("Helvetica", 8)
#     can6.drawString(410, 815, datos[3])
#     can6.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can6, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can6, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can6, 488, 800, '2022', 10)
#     #Servicio sanitario
#     if datos[299] == 'true':
#         can6.drawString(400, 743, "x")
#     if datos[300] == 'true':
#         can6.drawString(400, 731, "x")
#     if datos[301] == 'true':
#         can6.drawString(400, 719, "x")
#     if datos[302] == 'true':
#         can6.drawString(400, 707, "x")
#     if datos[303] == 'true':
#         can6.drawString(400, 695, "x")
#     if datos[304] == 'true':
#         can6.drawString(230, 685, datos[304])
#         can6.drawString(400, 683, "x")
#     #tiene acceso a gas
#     if datos[305] == 'Pipeta / Cilindro':
#         can6.drawString(400, 614, "x")
#     elif datos[305] == 'Gasoducto':
#         can6.drawString(400, 602, "x")
#     elif datos[305] == 'No tiene servicio de gas':
#         can6.drawString(400, 590, "x")
#     #tiene acceso al agua
#     if datos[365] == 'Si':
#         can6.drawString(320, 480, "x")
#     elif datos[365] == 'No':
#         can6.drawString(320, 467, "x")
#     #que cantidad de agua puede obtener
#     can6.drawString(100, 430, datos[366])
#     #promedio cantidad de agua
#     if datos[367] == None:
#         can6.drawString(400, 395, '-')
#     else:
#         can6.drawString(400, 395, datos[367])
        
#     #fuente principal de abastesimiento de agua
#     if datos[368] == 'Jagüey':
#         can6.drawString(400, 313, "x")
#     elif datos[368] == 'Pozo':
#         can6.drawString(400, 301, "x")
#     elif datos[368] == 'Molino':
#         can6.drawString(400, 289, "x")
#     elif datos[368] == 'Carrotanques':
#         can6.drawString(400, 277, "x")
#     elif datos[368] == 'Aguas lluvias':
#         can6.drawString(400, 265, "x")
#     elif datos[368] == 'Ríos':
#         can6.drawString(400, 253, "x")
#     elif datos[368] == 'Arroyos':
#         can6.drawString(400, 241, "x")
#     elif datos[368] == 'Quebradas':
#         can6.drawString(400, 228, "x")
#     elif datos[368] == 'Otro':
#         can6.drawString(400, 216, "x")
#     #la casimba es comunitaria
#     if datos[372] == 'Si':
#         can6.drawString(320, 147, "x")
#     elif datos[372] == 'No':    
#         can6.drawString(320, 135, "x")
#     # #cual
#     can6.drawString(120, 110, datos[371])
#     can6.save()

#     packet7 = io.BytesIO()
#     can7 = canvas.Canvas(packet7, pagesize=A4)
#     can7.setFont("Helvetica", 8)
#     can7.drawString(410, 815, datos[3])
#     can7.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can7, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can7, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can7, 488, 800, '2022', 10)
#      #uso del agua que obtienen
#     usosAgua = datos[373].split(',')
#     if 'Cocinar' in usosAgua:
#         can7.drawString(405, 744, "x")
#     if 'Higiene' in usosAgua:
#         can7.drawString(405, 732, "x")
#     if 'Actividades agropecuarias' in usosAgua:
#         can7.drawString(405, 720, "x")
#     if 'Actividades de ganadería' in usosAgua:
#         can7.drawString(405, 708, "x")
#     if 'Otro' in usosAgua:
#         can7.drawString(405, 696, "x")
#         # va al puesto de agua todos los dias
#     if datos[375] == 'Si':
#         can7.drawString(320, 626, "x")
#     elif datos[375] == 'No':
#         can7.drawString(320, 614, "x")
#     else:
#         can7.drawString(320, 602, "x")
#     #cuanto dura el agua que recolecta
#     can7.drawString(300, 573, datos[376])
#     #cantidad destinada higiene
#     can7.drawString(100, 528, datos[377])
#     #distancia para obtener agua
#     can7.drawString(300, 495, datos[378])
#     #ti3mpo destina a la recoleccion de agua
#     can7.drawString(100, 450, datos[379])
#     #medio de transporte para el agua
#     if datos[380] == 'Moto':
#         can7.drawString(405, 377, "x")
#     elif datos[380] == 'Transporte animal':    
#         can7.drawString(405, 365, "x")
#     elif datos[380] == 'Caminando':
#         can7.drawString(405, 353, "x")
#     elif datos[380] == 'Bicicleta':
#         can7.drawString(405, 341, "x")
#     elif datos[380] == 'Otro':
#         can7.drawString(405, 329, "x")
#         can7.drawString(250, 329, datos[381])
#     #adquiere agua de otra fuente
#     if datos[382] == 'Si':
#         can7.drawString(320, 260, "x")
#         #cuanta agua adquiere de esa fuente
#         can7.drawString(360, 220, datos[383])
#         #cual es la otra fuente
#         if datos[384] == 'Galón/pimpina':
#             can7.drawString(405, 145, "x")
#         elif datos[384] == 'Carrotanque':
#             can7.drawString(405, 134, "x")
#         elif datos[384] == 'Botellón':
#             can7.drawString(405, 122, "x")
#         elif datos[384] == 'Pozo':
#             can7.drawString(405, 111, "x")
#     elif datos[382] == 'No':
#         can7.drawString(320, 248, "x")
        
#     can7.save()

#     packet8 = io.BytesIO()
#     can8 = canvas.Canvas(packet8, pagesize=A4)
#     can8.setFont("Helvetica", 8)
#     can8.drawString(410, 815, datos[3])
#     can8.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can8, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can8, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can8, 488, 800, '2022', 10)

#     if datos[385] == 'Si':
#         can8.drawString(320, 743, 'x')
#     elif datos[385] == 'No':
#         can8.drawString(320, 730, 'x')
#     #cuanto debe pagar
#     if datos[386] == None:
#         can8.drawString(200, 712, '-')
#     else:
#         can8.drawString(200, 712, datos[386])
#     #tratamiento del agua
#     if datos[387] == 'Filtrarla':
#         can8.drawString(404,637,'x')
#     elif datos[387] == 'Calentarla':
#         can8.drawString(404,625,'x')
#     elif datos[387] == 'Pastillas de Cloro':
#         can8.drawString(404,613,'x')
#     elif datos[387] == 'Ninguno':
#         can8.drawString(404,601,'x')
#     elif datos[387] == 'Otro':
#         can8.drawString(404,591,'x')
#         can8.drawString(250,589,datos[388])
#     #espacio de almacenamiento de agua
#     if datos[389] == 'Si':
#         can8.drawString(320, 510, 'x')
#     elif datos[389] == 'No':
#         can8.drawString(320, 498, 'x')
#     #capacidad promedio
#     if datos[390] == None:
#         can8.drawString(310, 480, '-')
#     else:
#         can8.drawString(310, 480, datos[390])
#     #se utilizan los almacenamientos para otras actividades 
#     if datos[391] == 'Si':
#         can8.drawString(320, 405, 'x')
#     elif datos[391] == 'No' or datos[391] == '-':
#         can8.drawString(320, 393, 'x')
    
#     #se realizan procedimientos de limpieza
#     if datos[392] == 'Si':
#         can8.drawString(320, 315, 'x')
#     elif datos[392] == 'No':
#         can8.drawString(320, 303, 'x')
#     elif datos[392] == 'No sabe' or datos[392] == '-':
#         can8.drawString(320, 291, 'x')
#     #tiene sitio para las basuras
#     if datos[393] == 'Si':
#         can8.drawString(320, 224, 'x')
#     elif datos[393] == 'No':
#         can8.drawString(320, 212, 'x')
#     #cuenta con servicio de recoleccion
#     if datos[394] == 'Municipal':
#         can8.drawString(320, 140, 'x')
#     elif datos[394]== 'Veredal':
#         can8.drawString(320, 128, 'x')
#     elif datos[394] == 'No Tiene':
#         can8.drawString(320, 116, 'x')
#     can8.save()


#     packet9 = io.BytesIO()
#     can9 = canvas.Canvas(packet9, pagesize=A4)
#     can9.setFont("Helvetica", 8)
#     can9.drawString(410, 815, datos[3])
#     can9.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can9, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can9, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can9, 488, 800, '2022', 10)

#     if datos[395] == 'Cielo abierto':
#         can9.drawString(404,758,'x')
#     elif datos[395] == 'Botadero':
#         can9.drawString(404,746,'x')
#     elif datos[395] == 'Incineración':
#         can9.drawString(404,734,'x')
#     elif datos[395] == 'Enterramiento':
#         can9.drawString(404,722,'x')
#     #elementos emplea
#     if datos[396] == 'Bolsa plástica':
#         can9.drawString(404,664,'x')
#     elif datos[396] == 'En Caneca con tapa':
#         can9.drawString(404,652,'x')
#     elif datos[396] == 'Pozo comunitario':
#         can9.drawString(404,640,'x')
#     #dispocision aguas negras
#     if datos[397] == 'Alcantarrillado':
#         can9.drawString(404, 580, 'x')
#     elif datos[397] == 'Pozo séptico':
#         can9.drawString(404, 568, 'x')
#     elif datos[397] == 'Campo abierto':
#         can9.drawString(404, 556, 'x')
#     elif datos[397] == 'Letrina':
#         can9.drawString(404, 544, 'x')
#     elif datos[397] == 'Río':
#         can9.drawString(404, 532, 'x')
#     elif datos[397] == 'Quebrada':
#         can9.drawString(404, 520, 'x')
#     elif datos[397] == 'Arroyo':
#         can9.drawString(404, 508, 'x')
#     elif datos[397] == 'Otro':
#         can9.drawString(404, 496, 'x')
#         can9.drawString(240, 496, datos[398])
#     #dispocision de aguas residual99
#     if datos[399] == 'Pozo séptico':
#         can9.drawString(404,436, 'x')
#     elif datos[399] == 'Campo abierto':
#         can9.drawString(404,424, 'x')
#     elif datos[399] == 'Letrina':
#         can9.drawString(404,412, 'x')
#     elif datos[399] == 'Río':
#         can9.drawString(404,400, 'x')
#     elif datos[399] == 'Quebrada':
#         can9.drawString(404,388, 'x')
#     elif datos[399] == 'Arroyo':
#         can9.drawString(404,376, 'x')
#     elif datos[399] == 'Otro':
#         can9.drawString(404,364, 'x')
#         can9.drawString(240,364, datos[400])
#     familia = (json.loads(datos[13]))
#     hijo1 = False
#     hijo2 = False
#     hijo3 = False
#     hijo4 = False
#     hijo5 = False
#     for i in range(len(familia)):
#         integrante = dict(familia[i])
#         if integrante['Parentesco'] == 'Jefe (a) de hogar':
#             can9.drawString(130, 201, 'x')
#             can9.drawString(231, 201, integrante['Genero'])
#             can9.drawString(281, 201, str(integrante['Edad']))
#             can9.drawString(331, 201, integrante['Registro'])
#             can9.drawString(381, 201, integrante['Escolaridad'])
#             can9.drawString(476, 201, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Pareja, esposo(a), cónyuge, compañero(a)':
#             can9.drawString(130, 181, 'x')
#             can9.drawString(231, 181, integrante['Genero'])
#             can9.drawString(281, 181, str(integrante['Edad']))
#             can9.drawString(331, 181, integrante['Registro'])
#             can9.drawString(381, 181, integrante['Escolaridad'])
#             can9.drawString(476, 181, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)' and hijo1 == False:
#             hijo1 = True
#             can9.drawString(130, 168, 'x')
#             can9.drawString(231, 168, integrante['Genero'])
#             can9.drawString(281, 168, str(integrante['Edad']))
#             can9.drawString(331, 168, integrante['Registro'])
#             can9.drawString(381, 168, integrante['Escolaridad'])
#             can9.drawString(476, 168, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)' and hijo1 == True and hijo2 == False:
#             hijo2 = True
#             can9.drawString(130, 155, 'x')
#             can9.drawString(231, 155, integrante['Genero'])
#             can9.drawString(281, 155, str(integrante['Edad']))
#             can9.drawString(331, 155, integrante['Registro'])
#             can9.drawString(381, 155, integrante['Escolaridad'])
#             can9.drawString(476, 155, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 3' and hijo2 == True and hijo3 == False:
#             hijo3 = True
#             can9.drawString(130, 142, 'x')
#             can9.drawString(231, 142, integrante['Genero'])
#             can9.drawString(281, 142, str(integrante['Edad']))
#             can9.drawString(331, 142, integrante['Registro'])
#             can9.drawString(381, 142, integrante['Escolaridad'])
#             can9.drawString(476, 142, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 4' and hijo3 == True and hijo4 == False:
#             hijo4 = True
#             can9.drawString(130, 129, 'x')
#             can9.drawString(231, 129, integrante['Genero'])
#             can9.drawString(281, 129, str(integrante['Edad']))
#             can9.drawString(331, 129, integrante['Registro'])
#             can9.drawString(381, 129, integrante['Escolaridad'])
#             can9.drawString(476, 129, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 5' and hijo4 == True and hijo5 == False:
#             can9.drawString(130, 116, 'x')
#             can9.drawString(231, 116, integrante['Genero'])
#             can9.drawString(281, 116, str(integrante['Edad']))
#             can9.drawString(331, 116, integrante['Registro'])
#             can9.drawString(381, 116, integrante['Escolaridad'])
#             can9.drawString(476, 116, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Nieto(a)':
#             can9.drawString(130, 103, 'x')
#             can9.drawString(231, 103, integrante['Genero'])
#             can9.drawString(281, 103, str(integrante['Edad']))
#             can9.drawString(331, 103, integrante['Registro'])
#             can9.drawString(381, 103, integrante['Escolaridad'])
#             can9.drawString(476, 103, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Suegro(a)':
#             can9.drawString(130, 91, 'x')
#             can9.drawString(231, 91, integrante['Genero'])
#             can9.drawString(281, 91, str(integrante['Edad']))
#             can9.drawString(331, 91, integrante['Registro'])
#             can9.drawString(381, 91, integrante['Escolaridad'])
#             can9.drawString(476, 91, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Tios(as)':
#             can9.drawString(130, 78, 'x')
#             can9.drawString(231, 78, integrante['Genero'])
#             can9.drawString(281, 78, str(integrante['Edad']))
#             can9.drawString(331, 78, integrante['Registro'])
#             can9.drawString(381, 78, integrante['Escolaridad'])
#             can9.drawString(476, 78, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Yerno, nuera':
#             can9.drawString(130, 66, 'x')
#             can9.drawString(231, 66, integrante['Genero'])
#             can9.drawString(281, 66, str(integrante['Edad']))
#             can9.drawString(331, 66, integrante['Registro'])
#             can9.drawString(381, 66, integrante['Escolaridad'])
#             can9.drawString(476, 66, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Otro (a) pariente del (de la) jefe (a)':
#             can9.drawString(130, 48, 'x')
#             can9.drawString(231, 48, integrante['Genero'])
#             can9.drawString(281, 48, str(integrante['Edad']))
#             can9.drawString(331, 48, integrante['Registro'])
#             can9.drawString(381, 48, integrante['Escolaridad'])
#             can9.drawString(476, 48, integrante['Ocupacion'])
#         elif integrante['Parentesco'] == 'Otro (a) no pariente':
#             can9.drawString(130, 36, 'x')
#             can9.drawString(231, 36, integrante['Genero'])
#             can9.drawString(281, 36, str(integrante['Edad']))
#             can9.drawString(331, 36, integrante['Registro'])
#             can9.drawString(381, 36, integrante['Escolaridad'])
#             can9.drawString(476, 36, integrante['Ocupacion'])
#     can9.save()
#     packet10 = io.BytesIO()
#     can10 = canvas.Canvas(packet10, pagesize=A4)
#     can10.setFont("Helvetica", 8)
#     can10.drawString(410, 815, datos[3])
#     can10.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can10, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can10, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can10, 488, 800, '2022', 10)
#     #temporalidad de la vivienda
#     if datos[15]=='Permanente':
#         can10.drawString(390, 733, "x")
#     elif datos[15]=='Temporal':
#         can10.drawString(390, 721, "x")
#     #Contribuye al ingreso
#     if datos[18]=='Si':
#         can10.drawString(323, 663, "x")
#     elif datos[18]=='No':
#         can10.drawString(368, 663, "x")
#     #Se Reconoce como
#     if datos[20]=='Indígena':
#         can10.drawString(408, 596, "x")
#     elif datos[20]=='Gitano (a)(ROM)':
#         can10.drawString(408, 584, "x")
#     elif datos[20]=='Raizal de San Andrés, Providencia, Santa Catalina':
#         can10.drawString(408, 572, "x")
#     elif datos[20]=='Palenquero (a)':
#         can10.drawString(408, 560, "x")
#     elif datos[20]=='Negro (a), afrodescendiente, afrocolombiano (a)':
#         can10.drawString(408, 548, "x")
#     elif datos[20]=='Ninguno de los anteriores':   
#         can10.drawString(408, 536, "x")
#     #HABLA LA lengua nativa
#     if datos[22] == 'Si':
#         can10.drawString(320, 468, "x")
#     elif datos[22] == 'Si':
#         can10.drawString(320, 456, "x")
#     #cual lengua nativa habla
#     can10.drawString(70, 416, datos[23])
#     #alguna persona tiene problemas de salud
#     if datos[24] == 'Si':
#         can10.drawString(323, 338, "x")
#     elif datos[24] == 'No':
#         can10.drawString(368, 338, "x")
#     if datos[25] == 'Si':
#         can10.drawString(320, 270, "x")
#     elif datos[25] == 'No':
#         can10.drawString(320, 258, "x")
#     #cual organizacion pertenece
#     can10.drawString(70, 190, datos[26])
#      #domesticas
#     if datos[27] == 'true':
#         can10.drawString(364, 76, "x")
#     if datos[37] == 'true':
#         can10.drawString(404, 76, "x")
#     if datos[47] == 'true':
#         can10.drawString(444, 76, "x")
#     if datos[57] == 'true':
#         can10.drawString(484, 76, "x")
#         #pagos
#     if datos[28] == 'true':
#         can10.drawString(364, 64, "x")
#     if datos[38] == 'true':
#         can10.drawString(404, 64, "x")
#     if datos[48] == 'true':
#         can10.drawString(444, 64, "x")
#     if datos[58] == 'true':
#         can10.drawString(484, 64, "x")
#         #finca
#     if datos[29] == 'true':
#         can10.drawString(364, 50, "x")
#     if datos[39] == 'true':
#         can10.drawString(404, 50, "x")
#     if datos[49] == 'true':
#         can10.drawString(444, 50, "x")
#     if datos[59] == 'true':
#         can10.drawString(484, 50, "x")
#         #Transporte
#     if datos[30] == 'true':
#         can10.drawString(364, 35, "x")
#     if datos[40] == 'true':
#         can10.drawString(404, 35, "x")
#     if datos[50] == 'true':
#         can10.drawString(444, 35, "x")
#     if datos[60] == 'true':
#         can10.drawString(484, 35, "x")
#     can10.save()
#     packet11 = io.BytesIO()
#     can11 = canvas.Canvas(packet11, pagesize=A4)
#     can11.setFont("Helvetica", 8)
#     can11.drawString(410, 815, datos[3])
#     can11.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can11, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can11, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can11, 488, 800, '2022', 10)
#     # quienes realizan las labores
#         #admin finca
#     if datos[31] == 'true':
#         can11.drawString(364, 756, "x")
#     if datos[41] == 'true':
#         can11.drawString(404, 756, "x")
#     if datos[51] == 'true':
#         can11.drawString(444, 756, "x")
#     if datos[61] == 'true':
#         can11.drawString(484, 756, "x")
#         #comercia
#     if datos[32] == 'true':
#         can11.drawString(364, 744, "x")
#     if datos[42] == 'true':
#         can11.drawString(404, 744, "x")
#     if datos[52] == 'true':
#         can11.drawString(444, 744, "x")
#     if datos[62] == 'true':
#         can11.drawString(484, 744, "x")
#         #Estudia
#     if datos[33] == 'true':
#         can11.drawString(364, 732, "x")
#     if datos[43] == 'true':
#         can11.drawString(404, 732, "x")
#     if datos[53] == 'true':
#         can11.drawString(444, 732, "x")
#     if datos[63] == 'true':
#         can11.drawString(484, 732, "x")
#         #fORMACION HIJOS
#     if datos[34] == 'true':
#         can11.drawString(364, 719, "x")
#     if datos[44] == 'true':
#         can11.drawString(404, 719, "x")
#     if datos[54] == 'true':
#         can11.drawString(444, 719, "x")
#     if datos[64] == 'true':
#         can11.drawString(484, 719, "x")
#         #Cuidado adultos
#     if datos[35] == 'true':
#         can11.drawString(364, 706, "x")
#     if datos[45] == 'true':
#         can11.drawString(404, 706, "x")
#     if datos[55] == 'true':
#         can11.drawString(444, 706, "x")
#     if datos[65] == 'true':
#         can11.drawString(484, 706, "x")
#         #Otro
#     if datos[36] == 'true':
#         can11.drawString(364, 693, "x")
#     if datos[46] == 'true':
#         can11.drawString(404, 693, "x")
#     if datos[56] == 'true':
#         can11.drawString(444, 693, "x")
#     if datos[66] == 'true':
#         can11.drawString(160, 693, "Otro")
#         can11.drawString(484, 693, "x")
#     #fuentes de ingtreso en el hogar
#     if datos[123] == 'true':
#         can11.drawString(402, 543, "x")
#     if datos[124] == 'true':
#         can11.drawString(402, 531, "x")
#     if datos[125] == 'true':
#         can11.drawString(402, 519, "x")
#     if datos[126] == 'true':
#         can11.drawString(402, 507, "x")
#     if datos[127] == 'true':
#         can11.drawString(402, 493, "x")
#     if datos[128] == 'true':
#         can11.drawString(402, 481, "x")
#     if datos[129] == 'true':
#         can11.drawString(402, 469, "x")
#     if datos[130] == 'true':
#         can11.drawString(402, 457, "x")
#     if datos[131] == 'true':
#         can11.drawString(402, 445, "x")
#     if datos[132] == 'true':
#         can11.drawString(402, 431, "x")
#     if datos[133] == 'true':
#         can11.drawString(402, 419, "x")
#     if datos[134] == 'true':
#         can11.drawString(402, 407, "x")
#     if datos[135] == 'true':
#         can11.drawString(402, 393, "x")
#     if datos[136] == 'true':
#         can11.drawString(402, 381, "x")
#     if datos[137] == 'true':
#         can11.drawString(402, 369, "x")
#         can11.drawString(242, 369, datos[137])
#     #que cultivan
#     can11.drawString(142, 329, datos[138])
#     can11.drawString(142, 316, datos[139])
#     can11.drawString(142, 303, datos[140])
#     can11.drawString(142, 290, datos[141])
#     can11.drawString(350, 223, datos[142])
#     can11.drawString(350, 211, datos[143])
#     can11.drawString(350, 199, datos[144])
#     can11.drawString(350, 187, datos[145])
#     can11.drawString(350, 173, datos[146])
#     can11.drawString(350, 161, datos[147])
#     can11.drawString(350, 149, datos[148])
#     can11.drawString(350, 137, datos[149])
#     can11.drawString(350, 125, datos[150])
#     can11.drawString(350, 111, datos[151])
#     can11.drawString(350, 99, datos[152])
#     can11.drawString(350, 87, datos[153])
#     can11.drawString(242, 87, datos[155])
#     can11.drawString(350, 73, datos[154])    
#     can11.save()
#     packet12 = io.BytesIO()
#     can12 = canvas.Canvas(packet12, pagesize=A4)
#     can12.setFont("Helvetica", 8)
#     can12.drawString(410, 815, datos[3])
#     can12.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
#     #fecha de formulario
#     #dia
#     dia = random.randint(1, 8)
#     dia = '0'+str(dia)
#     llenarCampos(can12, 398, 800, dia, 10)
#     #mes
#     llenarCampos(can12, 440, 800, '04', 10)
#     #anio
#     llenarCampos(can12, 488, 800, '2022', 10)
#     #nombre
#     can12.drawString(110, 670, datos[81])
#     #telefono c
#     can12.drawString(300, 682, datos[83])
#     #telefono f
#     can12.drawString(300, 656, datos[84])
#     #correo 
#     can12.drawString(300, 632, datos[86])
#     # No ID
#     can12.drawString(110, 632, datos[85])
#     # firma
    
#     # No ID
#     can12.drawString(300, 490, datos[93])
#     #nombre encuestador
#     nombreEncuestador = datos[348] + " " + datos[349]
#     can12.drawString(110, 290, nombreEncuestador)
#     can12.drawString(310, 306,datos[355])
#     #telefono f
#     can12.drawString(310, 276, datos[356])
#     can12.drawString(310, 236, datos[358])
#     can12.drawString(110, 236, datos[357])

#     #firmaaa
#     with bd.cursor() as cursor:
#               cursor.execute("Select rutaserver from suncosurvey.fotos_firma where Id_Encuesta = '"+id+"';")
#               datos2 = cursor.fetchone()
#     urllib.request.urlretrieve("https://www.php.engenius.com.co"+datos2[0],"ejemplo.jpg")
#     filename = 'ejemplo.jpg'
#     filename1 = 'fondoblanco.jpg'
#     frontImage = Image.open(filename)
#     background = Image.open(filename1)
#     frontImage = frontImage.convert("RGBA")
#     background = background.convert("RGBA")
#     width = (background.width - frontImage.width) // 2
#     height = (background.height - frontImage.height) // 2
#     background.paste(frontImage, (width, height), frontImage)
#     background.save("new.png", format="png")

#     can12.drawImage('new.png', 75, 500, 200, 99)
#     #tipo id
#     #can12.drawString(490, 580, "x")
#     can12.drawString(490, 568, "x")
#     #can12.drawString(490, 553, "x")
#     #can12.drawString(360, 550, "otro")
#     can12.drawImage('blanco.JPG', 69, 730, 458, 20)
#     can12.save()

#     new_pdf = PyPDF2.PdfFileReader(packet)
#     new_pdf2 = PyPDF2.PdfFileReader(packet2)
#     new_pdf3 = PyPDF2.PdfFileReader(packet3)
#     new_pdf4 = PyPDF2.PdfFileReader(packet4)
#     new_pdf5 = PyPDF2.PdfFileReader(packet5)
#     new_pdf6 = PyPDF2.PdfFileReader(packet6)
#     new_pdf7 = PyPDF2.PdfFileReader(packet7)
#     new_pdf8 = PyPDF2.PdfFileReader(packet8)
#     new_pdf9 = PyPDF2.PdfFileReader(packet9)
#     new_pdf10 = PyPDF2.PdfFileReader(packet10)
#     new_pdf11 = PyPDF2.PdfFileReader(packet11)
#     new_pdf12 = PyPDF2.PdfFileReader(packet12)
#     existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-01.pdf", "rb"))
#     existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-02.pdf", "rb"))
#     existing_pdf3 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-03.pdf", "rb"))
#     existing_pdf4 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-04.pdf", "rb"))
#     existing_pdf5 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-05.pdf", "rb"))
#     existing_pdf6 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-06.pdf", "rb"))
#     existing_pdf7 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-07.pdf", "rb"))
#     existing_pdf8 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-08.pdf", "rb"))
#     existing_pdf9 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-09.pdf", "rb"))
#     existing_pdf10 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-10.pdf", "rb"))
#     existing_pdf11 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-11.pdf", "rb"))
#     existing_pdf12 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-12.pdf", "rb"))
#     output = PyPDF2.PdfFileWriter()
#     page = existing_pdf.getPage(0)
#     page2 = existing_pdf2.getPage(0)
#     page3 = existing_pdf3.getPage(0)
#     page4 = existing_pdf4.getPage(0)
#     page5 = existing_pdf5.getPage(0)
#     page6 = existing_pdf6.getPage(0)
#     page7 = existing_pdf7.getPage(0)
#     page8 = existing_pdf8.getPage(0)
#     page9 = existing_pdf9.getPage(0)
#     page10 = existing_pdf10.getPage(0)
#     page11 = existing_pdf11.getPage(0)
#     page12 = existing_pdf12.getPage(0)
#     page.mergePage(new_pdf.getPage(0))
#     page2.mergePage(new_pdf2.getPage(0))
#     page3.mergePage(new_pdf3.getPage(0))
#     page4.mergePage(new_pdf4.getPage(0))
#     page5.mergePage(new_pdf5.getPage(0))
#     page6.mergePage(new_pdf6.getPage(0))
#     page7.mergePage(new_pdf7.getPage(0))
#     page8.mergePage(new_pdf8.getPage(0))
#     page9.mergePage(new_pdf9.getPage(0))
#     page10.mergePage(new_pdf10.getPage(0))
#     page11.mergePage(new_pdf11.getPage(0))
#     page12.mergePage(new_pdf12.getPage(0))
#     output.addPage(page)
#     output.addPage(page2)
#     output.addPage(page3)
#     output.addPage(page4)
#     output.addPage(page5)
#     output.addPage(page6)
#     output.addPage(page7)
#     output.addPage(page8)
#     output.addPage(page9)
#     output.addPage(page10)
#     output.addPage(page11)
#     output.addPage(page12)
#     os.mkdir('pdfs/'+id)
#     outputStream = open("pdfs/"+id+"/"+id+"-replanteo.pdf", "wb")
#     output.write(outputStream)
#     outputStream.close()






    

if __name__ == '__main__':
   generarPdfId('307-1605790991386')