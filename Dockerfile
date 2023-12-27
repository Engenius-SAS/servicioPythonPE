FROM python:3

WORKDIR /src/app

# Copia el archivo requirements.txt
COPY requirements.txt ./

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos del proyecto
COPY . .

# Comando para ejecutar la aplicación
CMD ["python3", "src/app.py"]