from PIL import Image, ImageDraw, ImageFont
import os

def crear_logo():
    # Crear una imagen cuadrada con fondo blanco
    tamano = (256, 256)
    imagen = Image.new('RGBA', tamano, (255, 255, 255, 0))
    dibujo = ImageDraw.Draw(imagen)
    
    # Dibujar círculo de fondo
    centro = (128, 128)
    radio = 120
    dibujo.ellipse((centro[0] - radio, centro[1] - radio, 
                   centro[0] + radio, centro[1] + radio), 
                   fill=(40, 120, 200, 255))  # Azul profesional
    
    # Dibujar un certificado estilizado
    dibujo.rectangle((78, 73, 178, 153), fill=(255, 255, 255, 220))
    
    # Añadir líneas al certificado
    for i in range(5):
        y = 90 + i * 12
        dibujo.line([(93, y), (163, y)], fill=(80, 80, 200, 180), width=2)
    
    # Añadir sello
    dibujo.ellipse((138, 113, 158, 133), outline=(180, 40, 40, 200), width=3)
    
    # Añadir iniciales "CM"
    try:
        # Intenta cargar una fuente elegante, si está disponible
        fuente = ImageFont.truetype("arial.ttf", 72)
    except IOError:
        # Si no está disponible, usa una fuente predeterminada
        fuente = ImageFont.load_default()
    
    dibujo.text((90, 170), "CM Pro", fill=(255, 255, 255, 255), font=fuente)
    
    # Guardar las distintas versiones del logo
    directorio_logo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "recursos")
    if not os.path.exists(directorio_logo):
        os.makedirs(directorio_logo)
    
    # Guardar como PNG con transparencia
    imagen.save(os.path.join(directorio_logo, "certmanager_logo.png"))
    
    # Guardar una versión más pequeña para ícono
    icono = imagen.resize((64, 64), Image.LANCZOS)
    icono.save(os.path.join(directorio_logo, "certmanager_icon.png"))
    
    # Guardar como ICO para archivo ejecutable
    icono.save(os.path.join(directorio_logo, "certmanager_icon.ico"), format="ICO")
    
    print(f"Logos guardados en: {directorio_logo}")
    return os.path.join(directorio_logo, "certmanager_icon.ico")

if __name__ == "__main__":
    crear_logo()
