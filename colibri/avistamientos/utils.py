import requests
import os

def identificar_especie(imagen_path):
    api_url = "https://api.inaturalist.org/v1/computervision/identify"
    api_token = os.getenv("INATURALIST_API_TOKEN")

    if not api_token:
        print("⚠️ Error: Falta el token de la API")
        return "Error: Falta el token de la API"

    headers = {"Authorization": f"Bearer {api_token}"}

    try:
        with open(imagen_path, "rb") as img:
            print(f"🖼️ Imagen cargada correctamente desde: {imagen_path}")
            files = {"file": img}
            response = requests.post(api_url, headers=headers, files=files)

        print(f"📡 API Status: {response.status_code}")
        print(f"📡 API Response: {response.text}")

        if response.status_code == 200:
            data = response.json()
            if "results" in data and data["results"]:
                return data["results"][0].get("taxon", {}).get("name", "Especie no identificada")
        else:
            print(f"❌ Error en la API: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"❌ Error en la API: {e}")
        print(f"❌ Error al abrir la imagen: {e}")
        return "Error al abrir la imagen"

    return "Error en la API"