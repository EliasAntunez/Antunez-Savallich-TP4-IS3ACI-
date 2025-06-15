from flask import Flask, jsonify, request
import psycopg2
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración desde variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
PORT = int(os.getenv("FLASK_PORT", 8000))

# Función para obtener conexión a la base de datos
def obtener_conexion():
    return psycopg2.connect(DATABASE_URL)

# Ruta para inicializar la base de datos
@app.route("/inicializar-bd", methods=['GET'])
def inicializar_bd():
    try:
        # Obtenemos conexión y cursor
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Creamos la tabla de eventos si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                fecha DATE NOT NULL,
                lugar VARCHAR(100)
            )
        """)
        conexion.commit()
        
        return "Base de datos inicializada correctamente", 200
        
    except Exception as e:
        return f"Error: {str(e)}", 500
    finally:
        if 'conexion' in locals():
            conexion.close()

# Ruta para crear un nuevo evento
@app.route("/eventos", methods=['POST'])
def crear_evento():
    try:
        # Obtenemos los datos del cuerpo de la petición
        datos = request.get_json()
        nombre = datos['nombre']
        fecha = datos['fecha']
        lugar = datos.get('lugar', '')  # Campo opcional
        
        # Insertamos el evento en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute(
            "INSERT INTO eventos (nombre, fecha, lugar) VALUES (%s, %s, %s) RETURNING id",
            (nombre, fecha, lugar))
        id_evento = cursor.fetchone()[0]
        conexion.commit()
        
        return jsonify({
            "mensaje": "Evento creado exitosamente",
            "id": id_evento
        }), 201
       
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        if 'conexion' in locals():
            conexion.close()

# Ruta para listar todos los eventos
@app.route("/eventos", methods=['GET'])
def listar_eventos():
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        
        # Obtenemos todos los eventos
        cursor.execute("SELECT id, nombre, fecha, lugar FROM eventos")
        eventos = cursor.fetchall()
        
        # Formateamos la respuesta
        resultado = []
        for evento in eventos:
            resultado.append({
                "id": evento[0],
                "nombre": evento[1],
                "fecha": evento[2].isoformat(),
                "lugar": evento[3]
            })
            
        return jsonify(resultado), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if 'conexion' in locals():
            conexion.close()

# Iniciamos la aplicación
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)