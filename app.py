"""
Aplicación Flask CON OpenTelemetry
Esta versión genera traces automáticos y manuales que puedes ver en Jaeger
"""

from flask import Flask, jsonify
import time
import random

# ========== IMPORTS DE OPENTELEMETRY ==========
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# ========== CONFIGURACIÓN DE OPENTELEMETRY ==========

# 1. Crear un Resource (identifica tu servicio)
resource = Resource(attributes={
    "service.name": "flask-tutorial-otel",  # Nombre de tu servicio
    "service.version": "1.0.0",
    "deployment.environment": "tutorial"
})

# 2. Configurar el proveedor de traces
trace.set_tracer_provider(TracerProvider(resource=resource))

# 3. Configurar el exportador OTLP (envía traces a Jaeger)
otlp_exporter = OTLPSpanExporter(
    endpoint="http://localhost:4318/v1/traces",  # Endpoint de Jaeger
)

# 4. Añadir el procesador de spans
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# 5. Obtener un tracer para instrumentación manual
tracer = trace.get_tracer(__name__)

# ========== APLICACIÓN FLASK ==========

app = Flask(__name__)

# 6. Instrumentar Flask automáticamente
# Esto hace que TODOS los endpoints generen traces automáticamente
FlaskInstrumentor().instrument_app(app)


@app.route('/')
def home():
    """Endpoint simple - genera trace automático"""
    return jsonify({
        "mensaje": "¡Hola! Esta es la versión CON OpenTelemetry",
        "endpoints_disponibles": [
            "/",
            "/lento",
            "/rapido",
            "/cadena",
            "/manual",
            "/error"
        ],
        "jaeger_ui": "http://localhost:16686"
    })


@app.route('/lento')
def endpoint_lento():
    """
    Endpoint que tarda tiempo
    El trace mostrará cuánto tarda en Jaeger
    """
    tiempo_espera = random.uniform(2, 3)
    time.sleep(tiempo_espera)
    
    return jsonify({
        "mensaje": "Operación lenta completada",
        "tiempo_segundos": round(tiempo_espera, 2),
        "tip": "Mira en Jaeger el tiempo que tardó este endpoint"
    })


@app.route('/rapido')
def endpoint_rapido():
    """Endpoint rápido para comparar tiempos en Jaeger"""
    return jsonify({
        "mensaje": "Operación rápida",
        "tip": "Compara el tiempo de este trace vs /lento en Jaeger"
    })


@app.route('/cadena')
def endpoint_cadena():
    """
    Endpoint con múltiples pasos
    Cada sleep generará un span en el trace
    """
    # Paso 1: validación
    time.sleep(0.5)
    
    # Paso 2: procesamiento
    time.sleep(0.7)
    
    # Paso 3: respuesta
    time.sleep(0.3)
    
    return jsonify({
        "mensaje": "Cadena de operaciones completada",
        "pasos": ["validación", "procesamiento", "respuesta"],
        "tip": "Mira en Jaeger cómo se visualiza la secuencia de operaciones"
    })


@app.route('/manual')
def endpoint_manual():
    """
    Ejemplo de INSTRUMENTACIÓN MANUAL
    Aquí TÚ decides qué partes del código quieres trackear como spans
    """
    
    # Crear un span manual para "validar_datos"
    with tracer.start_as_current_span("validar_datos") as span:
        # Añadir atributos personalizados al span
        span.set_attribute("usuario.id", "12345")
        span.set_attribute("tipo.validacion", "avanzada")
        time.sleep(0.5)
    
    # Crear otro span manual para "calcular_precio"
    with tracer.start_as_current_span("calcular_precio") as span:
        precio_base = 100
        iva = 1.21
        precio_final = precio_base * iva
        
        # Añadir el resultado como atributo
        span.set_attribute("precio.base", precio_base)
        span.set_attribute("precio.final", precio_final)
        time.sleep(0.3)
    
    # Crear un tercer span para "guardar_resultado"
    with tracer.start_as_current_span("guardar_resultado") as span:
        span.set_attribute("bd.tabla", "pedidos")
        span.set_attribute("bd.operacion", "INSERT")
        time.sleep(0.4)
    
    return jsonify({
        "mensaje": "Operación con spans manuales completada",
        "precio_final": precio_final,
        "tip": "En Jaeger verás los 3 spans personalizados: validar_datos, calcular_precio, guardar_resultado"
    })


@app.route('/error')
def endpoint_error():
    """
    Endpoint que genera un error
    El trace en Jaeger mostrará el error con detalles
    """
    # Simulamos algo de procesamiento antes del error
    time.sleep(0.5)
    
    # El error será capturado automáticamente en el trace
    raise ValueError("¡Error simulado! Mira en Jaeger cómo se visualiza con toda la información del stack trace")


if __name__ == '__main__':
    print("=" * 60)
    print("Aplicación Flask CON OpenTelemetry")
    print("Los traces se envían a Jaeger automáticamente")
    print("=" * 60)
    print("\nEndpoints disponibles:")
    print("  http://localhost:5000/          - Inicio")
    print("  http://localhost:5000/lento     - Operación lenta")
    print("  http://localhost:5000/rapido    - Operación rápida")
    print("  http://localhost:5000/cadena    - Cadena de operaciones")
    print("  http://localhost:5000/manual    - Spans manuales personalizados")
    print("  http://localhost:5000/error     - Simula un error")
    print("\nJaeger UI:")
    print("  http://localhost:16686")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
