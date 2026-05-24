from PIL import Image
import os

files_to_convert = [
    ("img/foto_clean.png", (180, 180)),
    ("img/boutique-login.jpeg", None),
    ("img/boutique-dashboard.jpeg", None),
    ("img/boutique-market.jpeg", None)
]

print("Convirtiendo imágenes con Pillow...")

for file_in, resize in files_to_convert:
    if os.path.exists(file_in):
        try:
            img = Image.open(file_in)
            if resize:
                img = img.resize(resize, Image.Resampling.LANCZOS)
            
            file_out = file_in.rsplit('.', 1)[0] + '.webp'
            img.save(file_out, "WEBP", quality=85)
            print(f"✓ Convertido: {file_out}")
        except Exception as e:
            print(f"Error procesando {file_in}: {e}")
    else:
        print(f"Archivo no encontrado: {file_in}")

print("¡Conversión completada!")
