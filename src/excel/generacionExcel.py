import datetime
import pymysql 
from openpyxl import Workbook
from drive.drive import *


def obtener_conexion():
    return pymysql.connect(host='mysql.engenius.com.co',
                                user='infovisitas',
                                password='desarrollo2020'
                                )

def generarExcel(query, folderId=None):
    bd = obtener_conexion()
    encabezados = []
    conn = bd.cursor(pymysql.cursors.DictCursor)
    conn.execute(query)
    date = datetime.date.today()
    datosEncabezado=conn.fetchone()
    for key in datosEncabezado.keys():
        encabezados.append(key)
    wb = Workbook()
    ws = wb.active
    ws.title = "Excel datos"
    ws.append(encabezados)
    with bd.cursor() as cursor:
              cursor.execute(query)
              datos = cursor.fetchall()
    for row in datos:
        ws.append(row)
    ws.auto_filter.ref = ws.dimensions

    nombre_mes = date.strftime("%b")
    dia = date.strftime("%d")
    ano = date.strftime("%Y")
    concat = f"{nombre_mes} - {dia} - {ano}"

    file_path = os.path.abspath("Excels/" + ws.title + "  " + concat +".xlsx")
    wb.save(file_path)

    sendFiles(file_path=file_path, folder_id=folderId)


def generarExcelAlertas(idP):
    queryAlertas = "SELECT A.Id_Encuesta,CONCAT(E.Dia, '-', E.Mes,'-',E.Año) AS `Fecha Encuesta`, CONCAT(C.nombre, ' ', C.apellido) AS `Nombre Encuestador`, F.Nombre_encuestado, J.U_municipio, J.U_vereda, A.Descripcion, A.Fecha, F.Telefono_celular_encuestado  FROM aes2021.alertas A INNER JOIN aes2021.Encabezado E ON A.Id_Encuesta = E.Id_Encuesta INNER JOIN aes2021.Consentimiento F ON A.Id_Encuesta = F.Id_Encuesta INNER JOIN aes2021.Ubicacion J ON A.Id_Encuesta = J.Id_Encuesta INNER JOIN aes2021.Proyectos_funcionarios B ON E.Id_Proyecto_Funcionario = B.Id_Proyecto_Funcionario INNER JOIN aes2021.Funcionarios C ON B.Id_Funcionario = C.Id_Funcionario INNER JOIN aes2021.Porcentaje L ON A.Id_Encuesta = L.Id_Encuesta WHERE A.IsDelete = 0 AND E.IsDelete = 0 AND L.IsAlert=1 AND B.Id_Proyecto ="+str(idP)+" GROUP BY A.Id_Encuesta;"
    return generarExcel(queryAlertas)

def generarExcelGrande(idP):
    queryAlertas = "SELECT * from aes2021.Consentimiento;"
    return generarExcel(queryAlertas)


if __name__ == '__main__':
    generarExcelAlertas()
