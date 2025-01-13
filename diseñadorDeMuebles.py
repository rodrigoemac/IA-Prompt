import openai
from PIL import Image
import requests
from io import BytesIO

def generate_text_prompt(description, dimensions, materials):
    prompt = (
        f"Eres un experto en diseño de muebles industriales. Con la siguiente información: "
        f"Descripción: {description}. Dimensiones: {dimensions}. Materiales: {materials}. "
        "Genera lo siguiente: \n"
        "1. Un nombre atractivo para el mueble.\n"
        "2. Una reseña breve que explique por qué deberían comprar este mueble.\n"
    )
    return prompt

def generate_image_prompt(description, dimensions, materials, style):
    return (
        f"Diseña un mueble industrial basado en la descripción: {description}. Dimensiones: {dimensions}. "
        f"Materiales: {materials}. Estilo visual: {style}."
    )

def main():
    # Información de entrada del usuario
    description = input("Describe el mueble (ej. mesa de comedor rústica): ")
    dimensions = input("Proporciona las dimensiones (ej. 200x100x75 cm): ")
    materials = input("Lista los materiales (ej. acero y madera de roble): ")

    # Generar texto
    openai.api_key = ""
    text_prompt = generate_text_prompt(description, dimensions, materials)
    text_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Eres un asistente experto en diseño de muebles industriales."},
            {"role": "user", "content": text_prompt},
        ],
    )

    text_output = text_response["choices"][0]["message"]["content"]
    print("\n--- Resultado de Texto ---\n")
    print(text_output)

    # Generar imágenes
    styles = ["estilo sketchUp", "estilo render fotográfico"]
    images = []

    for style in styles:
        image_prompt = generate_image_prompt(description, dimensions, materials, style)
        image_response = openai.Image.create(
            prompt=image_prompt,
            n=1,
            size="1024x1024"
        )

        image_url = image_response['data'][0]['url']
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        images.append(img)

    # Mostrar imágenes
    for idx, img in enumerate(images):
        img.show(title=f"Imagen {idx+1}: {styles[idx]}")

if __name__ == "__main__":
    main()
