"""
Aplicación Flask SIN OpenTelemetry
Esta versión NO genera traces - es para comparar con la versión instrumentada
"""

from flask import Flask, jsonify
import time
import random

app = Flask(__name__)


@app.route('/')
def home():
    """Endpoint simple que devuelve un saludo"""
    return jsonify({
        "mensaje": "¡Hola! Esta es la versión SIN instrumentar",
        "endpoints_disponibles": [
            "/",
            "/lento",
            "/cadena",
            "/error"
        ]
    })


@app.route('/lento')
def endpoint_lento():
    """Simula una operación que tarda tiempo"""
    # Simulamos procesamiento lento (2-3 segundos)
    tiempo_espera = random.uniform(2, 3)
    time.sleep(tiempo_espera)
    
    return jsonify({
        "mensaje": "Operación lenta completada",
        "tiempo_segundos": round(tiempo_espera, 2)
    })


@app.route('/rapido')
def endpoint_rapido():
    """Endpoint rápido para comparar"""
    return jsonify({
        "mensaje": "Operación rápida"
    })


@app.route('/cadena')
def endpoint_cadena():
    """Simula una cadena de llamadas internas"""
    # Paso 1: validación
    time.sleep(0.5)
    
    # Paso 2: procesamiento
    time.sleep(0.7)
    
    # Paso 3: respuesta
    time.sleep(0.3)
    
    return jsonify({
        "mensaje": "Cadena de operaciones completada",
        "pasos": ["validación", "procesamiento", "respuesta"]
    })


@app.route('/error')
def endpoint_error():
    """Simula un error para ver cómo se registra"""
    # Simulamos algo de procesamiento antes del error
    time.sleep(0.5)
    
    # Generamos un error intencionado
    raise ValueError("¡Error simulado! Esto es para ver cómo se visualiza en el tracing")


if __name__ == '__main__':
    print("=" * 60)
    print("Aplicación Flask SIN OpenTelemetry")
    print("Esta versión NO genera traces")
    print("=" * 60)
    print("\nEndpoints disponibles:")
    print("  http://localhost:5000/")
    print("  http://localhost:5000/lento")
    print("  http://localhost:5000/rapido")
    print("  http://localhost:5000/cadena")
    print("  http://localhost:5000/error")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
