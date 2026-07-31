<!-- markdownlint-disable-file MD041 MD022 MD026 MD034 MD032-->
### Hexlet tests and linter status:
[![Actions Status](https://github.com/Bam-Manu-182/python-project-208/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Bam-Manu-182/python-project-208/actions)

Badge CodeClimate:
[![Maintainability](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-208/maintainability.svg)](https://qlty.sh/gh/Bam-Manu-182/projects/python-project-208)

Proyecto Gestor de Tareas

¡Hola! Este es mi proyecto **Gestor de Tareas**, una aplicación web desarrollada con Django como parte del programa de aprendizaje de Python. Es un sistema completo de gestión de tareas donde los usuarios pueden registrarse, crear tareas, asignarles un estado y clasificarlas mediante etiquetas.

Enlace a la aplicación en vivo

Puedes probar la aplicación desplegada en producción aquí:
**Render:** [(https://python-project-208.onrender.com)]

-----

Tecnologías utilizadas

**Lenguaje:** Python 3.14
**Framework Web:** Django 6
**Gestor de dependencias:** uv / Poetry
**Base de Datos:** SQLite en desarrollo / PostgreSQL en producción
**Servidor WSGI:** Gunicorn
**Monitoreo de Errores:** Rollbar
**Estilos:** Django Bootstrap 5

-----

Funcionalidades del proyecto

**Autenticación:** Registro de nuevos usuarios, inicio de sesión y cierre de sesión.
**Gestión de Estados (Statuses):** Crear, editar, ver y eliminar estados para las tareas (ej. Nuevo, En trabajo, Resuelto). Protegido contra eliminación si el estado está en uso.
**Gestión de Etiquetas (Labels):** Crear, editar y borrar etiquetas para organizarlas mejor. Protegido contra eliminación si la etiqueta está asociada a una tarea.
**Gestión de Tareas (Tasks):**
  Crear tareas asignando autor, ejecutor, estado y etiquetas.
  Ver el detalle de cada tarea.
  Editar tareas existentes.
  Solo el autor de una tarea tiene permiso para eliminarla.
**Filtros Avanzados:** Filtrar la lista de tareas por estado, etiqueta, ejecutor o ver únicamente las tareas propias.

-----

Instrucciones para ejecutarlo localmente

Si quieres clonar este proyecto y probarlo en tu máquina local, sigue estos pasos:

1. Requisitos previos
Tener instalado Python y el gestor de paquetes `uv`.

2. Clonar el repositorio
git clone
cd python-project-208

3. Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto con base en lo siguiente:
Plaintext
SECRET_KEY=tu_secret_key_local
DEBUG=True
ROLLBAR_ACCESS_TOKEN=tu_token_de_rollbar

4. Instalación de dependencias
uv sync

5. Aplicar migraciones
uv run python manage.py migrate

6. Ejecutar el servidor local
uv run python manage.py runserver
Abre tu navegador e ingresa a http://127.0.0.1:8000/.

-----

Pruebas unitarias
El proyecto cuenta con una suite de pruebas para asegurar el correcto funcionamiento del CRUD de etiquetas, estados y tareas:

uv run python manage.py test

-----

Link de Imagenes de Produccion
1. Render.com
https://drive.google.com/file/d/11jexmSDP5ItYfj3vtZw08qXtvluG2q38/view?usp=sharing
2. Rollbar.com
(https://drive.google.com/file/d/15KbaOn4xA1yuwe6gM3KRSgfXR0ClqZsb/view?usp=sharing)
