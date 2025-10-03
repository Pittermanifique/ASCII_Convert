import cv2
import numpy as np
import subprocess
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm

def frame_to_ascii_image(frame, new_width, font, ascii_chars=" .:-=+*#%@"):
    # Conversion OpenCV (BGR) -> Pillow (L pour grayscale)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image_pillow = Image.fromarray(frame_rgb).convert("L")

    # Calcul dimensions adaptées
    width, height = image_pillow.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)

    # Redimensionnement
    image_pillow = image_pillow.resize((new_width, new_height))
    pixels = image_pillow.load()

    # Taille caractère
    char_width = font.getbbox("M")[2] - font.getbbox("M")[0]
    char_height = font.getbbox("M")[3] - font.getbbox("M")[1]

    # Génération ASCII
    ascii_lines = []
    for y in range(new_height):
        line = ""
        for x in range(new_width):
            pixel_value = pixels[x, y]
            index = min(int(pixel_value / 256 * len(ascii_chars)), len(ascii_chars) - 1)
            line += ascii_chars[index]
        ascii_lines.append(line)

    # Création image texte
    frame_width = new_width * char_width
    frame_height = new_height * char_height
    img_txt = Image.new("RGB", (frame_width, frame_height), color="black")
    draw = ImageDraw.Draw(img_txt)

    # Dessin caractère par caractère
    for y, line in enumerate(ascii_lines):
        for x, ch in enumerate(line):
            draw.text((x * char_width, y * char_height), ch, fill="white", font=font)

    return img_txt

def video_to_ascii(
    video_path,
    output_final="ascii_with_audio.mp4",
    new_width=300,
    font_size=12,
    font_path=r"fonts\cour.ttf",
    with_audio=True
):
    # Charger la vidéo
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Impossible d'ouvrir la vidéo.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Charger la police
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        print("⚠️ Police non trouvée, utilisation de la police par défaut")
        font = ImageFont.load_default()

    # Test rapide : générer une frame ASCII pour connaître la taille finale
    ret, test_frame = cap.read()
    if not ret:
        print("❌ Impossible de lire la première frame.")
        return
    test_img = frame_to_ascii_image(test_frame, new_width, font)
    frame_width, frame_height = test_img.size

    # Réinitialiser la vidéo (après test_frame)
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Sortie temporaire muette
    output_ascii = "ascii_video.mp4"

    # 🎥 Préparation écriture vidéo ASCII
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_ascii, fourcc, fps, (frame_width, frame_height))

    # 🔄 Génération frame par frame
    for _ in tqdm(range(total_frames), desc="Génération ASCII vidéo"):
        ret, frame = cap.read()
        if not ret:
            break

        img_txt = frame_to_ascii_image(frame, new_width, font)

        # Conversion Pillow -> OpenCV
        frame_bgr = cv2.cvtColor(np.array(img_txt), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    cap.release()
    out.release()
    print("✅ Vidéo ASCII générée :", output_ascii)

    # 🎵 Gestion audio
    if with_audio:
        print("Ajout de l'audio d'origine avec ffmpeg...")
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