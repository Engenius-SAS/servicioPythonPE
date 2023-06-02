from PIL import Image, ImageFont, ImageDraw
import  urllib
from io import StringIO, BytesIO
import pymysql 
import os
import urllib.request
import zipfile
from pathlib import Path
import shutil, logging

try:
    import zlib
    compression = zipfile.ZIP_DEFLATED
except:
    compression = zipfile.ZIP_STORED
def LoggingStart():
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

def obtener_conexion():
    return pymysql.connect(host='mysql.engenius.com.co',
                                user='infovisitas',
                                password='desarrollo2020'
                                )

def generarRarFotos (ids):
    if os.path.exists("imagenes"):
        imagenesExistentes = os.listdir("imagenes")
        for imagen in imagenesExistentes:
            dirPath = Path('imagenes/'+imagen)
            shutil.rmtree(dirPath)
    if os.path.exists("imagenes.zip"):
        os.remove("imagenes.zip")
    ids = ids.split(",")
    idEnviar = ''
    for id in ids:
        if id == ids[-1]:
            print(ids.pop())
            idEnviar = idEnviar + "'"+id+"'"
        else:
            idEnviar = idEnviar + "'"+id+"', "
    generarFotosCoordenadas(idEnviar)
    zf = zipfile.ZipFile("imagenes.zip", mode="w")
    carpetasExistentes = os.listdir("imagenes")
    # pdfsExistentes = ([arch.name for arch in os.scandir("pdfs") if arch.is_file()])
    try:
        for carpeta in carpetasExistentes:
            imagenesExistentes = ([arch.name for arch in os.scandir("imagenes/"+ carpeta) if arch.is_file()])
            for imagen in imagenesExistentes:
                zf.write("imagenes/"+ carpeta+ "/" +imagen, compress_type=compression)
    finally:
        zf.close()


def generarFotosCoordenadas(ids):                                        
    bd = obtener_conexion()
    try:
        conn = bd.cursor(pymysql.cursors.DictCursor)
        conn.execute("SELECT D.*, E.`U_latitud`,E.`U_longitud` FROM db_ipse_7_0.Fotos_encuesta D INNER JOIN `db_ipse_7_0`.`Ubicacion` E ON D.`Id_Encuesta` = E.`Id_Encuesta` WHERE D.IsDelete = 0  AND  D.`rutaserver` != 'NO ENCONTRADO ARCHIVO LOCAL' AND D.Id_Encuesta IN ("+ids+");")
        fotos=conn.fetchall()
        if len(fotos) > 0:
            for foto in fotos:
                print( "latitud: " + foto['U_latitud'] +" , Longitud: " + foto['U_longitud'])
                if os.path.exists("imagenes/"+foto['Id_Encuesta']):
                    with urllib.request.urlopen('https://www.php.engenius.com.co'+foto['rutaserver']) as url:
                        data = url.read()
                    file = BytesIO(data)
                    im = Image.open(file)
                    my_image = im.convert('RGB')
                    my_image = my_image.resize((3500,2400))
                    title_font = ImageFont.truetype('src/fotos/Roboto-Black.ttf', 100)
                    title_text = "latitud: " + foto['U_latitud'] +" , Longitud: " + foto['U_longitud']
                    image_editable = ImageDraw.Draw(my_image)
                    image_editable.text((200,2100), title_text, (237, 230, 500), font=title_font)
                    my_image.save("imagenes/"+foto['Id_Encuesta']+"/"+foto['Id_Foto_Encuesta']+".jpg")
                else:
                    print("else:", foto['Id_Encuesta'])
                    os.mkdir("imagenes/"+foto['Id_Encuesta'])
                    with urllib.request.urlopen('https://www.php.engenius.com.co'+foto['rutaserver']) as url:
                        data = url.read()
                    file = BytesIO(data)
                    im = Image.open(file)
                    my_image = im.convert('RGB')
                    my_image = my_image.resize((3500,2400))
                    title_font = ImageFont.truetype('src/fotos/Roboto-Black.ttf', 100)
                    title_text = "latitud: " + foto['U_latitud'] +" , Longitud: " + foto['U_longitud']
                    image_editable = ImageDraw.Draw(my_image)
                    image_editable.text((200,2100), title_text, (237, 230, 500), font=title_font)
                    my_image.save("imagenes/"+foto['Id_Encuesta']+"/"+foto['Id_Foto_Encuesta']+".jpg")
            else:
                print("No trae fotos", foto['Id_Encuesta'])
        else:
            print("len->0",fotos)
    except Exception as e:
                logging.debug(e)
    
if __name__ == "__main__":
    LoggingStart()
    generarRarFotos()