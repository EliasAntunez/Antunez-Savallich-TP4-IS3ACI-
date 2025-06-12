# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Crea y establece el directorio de trabajo
WORKDIR /app

# Copia archivo de dependencias
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la app
COPY . .

# Expone el puerto 5000
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "app/app.py"]
