import os
import qrcode
import base64
import json
from PIL import Image, ImageDraw, ImageFont

# Cargar datos desde el archivo datos.json
with open('Pediculosis.json', 'r') as file:
    datos_lista = json.load(file)

# Configurar el tamaño de la fuente para el texto
font_size = 40

# Configurar el tamaño de la imagen (en milímetros)
image_size_mm = (28, 12)

# Convertir tamaño de milímetros a píxeles (considerando 1cm = 37.79 píxeles)
image_size = tuple(int(size_mm * 37.79) for size_mm in image_size_mm)

# Definir la fuente 
font = ImageFont.truetype("arial.ttf", font_size)

# Carpeta de destino para guardar los códigos QR
carpeta_destino = 'PruebaURLScanearNuevoCambios14'
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Generar un código QR para cada conjunto de datos
for datos in datos_lista:
    # Convertir datos a formato JSON
    datos_json = json.dumps(datos)

    # Codificar datos JSON en base64
    datos_base64 = base64.b64encode(datos_json.encode()).decode('utf-8')
    datos_decodificados = base64.b64decode(datos_base64).decode()
    datos_json = json.loads(datos_decodificados)

    # Crear un objeto QR Code con un tamaño más grande
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Tamaño del código QR más grande
        border=4,
    )

    # Agregar datos al QR Code
    qr.add_data(datos_json)
    qr.make(fit=True)

    # Crear la imagen del QR Code
    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Crear una nueva imagen con el nuevo tamaño deseado
    final_img = Image.new('RGB', (image_size[0] - 20, image_size[1]), "white")  # Reducir el ancho en 20 píxeles

    # Pegar el código QR hacia abajo en el eje y
    final_img.paste(qr_img, (0, int((image_size[1] - qr_img.size[1]) / 2) + 20))  # Ajustar la posición hacia abajo

    # Agregar un borde más abajo alrededor de la imagen final
    border_width = 5
    draw = ImageDraw.Draw(final_img)
    draw.rectangle([0, 0, final_img.width - 1, final_img.height - 1], outline="black", width=border_width)

    # Crear un objeto ImageDraw para dibujar sobre la imagen final
    draw = ImageDraw.Draw(final_img)

    # Dividir el nombre del producto en dos partes
    nombre_producto = datos['Detalle']
    mitad_longitud = len(nombre_producto) // 2
    parte_superior = nombre_producto[:mitad_longitud]
    parte_inferior = nombre_producto[mitad_longitud:]

    # Agregar la primera mitad del nombre del producto
    xy_primera_mitad = (qr_img.size[0], int((image_size[1] - font_size) / 2) + 20)  # Ajustar la posición hacia abajo
    draw.text(xy_primera_mitad, parte_superior, font=font, fill="black")

    # Agregar la segunda mitad del nombre del producto con más distancia
    xy_segunda_mitad = (qr_img.size[0], int((image_size[1] + font_size) / 2 + 40))  # Añadir más distancia
    draw.text(xy_segunda_mitad, parte_inferior, font=font, fill="black")

    # Agregar el Codigo de barra más abajo de la segunda mitad del nombre del producto con aún más distancia
    codigo_barra = datos['Codigo de barra']
    xy_codigo_barra = (qr_img.size[0], int((image_size[1] + 2 * font_size) / 2 + 60))  # Añadir aún más distancia
    draw.text(xy_codigo_barra, f"{codigo_barra}", font=font, fill="black")

    try:
        # Guardar la imagen del QR Code en la carpeta "CodigosQr"
        nombre_archivo = f"{codigo_barra}"
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo)

        # Manejar caracteres no válidos en el nombre del archivo
        nombre_archivo = ''.join(c for c in nombre_archivo if c.isalnum() or c in [' ', '.', '-'])
        ruta_archivo = os.path.join(carpeta_destino, nombre_archivo + ".png")

        final_img.save(ruta_archivo,quality=95)
        print(f"Se ha guardado el código QR en: {ruta_archivo}")

    except (FileNotFoundError, OSError) as e:
        print(f"Error al guardar el código QR: {e}")
        # Puedes agregar aquí cualquier acción adicional o simplemente pasar al siguiente archivo
        continue
