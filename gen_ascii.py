import time
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import subprocess
import os


def frame_to_ascii_image(
        frame,
        new_width,
        font,
        ascii_chars=" .:-=+*#%@",
        show_progress=False
    ):
    # Si la frame vient d'OpenCV (numpy array)
    if isinstance(frame, np.ndarray):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_pillow = Image.fromarray(frame_rgb).convert("L")

    # Si c'est déjà une image Pillow
    elif isinstance(frame, Image.Image):
        image_pillow = frame.convert("L")

    else:
        raise TypeError(f"Type de frame non supporté : {type(frame)}")

    # Taille d'un caractère (largeur / hauteur)
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    char_height = font.getbbox("M")[3] - font.getbbox("M")[1]

    # Calcul du ratio et redimensionnement
    width, height = image_pillow.size
    new_height = int(height * new_width / width * (char_width / char_height))
    image_pillow = image_pillow.resize((new_width, new_height))
    pixels = image_pillow.load()

    # Création canvas de sortie
    frame_width = new_width * char_width
    frame_height = new_height * char_height
    img_txt = Image.new("RGB", (frame_width, frame_height), "black")
    draw = ImageDraw.Draw(img_txt)

    # Progression optionnelle
    iterator_y = tqdm(range(new_height), desc="Conversion en ASCII") if show_progress else range(new_height)

    # Conversion pixel → caractère ASCII
    for y in iterator_y:
        for x in range(new_width):
            pixel_value = pixels[x, y]
            index = min(int(pixel_value / 256 * len(ascii_chars)), len(ascii_chars) - 1)
            draw.text((x * char_width, y * char_height), ascii_chars[index], fill="white", font=font)

    return img_txt

def frame_to_ascii_text(
        frame,
        new_width,
        font
    ):
    # Conversion en niveaux de gris
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(frame_rgb).convert("L")

    # Dimensions de caractère
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    char_height = font.getbbox("M")[3] - font.getbbox("M")[1]
    char_ratio = char_height / char_width

    # Calcul de la nouvelle hauteur en respectant le ratio
    width, height = img_pil.size
    new_height = int(height / width * new_width * char_ratio)

    img_pil = img_pil.resize((new_width, new_height))
    pixels = img_pil.load()

    ascii_chars = " .:-=+*#%@"
    ascii_text = ""
    for y in range(new_height):
        line = ""
        for x in range(new_width):
            pixel_value = pixels[x, y]
            index = min(int(pixel_value / 256 * len(ascii_chars)), len(ascii_chars) - 1)
            line += ascii_chars[index]
        ascii_text += line + "\n"
    return ascii_text


# Conversion d'une image en ASCII
def image_to_ascii(
        input_image,
        output_image="ascii_image.png",
        new_width=100,
        font_size=12,
        font_path=r"font\cour.ttf"
    ):
    # Charger la police
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("⚠️ Police introuvable, police par défaut utilisée")
        font = ImageFont.load_default()

    # Charger l'image
    image = Image.open(input_image)

    # Conversion via la fonction centrale
    ascii_img = frame_to_ascii_image(image, new_width, font, show_progress=True)

    # Sauvegarde
    ascii_img.save(output_image)
    print(f"✅ Image ASCII générée : {output_image}")


# Conversion d'une vidéo en ASCII
def video_to_ascii(
        video_path,
        output_final="ascii_with_audio.mp4",
        new_width=150,
        font_size=12,
        font_path=r"font\cour.ttf",
        with_audio=True
    ):
    # Charger vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la vidéo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Charger police
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("⚠️ Police introuvable, police par défaut utilisée")
        font = ImageFont.load_default()

    # Générer une frame test pour calculer dimensions
    ret, frame = cap.read()
    if not ret:
        print("❌ Impossible de lire la première frame.")
        return
    ascii_frame = frame_to_ascii_image(frame, new_width, font)
    frame_width, frame_height = ascii_frame.size

    # Préparer sortie temporaire muette
    output_ascii = "ascii_video.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_ascii, fourcc, fps, (frame_width, frame_height))

    # Revenir au début de la vidéo
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Génération frame par frame
    for _ in tqdm(range(total_frames), desc="🎥 Génération vidéo ASCII"):
        ret, frame = cap.read()
        if not ret:
            break
        ascii_frame = frame_to_ascii_image(frame, new_width, font)
        frame_bgr = cv2.cvtColor(np.array(ascii_frame), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    cap.release()
    out.release()

    print("✅ Vidéo ASCII générée :", output_ascii)

    # Fusion avec l'audio original
    if with_audio:
        print("🎵 Ajout de l'audio avec ffmpeg...")
        cmd = [
            "ffmpeg", "-y",
            "-i", output_ascii,
            "-i", video_path,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            "-map", "0:v:0",
            "-map", "1:a:0?",
            "-shortest",
            output_final
        ]
    else:
        print("Export sans audio...")
        cmd = [
            "ffmpeg", "-y",
            "-i", output_ascii,
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            output_final
        ]

    subprocess.run(cmd)
    print(f"✅ Vidéo finale générée : {output_final}")


def video_to_ascii_window(
        video_path,
        new_width=150,
        font_size=12,
        font_path=r"font\cour.ttf"
    ):

    # Charger vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la vidéo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = 1 / fps if fps > 0 else 0.033

    # Charger police
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("⚠️ Police introuvable, police par défaut utilisée")
        font = ImageFont.load_default()

    # Lecture frame par frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convertir frame en ASCII image
        ascii_img = frame_to_ascii_image(frame, new_width, font)

        # Convertir en BGR pour OpenCV
        frame_bgr = cv2.cvtColor(np.array(ascii_img), cv2.COLOR_RGB2BGR)

        # Affichage
        cv2.imshow("ASCII Video", frame_bgr)

        if cv2.waitKey(int(delay * 1000)) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Lecture ASCII terminée")



