import PyPDF2 
import io
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image, ImageFont, ImageDraw
import  urllib
import zipfile
import pymysql 
import tkinter as tk
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
              cursor.execute("SELECT A.*,B.*,C.*,D.*,E.*,F.*,G.*,H.*,I.*,J.*,K.*,M.* FROM db_ipse_7_0.Encabezado A INNER JOIN db_ipse_7_0.Sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN db_ipse_7_0.Caracteristicas C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN db_ipse_7_0.Consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN db_ipse_7_0.Datos E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN db_ipse_7_0.Economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN db_ipse_7_0.Energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN db_ipse_7_0.Servicios H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN db_ipse_7_0.Tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN db_ipse_7_0.Ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN db_ipse_7_0.URE K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN db_ipse_7_0.Proyectos_funcionarios L ON A.Id_Proyecto_Funcionario = L.Id_Proyecto_Funcionario INNER JOIN db_ipse_7_0.Funcionarios M ON M.Id_Funcionario = L.Id_Funcionario WHERE A.isdelete = 0 AND A.Id_Encuesta ='"+id+"';")
              datos = cursor.fetchone()
    print(id)
    if os.path.exists("src/destination.pdf"):
        os.remove('src/destination.pdf')

    #pagina 1
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica", 9)

    can.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can, 487, 800, str(datos[6]),10)# Año
    
    #coordenadas  latitud
    latitudUnidad = datos[332].split('.')[0]
    print(datos[332].split('.')[0])
    latitudDecimales = datos[332].split('.')[1]
    can.drawString(240, 495, latitudUnidad)
    llenarCampos(can, 290, 495, latitudDecimales, 24)
    #coordenadas  longitud
    longitudUnidad = datos[333].split('.')[0]
    longitudDecimales = datos[333].split('.')[1]
    can.drawString(237, 458, longitudUnidad)
    llenarCampos(can, 290, 458, longitudDecimales, 24)
    #coordenadas  altitud
    if datos[334] == 'null':
        altitud = '-'
    else:
        altitud = round(float(datos[334]))
    llenarCampos(can, 233, 421, str(altitud), 30)
    #nombre departamento
    llenarCampos(can, 124, 360, str(datos[336]), 16)
    #codigo departamento
    llenarCampos(can, 124, 315, str(datos[337]), 16)
    #nombre municipio
    llenarCampos(can, 124, 292, str(datos[338]), 16)
    #codigo municipio
    llenarCampos(can, 124, 245, str(datos[339]), 16)    
    #nombre vereda
    llenarCampos(can, 124, 225, str(datos[340]), 16)  
    #nombre corregimiento
    llenarCampos(can, 124, 182, str(datos[341]), 16)

    if str(datos[342]) == '1':
        can.drawString(415, 85, "X")
    if str(datos[342]) == '2':
        can.drawString(415, 74, "X")
    if str(datos[342]) == '3':
        can.drawString(415, 59, "X")
    if str(datos[342]) == '4':
        can.drawString(415, 47, "X")


    can.save()

    #pagina2
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=A4)
    
    can2.setFont("Helvetica", 9)

    can2.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can2, 398, 803, str(datos[4]),10)# Dia
    llenarCampos(can2, 437, 803, str(datos[5]),10)# Mes
    llenarCampos(can2, 487, 803, str(datos[6]),10)# Año

    if str(datos[321]) == '1':
        can2.drawString(318, 623, "X")
    else:
        can2.drawString(318, 613, "X")
    if str(datos[322]) == '1':
        can2.drawString(318, 538, "X")
        if str(datos[323]) == '1':
            can2.drawString(415, 468, "X")
        elif str(datos[323]) == '2':
            can2.drawString(415, 455, "X")
        elif str(datos[323]) == '3':
            can2.drawString(415, 442, "X")
        elif str(datos[323]) == '4':
            can2.drawString(415, 430, "X")
        elif str(datos[323]) == '5': 
            can2.drawString(415, 418, "X")
        elif str(datos[323]) == '6':
            can2.drawString(415, 405, "X")
        elif str(datos[323]) == '7':
            can2.drawString(415, 393, "x")
            can2.drawString(350, 393,str(datos[324]))
        elif str(datos[323]):
            can2.drawString(350, 393,str(datos[324]))
    elif str(datos[322]) == '2':
        can2.drawString(318, 526, "X")

    if str(datos[325]) == '1':
        can2.drawString(322, 333, "X")
    else:
        can2.drawString(322, 321, "X")

    # fuente = datos[185]
    # if fuente == 'Gas Propano': 
    #     can2.drawString(368, 168, datos[163])
    #     can2.drawString(458, 168, datos[174])
    # else:
    #     can2.drawString(368, 168, "0")
    #     can2.drawString(458, 168, "0")
    # if fuente == 'Gas Natural':
    #     can2.drawString(368, 156, datos[164])
    #     can2.drawString(458, 156, datos[175])
    # else:
    #     can2.drawString(368, 156, "0")
    #     can2.drawString(458, 156, "0")
    # if fuente == 'Gasolina':
    #     can2.drawString(368, 144, datos[165])
    #     can2.drawString(458, 144, datos[176])
    # else:
    #     can2.drawString(368, 144, "0")
    #     can2.drawString(458, 144, "0")
    # if fuente == 'Kerosene':
    #     can2.drawString(368, 132, datos[166])
    #     can2.drawString(458, 132, datos[177])
    # else:
    #     can2.drawString(368, 132, "0")
    #     can2.drawString(458, 132, "0")
    # if fuente == 'Petróleo':
    #     can2.drawString(368, 120, datos[167])
    #     can2.drawString(458, 120, datos[178])
    # else:
    #     can2.drawString(368, 120, "0")
    #     can2.drawString(458, 120, "0")
    # if fuente == 'Alcohol':
    #     can2.drawString(368, 108, datos[168])
    #     can2.drawString(458, 108, datos[179])
    # else:
    #     can2.drawString(368, 108, "0")
    #     can2.drawString(458, 108, "0")
    # if fuente == 'Carbón Mineral':
    #     can2.drawString(368, 96, datos[169])
    #     can2.drawString(458, 96, datos[180])
    # else:
    #     can2.drawString(368, 96, "0")
    #     can2.drawString(458, 96, "0")
    # if fuente == 'Leña Comprada':
    #     can2.drawString(368, 84, datos[170])
    #     can2.drawString(458, 84, datos[181])
    # else:
    #     can2.drawString(368, 84, "0")
    #     can2.drawString(458, 84, "0")
    # if fuente == 'Leña Auto Apropiada':
    #     can2.drawString(368, 72, datos[171])
    #     can2.drawString(458, 72, datos[182])
    # else:
    #     can2.drawString(368, 72, "0")
    #     can2.drawString(458, 72, "0")
    # if fuente == 'Residuos del Agro':
    #     can2.drawString(368, 60, datos[172])
    #     can2.drawString(458, 60, datos[183])
    # else:
    #     can2.drawString(368, 60, "0")
    #     can2.drawString(458, 60, "0")
    # if fuente == 'Otro':
    #     can2.drawString(150, 48, datos[186])
    #     can2.drawString(260, 48, "kg")
    #     can2.drawString(368, 44, datos[173])
    #     can2.drawString(458, 44, datos[184])
    # else:
    #     can2.drawString(150, 48, datos[186])
    #     can2.drawString(260, 48, "kg")
    #     can2.drawString(368, 44, datos[173])
    #     can2.drawString(458, 44, datos[184])

    can2.save()
    #hoja 3 del pdf
    packet3 = io.BytesIO()
    # create a new PDF with Reportlab
    can3 = canvas.Canvas(packet3, pagesize=A4)
    can3.setFont("Helvetica", 9)

    can3.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can3, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can3, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can3, 487, 800, str(datos[6]),10)# Año

    if str(datos[180]) == '2': 
        can3.drawString(320, 600, "X")
    else:
        can3.drawString(368, 600, "X")

    # print(datos[181])
    if str(datos[181])=='0':
        can3.drawString(372, 505, "0")
    else:
        if str(datos[182])=='1':         
            can3.drawString(372, 505, str(datos[181]/453.592))
        elif str(datos[182])=='2':
            can3.drawString(372, 505, str(datos[181]/0.453592))
        elif str(datos[182])=='3':
            can3.drawString(372, 505, str(datos[181]/0.05))
        elif str(datos[182])=='4':
            can3.drawString(372, 505, str(datos[181]/0.025))
        elif str(datos[182])=='5':
            can3.drawString(372, 505, str(datos[181]/0.01))
        elif str(datos[182])=='6':
            can3.drawString(372, 505, str(datos[181]))

    if str(datos[202])=='0':
        can3.drawString(465, 505, "0")
    else:
        can3.drawString(465, 505, str(datos[202]))
        
        #   //Gas Natural
    if str(datos[183]) == '0':
        can3.drawString(372, 493, "0")
    else:
        can3.drawString(372, 493, str(datos[183]))          
    if str(datos[203]) == '0':
        can3.drawString(465, 493, "0")
    else:
        can3.drawString(465, 493, str(datos[203]))
        # #   //Gasolina
    if str(datos[184]) == '0':
        can3.drawString(372, 480, "0")
    else:
        if str(datos[185])=='1':
            can3.drawString(372, 480, str(datos[184]/3785.4))
        elif str(datos[185])=='2':
            can3.drawString(372, 480, str(datos[184]/3.7854))
        elif str(datos[185])=='3':
            can3.drawString(372, 480, str(datos[184]/0.5))
        elif str(datos[185])=='4':
            can3.drawString(372, 480, str(datos[184]/0.2))
        elif str(datos[185])=='5':
            can3.drawString(372, 480, str(datos[184]))

    if str(datos[204]) == '0':
        can3.drawString(465, 480, "0")
    else:
        can3.drawString(465, 480, str(datos[204]))
        #   //Kerosene
    if str(datos[186]) == '0':
        can3.drawString(372, 468, "0")
    else:
        if str(datos[187])=='1':
            can3.drawString(372, 468, str(datos[186]/3785.4))
        elif str(datos[187])=='2':
            can3.drawString(372, 468, str(datos[186]/3.7854))
        elif str(datos[187])=='3':
            can3.drawString(372, 468, str(datos[186]/0.5))
        elif str(datos[187])=='4':
            can3.drawString(372, 468, str(datos[186]/0.2))
        elif str(datos[187])=='5':
            can3.drawString(372, 468, str(datos[186]))

    if str(datos[205]) == '0':
        can3.drawString(465, 468, "0")
    else:
        can3.drawString(465, 468, str(datos[205]))
        
        #    //Petróleo
    if str(datos[188]) == '0':
        can3.drawString(372, 456, "0")
    else:
        if str(datos[189])=='1':
            can3.drawString(372, 456, str(datos[188]/3785.4))
        elif str(datos[189])=='2':
            can3.drawString(372, 456, str(datos[188]/3.7854))
        elif str(datos[189])=='3':
            can3.drawString(372, 456, str(datos[188]/0.5))
        elif str(datos[189])=='4':
            can3.drawString(372, 456, str(datos[188]/0.2))
        elif str(datos[189])=='5':
            can3.drawString(372, 456, str(datos[188]))

    if str(datos[206]) == '0':
        can3.drawString(465, 456, "0")
    else:
        can3.drawString(465, 456, str(datos[206]))

        #   //Alcohol
    if str(datos[190]) == '0':
        can3.drawString(372, 444, "0")
    else:
        if str(datos[191])=='1':
            can3.drawString(372, 444, str(datos[190]/3785.4))
        elif str(datos[191])=='2':
            can3.drawString(372, 444, str(datos[190]/3.7854))
        elif str(datos[191])=='3':
            can3.drawString(372, 444, str(datos[190]/0.5))
        elif str(datos[191])=='4':
            can3.drawString(372, 444, str(datos[190]/0.2))
        elif str(datos[191])=='5':
            can3.drawString(372, 444, str(datos[190]))

    if str(datos[207]) == '0':
        can3.drawString(465, 444, "0")
    else:
        can3.drawString(465, 444, str(datos[207]))

        
        
        #   //Carbón Mineral
    if str(datos[192]) == '0':
        can3.drawString(372, 432, "0")
    else:
        if str(datos[193])=='1':
            can3.drawString(372, 432, str(datos[192]/0.08))
        elif str(datos[193])=='2':
            can3.drawString(372, 432, str(datos[192]/2.204624))
        elif str(datos[193])=='3':
            can3.drawString(372, 432, str(datos[192]/0.04))
        elif str(datos[193])=='4':
            can3.drawString(372, 432, str(datos[192]/0.02))
        elif str(datos[193])=='5':
            can3.drawString(372, 432, str(datos[192]/0.033))
        elif str(datos[193])=='6':
            can3.drawString(372, 432, str(datos[192]/0.14285))
        elif str(datos[193])=='7':
            can3.drawString(372, 432, str(datos[192]/0.125))
        elif str(datos[193])=='8':
            can3.drawString(372, 432, str(datos[192]))

    if str(datos[208]) == '0':
        can3.drawString(465, 432, "0")
    else:
        can3.drawString(465, 432, str(datos[208]))

    
        #  //Leña Comprada
    if str(datos[194]) == '0':
        can3.drawString(372, 420, "0")
    else:
        if str(datos[195])=='1':
            can3.drawString(372, 420, str(datos[194]/0.08))
        elif str(datos[195])=='2':
            can3.drawString(372, 420, str(datos[194]/2.204624))
        elif str(datos[195])=='3':
            can3.drawString(372, 420, str(datos[194]/0.05555))
        elif str(datos[195])=='4':
            can3.drawString(372, 420, str(datos[194]/0.04))
        elif str(datos[195])=='5':
            can3.drawString(372, 420, str(datos[194]/0.2))
        elif str(datos[195])=='6':
            can3.drawString(372, 420, str(datos[194]/0.1))
        elif str(datos[195])=='7':
            can3.drawString(372, 420, str(datos[194]/0.04))
        elif str(datos[195])=='8':
            can3.drawString(372, 420, str(datos[194]))


    if str(datos[209]) == '0':
        can3.drawString(465, 420, "0")
    else: 
        can3.drawString(465, 420, str(datos[209]))

           
        #   //Leña AutoApropiada
         
    if str(datos[196]) == '0':
        can3.drawString(372, 408, "0")
    else:
        if str(datos[197])=='1':
            can3.drawString(372, 408, str(datos[196]/0.08))
        elif str(datos[197])=='2':
            can3.drawString(372, 408, str(datos[196]/2.204624))
        elif str(datos[197])=='3':
            can3.drawString(372, 408, str(datos[196]/0.05555))
        elif str(datos[197])=='4':
            can3.drawString(372, 408, str(datos[196]/0.04))
        elif str(datos[197])=='5':
            can3.drawString(372, 408, str(datos[196]/0.2))
        elif str(datos[197])=='6':
            can3.drawString(372, 408, str(datos[196]/0.1))
        elif str(datos[197])=='7':
            can3.drawString(372, 408, str(datos[196]/0.04))
        elif str(datos[197])=='8':
            can3.drawString(372, 408, str(datos[196]))

    if str(datos[210]) == '0':
        can3.drawString(465, 408, "0")
    else:
        can3.drawString(465, 408, str(datos[210]))

        #   //Residuos del Agro

    if str(datos[198]) == '0':
        can3.drawString(372, 396, "0")
    else:
        if(datos[199])=='1':
            can3.drawString(372, 396, str(datos[198]/0.08))
        elif str(datos[199])=='2':
            can3.drawString(372, 396, str(datos[198]/2.204624))
        elif str(datos[199])=='3':
            can3.drawString(372, 396, str(datos[198]/0.08333))
        elif str(datos[199])=='4':
            can3.drawString(372, 396, str(datos[198]/0.0555))
        elif str(datos[199])=='5':
            can3.drawString(372, 396, str(datos[198]/0.125))
        elif str(datos[199])=='6':
            can3.drawString(372, 396, str(datos[198]))
        elif str(datos[199])=='7':
            can3.drawString(372, 396, str(datos[198]))

    if str(datos[211]) == '0':
        can3.drawString(465, 396, "0")
    else:
        can3.drawString(465, 396, str(datos[211]))

        # //otro
    if str(datos[200]) == '0':
        can3.drawString(372, 384, "0")
    else:
        can3.drawString(372, 384, str(datos[200]))

    can3.drawString(280, 384, str(datos[201]))

    if str(datos[212]) == '0':
        can3.drawString(465, 384, "0")
    else:
        can3.drawString(465, 384, str(datos[212]))

    can3.drawString(280, 384, str(datos[214]))


        #   //Baterias
    if str(datos[215]) == '0':
        can3.drawString(298, 264, "0")
    else:
        if str(datos[216])=='1':
            can3.drawString(298, 264, str(datos[215]/33.33333))
        elif str(datos[216])=='2':
            can3.drawString(298, 264, str(datos[215]/0.0734873))
        elif str(datos[216])=='3':
            can3.drawString(298, 264, str(datos[215]))

    if str(datos[231]) == '0':
        can3.drawString(365, 264, "0")
    else:
        can3.drawString(365, 264, str(datos[231]))

        #   //Gasolina
    if str(datos[217]) == '0':
        can3.drawString(298, 252, "0")
    else:
        if str(datos[218])=='1':
            can3.drawString(298, 252, str(datos[217]/3785.4))
        elif str(datos[218])=='2':
            can3.drawString(298, 252, str(datos[217]/3.7854))
        elif str(datos[218])=='3':
            can3.drawString(298, 252, str(datos[217]/0.5))
        elif str(datos[218])=='4':
            can3.drawString(298, 252, str(datos[217]/0.2))
        elif str(datos[218])=='5':
            can3.drawString(298, 252, str(datos[217]))

    if str(datos[232]) == '0':
        can3.drawString(365, 252, "0")
    else:
        can3.drawString(365, 252, str(datos[232]))

        #   //Kerosene
    if str(datos[219]) == '0':
        can3.drawString(298, 240, "0")
    else:
        if str(datos[220])=='1':
            can3.drawString(298, 240, str(datos[219]/3785.4))
        elif str(datos[220])=='2':
            can3.drawString(298, 240, str(datos[219]/3.7854))
        elif str(datos[220])=='3':
            can3.drawString(298, 240, str(datos[219]/0.5))
        elif str(datos[220])=='4':
            can3.drawString(298, 240, str(datos[219]/0.2))
        elif str(datos[220])=='5':
            can3.drawString(298, 240, str(datos[219]))


    if str(datos[233]) == '0':
        can3.drawString(365, 240, "0")
    else: 
        can3.drawString(365, 240, str(datos[233]))


        
        #    //Petróleo
    if str(datos[221]) == '0':
        can3.drawString(298, 227, "0")
    else:
        if str(datos[222])=='1':
            can3.drawString(298, 227, str(datos[221]/3785.4))
        elif str(datos[222])=='2':
            can3.drawString(298, 227, str(datos[221]/3.7854))
        elif str(datos[222])=='3':
            can3.drawString(298, 227, str(datos[221]/0.5))
        elif str(datos[222])=='4':
            can3.drawString(298, 227, str(datos[221]/0.2))
        elif str(datos[222])=='5':
            can3.drawString(298, 227, str(datos[221]))

    if str(datos[234]) == '0':
        can3.drawString(365, 227, "0")
    else:
        can3.drawString(365, 227, str(datos[234]))


        #   //Alcohol
    if str(datos[223]) == '0':
        can3.drawString(298, 214, "0")
    else:
        if str(datos[224])=='1':
            can3.drawString(298, 214, str(datos[233]/3785.4))
        elif str(datos[224])=='2':
            can3.drawString(298, 214, str(datos[233]/3.7854))
        elif str(datos[224])=='3':
            can3.drawString(298, 214, str(datos[233]/0.5))
        elif str(datos[224])=='4':
            can3.drawString(298, 214, str(datos[233]/0.2))
        elif str(datos[224])=='5':
            can3.drawString(298, 214, str(datos[233]))

    if str(datos[235]) == '0':
        can3.drawString(365, 214, "0")
    else:
        can3.drawString(365, 214, str(datos[235]))


        #   //Diésel
    if  str(datos[225]) == '0':
        can3.drawString(298, 202, "0")
    else:
        if str(datos[226])=='1':
            can3.drawString(298, 202, str(datos[225]/3785.4))
        elif str(datos[226])=='2':
            can3.drawString(298, 202, str(datos[225]/3.7854))
        elif str(datos[226])=='3':
            can3.drawString(298, 202, str(datos[225]/0.5))
        elif str(datos[226])=='4':
            can3.drawString(298, 202, str(datos[225]/0.2))
        elif str(datos[226])=='5':
            can3.drawString(298, 202, str(datos[225]))
            
    if str(datos[236]) == '0':
        can3.drawString(365, 202, "0")
    else:
        can3.drawString(365, 202, str(datos[236]))



        #   //Velas
    if str(datos[227]) == '0':
        can3.drawString(298, 190, "0")
    else:
        if str(datos[228])=='1':
            can3.drawString(298, 190, str(datos[227]/33.33333))
        elif str(datos[228])=='2':
            can3.drawString(298, 190, str(datos[227]/0.0734873))
        elif str(datos[228])=='3':
            can3.drawString(298, 190, str(datos[227]/0.3333))
        elif str(datos[228])=='4':
            can3.drawString(298, 190, str(datos[227]))

    if str(datos[237]) == '0':
        can3.drawString(365, 190, "0")
    else: 
        can3.drawString(365, 190, str(datos[237]))

        #   //otro
    if str(datos[229]) == '0':
        can3.drawString(298, 177, "0")
    else:
        can3.drawString(298, 177, str(datos[229]))

    if str(datos[238]) == '0':
        can3.drawString(365, 177, "0")
    else:
        can3.drawString(365, 177, str(datos[238]))

    can3.drawString(120, 177, str(datos[247]))

         # //localización
    if str(datos[239]) == '1':
        can3.drawString(414, 264, "X")
    elif str(datos[239]) == '2':
        can3.drawString(465, 264, "X")
    elif str(datos[239]) == '3':
        can3.drawString(502, 264, "X")

    if str(datos[240]) == '1':
        can3.drawString(414, 252, "X")
    elif str(datos[240]) == '2':
        can3.drawString(465, 252, "X")
    elif str(datos[240]) == '3':
        can3.drawString(502, 252, "X")

    if str(datos[241]) == '1':
        can3.drawString(414, 240, "X")
    elif str(datos[241]) == '2':
        can3.drawString(465, 240, "X")
    elif str(datos[241]) == '3':
        can3.drawString(502, 240, "X")

    if str(datos[242]) == '1':
        can3.drawString(414, 227, "X")
    elif str(datos[242]) == '2':
        can3.drawString(465, 227, "X")
    elif str(datos[242]) == '3':
        can3.drawString(502, 227, "X")

    if str(datos[243]) == '1':
        can3.drawString(414, 214, "X")
    elif str(datos[243]) == '2':
        can3.drawString(465, 214, "X")
    elif str(datos[243]) == '3':
        can3.drawString(502, 214, "X")

    if str(datos[244]) == '1':
        can3.drawString(414, 202, "X")
    elif str(datos[244]) == '2':
        can3.drawString(465, 202, "X")
    elif str(datos[244]) == '3':
        can3.drawString(502, 202, "X")

    if str(datos[245]) == '1':
        can3.drawString(414, 190, "X")
    elif str(datos[245]) == '2':
        can3.drawString(465, 190, "X")
    elif str(datos[245]) == '3':
        can3.drawString(502, 190, "X")

    if str(datos[246]) == '1':
        can3.drawString(414, 177, "X")
    elif str(datos[246]) == '2':
        can3.drawString(465, 177, "X")
    elif str(datos[246]) == '3':
        can3.drawString(502, 177, "X")


    if str(datos[285].decode("utf-8")) == '1':
        can3.drawString(320, 86, "X")
    elif str(datos[285]) == '2':
        can3.drawString(320, 72, "X")


    if str(datos[286]) == '0':
        can3.drawString(430, 54, "0")
    else:
        if str(datos[286]) < '1000':
            can3.drawString(430, 54, str(datos[286]* 1000))
        else:
            can3.drawString(430, 54, str(datos[286]))
    
            

    can3.save()
    #hoja 4 del pdf
    packet4 = io.BytesIO()
    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet4, pagesize=A4)
    can4.setFont("Helvetica", 9)

    can4.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can4, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can4, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can4, 487, 800, str(datos[6]),10)# Año
    #estrato del predio

            #   //tiene
    if  str(datos[249])== 'null':
        can4.drawString(352, 692, "0")
    else:
        can4.drawString(352, 692, str(datos[249]))

    if str(datos[250]) == 'null':
        can4.drawString(352, 680, "0")
    else:
        can4.drawString(352, 680, str(datos[250]))

    if str(datos[251]) == 'null':
        can4.drawString(352, 668, "0")
    else:
        can4.drawString(352, 668, str(datos[251]))

    if str(datos[252]) == 'null':
        can4.drawString(352, 656, "0")
    else:
        can4.drawString(352, 656, str(datos[252]))

    if str(datos[253]) == 'null':
        can4.drawString(352, 644, "0")
    else:
        can4.drawString(352, 644, str(datos[253]))

    if str(datos[254]) == 'null':
        can4.drawString(352, 632, "0")
    else:
        can4.drawString(352, 632, str(datos[254]))

    if str(datos[255]) == 'null':
        can4.drawString(352, 620, "0")
    else:
        can4.drawString(352, 620, str(datos[255]))

    if str(datos[256]) == 'null':
        can4.drawString(352, 608, "0")
    else:
        can4.drawString(352, 608, str(datos[256]))

    if str(datos[257]) == 'null':
        can4.drawString(352, 596, "0")
    else:
        can4.drawString(352, 596, str(datos[257]))

    if str(datos[258]) == 'null':
        can4.drawString(352, 584, "0")
    else:
        can4.drawString(352, 584, str(datos[258]))

    if str(datos[259]) == 'null':
        can4.drawString(352, 572, "0")
    else:
        can4.drawString(352, 572, str(datos[259]))

    if str(datos[260]) == 'null':
        can4.drawString(352, 560, "0")
    else:
        can4.drawString(352, 560, str(datos[260]))

    if str(datos[261]) == 'null':
        can4.drawString(352, 548, "0")
    else:
        can4.drawString(352, 548, str(datos[261]))

    if str(datos[262]) == 'null':
        can4.drawString(352, 536, "0")
    else:
        can4.drawString(352, 536, str(datos[262]))

    if str(datos[263]) == 'null':
        can4.drawString(352, 524, "0")
    else:
        can4.drawString(352, 524, str(datos[263]))

    
        #   //necesita
    if str(datos[264]) == 'null':
        can4.drawString(440, 692, "0")
    else:
        can4.drawString(440, 692, str(datos[264]))
          
    if str(datos[265]) == 'null':
        can4.drawString(440, 680, "0")
    else:
        can4.drawString(440, 680, str(datos[265]))

    if str(datos[266]) == 'null':
        can4.drawString(440, 668, "0")
    else:
        can4.drawString(440, 668, str(datos[266]))

    if str(datos[267]) == 'null':
        can4.drawString(440, 656, "0")
    else:
        can4.drawString(440, 656, str(datos[267]))

    if str(datos[268]) == 'null':
        can4.drawString(440, 644, "0")
    else:
        can4.drawString(440, 644, str(datos[268]))

    if str(datos[269]) == 'null':
        can4.drawString(440, 632, "0")
    else:
        can4.drawString(440, 632, str(datos[269]))

    if str(datos[270]) == 'null':
        can4.drawString(440, 620, "0")
    else:
        can4.drawString(440, 620, str(datos[270]))

    if str(datos[271]) == 'null':
        can4.drawString(440, 608, "0")
    else:
        can4.drawString(440, 608, str(datos[271]))

    if str(datos[272]) == 'null':
        can4.drawString(440, 596, "0")
    else:
        can4.drawString(440, 596, str(datos[272]))
    
    if str(datos[273]) == 'null':
        can4.drawString(440, 584, "0")
    else:
        can4.drawString(440, 584, str(datos[273]))

    if str(datos[274]) == 'null':
        can4.drawString(440, 572, "0")
    else:
        can4.drawString(440, 572, str(datos[274]))

    if str(datos[275]) == 'null':
        can4.drawString(440, 560, "0")
    else:
        can4.drawString(440, 560, str(datos[275]))

    if str(datos[276]) == 'null':
        can4.drawString(440, 548, "0")
    else:
        can4.drawString(440, 548, str(datos[276]))

    if str(datos[277]) == 'null':
        can4.drawString(440, 536, "0")
    else:
        can4.drawString(440, 536, str(datos[277]))

    if str(datos[278]) == 'null':
        can4.drawString(440, 524, "0")
    else:
        can4.drawString(440, 524, str(datos[278]))

    if str(datos[279]) == 'null' or str(datos[279]) == None:
        can4.drawString(200, 524, "-")
    else:
        can4.drawString(200, 524, str(datos[279]))


    if str(datos[280].decode("utf-8")) == '1':
        can4.drawString(382, 372, "X")
    elif str(datos[280].decode("utf-8")) == '2':
        can4.drawString(432, 372, "X")

    if str(datos[281].decode("utf-8")) == '1':
        can4.drawString(382, 358, "X")
    elif str(datos[281].decode("utf-8")) == '2':
        can4.drawString(432, 358, "X")


    if str(datos[282].decode("utf-8")) == '1':
        can4.drawString(320, 287, "X")
    elif str(datos[282].decode("utf-8")) == '2':
        can4.drawString(320, 275, "X")
    
    if str(datos[283]) == 'undefined' or str(datos[283]) == 'null' or str(datos[283]) == None:
        can4.drawString(90, 228, "No Aplica")
    else:
        can4.drawString(90, 228, datos[283])

    if str(datos[284].decode("utf-8")) == 'undefined' or str(datos[284].decode("utf-8")) == 'null' or str(datos[284].decode("utf-8")) == 'N' or str(datos[284].decode("utf-8")) == '2' or str(datos[284].decode("utf-8")) == None:
        can4.drawString(320, 120, "X")
    elif str(datos[284].decode("utf-8")) == '1':
        can4.drawString(368, 120, "X")



    can4.save()
    #hoja 5 del pdf
    packet5 = io.BytesIO()
    # create a new PDF with Reportlab
    can5 = canvas.Canvas(packet5, pagesize=A4)
    can5.setFont("Helvetica", 9)

    can5.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can5, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can5, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can5, 487, 800, str(datos[6]),10)# Año

    
    if str(datos[89]) == '1':
        can5.drawString(412, 705, "X")
    elif str(datos[89]) == '2':
        can5.drawString(412, 695, "X")
    elif str(datos[89]) == '3':
        can5.drawString(412, 683, "X")
    elif str(datos[89]) == '4' or str(datos[89]) == '4':
        can5.drawString(412, 672, "X")

    if str(datos[90]) == '1':
        can5.drawString(260, 605, "X")
    elif str(datos[90]) == '2':
        can5.drawString(280, 605, "X")
    elif str(datos[90]) == '3':
        can5.drawString(310, 605, "X")
    elif str(datos[90]) == '4':
        can5.drawString(330, 605, "X")
    elif str(datos[90]) == '5':
        can5.drawString(350, 605, "X")
    elif str(datos[90]) == '6':
        can5.drawString(376, 605, "X")


    if str(datos[123]) == 'undefined' or str(datos[123]) == 'null':
        can5.drawString(90, 525, "No Aplica")
    else:
        can5.drawString(90, 525, datos[123])


    if str(datos[124]) == '1':
        can5.drawString(404, 445, "X")
    elif str(datos[124]) == '2':
        can5.drawString(404, 433, "X")
    elif str(datos[124]) == '3':
        can5.drawString(404, 421, "X")
    elif str(datos[124]) == '4':
        can5.drawString(404, 409, "X")
    elif str(datos[124]) == '5':
        can5.drawString(404, 397, "X")
    elif str(datos[124]) == '6':
        can5.drawString(404, 382, "X")
    elif str(datos[124]) == '7':
        can5.drawString(404, 366, "X")
    elif str(datos[124]) == '8':
        can5.drawString(404, 350, "X")
    elif str(datos[124]) == '9':
        can5.drawString(404, 339, "X")
    elif str(datos[124]) == '10':
        can5.drawString(404, 328, "X")


    if str(datos[125]) == '1':
        can5.drawString(350, 268, "X")
    elif str(datos[125]) == '2':
        can5.drawString(350, 256, "X")
    elif str(datos[125]) == '3':
        can5.drawString(350, 244, "X")


    if str(datos[126]) == 'null' or str(datos[126]) == 'undefined':
        can5.drawString(340, 184, "00")
    else:
        can5.drawString(340, 184, str(datos[126]))

    if str(datos[127]) == 'null' or str(datos[127]) == 'undefined':
        can5.drawString(340, 142, "00")
    else:
        can5.drawString(340, 142, str(datos[127]))


    if str(datos[128]) == '1':
        can5.drawString(420, 68, "X")
    elif str(datos[128]) == '2':
        can5.drawString(420, 56, "X")
    elif str(datos[128]) == '3':
        can5.drawString(420, 42, "X")


    can5.save()
    #hoja 6 del pdf
    packet6 = io.BytesIO()
    # create a new PDF with Reportlab
    can6 = canvas.Canvas(packet6, pagesize=A4)
    can6.setFont("Helvetica", 9)

    can6.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can6, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can6, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can6, 487, 800, str(datos[6]),10)# Año

    if str(datos[128]) == '4':
        can6.drawString(420, 780, "X")
    elif str(datos[128]) == '5':
        can6.drawString(420, 768, "X")
    elif str(datos[128]) == '6':
        can6.drawString(420, 756, "X")
    elif str(datos[128]) == '7':
        can6.drawString(420, 744, "X")
    elif str(datos[128]) == '8':
        can6.drawString(420, 732, "X")

    if str(datos[129]) == '1':
        can6.drawString(420, 664, "X")
    elif str(datos[129]) == '2':
        can6.drawString(420, 652, "X")
    elif str(datos[129]) == '3':
        can6.drawString(420, 640, "X")
    elif str(datos[129]) == '4':
        can6.drawString(420, 628, "X")


    
    if str(datos[130]) == '1':
        can6.drawString(415, 540, "X")
    elif str(datos[130]) == '2':
        can6.drawString(415, 528, "X")
    elif str(datos[130]) == '3':
        can6.drawString(415, 516, "X")
    elif str(datos[130]) == '4':
        can6.drawString(415, 504, "X")
    elif str(datos[130]) == '5':
        can6.drawString(415, 492, "X")
    elif str(datos[130]) == '6':
        can6.drawString(415, 480, "X")

    if str(datos[131].decode("utf-8")) == '1':
        can6.drawString(380, 425, "X")
    elif str(datos[131].decode("utf-8")) == '2':
        can6.drawString(425, 425, "X")

    if str(datos[132].decode("utf-8")) == '1':
        can6.drawString(380, 413, "X")
    elif str(datos[132].decode("utf-8")) == '2':
        can6.drawString(425, 413, "X")

    if str(datos[133].decode("utf-8")) == '1':
        can6.drawString(380, 401, "X")
    elif str(datos[133].decode("utf-8")) == '2':
        can6.drawString(425, 401, "X")

    if str(datos[134].decode("utf-8")) == '1':
        can6.drawString(380, 389, "X")
    elif str(datos[134].decode("utf-8")) == '2':
        can6.drawString(425, 389, "X")

    if str(datos[293]) == 'true':
        can6.drawString(400, 288, "X")
    elif str(datos[294]) == 'true':
        can6.drawString(400, 276, "X")
    elif str(datos[295]) == 'true':
        can6.drawString(400, 264, "X")
    elif str(datos[296]) == 'true':
        can6.drawString(400, 252, "X")
    elif str(datos[297]) == 'true':
        can6.drawString(400, 240, "X")
    elif str(datos[298]) == 'true':
        can6.drawString(400, 228, "X")

    if str(datos[299]) == 'true':
        can6.drawString(295, 148, "X")
    elif str(datos[301]) == 'true':
        can6.drawString(295, 136, "X")
    elif str(datos[302]) == 'true':
        can6.drawString(295, 124, "X")
    elif str(datos[303]) == 'true':
        can6.drawString(295, 112, "X")
    elif str(datos[304]) == 'true':
       can6.drawString(295, 100, "X")
    elif str(datos[305]) == 'true':
        can6.drawString(295, 88, "X")
    elif str(datos[306]) == 'true':
        can6.drawString(295, 76, "X")
    elif str(datos[307]) == 'true':
        can6.drawString(295, 62, "X")

    if str(datos[300].decode("utf-8")) == 'null' or str(datos[300].decode("utf-8")) == 'undefined':
        can6.drawString(468, 148, "X")
    elif str(datos[300].decode("utf-8")) == '1':
        can6.drawString(502, 148, "X")
    elif str(datos[300].decode("utf-8")) == '2':
        can6.drawString(468, 148, "X")
    

    can6.save()
    #hoja 7 del pdf
    packet7 = io.BytesIO()
    # create a new PDF with Reportlab
    can7 = canvas.Canvas(packet7, pagesize=A4)
    can7.setFont("Helvetica", 9)

    can7.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can7, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can7, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can7, 487, 800, str(datos[6]),10)# Año

    
    if str(datos[308]) == 'true':
        can7.drawString(405, 740, "X")
    elif str(datos[309]) == 'true':
        can7.drawString(405, 728, "X")
    elif str(datos[310]) == 'true':
        can7.drawString(405, 716, "X")
    elif str(datos[311]) == 'true':
        can7.drawString(405, 704, "X")
    elif str(datos[312]) == 'true':
        can7.drawString(405, 692, "X")
    elif str(datos[313]) == '-':
        can7.drawString(250, 680, str(datos[313]))
    else:
        can7.drawString(405, 680, "X")
        can7.drawString(250, 680, str(datos[313]))

    if str(datos[314]) == '1':
        can7.drawString(405, 620, "X")
    elif (datos[314]) == '2':
        can7.drawString(405, 608, "X")
    elif (datos[314]) == '3':
        can7.drawString(405, 596, "X")

    if str(datos[13]) == '1':
        can7.drawString(388, 480, "X")
    elif str(datos[13]) == '2':
        can7.drawString(388, 468, "X")
    elif str(datos[13]) == '3':
        can7.drawString(388, 456, "X")
    elif str(datos[13]) == '4':
        can7.drawString(388, 444, "X")
    elif str(datos[13]) == '5':
        can7.drawString(388, 432, "X")
    elif str(datos[13]) == '6':
        can7.drawString(388, 420, "X")
    elif str(datos[13]) == '7': 
        can7.drawString(388, 408, "X")
    elif str(datos[13]) == '8':
        can7.drawString(388, 396, "X")
    elif str(datos[13]) == '9':
        can7.drawString(388, 384, "X")
    elif str(datos[13]) == '10':
        can7.drawString(388, 372, "X")
    elif str(datos[13]) == '11':
        can7.drawString(388, 360, "X")

    if str(datos[14]) == 'null' or str(datos[14]) == 'undefined':
       can7.drawString(358, 327, "00")
    else:
        can7.drawString(358, 327, str(datos[14]))

    if str(datos[15]) == '1':
        can7.drawString(391, 260, "X")
    elif str(datos[15]) == '2':
        can7.drawString(391, 246, "X")
          
    if str(datos[16]) == '1':
        can7.drawString(391, 192, "X")
    elif str(datos[16]) == '2':
        can7.drawString(391, 180, "X")
    elif str(datos[16]) == '3':
        can7.drawString(391, 168, "X")


        #   //edad mujer
    if str(datos[17]) == 'null' or str(datos[17]) == 'undefined':
        can7.drawString(290, 96, "0")
    else:
        can7.drawString(290, 96, str(datos[17]))
    if str(datos[18]) == 'null' or str(datos[18]) == 'undefined':
        can7.drawString(290, 84, "0")
    else:
        can7.drawString(290, 84, str(datos[18]))
    if str(datos[19]) == 'null' or str(datos[19]) == 'undefined':
        can7.drawString(290, 72, "0")
    else:
        can7.drawString(290, 72, str(datos[19]))
    if str(datos[20]) == 'null' or str(datos[20]) == 'undefined':
        can7.drawString(290, 60, "0")
    else:
        can7.drawString(290, 60, str(datos[20]))
    if str(datos[21]) == 'null' or str(datos[21]) == 'undefined':
        can7.drawString(290, 48, "0")
    else:
        can7.drawString(290, 48, str(datos[21]))

        #   //edad hombre

    if str(datos[22]) == 'null' or str(datos[22]) == 'undefined':
        can7.drawString(345, 96, "0")
    else:
        can7.drawString(345, 96, str(datos[22]))
    if str(datos[23]) == 'null' or str(datos[23]) == 'undefined':
        can7.drawString(345, 84, "0")
    else:
        can7.drawString(345, 84, str(datos[23]))

    if str(datos[24]) == 'null' or str(datos[24]) == 'undefined':
        can7.drawString(345, 72, "0")
    else:
        can7.drawString(345, 72, str(datos[24]))
    if str(datos[25]) == 'null' or str(datos[25]) == 'undefined':
        can7.drawString(345, 60, "0")
    else:
        can7.drawString(345, 60, str(datos[25]))

    if str(datos[26]) == 'null' or str(datos[26]) == 'undefined':
        can7.drawString(345, 48, "0")
    else:
        can7.drawString(345, 48, str(datos[26]))

        #   //edad otro

    if str(datos[27]) == 'null' or str(datos[27]) == 'undefined':
        can7.drawString(391, 96, "0")
    else:
        can7.drawString(391, 96, str(datos[27]))
    if str(datos[28]) == 'null' or str(datos[28]) == 'undefined':
        can7.drawString(391, 84, "0")
    else:
        can7.drawString(391, 84, str(datos[28]))
    if str(datos[29]) == 'null' or str(datos[29]) == 'undefined':
        can7.drawString(391, 72, "0")
    else :
        can7.drawString(391, 72, str(datos[29]))
    if str(datos[30]) == 'null' or str(datos[30]) == 'undefined':
        can7.drawString(391, 60, "0")
    else:
        can7.drawString(391, 60, str(datos[30]))
    if str(datos[31]) == 'null' or str(datos[31]) == 'undefined':
        can7.drawString(391, 48, "0")
    else:
        can7.drawString(391, 48,str(datos[31]))

    can7.save()
    #hoja 8 del pdf
    packet8 = io.BytesIO()
    # create a new PDF with Reportlab
    can8 = canvas.Canvas(packet8, pagesize=A4)
    can8.setFont("Helvetica", 9)

    can8.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can8, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can8, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can8, 487, 800, str(datos[6]),10)# Año

    if str(datos[32]) == '1':
        can8.drawString(385, 740, "X")
    elif str(datos[32]) == '2':
        can8.drawString(385, 728, "X")
    elif str(datos[32]) == '3':
        can8.drawString(385, 716, "X")
    elif str(datos[32]) == '4': 
        can8.drawString(385, 704, "X")
    elif str(datos[32]) == '5':
        can8.drawString(385, 692, "X")
    elif str(datos[32]) == '6':
        can8.drawString(385, 680, "X")
    elif str(datos[32]) == '7':
        can8.drawString(385, 668, "X")
    elif str(datos[32]) == '8':
        can8.drawString(385, 656, "X")


    if str(datos[33].decode("utf-8")) == '1':
        can8.drawString(320, 605, "X")
    elif str(datos[33].decode("utf-8")) == '2':
        can8.drawString(368, 605, "X")

    if str(datos[34])== '1':
        can8.drawString(385, 525, "X")
    elif str(datos[34]) == '2':
        can8.drawString(385, 513, "X")
    elif str(datos[34]) == '3':
        can8.drawString(385, 501, "X")
    elif str(datos[34]) == '4':
        can8.drawString(385, 489, "X")
    elif str(datos[34]) == '5':
        can8.drawString(385, 477, "X")
    elif str(datos[34]) == '6':
        can8.drawString(385, 465, "X")


    if str(datos[35]) == '1':
        can8.drawString(405, 384, "X")
    elif str(datos[35]) == '2':
        can8.drawString(405, 372, "X")
    elif str(datos[35]) == '3':
        can8.drawString(405, 360, "X")
    elif str(datos[35]) == '4':
        can8.drawString(405, 348, "X")
    elif str(datos[35]) == '5':
        can8.drawString(405, 336, "X")
    elif str(datos[35]) == '6':
        can8.drawString(405, 324, "X")

    if str(datos[36]) == '1':
        can8.drawString(320, 263, "X")
    elif str(datos[36]) == '2':
        can8.drawString(368, 263, "X")

    if str(datos[37]) == '1':
        can8.drawString(320, 201, "X")
    elif str(datos[37]) == '2':
        can8.drawString(320, 186, "X")

    if str(datos[38]) == 'undefined' or str(datos[38]) == 'null':
        can8.drawString(90, 150, 'No Aplica')
    else:
        can8.drawString(90, 150, str(datos[38]))
        
    if str(datos[39].decode("utf-8")) == '1':
        can8.drawString(320, 62, "X")
    elif str(datos[39].decode("utf-8")) == '2':
        can8.drawString(368, 62, "X")


    # can8.drawString(110, 758, datos[336]);

    # if datos[337] == "None" or datos[337] == None:
    #    can8.drawString(320, 720, " ")
    # else:
    #     can8.drawString(320, 720, datos[337]);
    # # can8.drawString(320, 720, datos[337]);
    # if datos[338] == "None" or datos[338] == None:
    #     can8.drawString(438, 695," ")
    # else:
    #     can8.drawString(438, 695, datos[338]);
    # # can8.drawString(438, 695, datos[338]);
    # if datos[339] == "None" or datos[339] == None:
    #     can8.drawString(356, 651," ")
    # else:
    #     can8.drawString(356, 651, datos[339]);
    # # can8.drawString(356, 651, datos[339]);

    # can8.drawString(360, 625, datos[340]);

    # can8.drawString(360, 595, datos[341]);

    # can8.drawString(360, 567, datos[342]);

    # can8.drawString(378, 540, datos[343]);

    # can8.drawString(380, 505, datos[344]);
    
    # can8.drawString(360, 478, datos[346]);

    # can8.drawString(385, 450, datos[348]);

    # can8.drawString(340, 423, datos[350]);

    # can8.drawString(360, 390, datos[351]);

    # can8.drawString(360, 365, datos[352]);
    
    # if datos[13] == "None" or datos[13] == None:
    #      can8.drawString(97 , 204," ")
    # else:
    #     familia = (json.loads(datos[13]))
    #     for i in range(len(familia)):
    #         integrante = dict(familia[i])
    #         if integrante['Parentesco'] == 'Jefe (a) de hogar':
    #             can8.drawString(97 , 204, 'x')
    #             can8.drawString(195, 204, integrante['Genero'])
    #             can8.drawString(244, 204, str(integrante['Edad']))
    #             can8.drawString(288, 204, integrante['Registro'])
    #             can8.drawString(324, 204, integrante['Escolaridad'])
    #             can8.drawString(434, 204, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Pareja, Esposo(a), cónyuge, compañero(a)':
    #             can8.drawString(97 , 185, 'x')
    #             can8.drawString(195, 185, integrante['Genero'])
    #             can8.drawString(244, 185, str(integrante['Edad']))
    #             can8.drawString(288, 185, integrante['Registro'])
    #             can8.drawString(324, 185, integrante['Escolaridad'])
    #             can8.drawString(434, 185, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)':
    #             can8.drawString(97 , 171, 'x')
    #             can8.drawString(195, 171, integrante['Genero'])
    #             can8.drawString(244, 171, str(integrante['Edad']))
    #             can8.drawString(288, 171, integrante['Registro'])
    #             can8.drawString(324, 171, integrante['Escolaridad'])
    #             can8.drawString(434, 171, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 2':
    #             can8.drawString(97 , 159, 'x')
    #             can8.drawString(195, 159, integrante['Genero'])
    #             can8.drawString(244, 159, str(integrante['Edad']))
    #             can8.drawString(288, 159, integrante['Registro'])
    #             can8.drawString(324, 159, integrante['Escolaridad'])
    #             can8.drawString(434, 159, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 3':
    #             can8.drawString(97 , 147, 'x')
    #             can8.drawString(195, 147, integrante['Genero'])
    #             can8.drawString(244, 147, str(integrante['Edad']))
    #             can8.drawString(288, 147, integrante['Registro'])
    #             can8.drawString(324, 147, integrante['Escolaridad'])
    #             can8.drawString(434, 147, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 4':
    #             can8.drawString(97 , 132, 'x')
    #             can8.drawString(195, 132, integrante['Genero'])
    #             can8.drawString(244, 132, str(integrante['Edad']))
    #             can8.drawString(288, 132, integrante['Registro'])
    #             can8.drawString(324, 132, integrante['Escolaridad'])
    #             can8.drawString(434, 132, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 5':
    #             can8.drawString(97 , 119, 'x')
    #             can8.drawString(195, 119, integrante['Genero'])
    #             can8.drawString(244, 119, str(integrante['Edad']))
    #             can8.drawString(288, 119, integrante['Registro'])
    #             can8.drawString(324, 119, integrante['Escolaridad'])
    #             can8.drawString(434, 119, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Nieto(a)':
    #             can8.drawString(97 , 106, 'x')
    #             can8.drawString(195, 106, integrante['Genero'])
    #             can8.drawString(244, 106, str(integrante['Edad']))
    #             can8.drawString(288, 106, integrante['Registro'])
    #             can8.drawString(324, 106, integrante['Escolaridad'])
    #             can8.drawString(434, 106, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Suegro(a)':
    #             can8.drawString(97 , 94, 'x')
    #             can8.drawString(195, 94, integrante['Genero'])
    #             can8.drawString(244, 94, str(integrante['Edad']))
    #             can8.drawString(288, 94, integrante['Registro'])
    #             can8.drawString(324, 94, integrante['Escolaridad'])
    #             can8.drawString(434, 94, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Tios(as)':
    #             can8.drawString(97 , 81, 'x')
    #             can8.drawString(195, 81, integrante['Genero'])
    #             can8.drawString(244, 81, str(integrante['Edad']))
    #             can8.drawString(288, 81, integrante['Registro'])
    #             can8.drawString(324, 81, integrante['Escolaridad'])
    #             can8.drawString(434, 81, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Yerno, nuera':
    #             can8.drawString(97 , 69, 'x')
    #             can8.drawString(195, 69, integrante['Genero'])
    #             can8.drawString(244, 69, str(integrante['Edad']))
    #             can8.drawString(288, 69, integrante['Registro'])
    #             can8.drawString(324, 69, integrante['Escolaridad'])
    #             can8.drawString(434, 69, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Otro (a) pariente del (de la) jefe (a)':
    #             can8.drawString(97 , 53, 'x')
    #             can8.drawString(195, 53, integrante['Genero'])
    #             can8.drawString(244, 53, str(integrante['Edad']))
    #             can8.drawString(288, 53, integrante['Registro'])
    #             can8.drawString(324, 53, integrante['Escolaridad'])
    #             can8.drawString(434, 53, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == 'Otro (a) no pariente':
    #             can8.drawString(97 , 39, 'x')
    #             can8.drawString(195, 39, integrante['Genero'])
    #             can8.drawString(244, 39, str(integrante['Edad']))
    #             can8.drawString(288, 39, integrante['Registro'])
    #             can8.drawString(324, 39, integrante['Escolaridad'])
    #             can8.drawString(434, 39, integrante['Ocupacion'])
    #         elif integrante['Parentesco'] == " " or integrante['Parentesco'] == None:
    #             can8.drawString(97 , 39, " ")
    #             can8.drawString(195, 39, " ")
    #             can8.drawString(244, 39, " ")
    #             can8.drawString(288, 39, " ")
    #             can8.drawString(324, 39, " ")
    #             can8.drawString(434, 39, " ")

    can8.save()
    #hoja 9 del pdf
    packet9 = io.BytesIO()
    # create a new PDF with Reportlab
    can9 = canvas.Canvas(packet9, pagesize=A4)
    can9.setFont("Helvetica", 9)

    can9.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can9, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can9, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can9, 487, 800, str(datos[6]),10)# Año

    if str(datos[40].decode("utf-8")) == '1':
        can9.drawString(320, 740, "X")
    elif str(datos[40].decode("utf-8")) == '2':
        can9.drawString(320, 728, "X")

    if str(datos[41]) == 'undefined' or str(datos[41]) == 'null':
        can9.drawString(90, 675, 'No Aplica')
    else:
        can9.drawString(90, 675, str(datos[41]))
        
    if str(datos[42]) == 'true':
        can9.drawString(365, 565, "X")
    if str(datos[43]) == 'true':
        can9.drawString(365, 552, "X")
    if str(datos[44]) == 'true':
        can9.drawString(365, 539, "X")
    if str(datos[45]) == 'true':
        can9.drawString(365, 526, "X")
    if str(datos[46]) == 'true':
        can9.drawString(365, 513, "X") 
    if str(datos[47]) == 'true':
        can9.drawString(365, 500, "X") 
    if str(datos[48]) == 'true':
        can9.drawString(365, 487, "X")
    if str(datos[49]) == 'true':
        can9.drawString(365, 474, "X")
    if str(datos[50]) == 'true':
        can9.drawString(365, 461, "X")
    if str(datos[51]) == 'true':
        can9.drawString(365, 448, "X")
