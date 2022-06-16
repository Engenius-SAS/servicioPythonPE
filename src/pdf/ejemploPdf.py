import PyPDF2 
import io
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import zipfile
import pymysql 

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
   
    
    

def generarPdfId( id):
    bd = obtener_conexion()
    with bd.cursor() as cursor:
              cursor.execute("SELECT A.*,B.*,C.*,D.*,E.*,F.*,G.*,H.*,N.*,I.*,J.*,K.*,M.* FROM aes2021.Encabezado A INNER JOIN aes2021.Sociodemograficas B ON A.Id_Encuesta = B.Id_Encuesta INNER JOIN aes2021.Caracteristicas C ON A.Id_Encuesta = C.Id_Encuesta INNER JOIN aes2021.Consentimiento D ON A.Id_Encuesta = D.Id_Encuesta INNER JOIN aes2021.Datos E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN aes2021.Economia F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN aes2021.Energia G ON A.Id_Encuesta = G.Id_Encuesta INNER JOIN aes2021.Servicios H ON A.Id_Encuesta = H.Id_Encuesta INNER JOIN aes2021.Tratamiento_DP I ON A.Id_Encuesta = I.Id_Encuesta INNER JOIN aes2021.Ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN aes2021.Sociales K ON A.Id_Encuesta = K.Id_Encuesta INNER JOIN aes2021.Agua N ON A.Id_Encuesta = N.Id_Encuesta INNER JOIN aes2021.Proyectos_funcionarios L ON A.Id_Proyecto_Funcionario = L.Id_Proyecto_Funcionario INNER JOIN aes2021.Funcionarios M ON M.Id_Funcionario = L.Id_Funcionario WHERE A.isdelete = 0 AND A.Id_Encuesta = '"+id+"';")
              datos = cursor.fetchone()
    print(datos[239])
    if os.path.exists("src/destination.pdf"):
        os.remove('src/destination.pdf')
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(380, 802, "100000000000")
    can.save()
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=letter)
    can2.drawString(380, 802, "100000000000")
    if datos[359] == 'Si':
        can2.drawString(315, 722, "X")
    else:
        can2.drawString(315, 710, "X")
    if datos[363] == 'Permanente': 
        can2.drawString(320, 633, "X")
    elif datos[363] == 'Temporal':
        can2.drawString(320, 620, "X")
    if datos[162] == 'Si': 
        can2.drawString(320, 368, "X")
    else:
        can2.drawString(370, 368, "X")
    fuente = datos[185]
    if fuente == 'Gas Propano': 
        can2.drawString(335, 290, datos[163])
        can2.drawString(450, 290, datos[174])
    elif fuente == 'Gas Natural':
        can2.drawString(335, 276, datos[164])
        can2.drawString(450, 276, datos[175])
    elif fuente == 'Gasolina':
        can2.drawString(335, 264, datos[165])
        can2.drawString(450, 264, datos[176])
    elif fuente == 'Kerosene':
        can2.drawString(335, 250, datos[166])
        can2.drawString(450, 250, datos[177])
    elif fuente == 'Petróleo':
        can2.drawString(335, 238, datos[167])
        can2.drawString(450, 238, datos[178])
    elif fuente == 'Alcohol':
        can2.drawString(335, 226, datos[168])
        can2.drawString(450, 226, datos[179])
    elif fuente == 'Carbón Mineral':
        can2.drawString(335, 214, datos[169])
        can2.drawString(450, 214, datos[180])
    elif fuente == 'Leña Comprada':
        can2.drawString(335, 202, datos[170])
        can2.drawString(450, 202, datos[181])
    elif fuente == 'Leña Auto Apropiada':
        can2.drawString(335, 190, datos[171])
    elif fuente == 'Residuos del Agro':
        can2.drawString(335, 178, datos[172])
        can2.drawString(450, 178, datos[183])
    elif fuente == 'Otro':
        can2.drawString(150, 168, datos[186])
        can2.drawString(260, 168, "kg")
        can2.drawString(335, 164, datos[173])
        can2.drawString(450, 164, datos[184])
    can2.drawString(350, 140, datos[187] + "  horas")
    can2.save()
    #hoja 3 del pdf
    packet3 = io.BytesIO()
    # create a new PDF with Reportlab
    can3 = canvas.Canvas(packet3, pagesize=letter)
    can3.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can3, 398, 800, "01", 10)
    #mes
    llenarCampos(can3, 440, 800, "01", 10)
    #anio
    llenarCampos(can3, 488, 800, "2021", 10)
    #fuente para iluminarse
    consumoMes= "1000"
    costo = "10000"
    localizacion = "Vereda"
    #pilas baterias
    if datos[239] == 'Baterias':
        can3.drawString(280, 740, datos[214])
        can3.drawString(340, 740, datos[222])
        if datos[230] == 'Cabecera municipal':
            can3.drawString(420, 740, 'x')
        elif datos[230] == 'Vereda':
            can3.drawString(462, 740, 'x')
        elif datos[230] == 'Domicilio':  
            can3.drawString(505, 740, 'x')
    #gasolina
    elif datos[239] == 'Planta eléctrica a gasolina':
        can3.drawString(280, 728, datos[215])
        can3.drawString(340, 728, datos[223])
        if datos[231] == 'Cabecera municipal':
            can3.drawString(420, 728, 'x')
        elif datos[231] == 'Vereda':
            can3.drawString(462, 728, 'x')
        elif datos[231] == 'Domicilio':
            can3.drawString(505, 728, 'x')
    #Kerosene
    elif datos[239] == 'Kerosene':
        can3.drawString(280, 716, datos[216])
        can3.drawString(340, 716, datos[224])
        if datos[232] == 'Cabecera municipal':
            can3.drawString(420, 716, 'x')
        elif datos[232] == 'Vereda':
            can3.drawString(462, 716, 'x')
        elif datos[232] == 'Domicilio':
            can3.drawString(505, 716, 'x')
    #Petroleo
    if datos[239] == 'Petróleo':
        can3.drawString(280, 702, datos[217])
        can3.drawString(340, 702, datos[225])
        if datos[233] == 'Cabecera municipal':
            can3.drawString(420, 702, 'x')
        elif datos[233] == 'Vereda':
            can3.drawString(462, 702, 'x')
        elif datos[233] == 'Domicilio':
            can3.drawString(505, 702, 'x')
    #Alcohol
    if datos[239] == 'Alcohol':
        can3.drawString(280, 692, datos[218])
        can3.drawString(340, 692, datos[226])
        if datos[234] == 'Cabecera municipal':
            can3.drawString(420, 692, 'x')
        elif datos[234] == 'Vereda':
            can3.drawString(462, 692, 'x')
        elif datos[234] == 'Domicilio':
            can3.drawString(505, 692, 'x')
    #Diesel
    if datos[239] == 'Planta eléctrica diesel':
        can3.drawString(280, 680, datos[219])
        can3.drawString(340, 680, datos[227])
        if datos[235] == 'Cabecera municipal':
            can3.drawString(420, 680, 'x')
        elif datos[235] == 'Vereda':
            can3.drawString(462, 680, 'x')
        elif datos[235] == 'Domicilio':
            can3.drawString(505, 680, 'x')
    #Velas
    if datos[239] == 'Velas':
        can3.drawString(280, 668, datos[220])
        can3.drawString(340, 668, datos[228])
        if datos[236] == 'Cabecera municipal':
            can3.drawString(420, 668, 'x')
        elif datos[236] == 'Vereda':
            can3.drawString(462, 668, 'x')
        elif datos[236] == 'Domicilio':
            can3.drawString(505, 668, 'x')
    #Otro
    if datos[239] == 'Otro':
        can3.drawString(120, 652, datos[238])
        can3.drawString(230, 652, " ")
        can3.drawString(280, 652, datos[221])
        can3.drawString(340, 652, datos[229])
        if datos[237] == 'Cabecera municipal':
            can3.drawString(420, 652, 'x')
        elif datos[237] == 'Vereda':
            can3.drawString(462, 652, 'x')
        elif datos[237] == 'Domicilio':
            can3.drawString(505, 652, 'x')
     #Horas al dia utiliza
    can3.drawString(410, 612, datos[240])
    #Queman residuos
    if datos[188] == 'Si':
        can3.drawString(320, 544, "x")
    else:
        can3.drawString(370, 544, "x")
    #Fuente quema residuos
    consumoQuemar = "10000"
    valorMesQuemar = "100000"
    #gas propano
    if datos[211] == "Gas Propano":
        can3.drawString(340, 455, datos[189])
        can3.drawString(442, 455, datos[200])
    #gas natural
    if datos[211] == "Gas Natural":
        can3.drawString(340, 442, datos[190])
        can3.drawString(442, 442, datos[201])
    #gasolina
    if datos[211] == "Gasolina":
        can3.drawString(340, 430, datos[191])
        can3.drawString(442, 430, datos[202])
    #
    if datos[211] == "Kerosene":
            can3.drawString(340, 417, datos[192])
            can3.drawString(442, 417, datos[203])
    #Petroleo
    if datos[211] == "Petróleo":
            can3.drawString(340, 404, datos[193])
            can3.drawString(442, 404, datos[204])
    #Carbon mineral
    if datos[211] == "Alcohol":
        can3.drawString(340, 391, datos[194])
        can3.drawString(442, 391, datos[205])
    #Leña comprada
    if datos[211] == "Carbón Mineral":
        can3.drawString(340, 378, datos[195])
        can3.drawString(442, 378, datos[206])
    #Leña autoapropiada
    if datos[211] == "Leña Comprada":
        can3.drawString(340, 367, datos[196])
        can3.drawString(442, 367, datos[207])
    #gas propano
    if datos[211] == "Leña Auto Apropiada":
        can3.drawString(340, 354, datos[197])
    #residuos del agro
    if datos[211] == "Residuos del Agro":
        can3.drawString(340, 343, datos[198])
        can3.drawString(442, 343, datos[209])
    #Otro
    if datos[211] == "Otro": 
        can3.drawString(150, 333, datos[212])
        can3.drawString(260, 333, " ")
        can3.drawString(340, 330, datos[199])
        can3.drawString(442, 330, datos[210])
    #cuantas horas al dia utiliza para ilumminar 
    can3.drawString(350, 305, datos[213])
    #contaminacion 
    #exceso de ruido
    if datos[274] == 'Si':
        can3.drawString(385, 210, "x")
    else:
        can3.drawString(430, 210, "x")
    #malos oloress
    if datos[272] == 'Si':
        can3.drawString(385, 195, "x")
    else:
        can3.drawString(430, 195, "x")
    # uso del predio
    #residencial
    if datos[73] == 'Residencial':
        can3.drawString(415, 92, "x")
    #negocio
    elif datos[73] == 'Negocio':
        can3.drawString(415, 80, "x")
    #mixto
    elif datos[73] == 'Mixto':
        can3.drawString(415, 68, "x")
    #institucional
    elif datos[73] == 'Institución':
        can3.drawString(415, 56, "x")
    can3.save()
    #hoja 4 del pdf
    packet4 = io.BytesIO()
    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet4, pagesize=letter)
    can4.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can4, 398, 800, "01", 10)
    #mes
    llenarCampos(can4, 440, 800, "01", 10)
    #anio
    llenarCampos(can4, 488, 800, "2021", 10)
    #estrato del predio
    print(datos[74])
    if datos[74] == 'Estrato 1':
        can4.drawString(255, 748, "x")
    #2
    elif datos[74] == 'Estrato 2':
        can4.drawString(280, 748, "x")
    #3
    elif datos[74] == 'Estrato 3':
        can4.drawString(305, 748, "x")
    #4
    elif datos[74] == 'Estrato 4':
        can4.drawString(330, 748, "x")
    #5
    elif datos[74] == 'Estrato 5':
        can4.drawString(350, 748, "x")
    #6
    elif datos[74] == 'Estrato 6':
        can4.drawString(375, 748, "x")
    #Nombre de la comunidad
    can4.drawString(90, 670, datos[103])
    #personas en la comunidad 
    llenarCampos(can4, 315, 598, datos[116], 30)
    #la vivienda se encuentra ubicada al interior de 
    #caserio
    if datos[104] == 'Caserío':
        can4.drawString(405, 536, "x")
    #resguardo indigena
    elif datos[104] == 'Resguardo indígena':
        can4.drawString(405, 523, "x")
    #parcialidad
    elif datos[104] == 'Parcialidad o asentamiento indígena fuera del resguardo':
        can4.drawString(405, 510, "x")
    #territorio colectivo
    elif datos[104] == 'Territorio colectivo de comunidad negra':
        can4.drawString(405, 497, "x")
    #territorio de comunidad
    elif datos[104] == 'Territorio de comunidad negra no titulada':
        can4.drawString(405, 484, "x")
    #territorio ancestral
    elif datos[104] == 'Territorio ancestral raizal del Archipiélago de San Andrés, Providencia y Santa Catalina':
        can4.drawString(405, 471, "x")
    #reancheria
    elif datos[104] == 'Ranchería - Guajira':
        can4.drawString(405, 458, "x")
    #territorio palenquero
    elif datos[104] == 'Territorio Palenquero de San Basilio':
        can4.drawString(405, 445, "x")
    #territorio gitano
    elif datos[104] == 'Territorio Gitano - ROM':
        can4.drawString(405, 432, "x")
    #zona rural
    elif datos[104] == 'Zona rural':
        can4.drawString(405, 419, "x")
    #tenencia de la vivenda
    if datos[105] == 'Propia':
        can4.drawString(350, 351, "x")
    elif datos[105] == 'Arriendo':
        can4.drawString(350, 339, "x")
    elif datos[105] == 'Colectiva':
        can4.drawString(350, 327, "x")
    # hogares en la vivienda
    llenarCampos(can4, 342, 267 , datos[106], 30)
    #personas en la vivienda
    llenarCampos(can4, 342, 222 , datos[107], 30)
    #material predominante en la vivienda
    #bloque
    if datos[108] == 'Bloque, ladrillo, piedra, madera pulida':
        can4.drawString(420, 152, "x")
    #concreto
    elif datos[108] == 'Concreto':
        can4.drawString(420, 140, "x")
    #tapia
    elif datos[108] == 'Tapia pisada, bahareque, adobe':
        can4.drawString(420, 128, "x")
    #madera
    elif datos[108] == 'Madera burda, tabla, tablón':
        can4.drawString(420, 116, "x")
    #prefabricado
    elif datos[108] == 'Material prefabricado':
        can4.drawString(420, 104, "x")
    #guadua
    elif datos[108] == 'Guadua, caña, esterilla, otros vegetales':
        can4.drawString(420, 92, "x")
    #desechos
    elif datos[108] == 'Materiales de desecho (zinc, tela, cartón, latas, plásticos, otros)':
        can4.drawString(420, 80, "x")
    #no tiene
    elif datos[108] == 'No tiene paredes':
        can4.drawString(420, 68, "x")
    can4.save()
    #hoja 5 del pdf
    packet5 = io.BytesIO()
    # create a new PDF with Reportlab
    can5 = canvas.Canvas(packet5, pagesize=letter)
    can5.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can5, 398, 800, "01", 10)
    #mes
    llenarCampos(can5, 440, 800, "01", 10)
    #anio
    llenarCampos(can5, 488, 800, "2021", 10)
    #material predominante techo
    if datos[109] == 'Paja, palma y otros vegetales':
        can5.drawString(420, 742, "x")
    elif datos[109] == 'Plancha de cemento, concreto y hormigón':
        can5.drawString(420, 730, "x")
    elif datos[109] == 'Tejas (barro, asbesto - cemento, metálica o lámina de zinc, plástica)':
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
    llenarCampos(can5, 300, 417, datos[115],30)
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
    if datos[291] == 'true':
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
    if datos[290] == 'true':
        can5.drawString(465, 167, "x")
    else:
        can5.drawString(500, 167, "x")
    can5.save()
    #hoja 6 del pdf
    packet6 = io.BytesIO()
    # create a new PDF with Reportlab
    can6 = canvas.Canvas(packet6, pagesize=letter)
    can6.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can6, 398, 800, "01", 10)
    #mes
    llenarCampos(can6, 440, 800, "01", 10)
    #anio
    llenarCampos(can6, 488, 800, "2021", 10)
    #Servicio sanitario
    print('sanitariop', datos[299])
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
    if datos[312] == 'Si':
        can6.drawString(320, 480, "x")
    elif datos[312] == 'No':
        can6.drawString(320, 467, "x")
    #que cantidad de agua puede obtener
    can6.drawString(100, 430, datos[313])
    #promedio cantidad de agua
    can6.drawString(400, 395, datos[314])
    #fuente principal de abastesimiento de agua
    if datos[315] == 'Jagüey':
        can6.drawString(400, 313, "x")
    elif datos[315] == 'Pozo':
        can6.drawString(400, 301, "x")
    elif datos[315] == 'Molino':
        can6.drawString(400, 289, "x")
    elif datos[315] == 'Carrotanques':
        can6.drawString(400, 277, "x")
    elif datos[315] == 'Aguas lluvias':
        can6.drawString(400, 265, "x")
    elif datos[315] == 'Ríos':
        can6.drawString(400, 253, "x")
    elif datos[315] == 'Arroyos':
        can6.drawString(400, 241, "x")
    elif datos[315] == 'Quebradas':
        can6.drawString(400, 228, "x")
    elif datos[315] == 'Otro':
        can6.drawString(400, 216, "x")
    #la casimba es comunitaria
    if datos[319] == 'Si':
        can6.drawString(320, 147, "x")
    elif datos[319] == 'No':    
        can6.drawString(320, 135, "x")
    #cual
    can6.drawString(120, 110, datos[318])
    can6.save()
    #hoja 7 del pdf
    packet7 = io.BytesIO()
    # create a new PDF with Reportlab
    can7 = canvas.Canvas(packet7, pagesize=letter)
    can7.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can7, 398, 800, "01", 10)
    #mes
    llenarCampos(can7, 440, 800, "01", 10)
    #anio
    llenarCampos(can7, 488, 800, "2021", 10)
     #uso del agua que obtienen
    usosAgua = datos[320].split(',')
    
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
    if datos[322] == 'Si':
        can7.drawString(320, 626, "x")
    elif datos[322] == 'No':
        can7.drawString(320, 614, "x")
    else:
        can7.drawString(320, 602, "x")
    #cuanto dura el agua que recolecta
    can7.drawString(300, 573, datos[323])
    #cantidad destinada higiene
    can7.drawString(100, 528, datos[324])
    #distancia para obtener agua
    can7.drawString(300, 495, datos[325])
    #ti3mpo destina a la recoleccion de agua
    can7.drawString(100, 450, datos[326])
    #medio de transporte para el agua
    if datos[327] == 'Moto':
        can7.drawString(405, 377, "x")
    elif datos[327] == 'Transporte animal':    
        can7.drawString(405, 365, "x")
    elif datos[327] == 'Caminando':
        can7.drawString(405, 353, "x")
    elif datos[327] == 'Bicicleta':
        can7.drawString(405, 341, "x")
    elif datos[327] == 'Otro':
        can7.drawString(405, 329, "x")
        can7.drawString(250, 329, datos[328])
    #adquiere agua de otra fuente
    if datos[329] == 'Si':
        can7.drawString(320, 260, "x")
    elif datos[329] == 'No':
        can7.drawString(320, 248, "x")
    #cuanta agua adquiere de esa fuente
    can7.drawString(360, 220, datos[330])
    #cual es la otra fuente
    if datos[331] == 'Galón/pimpina':
        can7.drawString(405, 145, "x")
    elif datos[331] == 'Carrotanque':
        can7.drawString(405, 134, "x")
    elif datos[331] == 'Botellón':
        can7.drawString(405, 122, "x")
    elif datos[331] == 'Pozo':
        can7.drawString(405, 111, "x")
    can7.save()
    #hoja 8 del pdf
    packet8 = io.BytesIO()
    # create a new PDF with Reportlab
    can8 = canvas.Canvas(packet8, pagesize=letter)
    can8.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can8, 398, 800, "01", 10)
    #mes
    llenarCampos(can8, 440, 800, "01", 10)
    #anio
    llenarCampos(can8, 488, 800, "2021", 10)
    if datos[332] == 'Si':
        can8.drawString(320, 743, 'x')
    elif datos[332] == 'No':
        can8.drawString(320, 730, 'x')
    #cuanto debe pagar
    can8.drawString(200, 712, datos[333])
    #tratamiento del agua
    if datos[334] == 'Filtrarla':
        can8.drawString(404,637,'x')
    elif datos[334] == 'Calentarla':
        can8.drawString(404,625,'x')
    elif datos[334] == 'Pastillas de Cloro':
        can8.drawString(404,613,'x')
    elif datos[334] == 'Ninguno':
        can8.drawString(404,601,'x')
    elif datos[334] == 'Otro':
        can8.drawString(404,591,'x')
        can8.drawString(250,589,datos[335])
    #espacio de almacenamiento de agua
    if datos[336] == 'Si':
        can8.drawString(320, 510, 'x')
    elif datos[336] == 'No':
        can8.drawString(320, 498, 'x')
    #capacidad promedio
    can8.drawString(310, 480, datos[337])
    #se utilizan los almacenamientos para otras actividades 
    if datos[338] == 'Si':
        can8.drawString(320, 405, 'x')
    elif datos[338] == 'No':
        can8.drawString(320, 393, 'x')
    #se realizan procedimientos de limpieza
    if datos[339] == 'Si':
        can8.drawString(320, 315, 'x')
    elif datos[339] == 'No':
        can8.drawString(320, 303, 'x')
    elif datos[339] == 'No sabe':
        can8.drawString(320, 291, 'x')
    #tiene sitio para las basuras
    if datos[340] == 'Si':
        can8.drawString(320, 224, 'x')
    elif datos[340] == 'No':
        can8.drawString(320, 212, 'x')
    #cuenta con servicio de recoleccion
    if datos[341] == 'Municipal':
        can8.drawString(320, 140, 'x')
    elif datos[341]== 'Veredal':
        can8.drawString(320, 128, 'x')
    elif datos[341] == 'No Tiene':
        can8.drawString(320, 116, 'x')
    can8.save()
    #hoja 9 del pdf
    packet9 = io.BytesIO()
    # create a new PDF with Reportlab
    can9 = canvas.Canvas(packet9, pagesize=letter)
    can9.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can9, 398, 800, "01", 10)
    #mes
    llenarCampos(can9, 440, 800, "01", 10)
    #anio
    llenarCampos(can9, 488, 800, "2021", 10)
    if datos[342] == 'Cielo abierto':
        can9.drawString(404,758,'x')
    elif datos[342] == 'Botadero':
        can9.drawString(404,746,'x')
    elif datos[342] == 'Incineración':
        can9.drawString(404,734,'x')
    elif datos[342] == 'Enterramiento':
        can9.drawString(404,722,'x')
    #elementos emplea
    if datos[343] == 'Bolsa plástica':
        can9.drawString(404,664,'x')
    elif datos[343] == 'En Caneca con tapa':
        can9.drawString(404,652,'x')
    elif datos[343] == 'Pozo comunitario':
        can9.drawString(404,640,'x')
    #dispocision aguas negras
    if datos[344] == 'Alcantarrillado':
        can9.drawString(404, 580, 'x')
    elif datos[344] == 'Pozo séptico':
        can9.drawString(404, 568, 'x')
    elif datos[344] == 'Campo abierto':
        can9.drawString(404, 556, 'x')
    elif datos[344] == 'Letrina':
        can9.drawString(404, 544, 'x')
    elif datos[344] == 'Río':
        can9.drawString(404, 532, 'x')
    elif datos[344] == 'Quebrada':
        can9.drawString(404, 520, 'x')
    elif datos[344] == 'Arroyo':
        can9.drawString(404, 508, 'x')
    elif datos[344] == 'Otro':
        can9.drawString(404, 496, 'x')
        can9.drawString(240, 496, datos[345])
    #dispocision de aguas residuales
    if datos[346] == 'Pozo séptico':
        can9.drawString(404,436, 'x')
    elif datos[346] == 'Campo abierto':
        can9.drawString(404,424, 'x')
    elif datos[346] == 'Letrina':
        can9.drawString(404,412, 'x')
    elif datos[346] == 'Río':
        can9.drawString(404,400, 'x')
    elif datos[346] == 'Quebrada':
        can9.drawString(404,388, 'x')
    elif datos[346] == 'Arroyo':
        can9.drawString(404,376, 'x')
    elif datos[346] == 'Otro':
        can9.drawString(404,364, 'x')
        can9.drawString(240,364, datos[346])
    familia = (json.loads(datos[13]))
    for i in range(len(familia)):
        integrante = dict(familia[i])
        if integrante['Parentesco'] == 'Jefe (a) de hogar':
            can9.drawString(130, 201, 'x')
            can9.drawString(231, 201, integrante['Genero'])
            can9.drawString(281, 201, str(integrante['Edad']))
            can9.drawString(331, 201, integrante['Registro'])
            can9.drawString(381, 201, integrante['Escolaridad'])
            can9.drawString(431, 201, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Pareja, Esposo(a), cónyuge, compañero(a)':
            can9.drawString(130, 181, 'x')
            can9.drawString(231, 181, integrante['Genero'])
            can9.drawString(281, 181, str(integrante['Edad']))
            can9.drawString(331, 181, integrante['Registro'])
            can9.drawString(381, 181, integrante['Escolaridad'])
            can9.drawString(431, 181, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a)':
            can9.drawString(130, 168, 'x')
            can9.drawString(231, 168, integrante['Genero'])
            can9.drawString(281, 168, str(integrante['Edad']))
            can9.drawString(331, 168, integrante['Registro'])
            can9.drawString(381, 168, integrante['Escolaridad'])
            can9.drawString(431, 168, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 2':
            can9.drawString(130, 155, 'x')
            can9.drawString(231, 155, integrante['Genero'])
            can9.drawString(281, 155, str(integrante['Edad']))
            can9.drawString(331, 155, integrante['Registro'])
            can9.drawString(381, 155, integrante['Escolaridad'])
            can9.drawString(431, 155, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 3':
            can9.drawString(130, 142, 'x')
            can9.drawString(231, 142, integrante['Genero'])
            can9.drawString(281, 142, str(integrante['Edad']))
            can9.drawString(331, 142, integrante['Registro'])
            can9.drawString(381, 142, integrante['Escolaridad'])
            can9.drawString(431, 142, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 4':
            can9.drawString(130, 129, 'x')
            can9.drawString(231, 129, integrante['Genero'])
            can9.drawString(281, 129, str(integrante['Edad']))
            can9.drawString(331, 129, integrante['Registro'])
            can9.drawString(381, 129, integrante['Escolaridad'])
            can9.drawString(431, 129, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Hijo(a), hijastro(a) 5':
            can9.drawString(130, 116, 'x')
            can9.drawString(231, 116, integrante['Genero'])
            can9.drawString(281, 116, str(integrante['Edad']))
            can9.drawString(331, 116, integrante['Registro'])
            can9.drawString(381, 116, integrante['Escolaridad'])
            can9.drawString(431, 116, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Nieto(a)':
            can9.drawString(130, 103, 'x')
            can9.drawString(231, 103, integrante['Genero'])
            can9.drawString(281, 103, str(integrante['Edad']))
            can9.drawString(331, 103, integrante['Registro'])
            can9.drawString(381, 103, integrante['Escolaridad'])
            can9.drawString(431, 103, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Suegro(a)':
            can9.drawString(130, 91, 'x')
            can9.drawString(231, 91, integrante['Genero'])
            can9.drawString(281, 91, str(integrante['Edad']))
            can9.drawString(331, 91, integrante['Registro'])
            can9.drawString(381, 91, integrante['Escolaridad'])
            can9.drawString(431, 91, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Tios(as)':
            can9.drawString(130, 78, 'x')
            can9.drawString(231, 78, integrante['Genero'])
            can9.drawString(281, 78, str(integrante['Edad']))
            can9.drawString(331, 78, integrante['Registro'])
            can9.drawString(381, 78, integrante['Escolaridad'])
            can9.drawString(431, 78, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Yerno, nuera':
            can9.drawString(130, 66, 'x')
            can9.drawString(231, 66, integrante['Genero'])
            can9.drawString(281, 66, str(integrante['Edad']))
            can9.drawString(331, 66, integrante['Registro'])
            can9.drawString(381, 66, integrante['Escolaridad'])
            can9.drawString(431, 66, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Otro (a) pariente del (de la) jefe (a)':
            can9.drawString(130, 48, 'x')
            can9.drawString(231, 48, integrante['Genero'])
            can9.drawString(281, 48, str(integrante['Edad']))
            can9.drawString(331, 48, integrante['Registro'])
            can9.drawString(381, 48, integrante['Escolaridad'])
            can9.drawString(431, 48, integrante['Ocupacion'])
        elif integrante['Parentesco'] == 'Otro (a) no pariente':
            can9.drawString(130, 36, 'x')
            can9.drawString(231, 36, integrante['Genero'])
            can9.drawString(281, 36, str(integrante['Edad']))
            can9.drawString(331, 36, integrante['Registro'])
            can9.drawString(381, 36, integrante['Escolaridad'])
            can9.drawString(431, 36, integrante['Ocupacion'])
    can9.save()
    #hoja 10 del pdf
    packet10 = io.BytesIO()
    # create a new PDF with Reportlab
    can10 = canvas.Canvas(packet10, pagesize=letter)
    can10.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can10, 398, 800, "01", 10)
    #mes
    llenarCampos(can10, 440, 800, "01", 10)
    #anio
    llenarCampos(can10, 488, 800, "2021", 10)

    
    can10.save()
    #hoja 11 del pdf
    packet11 = io.BytesIO()
    # create a new PDF with Reportlab
    can11 = canvas.Canvas(packet11, pagesize=letter)
    can11.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can11, 398, 800, "01", 10)
    #mes
    llenarCampos(can11, 440, 800, "01", 10)
    #anio
    llenarCampos(can11, 488, 800, "2021", 10)
    can11.save()
    #hoja 12 del pdf
    packet12 = io.BytesIO()
    # create a new PDF with Reportlab
    can12 = canvas.Canvas(packet12, pagesize=letter)
    can12.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can12, 398, 800, "01", 10)
    #mes
    llenarCampos(can12, 440, 800, "01", 10)
    #anio
    llenarCampos(can12, 488, 800, "2021", 10)
    can12.save()
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

    # read your existing PDF
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
    # finally, write "output" to a real file
    outputStream = open("pdfs/"+datos[3]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()





def generarPdfEjemplo():
    if os.path.exists("src/destination.pdf"):
        os.remove('src/destination.pdf')
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    #pagina 1
    #numero de formulario 
    can.drawString(380, 802, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can, 398, 790, "01", 10)
    #mes
    llenarCampos(can, 440, 790, "01", 10)
    #anio
    llenarCampos(can, 488, 790, "2021", 10)
    # coordenadas  latitud
    can.drawString(220, 396, "1")
    llenarCampos(can, 265, 396, "1234567892", 24)
    # coordenadas  longitud
    llenarCampos(can, 205, 359, "12", 30)
    #longitud
    llenarCampos(can, 265, 359, "1234567892", 24)
     # coordenadas  altitud
    llenarCampos(can, 205, 322, "12345", 30)
    #nombre departamento
    llenarCampos(can, 128, 255, "cundinamarca", 16)
    #codigo departamento
    llenarCampos(can, 128, 228, "21", 16)
    #nombre municipio
    llenarCampos(can, 128, 205, "guatupaque", 16)
    #codigo municipio
    llenarCampos(can, 128, 175, "0000", 16)    
    #nombre vereda
    llenarCampos(can, 128, 155, "Arricheriaaaa", 16)  
    #nombre corregimiento
    llenarCampos(can, 128, 127, "apaartadooooo", 16)
    can.save()
    #pagina2
    packet2 = io.BytesIO()
    # create a new PDF with Reportlab
    can2 = canvas.Canvas(packet2, pagesize=letter)
    can2.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can2, 398, 800, "01", 10)
    #mes
    llenarCampos(can2, 440, 800, "01", 10)
    #anio
    llenarCampos(can2, 488, 800, "2021", 10)
    #acepta la encuestas
    acepta= 'si'
    if acepta == 'si': 
        can2.drawString(315, 722, "X")
    else:
        can2.drawString(315, 710, "X")
    #uso de la vivienda
    uso= 'permanente'
    if uso == 'temporal': 
        can2.drawString(320, 633, "X")
    elif uso == 'permanente':
        can2.drawString(320, 620, "X")
    #cuenta con energia elcetrica
    cEnergia = 'no'
    if cEnergia == 'si': 
        can2.drawString(320, 368, "X")
    else:
        can2.drawString(370, 368, "X")

    #que fuente utiliza
    fuente = 'Otro'
    consumo = 'de 100 a 1000'
    costo = '100000'
    if fuente == 'Gas Propano': 
        can2.drawString(335, 290, consumo)
        can2.drawString(450, 290, costo)
    elif fuente == 'Gas Natural':
        can2.drawString(335, 276, consumo)
        can2.drawString(450, 276, costo)
    elif fuente == 'Gasolina':
        can2.drawString(335, 264, consumo)
        can2.drawString(450, 264, costo)
    elif fuente == 'Kerosene':
        can2.drawString(335, 250, consumo)
        can2.drawString(450, 250, costo)
    elif fuente == 'Petróleo':
        can2.drawString(335, 238, consumo)
        can2.drawString(450, 238, costo)
    elif fuente == 'Alcohol':
        can2.drawString(335, 226, consumo)
        can2.drawString(450, 226, costo)
    elif fuente == 'Carbón Mineral':
        can2.drawString(335, 214, consumo)
        can2.drawString(450, 214, costo)
    elif fuente == 'Leña Comprada':
        can2.drawString(335, 202, consumo)
        can2.drawString(450, 202, costo)
    elif fuente == 'Leña Auto Apropiada':
        can2.drawString(335, 190, consumo)
        can2.drawString(450, 190, costo)
    elif fuente == 'Residuos del Agro':
        can2.drawString(335, 178, consumo)
        can2.drawString(450, 178, costo)
    elif fuente == 'Otro':
        can2.drawString(150, 168, "ejemplo")
        can2.drawString(260, 168, "kg")
        can2.drawString(335, 164, consumo)
        can2.drawString(450, 164, costo)

    #cuantas horas utiliza para cocinar
    can2.drawString(350, 140, "10")
    can2.save()
    #hoja 3 del pdf
    packet3 = io.BytesIO()
    # create a new PDF with Reportlab
    can3 = canvas.Canvas(packet3, pagesize=letter)
    can3.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can3, 398, 800, "01", 10)
    #mes
    llenarCampos(can3, 440, 800, "01", 10)
    #anio
    llenarCampos(can3, 488, 800, "2021", 10)
    #fuente para iluminarse
    consumoMes= "1000"
    costoIl = "10000"
    localizacion = "Vereda"
    #pilas baterias
    can3.drawString(280, 740, consumoMes)
    can3.drawString(340, 740, costo)
    can3.drawString(420, 740, 'x')
    can3.drawString(462, 740, 'x')
    can3.drawString(505, 740, 'x')
    #gasolina
    can3.drawString(280, 728, consumoMes)
    can3.drawString(340, 728, costo)
    can3.drawString(420, 728, 'x')
    can3.drawString(462, 728, 'x')
    can3.drawString(505, 728, 'x')
    #Kerosene
    can3.drawString(280, 716, consumoMes)
    can3.drawString(340, 716, costo)
    can3.drawString(420, 716, 'x')
    can3.drawString(462, 716, 'x')
    can3.drawString(505, 716, 'x')
    #Petroleo
    can3.drawString(280, 702, consumoMes)
    can3.drawString(340, 702, costo)
    can3.drawString(420, 702, 'x')
    can3.drawString(462, 702, 'x')
    can3.drawString(505, 702, 'x')
    #Alcohol
    can3.drawString(280, 692, consumoMes)
    can3.drawString(340, 692, costo)
    can3.drawString(420, 692, 'x')
    can3.drawString(462, 692, 'x')
    can3.drawString(505, 692, 'x')
    #Diesel
    can3.drawString(280, 680, consumoMes)
    can3.drawString(340, 680, costo)
    can3.drawString(420, 680, 'x')
    can3.drawString(462, 680, 'x')
    can3.drawString(505, 680, 'x')
    #Velas
    can3.drawString(280, 668, consumoMes)
    can3.drawString(340, 668, costo)
    can3.drawString(420, 668, 'x')
    can3.drawString(462, 668, 'x')
    can3.drawString(505, 668, 'x')
    #Otro
    can3.drawString(120, 652, "consumoMes")
    can3.drawString(230, 652, "Galon")
    can3.drawString(280, 652, consumoMes)
    can3.drawString(340, 652, costo)
    can3.drawString(420, 652, 'x')
    can3.drawString(462, 652, 'x')
    can3.drawString(505, 652, 'x')
     #Horas al dia utiliza
    can3.drawString(410, 612, "consumoMes")
    #Queman residuos
    can3.drawString(320, 544, "x")
    can3.drawString(370, 544, "x")
    #Fuente quema residuos
    consumoQuemar = "10000"
    valorMesQuemar = "100000"
    #gas propano
    can3.drawString(340, 455, consumoQuemar)
    can3.drawString(442, 455, valorMesQuemar)
    #gas natural
    can3.drawString(340, 442, consumoQuemar)
    can3.drawString(442, 442, valorMesQuemar)
    #gasolina
    can3.drawString(340, 430, consumoQuemar)
    can3.drawString(442, 430, valorMesQuemar)
    #Kerosene
    can3.drawString(340, 417, consumoQuemar)
    can3.drawString(442, 417, valorMesQuemar)
    #Petroleo
    can3.drawString(340, 404, consumoQuemar)
    can3.drawString(442, 404, valorMesQuemar)
    #Alcohol
    can3.drawString(340, 455, consumoQuemar)
    can3.drawString(442, 455, valorMesQuemar)
    #Carbon mineral
    can3.drawString(340, 391, consumoQuemar)
    can3.drawString(442, 391, valorMesQuemar)
    #Leña comprada
    can3.drawString(340, 378, consumoQuemar)
    can3.drawString(442, 378, valorMesQuemar)
    #Leña autoapropiada
    can3.drawString(340, 367, consumoQuemar)
    can3.drawString(442, 367, valorMesQuemar)
    #gas propano
    can3.drawString(340, 354, consumoQuemar)
    can3.drawString(442, 354, valorMesQuemar)
    #residuos del agro
    can3.drawString(340, 343, consumoQuemar)
    can3.drawString(442, 343, valorMesQuemar)
    #Otro
    can3.drawString(150, 333, "Otrooooo")
    can3.drawString(260, 333, "uni")
    can3.drawString(340, 330, consumoQuemar)
    can3.drawString(442, 330, valorMesQuemar)
    #cuantas horas al dia utiliza para ilumminar 
    can3.drawString(350, 305, "1 horita")
    #contaminacion 
    #exceso de ruido
    can3.drawString(385, 210, "x")
    can3.drawString(430, 210, "x")
    #malos oloress
    can3.drawString(385, 195, "x")
    can3.drawString(430, 195, "x")
    # uso del predio
    #residencial
    can3.drawString(415, 92, "x")
    #negocio
    can3.drawString(415, 80, "x")
    #mixto
    can3.drawString(415, 68, "x")
    #institucional
    can3.drawString(415, 56, "x")
    can3.save()
    #hoja 4 del pdf
    packet4 = io.BytesIO()
    # create a new PDF with Reportlab
    can4 = canvas.Canvas(packet4, pagesize=letter)
    can4.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can4, 398, 800, "01", 10)
    #mes
    llenarCampos(can4, 440, 800, "01", 10)
    #anio
    llenarCampos(can4, 488, 800, "2021", 10)
    #estrato del predio
    #1
    can4.drawString(255, 748, "x")
    #2
    can4.drawString(280, 748, "x")
    #3
    can4.drawString(305, 748, "x")
    #4
    can4.drawString(330, 748, "x")
    #5
    can4.drawString(350, 748, "x")
    #6
    can4.drawString(375, 748, "x")
    #Nombre de la comunidad
    can4.drawString(90, 670, "guatapuriiia")
    #personas en la comunidad 
    llenarCampos(can4, 315, 598, "155", 30)
    #la vivienda se encuentra ubicada al interior de 
    #caserio
    can4.drawString(405, 536, "x")
    #resguardo indigena
    can4.drawString(405, 523, "x")
    #parcialidad
    can4.drawString(405, 510, "x")
    #territorio colectivo
    can4.drawString(405, 497, "x")
    #territorio de comunidad
    can4.drawString(405, 484, "x")
    #territorio ancestral
    can4.drawString(405, 471, "x")
    #reancheria
    can4.drawString(405, 458, "x")
    #territorio palenquero
    can4.drawString(405, 445, "x")
    #territorio gitano
    can4.drawString(405, 432, "x")
    #zona rural
    can4.drawString(405, 419, "x")
    #tenencia de la vivenda
    can4.drawString(350, 351, "x")
    #tenencia de la vivenda
    can4.drawString(350, 339, "x")
    #tenencia de la vivenda
    can4.drawString(350, 327, "x")
    # hogares en la vivienda
    llenarCampos(can4, 342, 267 , "15", 30)
    #personas en la vivienda
    llenarCampos(can4, 342, 222 , "15", 30)
    #material predominante en la vivienda
    #bloque
    can4.drawString(420, 152, "x")
    #concreto
    can4.drawString(420, 140, "x")
    #tapia
    can4.drawString(420, 128, "x")
    #madera
    can4.drawString(420, 116, "x")
    #prefabricado
    can4.drawString(420, 104, "x")
    #guadua
    can4.drawString(420, 92, "x")
    #desechos
    can4.drawString(420, 80, "x")
    #no tiene
    can4.drawString(420, 68, "x")
    can4.save()
    #hoja 5 del pdf
    packet5 = io.BytesIO()
    # create a new PDF with Reportlab
    can5 = canvas.Canvas(packet5, pagesize=letter)
    can5.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can5, 398, 800, "01", 10)
    #mes
    llenarCampos(can5, 440, 800, "01", 10)
    #anio
    llenarCampos(can5, 488, 800, "2021", 10)
    #material predominante techo
    can5.drawString(420, 742, "x")
    can5.drawString(420, 730, "x")
    can5.drawString(420, 718, "x")
    can5.drawString(420, 706, "x")
    #material predominante en piso
    can5.drawString(410, 640, "x")
    can5.drawString(410, 628, "x")
    can5.drawString(410, 616, "x")
    can5.drawString(410, 604, "x")
    can5.drawString(410, 592, "x")
    can5.drawString(410, 580, "x")
    #vivienda ha sido afectada
    can5.drawString(385, 523, "x")
    can5.drawString(432, 523, "x")
    can5.drawString(385, 511, "x")
    can5.drawString(432, 511, "x")
    can5.drawString(385, 499, "x")
    can5.drawString(432, 499, "x")
    can5.drawString(385, 487, "x")
    can5.drawString(432, 487, "x")
    can5.drawString(385, 475, "x")
    can5.drawString(432, 475, "x")
    #area de construccion
    llenarCampos(can5, 300, 417, "333",30)
    #la vivienda cuenta con servicios
    can5.drawString(400, 304, "x")
    can5.drawString(400, 292, "x")
    can5.drawString(400, 280, "x")
    can5.drawString(400, 268, "x")
    can5.drawString(400, 256, "x")
    can5.drawString(400, 244, "x")
    #obtencion de agua
    can5.drawString(295, 167, "x")
    can5.drawString(295, 153, "x")
    can5.drawString(295, 141, "x")
    can5.drawString(295, 129, "x")
    can5.drawString(295, 117, "x")
    can5.drawString(295, 105, "x")
    can5.drawString(295, 93, "x")
    can5.drawString(295, 81, "x")
    #tiene medidor de agua
    can5.drawString(465, 167, "x")
    can5.drawString(500, 167, "x")
    can5.save()
    #hoja 6 del pdf
    packet6 = io.BytesIO()
    # create a new PDF with Reportlab
    can6 = canvas.Canvas(packet6, pagesize=letter)
    can6.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can6, 398, 800, "01", 10)
    #mes
    llenarCampos(can6, 440, 800, "01", 10)
    #anio
    llenarCampos(can6, 488, 800, "2021", 10)
    #Servicio sanitario
    can6.drawString(400, 743, "x")
    can6.drawString(400, 731, "x")
    can6.drawString(400, 719, "x")
    can6.drawString(400, 707, "x")
    can6.drawString(400, 695, "x")
    can6.drawString(230, 685, "aguita de")
    can6.drawString(400, 683, "x")
    #tiene acceso a gas
    can6.drawString(400, 614, "x")
    can6.drawString(400, 602, "x")
    can6.drawString(400, 590, "x")
    #tiene acceso al agua
    can6.drawString(320, 480, "x")
    can6.drawString(320, 467, "x")
    #que cantidad de agua puede obtener
    can6.drawString(100, 430, "ubate")
    #promedio cantidad de agua
    can6.drawString(400, 395, "ubate")
    #fuente principal de abastesimiento de agua
    can6.drawString(400, 313, "x")
    can6.drawString(400, 301, "x")
    can6.drawString(400, 289, "x")
    can6.drawString(400, 277, "x")
    can6.drawString(400, 265, "x")
    can6.drawString(400, 253, "x")
    can6.drawString(400, 241, "x")
    can6.drawString(400, 228, "x")
    can6.drawString(400, 216, "x")
    #la casimba es comunitaria
    can6.drawString(320, 147, "x")
    can6.drawString(320, 135, "x")
    #cual
    can6.drawString(120, 110, "ejemplo")
    can6.save()
    #hoja 7 del pdf
    packet7 = io.BytesIO()
    # create a new PDF with Reportlab
    can7 = canvas.Canvas(packet7, pagesize=letter)
    can7.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can7, 398, 800, "01", 10)
    #mes
    llenarCampos(can7, 440, 800, "01", 10)
    #anio
    llenarCampos(can7, 488, 800, "2021", 10)
     #uso del agua que obtienen
    can7.drawString(405, 744, "x")
    can7.drawString(405, 732, "x")
    can7.drawString(405, 720, "x")
    can7.drawString(405, 708, "x")
    can7.drawString(405, 696, "x")
    # va al puesto de agua todos los dias
    can7.drawString(320, 626, "x")
    can7.drawString(320, 614, "x")
    can7.drawString(320, 602, "x")
    #cuanto dura el agua que recolecta
    can7.drawString(300, 573, "3dias ")
    #cantidad destinada higiene
    can7.drawString(100, 528, "40 litros")
    #distancia para obtener agua
    can7.drawString(300, 495, "40 kilomtros")
    #ti3mpo destina a la recoleccion de agua
    can7.drawString(100, 450, "10 horas")
    #medio de transporte para el agua
    can7.drawString(405, 377, "x")
    can7.drawString(405, 365, "x")
    can7.drawString(405, 353, "x")
    can7.drawString(405, 341, "x")
    can7.drawString(405, 329, "x")
    can7.drawString(250, 329, "otra")
    #adquiere agua de otra fuente
    can7.drawString(320, 260, "x")
    can7.drawString(320, 248, "x")
    #cuanta agua adquiere de esa fuente
    can7.drawString(360, 220, "20 litros")
    #cual es la otra fuente
    can7.drawString(405, 145, "x")
    can7.drawString(405, 134, "x")
    can7.drawString(405, 122, "x")
    can7.drawString(405, 111, "x")
    can7.save()
    #hoja 8 del pdf
    packet8 = io.BytesIO()
    # create a new PDF with Reportlab
    can8 = canvas.Canvas(packet8, pagesize=letter)
    can8.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can8, 398, 800, "01", 10)
    #mes
    llenarCampos(can8, 440, 800, "01", 10)
    #anio
    llenarCampos(can8, 488, 800, "2021", 10)
   
    can8.save()
    #hoja 9 del pdf
    packet9 = io.BytesIO()
    # create a new PDF with Reportlab
    can9 = canvas.Canvas(packet9, pagesize=letter)
    can9.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can9, 398, 800, "01", 10)
    #mes
    llenarCampos(can9, 440, 800, "01", 10)
    #anio
    llenarCampos(can9, 488, 800, "2021", 10)
    can9.save()
    #hoja 10 del pdf
    packet10 = io.BytesIO()
    # create a new PDF with Reportlab
    can10 = canvas.Canvas(packet10, pagesize=letter)
    can10.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can10, 398, 800, "01", 10)
    #mes
    llenarCampos(can10, 440, 800, "01", 10)
    #anio
    llenarCampos(can10, 488, 800, "2021", 10)
    can10.save()
    #hoja 11 del pdf
    packet11 = io.BytesIO()
    # create a new PDF with Reportlab
    can11 = canvas.Canvas(packet11, pagesize=letter)
    can11.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can11, 398, 800, "01", 10)
    #mes
    llenarCampos(can11, 440, 800, "01", 10)
    #anio
    llenarCampos(can11, 488, 800, "2021", 10)
    can11.save()
    #hoja 12 del pdf
    packet12 = io.BytesIO()
    # create a new PDF with Reportlab
    can12 = canvas.Canvas(packet12, pagesize=letter)
    can12.drawString(380, 815, "100000000000")
    #fecha de formulario
    #dia
    llenarCampos(can12, 398, 800, "01", 10)
    #mes
    llenarCampos(can12, 440, 800, "01", 10)
    #anio
    llenarCampos(can12, 488, 800, "2021", 10)
    can12.save()
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

    
    # read your existing PDF
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
    # finally, write "output" to a real file
    outputStream = open("src/destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return "destination.pdf"




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
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, "Hello worldasasas")
    can.line(120,700,590,747)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-02.pdf", "rb"))
    existing_pdf2 = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-03.pdf", "rb"))
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