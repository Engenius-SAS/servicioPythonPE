import PyPDF2 
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import zipfile
import pymysql 

def obtener_conexion():
    return pymysql.connect(host='mysql.engenius.com.co',
                                user='infovisitas',
                                password='desarrollo2020'
                                )


def generarPdfEjemplo():
    if os.path.exists("src/destination.pdf"):
        os.remove('src/destination.pdf')
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(10, 100, "Hello worldasasasassa")
    #can.line(120,700,590,747)
    can.save()
    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PyPDF2.PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PyPDF2.PdfFileReader(open("src/pdf/encuestas/AES-01.pdf", "rb"))
    output = PyPDF2.PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open("src/destination.pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return "destination.pdf"
