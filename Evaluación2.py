import requests
import json
from faker import Faker

APIHOST = "http://library.demo.local" 
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def obtener_token():
    """Obtener token de autenticación"""
    credenciales = (LOGIN, PASSWORD)
    respuesta = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic",
        auth=credenciales
    )
    if respuesta.status_code == 200:
        return respuesta.json()["token"]
    else:
        raise Exception(f"Error al obtener token: {respuesta.status_code}")

def agregar_libro(libro, token):
    """Agregar un libro a la biblioteca"""
    respuesta = requests.post(
        f"{APIHOST}/api/v1/books",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": token
        },
        data=json.dumps(libro)
    )
    if respuesta.status_code == 200:
        print(f"Libro agregado: {libro['title']}")
    else:
        print(f"Error con libro {libro['id']}: {respuesta.status_code} - {respuesta.text}")

def agregar_50_libros():
    """Generar y agregar 50 libros aleatorios"""
    print("\n=== AGREGANDO 50 LIBROS A LA BIBLIOTECA ===")
    token = obtener_token()
    print("Token obtenido correctamente")

    fake = Faker()
    for i in range(105, 155):
        libro = {
            "id": i,
            "title": fake.catch_phrase(),
            "author": fake.name(),
            "isbn": fake.isbn13()
        }
        agregar_libro(libro, token)
    print("\n¡50 libros agregados exitosamente!")


API_KEY = "cisco|nfa6otVRWugYd_Ay7-XO0APEaKJqDye6Inmuef43Ujw" 
GEOCODE_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_URL = "https://graphhopper.com/api/1/route"

def obtener_coordenadas(direccion):
    """Obtiene coordenadas (lat,lng) de una dirección en español"""
    params = {
        "key": API_KEY,
        "q": direccion,
        "locale": "es",
        "limit": 1
    }
    respuesta = requests.get(GEOCODE_URL, params=params, timeout=10)
    respuesta.raise_for_status()
    datos = respuesta.json()
    hits = datos.get("hits", [])
    if hits:
        lat = hits[0]["point"]["lat"]
        lng = hits[0]["point"]["lng"]
        return f"{lat},{lng}"
    else:
        raise ValueError(f"No se encontraron coordenadas para: {direccion}")

def geolocalizacion_interactiva():
    """Permite calcular rutas entre dos direcciones ingresadas por el usuario"""
    print("\n===Sistema de Geolocalización ===")
    while True:
        origen = input("Ingrese la dirección de ORIGEN (o 's' para salir): ")
        if origen.lower() in ["s", "salir"]:
            print("Saliendo del programa de geolocalización...")
            break

        destino = input("Ingrese la dirección de DESTINO (o 's' para salir): ")
        if destino.lower() in ["s", "salir"]:
            print("Saliendo del programa de geolocalización...")
            break

        try:
            coord_origen = obtener_coordenadas(origen)
            coord_destino = obtener_coordenadas(destino)

            params = {
                "key": API_KEY,
                "point": [coord_origen, coord_destino],
                "locale": "es",
                "instructions": "true",
                "vehicle": "car"
            }

            respuesta = requests.get(ROUTE_URL, params=params, timeout=10)
            respuesta.raise_for_status()
            datos = respuesta.json()

            if not datos.get("paths"):
                raise ValueError("No se encontró una ruta entre los puntos especificados.")

            ruta = datos["paths"][0]
            distancia_km = ruta["distance"] / 1000
            tiempo_min = ruta["time"] / 60000

            print(f"\nRuta desde '{origen}' hasta '{destino}'")
            print(f"Distancia total: {distancia_km:.2f} km")
            print(f"⏱Tiempo estimado: {tiempo_min:.2f} minutos\n")

            print("Instrucciones paso a paso:")
            for paso in ruta["instructions"]:
                print(f"- {paso['text']} ({paso['distance']:.2f} m)")

        except requests.exceptions.HTTPError as err:
            print(f"Error HTTP: {err}")
        except requests.exceptions.ConnectionError:
            print("Error de conexión. Verifique su Internet.")
        except Exception as e:
            print(f"Ocurrió un error: {e}")

        print("\n------------------------------------\n")

def menu_principal():
    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Agregar 50 libros a la biblioteca")
        print("2. Usar sistema de geolocalización")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_50_libros()
        elif opcion == "2":
            geolocalizacion_interactiva()
        elif opcion == "3":
            print("Saliendo del programa. ¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    menu_principal()
