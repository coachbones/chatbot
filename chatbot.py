import re
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from bs4 import BeautifulSoup
import requests

def obtener_informacion():
    # Realizar una solicitud GET a la página del CESDE
    url = "https://www.cesde.edu.co/"
    response = requests.get(url, verify=False)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Parsear el contenido HTML de la página
        soup = BeautifulSoup(response.content, 'html.parser')

        # Convertir todo el contenido de la página a texto
        text = soup.get_text().lower()

        # Patrón común para números de teléfono
        pattern_common = re.compile(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b')
    
        # Patrón para números de celular con el prefijo (60)(4)
        pattern_60_4 = re.compile(r'\(60\)\(4\)\s?\d{7}')
    
        # Patrón para números de celular con el prefijo (60)(1)
        pattern_60_1 = re.compile(r'\(60\)\(1\)\s?\d{7}')

        # Definir patrones de regex para buscar información relevante
        patterns = {
            "escuelas": [],
            "contactos": [],
            "direcciones": [
                r'\bmedell[ií]n: (.+)',
                r'\bbello: (.+)',
                r'\brionegro: (.+)',
                r'\bla pintada: (.+)',
                r'\bapartad[oó]: (.+)',
                r'\bbogot[aá]: (.+)'
            ],
            "nuestros servicios":[]
        }

        # Buscar coincidencias de números de contacto
        patterns["contactos"].extend(pattern_common.findall(text))
        patterns["contactos"].extend(pattern_60_4.findall(text))
        patterns["contactos"].extend(pattern_60_1.findall(text))

        # Obtener enlaces a las escuelas y filtrar duplicados
        enlaces_escuelas = set([a['href'] for a in soup.find_all('a', href=True) if 'escuela' in a.get_text().lower()])
        patterns["escuelas"] = list(enlaces_escuelas)

        # Obtener enlaces a los servicios y filtrar duplicados
        enlaces_servicios = set([a['href'] for a in soup.find_all('a', href=True) if 'servicio' in a.get_text().lower()])
        patterns["nuestros servicios"] = list(enlaces_servicios)

        # Buscar coincidencias de direcciones
        matching_responses = {}
        for keyword, pattern_list in patterns.items():
            if keyword == "direcciones":
                direcciones = []
                for pattern in pattern_list:
                    matches = re.findall(pattern, text)
                    direcciones.extend(matches)
                matching_responses[keyword] = direcciones
            else:
                matching_responses[keyword] = pattern_list

        return matching_responses
    else:
        return {"error": "No se pudo acceder a la página del CESDE."}

def mostrar_opciones():
    opciones = [
        "1. Nuestros programas",
        "2. Escuelas",
        "3. Sedes",
        "4. Contacto",
        "5. Aspirantes",
        "6. Estudiantes"
    ]
    print("******************************")
    print("*                            *")
    print("*    Información del CESDE   *")
    print("*                            *")
    print("******************************")
    print("\nBienvenido al chatbot del Cesde! A continuación, te mostraré las opciones en las que puedo ayudarte:")
    for opcion in opciones:
        print(opcion)
    print("\nEscribe el número de la opción o la pregunta correspondiente:")

def main():
    mostrar_opciones()
    while True:
        user_input = input("Tú: ")
        if user_input == "4" or "contacto" in user_input.lower():
            informacion = obtener_informacion()
            if "contactos" in informacion:
                print("******************************")
                print("*                            *")
                print("*    Información de Contacto  *")
                print("*                            *")
                print("******************************")
                print("Bot: Los contactos del Cesde son:")
                for match in informacion["contactos"]:
                    print("- ", match)
            else:
                print("Bot: No encontré información de contacto en la página del CESDE.")
        elif user_input == "3" or "direcciones" in user_input.lower():
            informacion = obtener_informacion()
            if "direcciones" in informacion:
                direcciones = informacion["direcciones"]
                if direcciones:
                    print("******************************")
                    print("*                            *")
                    print("*   Información de Dirección  *")
                    print("*                            *")
                    print("******************************")
                    print("Bot: Las direcciones del Cesde son:")
                    for direccion in direcciones:
                        print("- ", direccion)
                else:
                    print("Bot: No encontré información de direcciones en la página del CESDE.")
        elif user_input == "2" or "escuelas" in user_input.lower():
            informacion = obtener_informacion()
            if "escuelas" in informacion:
                print("******************************")
                print("*                            *")
                print("*    Información de Escuelas  *")
                print("*                            *")
                print("******************************")
                print("Bot: Los enlaces a las escuelas del CESDE son:")
                for enlace in informacion["escuelas"]:
                    print("- ", enlace)
            else:
                print("Bot: No encontré información de escuelas en la página del CESDE.")
        elif user_input == "1" or "programas" in user_input.lower():
            print("Nos alegra mucho que quieras ser parte del CESDE!\n a continuacion, te dejamos el link donde puedes ver nuestros distintos programas: https://www.cesde.edu.co/programas/")
        elif user_input == "5" or "aspirantes" in user_input.lower():
            print("Si deseas inscribirte en el CESDE, en el siguiente enlace podras hacerlo! https://www.cesde.edu.co/aspirantes/ \n Aqui, podras visualizar tambien el cronograma CESDE 2024, donde podras visualizar fechas de matricula, Induccion a nuevos estudiantes, etc.")
        elif user_input == "6" or "estudiantes" in user_input.lower():
            print("Si ya eres un estudiante CESDE, en el siguiente link podras visualizar las distintas opciones para los estudiantes: https://www.cesde.edu.co/estudiantes/")
        else:
            print("Bot: No entendí tu pregunta. Intenta nuevamente.")
        respuesta = input("¿Te ha sido de ayuda esta información? (Sí/No): ")
        if respuesta.lower() == "sí" or respuesta.lower() == "si":
            print("Bot: Me alegra haberte ayudado. ¡Hasta luego!")
            break
        elif respuesta.lower() == "no":
            print("Bot: Lamento que no haya sido útil. ¿En qué más puedo ayudarte?\n Opciones disponibles: \n 1.Nuestros programas \n 2. Escuelas \n 3. Sedes \n 4. Contacto \n 5. Aspirantes \n 6. Estudiantes")
        else:
            print("Bot: Por favor, responde 'Sí' o 'No'.")
            continue

if __name__ == "__main__":
    main()