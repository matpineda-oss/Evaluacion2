# Evaluación 2

Descripción del proyecto:

Este proyecto tiene como objetivo agregar libros de forma automática a la API de la biblioteca escolar (School Library API) mediante un script en Python. El programa realiza una conexión a la API utilizando credenciales de autenticación, genera 50 libros con títulos, autores e ISBN aleatorios usando la librería Faker, y los añade al catálogo.

Además, permite visualizar el proceso en consola, mostrar los datos agregados y finalizar el programa escribiendo “s” o “salir”. Todos los mensajes del programa están traducidos al español y los valores numéricos se muestran con dos decimales como máximo.

Instrucciones de como ejecutar el Script:

El script inicia conectándose a la API de la biblioteca mediante un inicio de sesión que genera un token de autenticación. Luego, usa la librería Faker para crear automáticamente 50 libros con títulos, autores e ISBN generados de forma aleatoria.

Por cada libro, el script construye un objeto con esos datos y envía una solicitud HTTP POST al servidor de la API utilizando la librería requests, agregando cada libro al catálogo remoto. Durante el proceso, imprime en pantalla los detalles de cada libro agregado y maneja posibles errores de conexión o autenticación. Al finalizar, muestra un mensaje indicando que la carga fue completada o permite salir del programa escribiendo “s” o “salir”.
