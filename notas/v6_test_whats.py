# from lib_ import whats as whatsapp

# bot = whatsapp()
# bot.main('INTERNET_FREE') 

import requests

# URL de la API de Free OCR
api_url = 'https://api.ocr.space/parse/image'

# Clave de API proporcionada por Free OCR
api_key = 'K86323011388957'

# Ruta de la imagen que deseas procesar
image_path = r'C:\Users\upset\Pictures\capcha\image1.jpg'

# Parámetros de solicitud
params = {
    'apikey': api_key,
    'language': 'es',  # Idioma de la imagen (puedes cambiarlo según tus necesidades)
}

# Cargar la imagen desde el archivo
with open(image_path, 'rb') as image_file:
    files = {'file': (image_path, image_file)}

# Realizar la solicitud POST a la API
response = requests.post(api_url, files=files, data=params)

# # Analizar la respuesta JSON
# result = response.json()

# # Ver el texto extraído
# if result.get('ParsedResults'):
#     parsed_text = result['ParsedResults'][0]['ParsedText']
#     print("Texto extraído:")
#     print(parsed_text)
# else:
#     print("No se pudo extraer texto.")

