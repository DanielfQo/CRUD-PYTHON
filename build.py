from pybuilder.core import use_plugin, init

# Importar plugins necesarios
use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.install_dependencies")
use_plugin("python.distutils")

# Metadatos del proyecto
name = "CRUD-PYTHON"
version = "1.0.0"
default_task = "publish"

@init
def set_properties(project):
    # Dependencias del proyecto
    project.depends_on("blinker==1.6.2")
    project.depends_on("click==8.1.6")
    project.depends_on("colorama==0.4.6")
    project.depends_on("et-xmlfile==1.1.0")
    project.depends_on("Flask==2.3.2")
    project.depends_on("itsdangerous==2.1.2")
    project.depends_on("Jinja2==3.1.2")
    project.depends_on("MarkupSafe==2.1.3")
    project.depends_on("mysql-connector-python==8.1.0")
    project.depends_on("openpyxl==3.1.2")
    project.depends_on("protobuf==4.21.12")
    project.depends_on("Werkzeug==2.3.6")

    # Configuración de directorios
    project.set_property("verbose", True)
    project.set_property("dir_source_main_python", "my-app")
    project.set_property("dir_source_unittest_python", "tests")
