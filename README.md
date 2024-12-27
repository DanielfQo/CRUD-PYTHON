# CRUD con Python 🐍 MySQL 💾 y un Dashboard Asombroso 🚀

## NOMBRE EQUIPO: BAJANDO KILITOS

- Daniel Frank Quiñones Olgado
- Kevin Andres Rodriguez Lima
- Leonardo Gustavo Gaona Briceño
- Michael Jarnie Ticona Larico

## Objetivo

El objetivo de este proyecto es desarrollar una aplicación web que permita la gestión de empleados y usuarios. La plataforma incluye un sistema de **autenticación** (registro e inicio de sesión), un **CRUD** (Crear, Leer, Actualizar, Eliminar) para empleados y usuarios, un **perfil de usuario** personalizable, y un **dashboard** interactivo para visualizar métricas clave.

## Arquitectura de Software

La arquitectura de la aplicación se basa en un diseño **MVC (Modelo-Vista-Controlador)**. 

## Funcionalidades Principales

1. **Sistema de Autenticación**:
   - Registro de nuevos usuarios.
   - Inicio de sesión con validación de credenciales.
![image](https://github.com/user-attachments/assets/280a1ae2-5542-4e82-90be-923809955d11)

2. **Gestión de Usuarios y Empleados**:
   - Crear, Leer, Actualizar y Eliminar registros.
   - Asignación de roles (usuario estándar, administrador).
![image](https://github.com/user-attachments/assets/4a471938-5c47-4e4b-b524-0a4baab21089)

3. **Dashboard Interactivo**:
   - Visualización de componentes clave como listar usuario, empleado, perfil, reportes y salir.
![image](https://github.com/user-attachments/assets/3a0b1946-494c-4bf7-9916-7cfeab53395d)

4. **Perfil de Usuario**:
   - Edición de información personal.
   - Cambio de contraseña.
![image](https://github.com/user-attachments/assets/4b117bfc-7333-4299-89ee-2d146f8394c5)

---

## Tecnologías

### Lenguaje de Programación
- **Python**: Para la lógica del backend.

### Frameworks
- **Flask**: Para la construcción del backend y la API RESTful.

### Bibliotecas
- **SQLAlchemy**: Para la gestión de la base de datos.
- **Jinja2**: Para las plantillas HTML.
- **Chart.js**: Para los gráficos interactivos en el dashboard.

### Herramientas de Construcción y Pruebas
- **PyBuilder**
- **SonarQube**
- **xUnit**
- **JMeter**
- - **OWASP ZAP**
---

## Requisitos para Ejecutar el Proyecto

1. **Entorno de desarrollo**:
   - Python 3.10 o superior.
2. **Dependencias**:
   Ejecutar el siguiente comando para instalar las dependencias necesarias:
   pip install -r requirements.txt
3. **Lanzar el proyecto**:
   Dentro de my-app lanzar con pythonn run.py


# Pipeline de Integración Continua

# 1. **Construcción Automática**
   - **Herramientas**: PyBuilder
   - **Descripción**: En esta etapa, se compila y construye el proyecto automáticamente.

![image](https://github.com/user-attachments/assets/f8cdb352-d3d6-4d81-b1cc-8fc8fcf2ce74)

```bash
pipeline {
    agent any

    environment {
        VENV_PATH = './venv' // Ruta del entorno virtual
    }

    stages {
        stage("Git Checkout") {
            steps {
                git branch: 'main', 
                    changelog: false, 
                    poll: false, 
                    url: 'https://github.com/DanielfQo/CRUD-PYTHON.git'
            }
        }

        stage("Setup Virtual Environment") {
            steps {
                sh '''
                python3 -m venv ${VENV_PATH}
                . ${VENV_PATH}/bin/activate
                '''
            }
        }

        stage("Install Dependencies") {
            steps {
                sh '''
                . ${VENV_PATH}/bin/activate
                pip install -r requirements.txt
                '''
            }
        }

        stage("Start Application") {
            steps {
                script {
                    sh """
                    cd my-app
                    . ../venv/bin/activate
                    nohup python3 run.py > ../app.log 2>&1 &
                    sleep 20
                    if ! ss -tuln | grep ':5600'; then
                        echo "El servidor no se levantó en el puerto 5600" >&2
                        cat ../app.log
                        exit 1
                    fi
                    """
                }
                echo "Aplicación iniciada correctamente."
            }
        }

        stage("Run Unit/Functional Tests") {
            steps {
                script {
                    sh '''
                    export PYTHONPATH=$(pwd)/my-app:$PYTHONPATH
                    . ${VENV_PATH}/bin/activate
                    pip install coverage
                    coverage run -m unittest discover -s my-app/tests
                    coverage report -m
                    coverage html
                    '''
                }
                echo "Pruebas unitarias ejecutadas correctamente."
            }
        }
    }

    post {
        always {
            sh "pkill -f run.py || true"
            echo "Aplicación detenida."
        }
    }
}

```

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

### Resultado Esperado

Después de ejecutar `pyb`, deberías encontrar:

1. Un paquete compilado en:

   ```
    /dist/CRUD-PYTHON-1.0.0/
   ```

2. Un archivo instalable (`.tar.gz` o `.whl`) dentro del mismo directorio.

---

### Instalación del Paquete Generado

Para instalar el paquete generado localmente:

```bash
pip install target/dist/CRUD-PYTHON-1.0.0.tar.gz
```

Esto instalará la aplicación en tu entorno Python.

---

# 2. **Análisis Estático de Código Fuente**
   - **Herramientas**: SonarQube
   - **Descripción**: El análisis estático del código fuente permite detectar vulnerabilidades, bugs, code smells y otros problemas.
![image](https://github.com/user-attachments/assets/e14310bb-56fe-4ca4-8468-62f0e3c0acf5)
```bash
pipeline {
    ....
     stage("Pruebas_Unitarias/Funcionales") {
            steps {
                script {
                    sh '''
                    # Exportar la ruta del proyecto
                    export PYTHONPATH=$(pwd)/my-app:$PYTHONPATH
                    
                    # Activar el entorno virtual (si lo tienes)
                    . venv/bin/activate
        
                    # Instalar coverage si no está instalado
                    pip install coverage
                    
                    # Ejecutar las pruebas unitarias con cobertura
                    coverage run -m unittest discover -s my-app/tests
                    
                    # Generar reporte en consola
                    coverage report -m
                    
                    # Generar reporte en formato HTML
                    coverage html
                    '''
                }
                echo "Pruebas unitarias ejecutadas correctamente."
                script {
                    sh '''
                    # Servir el reporte en un servidor local
                    cd htmlcov
                    python3 -m http.server 8000 &
                    sleep 5  # Esperar a que el servidor inicie

                    echo "Accede al reporte de cobertura en: http://localhost:8000/index.html"
                    '''
                }
            }
}
```

# 3. **Pruebas Unitarias**
   - **Herramientas**: xUnit
   - **Descripción**: Las pruebas unitarias validan que el código funciona correctamente a nivel de funciones o métodos individuales.
### Ejecutar Pruebas Unitarias
Para validar que las pruebas unitarias están funcionando correctamente:
```bash
pyb run_unit_tests
```
![image](https://github.com/user-attachments/assets/e856f7e1-724c-4cb5-bbb4-e3dd68a7302d)

```bash
pipeline {
      stage("Pruebas_Unitarias/Funcionales") {
            steps {
                script {
                    sh '''
                    # Exportar la ruta del proyecto
                    export PYTHONPATH=$(pwd)/my-app:$PYTHONPATH
                    
                    # Activar el entorno virtual (si lo tienes)
                    . venv/bin/activate
        
                    # Instalar coverage si no está instalado
                    pip install selenium coverage
                    
                    # Ejecutar las pruebas unitarias con cobertura
                    coverage run -m unittest discover -s my-app/tests
                    
                    # Generar reporte en consola
                    coverage report -m
                    
                    # Generar reporte en formato HTML
                    coverage html
                    '''
                }
                echo "Pruebas unitarias ejecutadas correctamente."
                script {
                    sh '''
                    # Servir el reporte en un servidor local
                    cd htmlcov
                    python3 -m http.server 8000 &
                    sleep 5  # Esperar a que el servidor inicie

                    echo "Accede al reporte de cobertura en: http://localhost:8000/index.html"
                    '''
                }
            }
        }
}
```

# 4. **Pruebas Funcionales**
   - **Herramientas**: 
   - **Descripción**: Las pruebas funcionales validan que las funcionalidades de la aplicación funcionen según lo esperado.

```bash
pipeline {
}
```
# 5. **Pruebas de Performance**
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

![image](https://github.com/user-attachments/assets/9bff1846-0107-4c55-9f51-55a980ef0c42)

```bash
pipeline {
    agent any

    environment {
        JMETER_HOME = '/opt/apache-jmeter/bin' // Ruta de instalación de JMeter
        TEST_PLAN_PATH = './Performance/plan.jmx' // Ruta del plan JMX
        RESULT_DIR = './Performance/results' // Ruta para guardar los resultados
    }

    stages {
        stage("Run JMeter Performance Test") {
            steps {
                script {
                    sh """
                    if [ -f "$RESULT_DIR/results.jtl" ]; then
                        rm -f $RESULT_DIR/results.jtl
                    fi
                    if [ -d "$RESULT_DIR/report" ]; then
                        rm -rf $RESULT_DIR/report
                    fi

                    mkdir -p $RESULT_DIR

                    $JMETER_HOME/jmeter.sh -n -t $TEST_PLAN_PATH -l $RESULT_DIR/results.jtl -e -o $RESULT_DIR/report

                    echo "Pruebas de rendimiento completadas. Resultados guardados en: $RESULT_DIR"
                    """
                }
            }
        }

        stage("Publish JMeter Report") {
            steps {
                script {
                    archiveArtifacts artifacts: "$RESULT_DIR/**", fingerprint: true
                    echo "Resultados de JMeter publicados."
                }
            }
        }
    }
}

```

# 6. **Pruebas de Seguridad: OWASP ZAP**
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
![image](https://github.com/user-attachments/assets/83daaaa7-b00e-4533-9c39-dea46b4fd4b3)
```bash
pipeline {
    agent any

    environment {
        CLAVE_API = '6b83sjeikn0soaaou69vl0ckbv'
        OBJETIVO = 'http://127.0.0.1:5600'
        ZAP_URL = 'http://localhost:8090'
    }

    stages {
        stage("Preparar Escaneo OWASP ZAP") {
            steps {
                script {
                    waitUntil {
                        try {
                            def respuesta = sh(script: "curl -s '${ZAP_URL}/JSON/core/view/version/?apikey=${CLAVE_API}'", returnStdout: true).trim()
                            echo "Respuesta de OWASP ZAP: ${respuesta}"
                            return respuesta.contains("version")
                        } catch (Exception e) {
                            echo "Error al conectar con ZAP: ${e.message}"
                            return false
                        }
                    }

                    sh """
                    curl -s '${ZAP_URL}/JSON/core/action/accessUrl/?url=${OBJETIVO}&apikey=${CLAVE_API}'
                    curl -s '${ZAP_URL}/JSON/spider/action/scan/?url=${OBJETIVO}&apikey=${CLAVE_API}'
                    """
                }
            }
        }

        stage("Ejecutar Escaneo OWASP ZAP") {
            steps {
                script {
                    def estado = '0'
                    def maxIntentos = 30
                    def intentos = 0
                    while (intentos < maxIntentos) {
                        def estadoJson = sh(script: "curl -s '${ZAP_URL}/JSON/ascan/view/status/?apikey=${CLAVE_API}'", returnStdout: true).trim()
                        estado = estadoJson =~ /"status":"(\d+)"/ ? (estadoJson =~ /"status":"(\d+)"/)[0][1] : '0'

                        echo "Estado del escaneo: ${estado}"
                        if (estado == '100') {
                            echo "Escaneo completado con éxito."
                            break
                        }

                        sleep 10
                        intentos++
                    }

                    if (estado != '100') {
                        error "El escaneo no completó correctamente después de ${maxIntentos} intentos."
                    }
                }
            }
        }

        stage("Publicar Resultados OWASP ZAP") {
            steps {
                script {
                    sh "curl -s '${ZAP_URL}/OTHER/core/other/htmlreport/?apikey=${CLAVE_API}' -o reporte-zap.html"
                    echo "Reporte de OWASP ZAP disponible en: ${pwd()}/reporte-zap.html"
                    archiveArtifacts artifacts: 'reporte-zap.html', fingerprint: true
                }
            }
        }
    }
}

```
![imagen](https://github.com/user-attachments/assets/e78e401c-cf77-4d59-8e81-977eba1622e0)

