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
            generarPdfSocializacion(id)
        except Exception as e: 
             print(str(id), 'No se pudo', e)
    


def generarFotosCoordenadas(ids, carpeta):   
    os.mkdir('pdfs/'+carpeta+"/registrofotografico-replanteo")                                     
    bd = obtener_conexion()
    conn = bd.cursor(pymysql.cursors.DictCursor)
    conn.execute("SELECT D.*, E.`U_latitud`,E.`U_longitud` FROM suncosurvey.fotos_encuesta D INNER JOIN `suncosurvey`.`ubicacion` E ON D.`Id_Encuesta` = E.`Id_Encuesta` WHERE D.Id_Encuesta IN ('"+ids+"');")
    fotos=conn.fetchall()
    print(fotos)
    if len(fotos) > 0:
        for foto in fotos:
            print( "latitud: " + foto['U_latitud'] +" , Longitud: " + foto['U_longitud'])
            with urllib.request.urlopen('https://www.php.engenius.com.co'+foto['rutaserver']) as url:
                data = url.read()
            file = BytesIO(data)
            my_image = Image.open(file)
            my_image = my_image.resize((3500,2400))
            title_font = ImageFont.truetype('src/fotos/Roboto-Black.ttf', 100)
            title_text = "latitud: " + foto['U_latitud'] +" , Longitud: " + foto['U_longitud']
            image_editable = ImageDraw.Draw(my_image)
            image_editable.text((200,2100), title_text, (237, 230, 500), font=title_font)
            
            my_image.save("pdfs/"+carpeta+"/registrofotografico-replanteo/"+foto['Id_Foto_Encuesta']+".jpg")
            
        else:
            print("No trae fotos")

