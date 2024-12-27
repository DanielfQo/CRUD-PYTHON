## CRUD con Python 🐍 MySQL 💾 y un Dashboard Asombroso 🚀

## NOMBRE EQUIPO

- Daniel Frank Quiñones Olgado
- Kevin Andres Rodriguez Lima
- Leonardo Gustavo Gaona Briceño
- Michael Jarnie Ticona Larico

# Pipeline de Integración Continua

## 1. **Construcción Automática**
   - **Herramientas**: PyBuilder
   - **Descripción**: En esta etapa, se compila y construye el proyecto automáticamente.

### Instalar Dependencias

Desde la raíz del proyecto, ejecuta y esto instalará todas las dependencias definidas en el archivo `build.py`.

```bash
pyb install_dependencies
```

### Compilar y Empaquetar el Proyecto

Para generar los artefactos del proyecto:

```bash
pyb
```

Esto generará los paquetes compilados en el directorio `target/`.

---

## Resultado Esperado

Después de ejecutar `pyb`, deberías encontrar:

1. Un paquete compilado en:

   ```
    /dist/CRUD-PYTHON-1.0.0/
   ```

2. Un archivo instalable (`.tar.gz` o `.whl`) dentro del mismo directorio.

---

## Instalación del Paquete Generado

Para instalar el paquete generado localmente:

```bash
pip install target/dist/CRUD-PYTHON-1.0.0.tar.gz
```

Esto instalará la aplicación en tu entorno Python.

---

## 2. **Análisis Estático de Código Fuente**
   - **Herramientas**: SonarQube
   - **Descripción**: El análisis estático del código fuente permite detectar vulnerabilidades, bugs, code smells y otros problemas.

## 3. **Pruebas Unitarias**
   - **Herramientas**: xUnit
   - **Descripción**: Las pruebas unitarias validan que el código funciona correctamente a nivel de funciones o métodos individuales.
### Ejecutar Pruebas Unitarias
Para validar que las pruebas unitarias están funcionando correctamente:
```bash
pyb run_unit_tests
```

## 4. **Pruebas Funcionales**
   - **Herramientas**: Selenium
   - **Descripción**: Las pruebas funcionales validan que las funcionalidades de la aplicación funcionen según lo esperado.

## 5. **Pruebas de Performance**
   - **Herramientas**: JMeter
   - **Descripción**:
     - Las pruebas de rendimiento permiten evaluar la capacidad de la aplicación para manejar múltiples usuarios y solicitudes simultáneamente bajo diferentes condiciones de carga.
     - Se utiliza **JMeter**, una herramienta ampliamente conocida para realizar pruebas de rendimiento mediante planes de prueba predefinidos.
     - En este caso, se diseñó un plan de prueba (`plan.jmx`) con varios grupos de hilos (*Thread Groups*) que simulan distintos escenarios, como inicios de sesión, registros y consultas.
     - El pipeline automatiza la ejecución de estas pruebas, recopilando resultados en formatos compatibles para análisis posterior.

### **Creación del `plan.jmx`**
   - El plan de prueba contiene las siguientes características:
     1. **Thread Groups**: Configurados para simular 50 usuarios concurrentes con un tiempo de rampa de 2 segundos.
     2. **Solicitudes HTTP**: Pruebas específicas para los endpoints `/login`, `/form-registrar-empleado` y `/lista-de-empleados`, enviando datos relevantes en formato JSON o parámetros URL.
     3. **Assertions**: Se añaden validaciones para asegurar que las respuestas contienen datos esperados, como la aparición de "Juan Perez" en el caso de la consulta de empleados.
     4. **Resultados**: Configurados para registrar métricas como tiempo de respuesta, latencia, código de estado, éxito o falla de cada solicitud.

   - El archivo XML (`plan.jmx`) se crea y configura directamente desde la interfaz gráfica de **JMeter**:
     1. Configuración de los *Thread Groups*.
     2. Creación de muestras HTTP (`HTTP Samplers`) para cada endpoint.
     3. Configuración de validaciones (`Assertions`) y recopiladores de resultados (`Result Collectors`).
     4. Exportación del plan en formato `.jmx`.
        
### **Integración en Jenkins**
   - **Pipeline**: Automáticamente clona el repositorio, instala dependencias, arranca la aplicación y ejecuta el plan de prueba de performance. Adicional a esto, los resultados de JMeter se almacenan en una carpeta `Performance/results` para tener un análisis detallado.


## 6. **Pruebas de Seguridad: OWASP ZAP**
   - **Herramientas**: OWASP ZAP
   - **Descripción**:
     - **OWASP ZAP** es una herramienta de seguridad para probar aplicaciones web. Realiza escaneos automáticos para detectar vulnerabilidades de seguridad en aplicaciones web. Esta herramienta se puede integrar en Jenkins para realizar pruebas de seguridad en cada construcción.
     - Se configura OWASP ZAP para ejecutarse como un *daemon* en el puerto 8090, con una clave API para habilitar su uso remoto.
     - En este pipeline, se incluye un paso para preparar, ejecutar el escaneo y publicar los resultados generados por OWASP ZAP.
     - **Requisitos:**
       - Instalar los complementos necesarios de OWASP en Jenkins (incluyendo el plugin de OWASP y el plugin de pipeline de OWASP).
       - Iniciar OWASP ZAP en el puerto 8090 usando el siguiente comando:
         ```bash
         ./zap.sh -daemon -port 8090 -config api.key=h7p3lfqsmh62qvb0gmc6t6ksmb
         ```
       - Aseguràndonos de que la aplicación a analizar esté corriendo en el puerto especificado (en este caso, el puerto 5600).
       - La clave API utilizada en el comando debe coincidir con la que se usa en el pipeline en este caso (`h7p3lfqsmh62qvb0gmc6t6ksmb`).

### Ejemplo del pipeline de OWASP ZAP:
![imagen](https://github.com/user-attachments/assets/b604434b-b4a4-4020-a901-b7e60191a9ce)
![imagen](https://github.com/user-attachments/assets/e78e401c-cf77-4d59-8e81-977eba1622e0)