# // ------------------------------------------------------------
    if str(datos[52]) == 'true':
        can9.drawString(405, 565, "X")
    if str(datos[53]) == 'true':
        can9.drawString(405, 552, "X")
    if str(datos[54]) == 'true':
        can9.drawString(405, 539, "X")
    if str(datos[55]) == 'true':
        can9.drawString(405, 526, "X")
    if str(datos[56]) == 'true':
        can9.drawString(405, 513, "X")
    if str(datos[57]) == 'true':
        can9.drawString(405, 500, "X") 
    if str(datos[58]) == 'true':
        can9.drawString(405, 487, "X")
    if str(datos[59]) == 'true':
        can9.drawString(405, 474, "X")
    if str(datos[60]) == 'true':
        can9.drawString(405, 461, "X")
    if str(datos[61]) == 'true':
        can9.drawString(405, 448, "X")

        #   // ------------------------------------------------------------
    if str(datos[62]) == 'true':
        can9.drawString(445, 565, "X")
    if str(datos[63]) == 'true':
        can9.drawString(445, 552, "X")
    if str(datos[64]) == 'true':
        can9.drawString(445, 539, "X")
    if str(datos[65]) == 'true':
        can9.drawString(445, 526, "X") 
    if str(datos[66]) == 'true':
        can9.drawString(445, 513, "X")
    if str(datos[67]) == 'true':
        can9.drawString(445, 500, "X")
    if str(datos[68]) == 'true':
        can9.drawString(445, 487, "X")
    if str(datos[69]) == 'true':
        can9.drawString(445, 474, "X")
    if str(datos[70]) == 'true':
        can9.drawString(445, 461, "X")
    if str(datos[71]) == 'true':
        can9.drawString(445, 448, "X")

        #   // ------------------------------------------------------------
    if str(datos[72]) == 'true':
        can9.drawString(485, 565, "X")
    if str(datos[73]) == 'true':
        can9.drawString(485, 552, "X")
    if str(datos[74]) == 'true':
        can9.drawString(485, 539, "X")
    if str(datos[75]) == 'true':
        can9.drawString(485, 526, "X")
    if str(datos[76]) == 'true':
        can9.drawString(485, 513, "X")
    if str(datos[77]) == 'true':
        can9.drawString(485, 500, "X")
    if str(datos[78]) == 'true':
        can9.drawString(485, 487, "X")
    if str(datos[79]) == 'true':
        can9.drawString(485, 474, "X")
    if str(datos[80]) == 'true':
        can9.drawString(485, 461, "X")
    if str(datos[81]) == 'true': 
        can9.drawString(485, 448, "X")
    if str(datos[82]) == 'undefined' or str(datos[82]) == 'null':
        can9.drawString(210, 448,'No Aplica')
    else:
        can9.drawString(210, 448,str(datos[82]))

        #   //actividades

    if str(datos[141]) == 'true':
        can9.drawString(405, 333, "X")
    if str(datos[142]) == 'true':
        can9.drawString(405, 321, "X")
    if str(datos[143]) == 'true':
        can9.drawString(405, 309, "X")
    if str(datos[144]) == 'true':
        can9.drawString(405, 297, "X")
    if str(datos[145]) == 'true':
        can9.drawString(405, 285, "X")
    if str(datos[146]) == 'true':
        can9.drawString(405, 273, "X")
    if str(datos[147]) == 'true':
        can9.drawString(405, 261, "X")
    if str(datos[148]) == 'true':
        can9.drawString(405, 249, "X")
    if str(datos[149]) == 'true':
        can9.drawString(405, 237, "X")
    if str(datos[150]) == 'true':
        can9.drawString(405, 225, "X")
    if str(datos[151]) == 'true':
        can9.drawString(405, 213, "X")
    if str(datos[152]) == 'true':
        can9.drawString(405, 201, "X")
    if str(datos[153]) == 'true':
        can9.drawString(405, 189, "X")
    if str(datos[154]) == 'true':
        can9.drawString(405, 177, "X")
    if str(datos[155]) != '-' and str(datos[155]) != 'null':
        can9.drawString(405, 165, "X")
        can9.drawString(210, 165, str(datos[155]))
    if str(datos[156]) == 'null' or str(datos[156]) == '-':
        can9.drawString(138, 125, "No Registra")
    else:
        can9.drawString(138, 125, str(datos[156]))
    if str(datos[157]) == 'null' or str(datos[157]) == '-':
        can9.drawString(138, 111, "No Registra")
    else:
        can9.drawString(138, 111, str(datos[157]))
    if str(datos[158]) == 'null' or str(datos[158]) == '-':
        can9.drawString(138, 97, "No Registra")
    else:
        can9.drawString(138, 97, str(datos[158]))
    if str(datos[159]) == 'null' or str(datos[159]) == '-':
        can9.drawString(138, 83, "No Registra")
    else:
        can9.drawString(138, 83, str(datos[159]))



    # if datos[15] == "Permanente":
    #     can9.drawString(392,710, "x")
    # elif datos[15] == "Temporal":
    #     can9.drawString(392, 696, "x")


    # if datos[317] == 'Si':
    #     can9.drawString(325, 628, "x")
    # elif datos[317] == 'No':
    #     can9.drawString(372, 628, "x")

    # if datos[20]=='Indígena':
    #     can9.drawString(408, 548, "x")
    # elif datos[20]=='Gitano (a)(ROM)':
    #     can9.drawString(408, 536, "x")
    # elif datos[20]=='Raizal de San Andrés, Providencia, Santa Catalina':
    #     can9.drawString(408, 522, "x")
    # elif datos[20]=='Palenquero (a)':
    #     can9.drawString(408, 510, "x")
    # elif datos[20]=='Negro (a), afrodescendiente, afrocolombiano (a)':
    #     can9.drawString(408, 498, "x")
    # elif datos[20]=='Ninguno de los anteriores':   
    #     can9.drawString(408, 486, "x")

    # if datos[22] == 'Si':
    #     can9.drawString(320, 412, "x")
    # elif datos[22] == 'No':
    #     can9.drawString(320, 400, "x")

    # can9.drawString(70, 355, datos[23])

    # if datos[24] == 'Si':
    #     can9.drawString(323, 258, "x")
    # elif datos[24] == 'No':
    #     can9.drawString(368, 258, "x")
    # if datos[25] == 'Si':
    #     can9.drawString(320, 176, "x")
    # elif datos[25] == 'No':
    #     can9.drawString(320, 168, "x")
    # #cual organizacion pertenece
    # can9.drawString(70, 100, datos[26])
    

    can9.save()
    #hoja 10 del pdf
    packet10 = io.BytesIO()
    # create a new PDF with Reportlab
    can10 = canvas.Canvas(packet10, pagesize=A4)
    can10.setFont("Helvetica", 9)

    can10.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can10, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can10, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can10, 487, 800, str(datos[6]),10)# Año

        #   //gastos
        
    if str(datos[160]) == 'null' or str(datos[160]) == '-':
        can10.drawString(378, 742, "No Registra")
    else:
        can10.drawString(378, 742,str(datos[160]))
    if str(datos[161]) == 'null' or str(datos[161]) == '-':
        can10.drawString(378, 730, "No Registra")
    else:
        can10.drawString(378, 730, str(datos[161]))
    if str(datos[162]) == 'null' or str(datos[162]) == '-':
        can10.drawString(378, 718, "No Registra")
    else:
        can10.drawString(378, 718, str(datos[162]))
    if str(datos[163]) == 'null' or str(datos[163]) == '-':
        can10.drawString(378, 706, "No Registra")
    else:
        can10.drawString(378, 706, str(datos[163]))
    if str(datos[164]) == 'null' or str(datos[164]) == '-':
        can10.drawString(378, 694, "No Registra")
    else:
        can10.drawString(378, 694, str(datos[164]))
    if str(datos[165]) == 'null' or str(datos[165]) == '-':
        can10.drawString(378, 682, 'No Registra')
    else:
        can10.drawString(378, 682, str(datos[165]))
    if str(datos[166]) == 'null' or str(datos[166]) == '-':
        can10.drawString(378, 670, "No Registra")
    else:
        can10.drawString(378, 670, str(datos[166]))
    if str(datos[167]) == 'null' or str(datos[167]) == '-':
        can10.drawString(378, 658, "No Registra")
    else:
        can10.drawString(378, 658, str(datos[167]))
    if str(datos[168]) == 'null' or str(datos[168]) == '-':
        can10.drawString(378, 646, "No Registra")
    else:
        can10.drawString(378, 646, str(datos[168]))
    if str(datos[169]) == 'null' or str(datos[169]) == '-':
        can10.drawString(378, 634, "No Registra")
    else:
        can10.drawString(378, 634, str(datos[169]))
    if str(datos[170]) == 'null' or str(datos[170]) == '-':
        can10.drawString(378, 622, "No Registra")
    else:
        can10.drawString(378, 622, str(datos[170]))
    if str(datos[171]) == 'null' or str(datos[171]) == '-' or str(datos[171]) == 'undefined':
        can10.drawString(378, 606, "0")
    else:
        can10.drawString(378, 606, str(datos[171]))
    if str(datos[173]) == 'null' or str(datos[173]) == '-' or str(datos[173]) == 'undefined':
        can10.drawString(250, 606, "No Registra")
    else:
        can10.drawString(250, 606, str(datos[173]))
    if str(datos[172]) == 'null' or str(datos[172]) == '-':
        can10.drawString(378, 594, "0")
    else:
        can10.drawString(378, 594, str(datos[172]))


    if str(datos[349]) == '1':
        can10.drawString(328, 480, "X")
    elif str(datos[349]) == '2':
        can10.drawString(328, 468, "X")
    elif str(datos[349]) == '3':
        can10.drawString(328, 456, "X")

    if str(datos[350].decode("utf-8")) == '1':
        can10.drawString(320, 370, "X")
    elif str(datos[350].decode("utf-8")) == '2':
        can10.drawString(368, 370, "X")

    if str(datos[351].decode("utf-8")) == '1':
        can10.drawString(328, 295, "X")
    elif str(datos[351].decode("utf-8")) == '2':
        can10.drawString(328, 283, "X")

    if str(datos[352]) == 'null' or str(datos[352]) == '-':
        can10.drawString(90, 220, "No Registra")
    else:
        can10.drawString(90, 220, str(datos[352]))

    if str(datos[353].decode("utf-8")) == '1':
        can10.drawString(320, 120, "X")
    elif str(datos[353].decode("utf-8")) == '2':
        can10.drawString(368, 120, "X")


    #domesticas
    # if datos[27] == 'true':
    #     can10.drawString(364, 692, "x")
    # if datos[37] == 'true':
    #     can10.drawString(404, 692, "x")
    # if datos[47] == 'true':
    #     can10.drawString(444, 692, "x")
    # if datos[57] == 'true':
    #     can10.drawString(484, 692, "x")
    #     #pagos
    # if datos[28] == 'true':
    #     can10.drawString(364, 679, "x")
    # if datos[38] == 'true':
    #     can10.drawString(404, 679, "x")
    # if datos[48] == 'true':
    #     can10.drawString(444, 679, "x")
    # if datos[58] == 'true':
    #     can10.drawString(484, 679, "x")
    #     #finca
    # if datos[29] == 'true':
    #     can10.drawString(364, 666, "x")
    # if datos[39] == 'true':
    #     can10.drawString(404, 666, "x")
    # if datos[49] == 'true':
    #     can10.drawString(444, 666, "x")
    # if datos[59] == 'true':
    #     can10.drawString(484, 666, "x")
    #     #Transporte
    # if datos[30] == 'true':
    #     can10.drawString(364, 653, "x")
    # if datos[40] == 'true':
    #     can10.drawString(404, 653, "x")
    # if datos[50] == 'true':
    #     can10.drawString(444, 653, "x")
    # if datos[60] == 'true':
    #     can10.drawString(484, 653, "x")
    #     #admin finca
    # if datos[31] == 'true':
    #     can10.drawString(364, 640, "x")
    # if datos[41] == 'true':
    #     can10.drawString(404, 640, "x")
    # if datos[51] == 'true':
    #     can10.drawString(444, 640, "x")
    # if datos[61] == 'true':
    #     can10.drawString(484, 640, "x")
    #     #comercia
    # if datos[32] == 'true':
    #     can10.drawString(364, 627, "x")
    # if datos[42] == 'true':
    #     can10.drawString(404, 627, "x")
    # if datos[52] == 'true':
    #     can10.drawString(444, 627, "x")
    # if datos[62] == 'true':
    #     can10.drawString(484, 627, "x")
    #     #Estudia
    # if datos[33] == 'true':
    #     can10.drawString(364, 614, "x")
    # if datos[43] == 'true':
    #     can10.drawString(404, 614, "x")
    # if datos[53] == 'true':
    #     can10.drawString(444, 614, "x")
    # if datos[63] == 'true':
    #     can10.drawString(484, 614, "x")
    #     # fORMACION HIJOS
    # if datos[34] == 'true':
    #     can10.drawString(364, 601, "x")
    # if datos[44] == 'true':
    #     can10.drawString(404, 601, "x")
    # if datos[54] == 'true':
    #     can10.drawString(444, 601, "x")
    # if datos[64] == 'true':
    #     can10.drawString(484, 601, "x")
    #     #Cuidado adultos
    # if datos[35] == 'true':
    #     can10.drawString(364, 588, "x")
    # if datos[45] == 'true':
    #     can10.drawString(404, 588, "x")
    # if datos[55] == 'true':
    #     can10.drawString(444, 588, "x")
    # if datos[65] == 'true':
    #     can10.drawString(484, 588, "x")
    #     #Otro
    # if datos[36] == 'true':
    #     can10.drawString(364, 575, "x")
    # if datos[46] == 'true':
    #     can10.drawString(404, 575, "x")
    # if datos[56] == 'true':
    #     can10.drawString(444, 575, "x")
    # if datos[66] == 'true':
    #     can10.drawString(160, 575, "Otro")
    #     can10.drawString(484, 575, "x")
    # #fuentes de ingtreso en l hogar
    # if datos[123] == 'true':
    #     can10.drawString(402, 407, "x")
    # if datos[124] == 'true':
    #     can10.drawString(402, 394, "x")
    # if datos[125] == 'true':
    #     can10.drawString(402, 381, "x")
    # if datos[126] == 'true':
    #     can10.drawString(402, 368, "x")
    # if datos[127] == 'true':
    #     can10.drawString(402, 355, "x")
    # if datos[128] == 'true':
    #     can10.drawString(402, 342, "x")
    # if datos[129] == 'true':
    #     can10.drawString(402, 329, "x")
    # if datos[130] == 'true':
    #     can10.drawString(402, 316, "x")
    # if datos[131] == 'true':
    #     can10.drawString(402, 303, "x")
    # if datos[132] == 'true':
    #     can10.drawString(402, 290, "x")
    # if datos[133] == 'true':
    #     can10.drawString(402, 277, "x")
    # if datos[134] == 'true':
    #     can10.drawString(402, 264, "x")
    # if datos[135] == 'true':
    #     can10.drawString(402, 251, "x")
    # if datos[136] == 'true':
    #     can10.drawString(402, 238, "x")
    # if datos[137] == 'true':
    #     can10.drawString(402, 225, "x")
    #     can10.drawString(242, 225, datos[137])

    # if datos[138] == "null":
    #     can10.drawString(142, 169, "No registra")
    # else:    
    #     can10.drawString(142, 169, datos[138])
    # if datos[139] == "null":
    #     can10.drawString(142, 156, "No registra")
    # else:
    #     can10.drawString(142, 156, datos[139])  
    # if datos[140] == "null":
    #     can10.drawString(142, 143, "No registra")
    # else:
    #     can10.drawString(142, 143, datos[140])
    # if datos[141] == "null":
    #     can10.drawString(142, 130, "No registra")
    # else: 
    #     can10.drawString(142, 130, datos[141])
        
    can10.save()
    #hoja 11 del pdf
    packet11 = io.BytesIO()
    # create a new PDF with Reportlab
    can11 = canvas.Canvas(packet11, pagesize=A4)
    can11.setFont("Helvetica", 9)

    can11.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can11, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can11, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can11, 487, 800, str(datos[6]),10)# Año

    

    

    


    

    

    
    
    

    

    

    

    if str(datos[97]) == 'null' or str(datos[97]) == '-':
        can11.drawString(90, 635, 'No Registra')
    else :
        can11.drawString(90, 635, str(datos[97]))

    if str(datos[98]) == '1':
        can11.drawString(487, 655, "x")
    elif str(datos[98]) == '2':
        can11.drawString(487, 643, "x")
    elif str(datos[98]) == '3':
        can11.drawString(487, 631, "x")
          
    if str(datos[99]) == 'null' or str(datos[99]) == '-':
        can11.drawString(330, 619, "No Registra")
    else:
        can11.drawString(330, 619, str(datos[99]))

    if str(datos[100]) == 'null' or str(datos[100]) == '-':
        can11.drawString(330, 568, "No Registra")
    else:
        can11.drawString(330, 568,str(datos[100]))

    if str(datos[101]) == 'null' or str(datos[101]) == '-':
        can11.drawString(90, 482, 'No Registra')
    else:
        can11.drawString(90, 482, str(datos[101]))

    if str(datos[102]) == 'null' or str(datos[102]) == '-':
        can11.drawString(330, 506, "No Registra")
    else:
        can11.drawString(330, 506, str(datos[102]))
    
    if str(datos[103]) == 'null' or str(datos[103]) == '-':
        can11.drawString(330, 482, "No Registra")
    else:
        can11.drawString(330, 482, str(datos[103]))

    if str(datos[104]) == 'null' or str(datos[104]) == '-':
        can11.drawString(90, 460, 'No Registra')
    else:
        can11.drawString(90, 460, str(datos[104]))
          
    if str(datos[105]) == 'null' or str(datos[105]) == '-':
        can11.drawString(330, 460, "No Registra")
    else:
        can11.drawString(330, 460, str(datos[105]))

    # can11.drawString(350, 710, datos[142])
    # can11.drawString(350, 697, datos[143])
    # can11.drawString(350, 684, datos[144])
    # can11.drawString(350, 671, datos[145])
    # can11.drawString(350, 658, datos[146])
    # can11.drawString(350, 647, datos[147])
    # can11.drawString(350, 635, datos[148])
    # can11.drawString(350, 622, datos[149])
    # can11.drawString(350, 610, datos[150])
    # can11.drawString(350, 596, datos[151])
    # can11.drawString(350, 583, datos[152])
    # can11.drawString(350, 574, datos[153])
    # can11.drawString(242, 562, datos[155])
    # can11.drawString(350, 562, datos[154]) 

    # if datos[387] == 'Si':
    #     can11.drawString(320, 440, "x")
    # elif datos[387] == 'No':
    #     can11.drawString(320, 428, "x")

    # can11.drawString(340, 390, datos[388])
    # can11.drawString(318, 410, datos[389])

    # can11.drawString(320, 359, datos[390])
    # can11.drawString(280, 342, datos[392])
    # can11.drawString(320, 299, datos[393])
    # can11.drawString(320, 275, datos[394])
    # can11.drawString(320, 246, datos[395])
    # can11.drawString(320, 218, datos[396])




    can11.save()
    #hoja 12 del pdf
    packet12 = io.BytesIO()
    # create a new PDF with Reportlab
    can12 = canvas.Canvas(packet12, pagesize=A4)
    can12.setFont("Helvetica", 9)

    can12.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can12, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can12, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can12, 487, 800, str(datos[6]),10)# Año
    #nombre

    # can12.drawString(110, 670, datos[81])

    # can12.drawString(110, 595, datos[81])
    # #telefono c
    # can12.drawString(310, 602, datos[83])
    # #telefono f
    # if datos[84] == "None" or datos[84] == None:
    #     can12.drawString(310, 575," ")
    # else:
    #     can12.drawString(310, 575, datos[84])
    
    # #correo 
    # if datos[86] == "None" or datos[86] == None:
    #     can12.drawString(310, 555," ")
    # else:
    #     can12.drawString(310, 555, datos[86])
    
    # # No ID
    # can12.drawString(110, 546, datos[85])
    # can12.drawString(310, 138, datos[85])
    # # firma

    if datos[106] == "true" :
        can12.drawString(420, 700, "x")
    else :
        can12.drawString(485, 700, "x")

    if datos[107] == "true" :
        can12.drawString(420, 670, "x")
    else :
        can12.drawString(485, 670, "x")
 
    if datos[108] == "true" :
        can12.drawString(420, 645, "x")
    else :
        can12.drawString(485, 645, "x")

    if datos[109] == "true" :
        can12.drawString(420, 605, "x")
    else :
        can12.drawString(485, 605, "x")

    if datos[110] == "true" :
        can12.drawString(420, 578, "x")
    else :
        can12.drawString(485, 578, "x")

    #firmaaa
    with bd.cursor() as cursor:
              cursor.execute("Select rutaserver from db_ipse_7_0.Fotos_firma where Id_Encuesta = '"+id+"';")
              datos2 = cursor.fetchone()
    print(datos2)

    if datos2 ==  None :
        print(datos2,"asd")
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

        can12.drawImage('new.png', 80,375, 200, 99)
        can12.drawImage('blanco.JPG', 690, 400, 800, 20)
    elif str(datos2[0]) != "NO ENCONTRADO ARCHIVO LOCAL" and str(datos2[0]) != "null" :   
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

        can12.drawImage('new.png', 80,375, 200, 99)
        can12.drawImage('blanco.JPG', 690, 400, 800, 20)
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

        can12.drawImage('new.png', 80,375, 200, 99)
        can12.drawImage('blanco.JPG', 690, 400, 800, 20)
    can12.save()
    packet13 = io.BytesIO()
    # create a new PDF with Reportlab
    can13 = canvas.Canvas(packet13, pagesize=A4)
    can13.setFont("Helvetica", 9)

    can13.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can13, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can13, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can13, 487, 800, str(datos[6]),10)# Año

    can13.drawString(110, 700, datos[358])
    can13.drawString(340, 725, datos[359])

    can13.drawString(340, 689, datos[365])
    can13.drawString(110, 650, datos[366])
    can13.drawString(340, 650, datos[368])

    if datos[114] == '1' :
        can13.drawString(325, 596, "x")
    elif datos[114] == '2' :
        can13.drawString(325, 582, "x")

    if datos[115] == '1' :
        can13.drawString(325, 515, "x")
    elif datos[115] == '2' :
        can13.drawString(325, 502, "x")
    elif datos[115] == '3' :
        can13.drawString(325, 490, "x")

    can13.drawString(100, 450, datos[116])      

    can13.save()

    packet14 = io.BytesIO()
    # create a new PDF with Reportlab
    can14 = canvas.Canvas(packet14, pagesize=A4)
    can14.setFont("Helvetica", 9)

    can14.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can14, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can14, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can14, 487, 800, str(datos[6]),10)# Año
    can14.save()

    packet15 = io.BytesIO()
    # create a new PDF with Reportlab
    can15 = canvas.Canvas(packet15, pagesize=A4)
    can15.setFont("Helvetica", 9)

    can15.drawString(420, 813, str(datos[3]))# num Formulario
    llenarCampos(can15, 398, 800, str(datos[4]),10)# Dia
    llenarCampos(can15, 437, 800, str(datos[5]),10)# Mes
    llenarCampos(can15, 487, 800, str(datos[6]),10)# Año
    can15.save()

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
    packet14.seek(0)
    packet15.seek(0)
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

    # read your existing PDF
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-1.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-2.pdf", "rb"))
    existing_pdf3 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-3.pdf", "rb"))
    existing_pdf4 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-4.pdf", "rb"))
    existing_pdf5 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-5.pdf", "rb"))
    existing_pdf6 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-6.pdf", "rb"))
    existing_pdf7 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-7.pdf", "rb"))
    existing_pdf8 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-8.pdf", "rb"))
    existing_pdf9 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-9.pdf", "rb"))
    existing_pdf10 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-10.pdf", "rb"))
    existing_pdf11 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-11.pdf", "rb"))
    existing_pdf12 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-12.pdf", "rb"))
    existing_pdf13 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-13.pdf", "rb"))
    existing_pdf14 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-14.pdf", "rb"))
    existing_pdf15 = PyPDF2.PdfFileReader(open("src/pdf/ipse/ENCUESTA-15.pdf", "rb"))
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
    page14 = existing_pdf14.getPage(0)
    page15 = existing_pdf15.getPage(0)
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
    # finally, write "output" to a real file
    outputStream = open("pdfs/"+str(datos[3])+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()





def generarRar():
    if os.path.exists("src/pdf/a"):
        os.remove("src/pdf/a/destination.zip")
        os.remove("src/pdf/a/destination.pdf")
        os.remove("src/pdf/a/destination2.pdf")
        os.rmdir("src/pdf/a")
    os.mkdir("src/pdf/a")
    zf = zipfile.ZipFile("src/pdf/a/destination.zip", mode="w")
    # if os.path.exists("src/destination.pdf"):
    #     os.remove('src/destination.pdf')
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    can.drawString(10, 100, "Hello worldasasas")
    can.line(120,700,590,747)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-2.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-3.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    output2 = PyPDF2.PdfFileWriter()
    # existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/ejemplo.pdf", "rb"))
    # output2 = PyPDF2.PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    page2 = existing_pdf2.getPage(0)
    output.addPage(page)
    output2.addPage(page2)
    #output2.addPage(page)
   
    # finally, write "output" to a real file
    outputStream = open("src/pdf/a/destination.pdf", "wb")
    output.write(outputStream)
    #output2.write(outputStream)
    outputStream.close()
    outputStream2 = open("src/pdf/a/destination2.pdf", "wb")
    output2.write(outputStream2)
    #output2.write(outputStream)
    outputStream.close()
    outputStream2.close()
    try:
        zf.write("src/pdf/a/destination.pdf", compress_type=compression)
        zf.write("src/pdf/a/destination2.pdf", compress_type=compression)
    finally:
        zf.close()
    return "destination.pdf"

if __name__ == '__main__':
    generarVariosPdf()