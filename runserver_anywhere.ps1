# Script para ejecutar el servidor Django desde cualquier subcarpeta
$projectRoot = "C:\Users\andre\Desktop\proyecto pw\Testeo de crucero\Crucero-Testeo"
$env:PYTHONPATH=$projectRoot
python "$projectRoot\manage.py" runserver
