# 🔭 Tutorial OpenTelemetry con Python y Flask

Tutorial práctico para aprender observabilidad con OpenTelemetry, instrumentando una aplicación Flask y visualizando traces en Jaeger.

## 📖 Artículo completo

Lee el tutorial paso a paso en: **[observasistemas.com]([https://observasistemas.com](https://observasistemas.com/mini-tutorial-opentelemetry-con-python-y-flask/)** 

## 🎯 ¿Qué aprenderás?

- Qué es OpenTelemetry y por qué es importante
- Diferencia entre instrumentación automática y manual
- Configurar una aplicación Flask con OpenTelemetry
- Levantar Jaeger con Docker para visualizar traces
- Crear spans personalizados con atributos de negocio
- Analizar errores y cuellos de botella

## 🛠️ Requisitos previos

- **VirtualBox** con Ubuntu Server (o cualquier Linux)
- **Docker** y **Docker Compose**
- **Python 3.9+**
- Conocimientos básicos de Python y terminal

## 🚀 Inicio rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/opentelemetry-flask-tutorial.git
cd opentelemetry-flask-tutorial
```

### 2. Crear entorno virtual de Python

```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Levantar Jaeger

```bash
docker-compose up -d
```

Verifica que Jaeger está corriendo: http://localhost:16686

### 5. Ejecutar la aplicación

```bash
python app.py
```

### 6. Generar traces

Desde otra terminal:

```bash
curl http://localhost:5000/
curl http://localhost:5000/lento
curl http://localhost:5000/rapido
curl http://localhost:5000/cadena
curl http://localhost:5000/manual
curl http://localhost:5000/error
```

### 7. Ver los traces en Jaeger

Abre tu navegador en: http://localhost:16686

1. En el dropdown "Service" selecciona: **flask-tutorial-otel**
2. Click en "Find Traces"
3. Explora los traces generados

## 📁 Estructura del proyecto

```
.
├── README.md                    # Este archivo
├── docker-compose.yml           # Configuración de Jaeger
├── requirements.txt             # Dependencias Python
├── app.py                       # Aplicación Flask CON OpenTelemetry
├── app_sin_instrumentar.py      # Aplicación sin instrumentar (para comparar)
└── .gitignore                   # Archivos ignorados por Git
```

## 🔍 Endpoints disponibles

| Endpoint | Descripción |
|----------|-------------|
| `/` | Endpoint principal con información |
| `/lento` | Simula operación lenta (2-3 segundos) |
| `/rapido` | Operación rápida para comparar tiempos |
| `/cadena` | Múltiples operaciones en secuencia |
| `/manual` | Ejemplo de instrumentación manual con spans personalizados |
| `/error` | Simula un error para visualizar en Jaeger |

## 🧪 Probar sin OpenTelemetry

Si quieres ver la diferencia, puedes ejecutar la versión sin instrumentar:

```bash
python app_sin_instrumentar.py
```

Esta versión NO genera traces. Útil para comparar y entender qué aporta OpenTelemetry.

## 📊 ¿Qué verás en Jaeger?

- **Duración total** de cada petición
- **Spans anidados** mostrando la jerarquía de operaciones
- **Tags automáticos**: método HTTP, ruta, código de respuesta
- **Atributos personalizados**: los que añadas manualmente
- **Errores**: stack traces completos cuando algo falla

## 🎓 Conceptos clave

### Instrumentación Automática
OpenTelemetry detecta automáticamente frameworks como Flask y genera traces sin modificar tu código. Solo necesitas:

```python
FlaskInstrumentor().instrument_app(app)
```

### Instrumentación Manual
Para trackear lógica de negocio específica:

```python
with tracer.start_as_current_span("nombre_operacion") as span:
    span.set_attribute("clave", "valor")
    # Tu código aquí
```

## 🔧 Configuración de port forwarding (VirtualBox)

Si usas VirtualBox con Ubuntu Server, configura estos puertos:

| Nombre | Puerto Host | Puerto Guest |
|--------|-------------|--------------|
| SSH | 2222 | 22 |
| Flask | 5000 | 5000 |
| Jaeger UI | 16686 | 16686 |

## 🐛 Troubleshooting

### Jaeger no arranca
```bash
docker-compose logs jaeger
```

### La app no se conecta a Jaeger
Verifica que el endpoint en `app.py` es correcto:
```python
endpoint="http://localhost:4318/v1/traces"
```

### No veo traces en Jaeger
1. Verifica que la app está corriendo
2. Haz peticiones a los endpoints
3. Refresca la página de Jaeger
4. Asegúrate de seleccionar el servicio correcto

## 📚 Recursos adicionales

- [Documentación oficial de OpenTelemetry](https://opentelemetry.io/docs/)
- [OpenTelemetry Python](https://opentelemetry.io/docs/languages/python/)
- [Jaeger Documentation](https://www.jaegertracing.io/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras algún error o quieres mejorar el tutorial:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añadir mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## ✉️ Contacto

**Observa Sistemas** - [observasistemas.com](https://observasistemas.com)

---

⭐ Si este tutorial te resultó útil, ¡dale una estrella al repositorio!
