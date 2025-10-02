from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

def image_to_ascii(
    input_image,
    output_image="ascii_image.png",
    new_width=100,        # largeur cible en caractères
    font_size=12,
    font_path=r"fonts\cour.ttf"
    ):
    ascii_char = " .:-=+*#%@"

    # Charger image
    image = Image.open(input_image).convert("L")
    width, height = image.size

    # Charger police
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    # Taille d'un caractère
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    char_height = font.getbbox("M")[3] - font.getbbox("M")[1]

    # Calcul hauteur en tenant compte du ratio caractère
    new_height = int(height * new_width / width * (char_width / char_height))
    image = image.resize((new_width, new_height))
    pixels = image.load()

    # Créer canvas
    canvas_width = new_width * char_width
    canvas_height = new_height * char_height
    output_img = Image.new("RGB", (canvas_width, canvas_height), "black")
    draw = ImageDraw.Draw(output_img)

    # Conversion pixel -> ASCII
    for y in tqdm(range(new_height)):
        for x in range(new_width):
            pixel_value = pixels[x, y]
            index = min(int(pixel_value / 256 * len(ascii_char)), len(ascii_char) - 1)
            draw.text((x * char_width, y * char_height), ascii_char[index], fill="white", font=font)

    output_img.save(output_image)
    print(f"✅ Image ASCII générée : {output_image}")