def generarPdfSocializacion(idFormulario='302-1605359064075'):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT *, (SELECT DISTINCT rutaserver from suncosurvey.fotos_firma B WHERE B.`Id_Encuesta`= A.`Id_Encuesta` AND B.IsDelete=0) FROM suncosurvey.Users3 A Where `Id_Encuesta` = '"+idFormulario+"';")
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
    can.drawString(435, 672, str(datos[0]))
    can.drawString(90, 632, datos[1])
    can.drawString(60, 619, datos[2])
    can.drawString(330, 606, datos[3])
    can.drawString(60, 593, datos[4])
    can.drawString(458, 593, datos[5])
    can.drawString(107, 580, datos[6])
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
    can.drawString(93, 313, datos[1])
    can.drawString(93, 300, datos[2])
    can.drawString(103, 287, datos[7])
    can.save()
    new_pdf = PyPDF2.PdfFileReader(packet)
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/formatoEnTerritorio/FORMATO_SOCIALIZACIÓN_Y_REPLANTEO_DE_USUARIOS_DISPAC.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    os.mkdir('pdfs/'+str(datos[0]))
    outputStream = open("pdfs/"+str(datos[0])+"/"+str(datos[0])+"_FormatoSocializacionyReplanteo.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    generarPdfId(idFormulario, str(datos[0]))

def generarPdfId(id = '302-1605359064075', carpeta= "1"):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT A.*,B.*,C.*,D.*,E.*,F.*,G.*,H.*,I.*,J.*,K.*,M.*, N.* FROM suncosurvey.encabezado A INNER JOIN suncosurvey.c_sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN suncosurvey.caracteristicas_predio C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN suncosurvey.consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN suncosurvey.datos_vivienda_I E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN suncosurvey.economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN suncosurvey.energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN suncosurvey.servicios_publicos H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN suncosurvey.tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN suncosurvey.ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN suncosurvey.URE K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN suncosurvey.proyectos_funcionarios L ON A.Id_Proyecto_Funcionario = L.Id_Proyecto_Funcionario INNER JOIN suncosurvey.funcionarios M ON M.Id_Funcionario = L.Id_Funcionario INNER JOIN suncosurvey.agua N ON A.Id_Encuesta = N.Id_Encuesta WHERE A.isdelete = 0 AND A.Id_Encuesta = '"+id+"';")
              datos = cursor.fetchone()
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    #pagina 1
    can.setFont("Helvetica", 8)
    #numero de formulario 
    can.drawString(410, 802, datos[3])
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can, 398, 790, dia, 10)
    #mes
    llenarCampos(can, 440, 790, '04', 10)
    #anio
    llenarCampos(can, 488, 790, '2022', 10)
    can.drawImage('encabezadoPP.JPG', 69, 725, 458, 60)
    can.drawImage('blanco.JPG', 69, 660, 458, 20)
    # coordenadas  latitud
    latitudUnidad = datos[323].split('.')[0]
    latitudDecimales = datos[323].split('.')[1]
    can.drawString(220, 396, latitudUnidad)
    llenarCampos(can, 265, 396, latitudDecimales, 24)
    # coordenadas  longitud
    longitudUnidad = datos[324].split('.')[0]
    longitudDecimales = datos[324].split('.')[1]
    can.drawString(205, 359, longitudUnidad)
    llenarCampos(can, 265, 359, longitudDecimales, 24)
    # coordenadas  altitud
    if datos[325] == 'null':
        altitud = '-'
    else:
        altitud = round(float(datos[325]))
    llenarCampos(can, 205, 322, str(altitud), 30)
    #nombre departamento
    llenarCampos(can, 128, 255, datos[326], 16)
    #codigo departamento
    llenarCampos(can, 128, 228, datos[327], 16)
    #nombre municipio
    llenarCampos(can, 128, 205, datos[328], 16)
    #codigo municipio
    llenarCampos(can, 128, 175, datos[329], 16)    
    #nombre vereda
    llenarCampos(can, 128, 155, datos[330], 16)  
    #nombre corregimiento
    llenarCampos(can, 128, 127, datos[331], 16)
    can.save()
    #pagina2
    packet2 = io.BytesIO()
    # create a new PDF with Reportlab
    can2 = canvas.Canvas(packet2, pagesize=A4)
    can2.setFont("Helvetica", 8)
    can2.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #numero de formulario 
    can2.drawString(410, 815, datos[3])
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can2, 398, 800, dia, 10)
    #mes
    llenarCampos(can2, 440, 800, '04', 10)
    #anio
    llenarCampos(can2, 488, 800, '2022', 10)
    #autoriza la encuesta
    if datos[312] == 'Si':
        can2.drawString(315, 722, "X")
    else:
        can2.drawString(315, 710, "X")
    #uso de vivienda
    if datos[316] == 'Permanente': 
        can2.drawString(320, 633, "X")
    elif datos[316] == 'Temporal':
        can2.drawString(320, 620, "X")
    #cuenta con energia elcetrica
    if datos[162] == 'Si': 
        can2.drawString(320, 368, "X")
    elif datos[162] == 'No':
        can2.drawString(370, 368, "X")
    #que fuente utiliza
    can2.drawString(335, 290, datos[163])
    can2.drawString(450, 290, datos[174])
    can2.drawString(335, 276, datos[164])
    can2.drawString(450, 276, datos[175])
    can2.drawString(335, 264, datos[165])
    can2.drawString(450, 264, datos[176])
    can2.drawString(335, 250, datos[166])
    can2.drawString(450, 250, datos[177])
    can2.drawString(335, 238, datos[167])
    can2.drawString(450, 238, datos[178])
    can2.drawString(335, 226, datos[168])
    can2.drawString(450, 226, datos[179])
    can2.drawString(335, 214, datos[169])
    can2.drawString(450, 214, datos[180])
    can2.drawString(335, 202, datos[170])
    can2.drawString(450, 202, datos[181])
    can2.drawString(335, 190, datos[171])
    can2.drawString(450, 190, datos[182])
    can2.drawString(335, 178, datos[172])
    can2.drawString(450, 178, datos[183])
    can2.drawString(335, 164, datos[173])
    can2.drawString(450, 164, datos[184])
    #cuantas horas utiliza para cocinar
    if datos[187] == None:
        can2.drawString(350, 140, '-')
    else:
        can2.drawString(350, 140, datos[187])

    can2.save()
    packet3 = io.BytesIO()
    # create a new PDF with Reportlab
    can3 = canvas.Canvas(packet3, pagesize=A4)
    can3.setFont("Helvetica", 8)
    can3.drawString(410, 815, datos[3])
    can3.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can3, 398, 800, dia, 10)
    #mes
    llenarCampos(can3, 440, 800, '04', 10)
    #anio
    llenarCampos(can3, 488, 800, '2022', 10)
    #fuente para iluminarse
    #pilas baterias
    can3.drawString(280, 740, datos[214])
    can3.drawString(340, 740, datos[222])
    if datos[230] == "Cabecera municipal":
        can3.drawString(420, 740, 'x')
    elif datos[230] == "Vereda":
        can3.drawString(462, 740, 'x')
    elif datos[230] == "Domicilio":
        can3.drawString(505, 740, 'x')
    #gasolina
    can3.drawString(280, 728, datos[215])
    can3.drawString(340, 728, datos[223])
    if datos[231] == "Cabecera municipal":
        can3.drawString(420, 728, 'x')
    elif datos[231] == "Vereda":
        can3.drawString(462, 728, 'x')
    elif datos[231] == "Domicilio":
        can3.drawString(505, 728, 'x')
    #Kerosene
    can3.drawString(280, 716, datos[216])
    can3.drawString(340, 716, datos[224])
    if datos[232] == "Cabecera municipal":
        can3.drawString(420, 716, 'x')
    elif datos[232] == "Vereda":
        can3.drawString(462, 716, 'x')
    elif datos[232] == "Domicilio":
        can3.drawString(505, 716, 'x')
    #Petroleo
    can3.drawString(280, 702, datos[217])
    can3.drawString(340, 702, datos[225])
    if datos[233] == "Cabecera municipal":
        can3.drawString(420, 702, 'x')
    elif datos[233] == "Vereda":
        can3.drawString(462, 702, 'x')
    elif datos[233] == "Domicilio":
        can3.drawString(505, 702, 'x')
    #Alcohol
    can3.drawString(280, 692, datos[218])
    can3.drawString(340, 692, datos[226])
    if datos[234] == "Cabecera municipal":
        can3.drawString(420, 692, 'x')
    elif datos[234] == "Vereda":
        can3.drawString(462, 692, 'x')
    elif datos[234] == "Domicilio":
        can3.drawString(505, 692, 'x')
    #Diesel
    can3.drawString(280, 680, datos[219])
    can3.drawString(340, 680, datos[227])
    if datos[235] == "Cabecera municipal":
        can3.drawString(420, 680, 'x')
    elif datos[235] == "Vereda":
        can3.drawString(462, 680, 'x')
    elif datos[235] == "Domicilio":
        can3.drawString(505, 680, 'x')
    #Velas
    can3.drawString(280, 668, datos[220])
    can3.drawString(340, 668, datos[228])
    if datos[236] == "Cabecera municipal":
        can3.drawString(420, 668, 'x')
    elif datos[236] == "Vereda":
        can3.drawString(462, 668, 'x')
    elif datos[236] == "Domicilio":
        can3.drawString(505, 668, 'x')
    #Otro
    can3.drawString(120, 652, datos[238])
    can3.drawString(230, 652, "-")
    can3.drawString(280, 652, datos[221])
    can3.drawString(340, 652, datos[229])
    if datos[237] == "Cabecera municipal":
        can3.drawString(420, 652, 'x')
    elif datos[237] == "Vereda":
        can3.drawString(462, 652, 'x')
    elif datos[237] == "Domicilio":
        can3.drawString(505, 652, 'x')
     #Horas al dia utiliza
    if datos[240] == None:
        can3.drawString(410, 612, '-')
    else:
        can3.drawString(410, 612, datos[240])
    #Queman residuos
    if datos[188]=='Si':
        can3.drawString(320, 544, "x")
    else:
        can3.drawString(370, 544, "x")
    #Fuente quema residuos
    #gas propano
    can3.drawString(340, 455, datos[189])
    can3.drawString(442, 455, datos[200])
    #gas natural
    can3.drawString(340, 442, datos[190])
    can3.drawString(442, 442, datos[201])
    #gasolina
    can3.drawString(340, 430, datos[191])
    can3.drawString(442, 430, datos[202])
    #Kerosene
    can3.drawString(340, 417, datos[192])
    can3.drawString(442, 417, datos[203])
    #Petroleo
    can3.drawString(340, 404, datos[193])
    can3.drawString(442, 404, datos[204])
    #Alcohol
    #Carbon mineral
    can3.drawString(340, 391, datos[194])
    can3.drawString(442, 391, datos[205])
    #Leña comprada
    can3.drawString(340, 378, datos[195])
    can3.drawString(442, 378, datos[206])
    #Leña autoapropiada
    can3.drawString(340, 367, datos[196])
    can3.drawString(442, 367, datos[207])
    #gas propano
    can3.drawString(340, 354, datos[197])
    can3.drawString(442, 354, datos[208])
    #residuos del agro
    can3.drawString(340, 343, datos[198])
    can3.drawString(442, 343, datos[209])
    #Otro
    if datos[212] == None:
        can3.drawString(150, 333, '-')
    else:
        can3.drawString(150, 333, datos[212])
    can3.drawString(260, 333, "-")
    can3.drawString(340, 330, datos[199])
    
    #cuantas horas al dia utiliza para ilumminar
    if datos[210] == None:
        can3.drawString(350, 305, '-')
    else:
        can3.drawString(442, 330, datos[210])
        can3.drawString(350, 305, datos[210])
    #contaminacion 
    #exceso de ruido
    if datos[271]=='Si':
        can3.drawString(385, 210, "x")
    else:
        can3.drawString(430, 210, "x")
    #malos oloress
    if datos[272] =='Si':
        can3.drawString(385, 195, "x")
    else:
        can3.drawString(430, 195, "x")
    # uso del predio
    #residencial
    if datos[74] == 'Residencial':
        can3.drawString(415, 92, "x")
    #negocio
    elif datos[74] == 'Negocio':
        can3.drawString(415, 80, "x")
    #mixto
    elif datos[74] == 'Mixto':
        can3.drawString(415, 68, "x")
    #institucional
    elif datos[74] == 'Institucional':
        can3.drawString(415, 56, "x")
    can3.save()
    packet4 = io.BytesIO()
    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet4, pagesize=A4)
    can4.setFont("Helvetica", 8)
    can4.drawString(410, 815, datos[3])
    #fecha de formulario
    can4.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can4, 398, 800, dia, 10)
    #mes
    llenarCampos(can4, 440, 800, '04', 10)
    #anio
    llenarCampos(can4, 488, 800, '2022', 10)
    #estrato del predio
    if datos[73] == "Estrato 1":
        can4.drawString(255, 748, "x")
    elif datos[73] == "Estrato 2":
        can4.drawString(280, 748, "x")
    elif datos[73] == "Estrato 3":
        can4.drawString(305, 748, "x")
    elif datos[73] == "Estrato 4":
        can4.drawString(330, 748, "x")
    elif datos[73] == "Estrato 5":
        can4.drawString(350, 748, "x")
    elif datos[73] == "Estrato 6":
        can4.drawString(375, 748, "x")
    #Nombre de la comunidad
    can4.drawString(90, 670, datos[103])
    #personas en la comunidad 
    llenarCampos(can4, 315, 598, datos[116], 30)
    #la vivienda se encuentra ubicada al interior de 
    if datos[104]=='Caserío' :
        can4.drawString(405, 536, "x")
    elif datos[104]=='Resguardo indígena' :
        can4.drawString(405, 523, "x")
    #parcialidad
    elif datos[104]=='Parcialidad o asentamiento indígena fuera del resguardo' :
        can4.drawString(405, 510, "x")
    elif datos[104]=='Territorio colectivo de comunidad negra' :
        can4.drawString(405, 497, "x")
    #territorio de comunidad
    elif datos[104]=='Territorio de comunidad negra no titulada' :
        can4.drawString(405, 484, "x")
    #territorio ancestral
    elif datos[104]=='Territorio ancestral raiza del Archipiélago de Sán Andrés, Providencia y Santa Catalina' :
        can4.drawString(405, 471, "x")
    #reancheria
    elif datos[104]=='Ranchería - Guajira' :
        can4.drawString(405, 458, "x")
    #territorio palenquero
    elif datos[104]=='Territorio Palenquero de San Basilio' :
        can4.drawString(405, 445, "x")
    #territorio gitano
    elif datos[104]=='Territorio Gitano - ROOM' :
        can4.drawString(405, 432, "x")
    #zona rural
    elif datos[104]=='Zona rural' :
        can4.drawString(405, 419, "x")
    #tenencia de la vivenda
    if datos[105] == 'Propia':
        can4.drawString(350, 351, "x")
    #tenencia de la vivenda
    elif datos[105] == 'Arriendo':
        can4.drawString(350, 339, "x")
    #tenencia de la vivenda
    elif datos[105] == 'Colectiva':
        can4.drawString(350, 327, "x")
    # hogares en la vivienda
    llenarCampos(can4, 342, 267 , datos[106], 30)
    #personas en la vivienda
    llenarCampos(can4, 342, 222 , datos[107], 30)
    #material predominante en la vivienda
    if datos[108] == 'Bloque, ladrillo, piedra, madera pulida' :
        can4.drawString(420, 152, "x")
    elif datos[108] == 'Concreto' :
        can4.drawString(420, 140, "x")
    elif datos[108] == 'Tapia pisada, adobe, bahareque' :
        can4.drawString(420, 128, "x")
    elif datos[108] == 'Madera burda, tabla, tablón' :
        can4.drawString(420, 116, "x")
    elif datos[108] == 'Material prefabricado' :
        can4.drawString(420, 104, "x")
    elif datos[108] == 'Guadua, caña, esterilla, otros vegetales' :
        can4.drawString(420, 92, "x")
    elif datos[108] == 'Materiales de desecho (zinc, tela, cartón, latas, plásticos, otros)' :
        can4.drawString(420, 80, "x")
    elif datos[108] == 'No tiene paredes' :
        can4.drawString(420, 68, "x")
    can4.save()

    #hoja 5 del pdf
    packet5 = io.BytesIO()
    can5 = canvas.Canvas(packet5, pagesize=A4)
    can5.setFont("Helvetica", 8)
    can5.drawString(410, 815, datos[3])
    can5.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can5, 398, 800, dia, 10)
    #mes
    llenarCampos(can5, 440, 800, '04', 10)
    #anio
    llenarCampos(can5, 488, 800, '2022', 10)
    #material predominante techo
    if datos[109] == 'Paja, palma y otros vegetales':
        can5.drawString(420, 742, "x")
    elif datos[109] == 'Plancha de cemento, concreto y hormigón':
        can5.drawString(420, 730, "x")
    elif datos[109] == 'Tejas (barro, asbesto – cemento, metálica o lámina de zinc, plástica)':
        can5.drawString(420, 718, "x")
    elif datos[109] == 'Material de desecho (tela, cartón, latas, plástico, otros)':    
        can5.drawString(420, 706, "x")
    #material predominante en piso
    if datos[110] == 'Alfombra o tapete de pared a pared':
        can5.drawString(410, 640, "x")
    if datos[110] == 'Mármol, parqué, madera pulida y lacada':
        can5.drawString(410, 628, "x")
    if datos[110] == 'Baldosa, vinilo, tableta, ladrillo, laminado':
        can5.drawString(410, 616, "x")
    if datos[110] == 'Cemento, gravilla':
        can5.drawString(410, 604, "x")
    if datos[110] == 'Madera burda, tabla, tablón, otro vegetal':
        can5.drawString(410, 592, "x")
    if datos[110] == 'Tierra, arena, barro':
        can5.drawString(410, 580, "x")
    #vivienda ha sido afectada
    if datos[111] == 'Si':
        can5.drawString(385, 523, "x")
    else:
        can5.drawString(432, 523, "x")
    if datos[112] == 'Si':
        can5.drawString(385, 511, "x")
    else:
        can5.drawString(432, 511, "x")
    if datos[113] == 'Si':
        can5.drawString(385, 499, "x")
    else:
        can5.drawString(432, 499, "x")
    if datos[114] == 'Si':
        can5.drawString(385, 487, "x")
    else:
        can5.drawString(432, 487, "x")
    if datos[114] == 'Si':
        can5.drawString(385, 475, "x")
    else:
        can5.drawString(432, 475, "x")
    #area de construccion
    # area = datos[115].split('x')
    can5.drawString(300, 417,  datos[115])
    # can5.drawString(330, 417, 'X')
    # can5.drawString(360, 417, area[1])
    
    #la vivienda cuenta con servicios
    if datos[284] == 'true':
        can5.drawString(400, 304, "x")
    if datos[285] == 'true':
        can5.drawString(400, 292, "x")
    if datos[286] == 'true':
        can5.drawString(400, 280, "x")
    if datos[287] == 'true':
        can5.drawString(400, 268, "x")
    if datos[288] == 'true':
        can5.drawString(400, 256, "x")
    if datos[289] == 'true':    
        can5.drawString(400, 244, "x")
    #obtencion de agua
    if datos[289] == 'true':
        can5.drawString(295, 167, "x")
    if datos[292] == 'true':
        can5.drawString(295, 153, "x")
    if datos[293] == 'true':
        can5.drawString(295, 141, "x")
    if datos[294] == 'true':
        can5.drawString(295, 129, "x")
    if datos[295] == 'true':
        can5.drawString(295, 117, "x")
    if datos[296] == 'true':
        can5.drawString(295, 105, "x")
    if datos[297] == 'true':
        can5.drawString(295, 93, "x")
    if datos[298] == 'true':
        can5.drawString(295, 81, "x")
    #tiene medidor de agua
    if datos[291] == 'true':
        can5.drawString(465, 167, "x")
    else:
        can5.drawString(500, 167, "x")
    can5.save()
     #hoja 6 del pdf
    packet6 = io.BytesIO()
    can6 = canvas.Canvas(packet6, pagesize=A4)
    can6.setFont("Helvetica", 8)
    can6.drawString(410, 815, datos[3])
    can6.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can6, 398, 800, dia, 10)
    #mes
    llenarCampos(can6, 440, 800, '04', 10)
    #anio
    llenarCampos(can6, 488, 800, '2022', 10)
    #Servicio sanitario
    if datos[299] == 'true':
        can6.drawString(400, 743, "x")
    if datos[300] == 'true':
        can6.drawString(400, 731, "x")
    if datos[301] == 'true':
        can6.drawString(400, 719, "x")
    if datos[302] == 'true':
        can6.drawString(400, 707, "x")
    if datos[303] == 'true':
        can6.drawString(400, 695, "x")
    if datos[304] == 'true':
        can6.drawString(230, 685, datos[304])
        can6.drawString(400, 683, "x")
    #tiene acceso a gas
    if datos[305] == 'Pipeta / Cilindro':
        can6.drawString(400, 614, "x")
    elif datos[305] == 'Gasoducto':
        can6.drawString(400, 602, "x")
    elif datos[305] == 'No tiene servicio de gas':
        can6.drawString(400, 590, "x")
    #tiene acceso al agua
    if datos[365] == 'Si':
        can6.drawString(320, 480, "x")
    elif datos[365] == 'No':
        can6.drawString(320, 467, "x")
    #que cantidad de agua puede obtener
    can6.drawString(100, 430, datos[366])
    #promedio cantidad de agua
    if datos[367] == None:
        can6.drawString(400, 395, '-')
    else:
        can6.drawString(400, 395, datos[367])
        
    #fuente principal de abastesimiento de agua
    if datos[368] == 'Jagüey':
        can6.drawString(400, 313, "x")
    elif datos[368] == 'Pozo':
        can6.drawString(400, 301, "x")
    elif datos[368] == 'Molino':
        can6.drawString(400, 289, "x")
    elif datos[368] == 'Carrotanques':
        can6.drawString(400, 277, "x")
    elif datos[368] == 'Aguas lluvias':
        can6.drawString(400, 265, "x")
    elif datos[368] == 'Ríos':
        can6.drawString(400, 253, "x")
    elif datos[368] == 'Arroyos':
        can6.drawString(400, 241, "x")
    elif datos[368] == 'Quebradas':
        can6.drawString(400, 228, "x")
    elif datos[368] == 'Otro':
        can6.drawString(400, 216, "x")
    #la casimba es comunitaria
    if datos[372] == 'Si':
        can6.drawString(320, 147, "x")
    elif datos[372] == 'No':    
        can6.drawString(320, 135, "x")
    # #cual
    can6.drawString(120, 110, datos[371])
    can6.save()

    packet7 = io.BytesIO()
    can7 = canvas.Canvas(packet7, pagesize=A4)
    can7.setFont("Helvetica", 8)
    can7.drawString(410, 815, datos[3])
    can7.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can7, 398, 800, dia, 10)
    #mes
    llenarCampos(can7, 440, 800, '04', 10)
    #anio
    llenarCampos(can7, 488, 800, '2022', 10)
     #uso del agua que obtienen
    usosAgua = datos[373].split(',')
    if 'Cocinar' in usosAgua:
        can7.drawString(405, 744, "x")
    if 'Higiene' in usosAgua:
        can7.drawString(405, 732, "x")
    if 'Actividades agropecuarias' in usosAgua:
        can7.drawString(405, 720, "x")
    if 'Actividades de ganadería' in usosAgua:
        can7.drawString(405, 708, "x")
    if 'Otro' in usosAgua:
        can7.drawString(405, 696, "x")
        # va al puesto de agua todos los dias
    if datos[375] == 'Si':
        can7.drawString(320, 626, "x")
    elif datos[375] == 'No':
        can7.drawString(320, 614, "x")
    else:
        can7.drawString(320, 602, "x")
    #cuanto dura el agua que recolecta
    can7.drawString(300, 573, datos[376])
    #cantidad destinada higiene
    can7.drawString(100, 528, datos[377])
    #distancia para obtener agua
    can7.drawString(300, 495, datos[378])
    #ti3mpo destina a la recoleccion de agua
    can7.drawString(100, 450, datos[379])
    #medio de transporte para el agua
    if datos[380] == 'Moto':
        can7.drawString(405, 377, "x")
    elif datos[380] == 'Transporte animal':    
        can7.drawString(405, 365, "x")
    elif datos[380] == 'Caminando':
        can7.drawString(405, 353, "x")
    elif datos[380] == 'Bicicleta':
        can7.drawString(405, 341, "x")
    elif datos[380] == 'Otro':
        can7.drawString(405, 329, "x")
        can7.drawString(250, 329, datos[381])
    #adquiere agua de otra fuente
    if datos[382] == 'Si':
        can7.drawString(320, 260, "x")
        #cuanta agua adquiere de esa fuente
        can7.drawString(360, 220, datos[383])
        #cual es la otra fuente
        if datos[384] == 'Galón/pimpina':
            can7.drawString(405, 145, "x")
        elif datos[384] == 'Carrotanque':
            can7.drawString(405, 134, "x")
        elif datos[384] == 'Botellón':
            can7.drawString(405, 122, "x")
        elif datos[384] == 'Pozo':
            can7.drawString(405, 111, "x")
    elif datos[382] == 'No':
        can7.drawString(320, 248, "x")
        
    can7.save()

    packet8 = io.BytesIO()
    can8 = canvas.Canvas(packet8, pagesize=A4)
    can8.setFont("Helvetica", 8)
    can8.drawString(410, 815, datos[3])
    can8.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can8, 398, 800, dia, 10)
    #mes
    llenarCampos(can8, 440, 800, '04', 10)
    #anio
    llenarCampos(can8, 488, 800, '2022', 10)

    if datos[385] == 'Si':
        can8.drawString(320, 743, 'x')
    elif datos[385] == 'No':
        can8.drawString(320, 730, 'x')
    #cuanto debe pagar
    if datos[386] == None:
        can8.drawString(200, 712, '-')
    else:
        can8.drawString(200, 712, datos[386])
    #tratamiento del agua
    if datos[387] == 'Filtrarla':
        can8.drawString(404,637,'x')
    elif datos[387] == 'Calentarla':
        can8.drawString(404,625,'x')
    elif datos[387] == 'Pastillas de Cloro':
        can8.drawString(404,613,'x')
    elif datos[387] == 'Ninguno':
        can8.drawString(404,601,'x')
    elif datos[387] == 'Otro':
        can8.drawString(404,591,'x')
        can8.drawString(250,589,datos[388])
    #espacio de almacenamiento de agua
    if datos[389] == 'Si':
        can8.drawString(320, 510, 'x')
    elif datos[389] == 'No':
        can8.drawString(320, 498, 'x')
    #capacidad promedio
    if datos[390] == None:
        can8.drawString(310, 480, '-')
    else:
        can8.drawString(310, 480, datos[390])
    #se utilizan los almacenamientos para otras actividades 
    if datos[391] == 'Si':
        can8.drawString(320, 405, 'x')
    elif datos[391] == 'No' or datos[391] == '-':
        can8.drawString(320, 393, 'x')
    
    #se realizan procedimientos de limpieza
    if datos[392] == 'Si':
        can8.drawString(320, 315, 'x')
    elif datos[392] == 'No':
        can8.drawString(320, 303, 'x')
    elif datos[392] == 'No sabe' or datos[392] == '-':
        can8.drawString(320, 291, 'x')
    #tiene sitio para las basuras
    if datos[393] == 'Si':
        can8.drawString(320, 224, 'x')
    elif datos[393] == 'No':
        can8.drawString(320, 212, 'x')
    #cuenta con servicio de recoleccion
    if datos[394] == 'Municipal':
        can8.drawString(320, 140, 'x')
    elif datos[394]== 'Veredal':
        can8.drawString(320, 128, 'x')
    elif datos[394] == 'No Tiene':
        can8.drawString(320, 116, 'x')
    can8.save()


    packet9 = io.BytesIO()
    can9 = canvas.Canvas(packet9, pagesize=A4)
    can9.setFont("Helvetica", 8)
    can9.drawString(410, 815, datos[3])
    can9.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can9, 398, 800, dia, 10)
    #mes
    llenarCampos(can9, 440, 800, '04', 10)
    #anio
    llenarCampos(can9, 488, 800, '2022', 10)

    if datos[395] == 'Cielo abierto':
        can9.drawString(404,758,'x')
    elif datos[395] == 'Botadero':
        can9.drawString(404,746,'x')
    elif datos[395] == 'Incineración':
        can9.drawString(404,734,'x')
    elif datos[395] == 'Enterramiento':
        can9.drawString(404,722,'x')
    #elementos emplea
    if datos[396] == 'Bolsa plástica':
        can9.drawString(404,664,'x')
    elif datos[396] == 'En Caneca con tapa':
        can9.drawString(404,652,'x')
    elif datos[396] == 'Pozo comunitario':
        can9.drawString(404,640,'x')
    #dispocision aguas negras
    if datos[397] == 'Alcantarrillado':
        can9.drawString(404, 580, 'x')
    elif datos[397] == 'Pozo séptico':
        can9.drawString(404, 568, 'x')
    elif datos[397] == 'Campo abierto':
        can9.drawString(404, 556, 'x')
    elif datos[397] == 'Letrina':
        can9.drawString(404, 544, 'x')
    elif datos[397] == 'Río':
        can9.drawString(404, 532, 'x')
    elif datos[397] == 'Quebrada':
        can9.drawString(404, 520, 'x')
    elif datos[397] == 'Arroyo':
        can9.drawString(404, 508, 'x')
    elif datos[397] == 'Otro':
        can9.drawString(404, 496, 'x')
        can9.drawString(240, 496, datos[398])
    #dispocision de aguas residual99
    if datos[399] == 'Pozo séptico':
        can9.drawString(404,436, 'x')
    elif datos[399] == 'Campo abierto':
        can9.drawString(404,424, 'x')
    elif datos[399] == 'Letrina':
        can9.drawString(404,412, 'x')
    elif datos[399] == 'Río':
        can9.drawString(404,400, 'x')
    elif datos[399] == 'Quebrada':
        can9.drawString(404,388, 'x')
    elif datos[399] == 'Arroyo':
        can9.drawString(404,376, 'x')
    elif datos[399] == 'Otro':
        can9.drawString(404,364, 'x')
        can9.drawString(240,364, datos[400])
    familia = (json.loads(datos[13]))
    hijo1 = False
    hijo2 = False
    hijo3 = False
    hijo4 = False
    hijo5 = False
    for i in range(len(familia)):
        integrante = dict(familia[i])
        if integrante['Parentesco'] == 'Jefe (a) de hogar':
            can9.drawString(130, 201, 'x')
            can9.drawString(231, 201, integrante['Genero'])
            can9.drawString(281, 201, str(integrante['Edad']))
            can9.drawString(331, 201, integrante['Registro'])
            can9.drawString(381, 201, integrante['Escolaridad'])
            can9.drawString(476, 201, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Pareja, esposo(a), cónyuge, compañero(a)':
            can9.drawString(130, 181, 'x')
            can9.drawString(231, 181, integrante['Genero'])
            can9.drawString(281, 181, str(integrante['Edad']))
            can9.drawString(331, 181, integrante['Registro'])
            can9.drawString(381, 181, integrante['Escolaridad'])
            can9.drawString(476, 181, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)' and hijo1 == False:
            hijo1 = True
            can9.drawString(130, 168, 'x')
            can9.drawString(231, 168, integrante['Genero'])
            can9.drawString(281, 168, str(integrante['Edad']))
            can9.drawString(331, 168, integrante['Registro'])
            can9.drawString(381, 168, integrante['Escolaridad'])
            can9.drawString(476, 168, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)' and hijo1 == True and hijo2 == False:
            hijo2 = True
            can9.drawString(130, 155, 'x')
            can9.drawString(231, 155, integrante['Genero'])
            can9.drawString(281, 155, str(integrante['Edad']))
            can9.drawString(331, 155, integrante['Registro'])
            can9.drawString(381, 155, integrante['Escolaridad'])
            can9.drawString(476, 155, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 3' and hijo2 == True and hijo3 == False:
            hijo3 = True
            can9.drawString(130, 142, 'x')
            can9.drawString(231, 142, integrante['Genero'])
            can9.drawString(281, 142, str(integrante['Edad']))
            can9.drawString(331, 142, integrante['Registro'])
            can9.drawString(381, 142, integrante['Escolaridad'])
            can9.drawString(476, 142, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 4' and hijo3 == True and hijo4 == False:
            hijo4 = True
            can9.drawString(130, 129, 'x')
            can9.drawString(231, 129, integrante['Genero'])
            can9.drawString(281, 129, str(integrante['Edad']))
            can9.drawString(331, 129, integrante['Registro'])
            can9.drawString(381, 129, integrante['Escolaridad'])
            can9.drawString(476, 129, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 5' and hijo4 == True and hijo5 == False:
            can9.drawString(130, 116, 'x')
            can9.drawString(231, 116, integrante['Genero'])
            can9.drawString(281, 116, str(integrante['Edad']))
            can9.drawString(331, 116, integrante['Registro'])
            can9.drawString(381, 116, integrante['Escolaridad'])
            can9.drawString(476, 116, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Nieto(a)':
            can9.drawString(130, 103, 'x')
            can9.drawString(231, 103, integrante['Genero'])
            can9.drawString(281, 103, str(integrante['Edad']))
            can9.drawString(331, 103, integrante['Registro'])
            can9.drawString(381, 103, integrante['Escolaridad'])
            can9.drawString(476, 103, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Suegro(a)':
            can9.drawString(130, 91, 'x')
            can9.drawString(231, 91, integrante['Genero'])
            can9.drawString(281, 91, str(integrante['Edad']))
            can9.drawString(331, 91, integrante['Registro'])
            can9.drawString(381, 91, integrante['Escolaridad'])
            can9.drawString(476, 91, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Tios(as)':
            can9.drawString(130, 78, 'x')
            can9.drawString(231, 78, integrante['Genero'])
            can9.drawString(281, 78, str(integrante['Edad']))
            can9.drawString(331, 78, integrante['Registro'])
            can9.drawString(381, 78, integrante['Escolaridad'])
            can9.drawString(476, 78, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Yerno, nuera':
            can9.drawString(130, 66, 'x')
            can9.drawString(231, 66, integrante['Genero'])
            can9.drawString(281, 66, str(integrante['Edad']))
            can9.drawString(331, 66, integrante['Registro'])
            can9.drawString(381, 66, integrante['Escolaridad'])
            can9.drawString(476, 66, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Otro (a) pariente del (de la) jefe (a)':
            can9.drawString(130, 48, 'x')
            can9.drawString(231, 48, integrante['Genero'])
            can9.drawString(281, 48, str(integrante['Edad']))
            can9.drawString(331, 48, integrante['Registro'])
            can9.drawString(381, 48, integrante['Escolaridad'])
            can9.drawString(476, 48, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Otro (a) no pariente':
            can9.drawString(130, 36, 'x')
            can9.drawString(231, 36, integrante['Genero'])
            can9.drawString(281, 36, str(integrante['Edad']))
            can9.drawString(331, 36, integrante['Registro'])
            can9.drawString(381, 36, integrante['Escolaridad'])
            can9.drawString(476, 36, integrante['Ocupacion'])
    can9.save()
    packet10 = io.BytesIO()
    can10 = canvas.Canvas(packet10, pagesize=A4)
    can10.setFont("Helvetica", 8)
    can10.drawString(410, 815, datos[3])
    can10.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can10, 398, 800, dia, 10)
    #mes
    llenarCampos(can10, 440, 800, '04', 10)
    #anio
    llenarCampos(can10, 488, 800, '2022', 10)
    #temporalidad de la vivienda
    if datos[15]=='Permanente':
        can10.drawString(390, 733, "x")
    elif datos[15]=='Temporal':
        can10.drawString(390, 721, "x")
    #Contribuye al ingreso
    if datos[18]=='Si':
        can10.drawString(323, 663, "x")
    elif datos[18]=='No':
        can10.drawString(368, 663, "x")
    #Se Reconoce como
    if datos[20]=='Indígena':
        can10.drawString(408, 596, "x")
    elif datos[20]=='Gitano (a)(ROM)':
        can10.drawString(408, 584, "x")
    elif datos[20]=='Raizal de San Andrés, Providencia, Santa Catalina':
        can10.drawString(408, 572, "x")
    elif datos[20]=='Palenquero (a)':
        can10.drawString(408, 560, "x")
    elif datos[20]=='Negro (a), afrodescendiente, afrocolombiano (a)':
        can10.drawString(408, 548, "x")
    elif datos[20]=='Ninguno de los anteriores':   
        can10.drawString(408, 536, "x")
    #HABLA LA lengua nativa
    if datos[22] == 'Si':
        can10.drawString(320, 468, "x")
    elif datos[22] == 'Si':
        can10.drawString(320, 456, "x")
    #cual lengua nativa habla
    can10.drawString(70, 416, datos[23])
    #alguna persona tiene problemas de salud
    if datos[24] == 'Si':
        can10.drawString(323, 338, "x")
    elif datos[24] == 'No':
        can10.drawString(368, 338, "x")
    if datos[25] == 'Si':
        can10.drawString(320, 270, "x")
    elif datos[25] == 'No':
        can10.drawString(320, 258, "x")
    #cual organizacion pertenece
    can10.drawString(70, 190, datos[26])
     #domesticas
    if datos[27] == 'true':
        can10.drawString(364, 76, "x")
    if datos[37] == 'true':
        can10.drawString(404, 76, "x")
    if datos[47] == 'true':
        can10.drawString(444, 76, "x")
    if datos[57] == 'true':
        can10.drawString(484, 76, "x")
        #pagos
    if datos[28] == 'true':
        can10.drawString(364, 64, "x")
    if datos[38] == 'true':
        can10.drawString(404, 64, "x")
    if datos[48] == 'true':
        can10.drawString(444, 64, "x")
    if datos[58] == 'true':
        can10.drawString(484, 64, "x")
        #finca
    if datos[29] == 'true':
        can10.drawString(364, 50, "x")
    if datos[39] == 'true':
        can10.drawString(404, 50, "x")
    if datos[49] == 'true':
        can10.drawString(444, 50, "x")
    if datos[59] == 'true':
        can10.drawString(484, 50, "x")
        #Transporte
    if datos[30] == 'true':
        can10.drawString(364, 35, "x")
    if datos[40] == 'true':
        can10.drawString(404, 35, "x")
    if datos[50] == 'true':
        can10.drawString(444, 35, "x")
    if datos[60] == 'true':
        can10.drawString(484, 35, "x")
    can10.save()
    packet11 = io.BytesIO()
    can11 = canvas.Canvas(packet11, pagesize=A4)
    can11.setFont("Helvetica", 8)
    can11.drawString(410, 815, datos[3])
    can11.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)
    llenarCampos(can11, 398, 800, dia, 10)
    #mes
    llenarCampos(can11, 440, 800, '04', 10)
    #anio
    llenarCampos(can11, 488, 800, '2022', 10)
    # quienes realizan las labores
        #admin finca
    if datos[31] == 'true':
        can11.drawString(364, 756, "x")
    if datos[41] == 'true':
        can11.drawString(404, 756, "x")
    if datos[51] == 'true':
        can11.drawString(444, 756, "x")
    if datos[61] == 'true':
        can11.drawString(484, 756, "x")
        #comercia
    if datos[32] == 'true':
        can11.drawString(364, 744, "x")
    if datos[42] == 'true':
        can11.drawString(404, 744, "x")
    if datos[52] == 'true':
        can11.drawString(444, 744, "x")
    if datos[62] == 'true':
        can11.drawString(484, 744, "x")
        #Estudia
    if datos[33] == 'true':
        can11.drawString(364, 732, "x")
    if datos[43] == 'true':
        can11.drawString(404, 732, "x")
    if datos[53] == 'true':
        can11.drawString(444, 732, "x")
    if datos[63] == 'true':
        can11.drawString(484, 732, "x")
        #fORMACION HIJOS
    if datos[34] == 'true':
        can11.drawString(364, 719, "x")
    if datos[44] == 'true':
        can11.drawString(404, 719, "x")
    if datos[54] == 'true':
        can11.drawString(444, 719, "x")
    if datos[64] == 'true':
        can11.drawString(484, 719, "x")
        #Cuidado adultos
    if datos[35] == 'true':
        can11.drawString(364, 706, "x")
    if datos[45] == 'true':
        can11.drawString(404, 706, "x")
    if datos[55] == 'true':
        can11.drawString(444, 706, "x")
    if datos[65] == 'true':
        can11.drawString(484, 706, "x")
        #Otro
    if datos[36] == 'true':
        can11.drawString(364, 693, "x")
    if datos[46] == 'true':
        can11.drawString(404, 693, "x")
    if datos[56] == 'true':
        can11.drawString(444, 693, "x")
    if datos[66] == 'true':
        can11.drawString(160, 693, "Otro")
        can11.drawString(484, 693, "x")
    #fuentes de ingtreso en el hogar
    if datos[123] == 'true':
        can11.drawString(402, 543, "x")
    if datos[124] == 'true':
        can11.drawString(402, 531, "x")
    if datos[125] == 'true':
        can11.drawString(402, 519, "x")
    if datos[126] == 'true':
        can11.drawString(402, 507, "x")
    if datos[127] == 'true':
        can11.drawString(402, 493, "x")
    if datos[128] == 'true':
        can11.drawString(402, 481, "x")
    if datos[129] == 'true':
        can11.drawString(402, 469, "x")
    if datos[130] == 'true':
        can11.drawString(402, 457, "x")
    if datos[131] == 'true':
        can11.drawString(402, 445, "x")
    if datos[132] == 'true':
        can11.drawString(402, 431, "x")
    if datos[133] == 'true':
        can11.drawString(402, 419, "x")
    if datos[134] == 'true':
        can11.drawString(402, 407, "x")
    if datos[135] == 'true':
        can11.drawString(402, 393, "x")
    if datos[136] == 'true':
        can11.drawString(402, 381, "x")
    if datos[137] == 'true':
        can11.drawString(402, 369, "x")
        can11.drawString(242, 369, datos[137])
    #que cultivan
    can11.drawString(142, 329, datos[138])
    can11.drawString(142, 316, datos[139])
    can11.drawString(142, 303, datos[140])
    can11.drawString(142, 290, datos[141])
    can11.drawString(350, 223, datos[142])
    can11.drawString(350, 211, datos[143])
    can11.drawString(350, 199, datos[144])
    can11.drawString(350, 187, datos[145])
    can11.drawString(350, 173, datos[146])
    can11.drawString(350, 161, datos[147])
    can11.drawString(350, 149, datos[148])
    can11.drawString(350, 137, datos[149])
    can11.drawString(350, 125, datos[150])
    can11.drawString(350, 111, datos[151])
    can11.drawString(350, 99, datos[152])
    can11.drawString(350, 87, datos[153])
    can11.drawString(242, 87, datos[155])
    can11.drawString(350, 73, datos[154])    
    can11.save()
    packet12 = io.BytesIO()
    can12 = canvas.Canvas(packet12, pagesize=A4)
    can12.setFont("Helvetica", 8)
    can12.drawString(410, 815, datos[3])
    can12.drawImage('encabezadopgs.JPG', 54, 795, 170, 40)
    #fecha de formulario
    #dia
    dia = random.randint(1, 8)
    dia = '0'+str(dia)  
    llenarCampos(can12, 398, 800, dia, 10)
    #mes
    llenarCampos(can12, 440, 800, '04', 10)
    #anio
    llenarCampos(can12, 488, 800, '2022', 10)
    #nombre
    can12.drawString(110, 670, datos[81])
    #telefono c
    can12.drawString(300, 682, datos[83])
    #telefono f
    can12.drawString(300, 656, datos[84])
    #correo 
    can12.drawString(300, 632, datos[86])
    # No ID
    can12.drawString(110, 632, datos[85])
    # firma
    
    # No ID
    can12.drawString(300, 490, datos[93])
    #nombre encuestador
    nombreEncuestador = datos[348] + " " + datos[349]
    can12.drawString(110, 290, nombreEncuestador)
    can12.drawString(310, 306,datos[355])
    #telefono f
    can12.drawString(310, 276, datos[356])
    can12.drawString(310, 236, datos[358])
    can12.drawString(110, 236, datos[357])

    #firmaaa
    with bd.cursor() as cursor:
              cursor.execute("Select rutaserver from suncosurvey.fotos_firma where Id_Encuesta = '"+id+"';")
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

    can12.drawImage('new.png', 75, 500, 200, 99)
    #tipo id
    #can12.drawString(490, 580, "x")
    can12.drawString(490, 568, "x")
    #can12.drawString(490, 553, "x")
    #can12.drawString(360, 550, "otro")
    can12.drawImage('blanco.JPG', 69, 730, 458, 20)
    can12.save()

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
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-01.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-02.pdf", "rb"))
    existing_pdf3 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-03.pdf", "rb"))
    existing_pdf4 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-04.pdf", "rb"))
    existing_pdf5 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-05.pdf", "rb"))
    existing_pdf6 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-06.pdf", "rb"))
    existing_pdf7 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-07.pdf", "rb"))
    existing_pdf8 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-08.pdf", "rb"))
    existing_pdf9 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-09.pdf", "rb"))
    existing_pdf10 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-10.pdf", "rb"))
    existing_pdf11 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-11.pdf", "rb"))
    existing_pdf12 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-12.pdf", "rb"))
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
    outputStream = open("pdfs/"+carpeta+"/"+carpeta+"-replanteo.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    generarFotosCoordenadas(id, carpeta)




    

if __name__ == '__main__':
   generarPdfSocializacion('307-1605790991386')