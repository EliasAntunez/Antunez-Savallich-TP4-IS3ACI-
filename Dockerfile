# Usamos una imagen base de Python
FROM python:3.13-alpine

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de dependencias
COPY requirements.txt .

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto de los archivos
COPY app/ .

# Exponemos el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]