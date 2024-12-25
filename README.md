## CRUD con Python 🐍 MySQL 💾 y un Dashboard Asombroso 🚀

## NOMBRE EQUIPO

- Daniel Frank Quiñones Olgado
- Kevin Andres Rodriguez Lima
- Leonardo Gustavo Gaona Briceño
- Michael Jarnie Ticona Larico

# Compilación, Gestión de Dependencias y Empaquetado de la Aplicación

Este documento detalla cómo compilar, gestionar dependencias y empaquetar la aplicación `CRUD-PYTHON` utilizando **PyBuilder**.

## Pasos para Ejecutar PyBuilder

### 1. Instalar Dependencias

Desde la raíz del proyecto, ejecuta:

```bash
pyb install_dependencies
```

Esto instalará todas las dependencias definidas en el archivo `build.py`.

### 2. Ejecutar Pruebas Unitarias

Para validar que las pruebas unitarias están funcionando correctamente:

```bash
pyb run_unit_tests
```

### 3. Compilar y Empaquetar el Proyecto

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

Con estos pasos, tu aplicación estará completamente gestionada, compilada y empaquetada. Si tienes dudas o necesitas más ayuda, no dudes en consultarlo.

