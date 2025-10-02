# ASCII_Convert

ASCII_Convert est un outil Python pour convertir des **images** et des **vidéos** en art ASCII, avec possibilité d’ajouter l’audio pour les vidéos.

---

## Fonctionnalités

### 1. Conversion d’images en ASCII
- Convertit une image en art ASCII.
- Garde le ratio original pour éviter les déformations.
- Permet de choisir :
  - Largeur en caractères
  - Taille de la police
  - Police à utiliser (monospace recommandée)
- Sauvegarde le résultat sous forme d’image `.png`.

### 2. Conversion de vidéos en ASCII
- Convertit une vidéo frame par frame en ASCII.
- Possibilité de conserver l’audio original ou de générer une vidéo muette.
- Permet de choisir :
  - Largeur des caractères
  - Taille de la police
  - Police à utiliser
  - Inclure ou non l’audio
- Sauvegarde le résultat en `.mp4`.

---

## Installation

### 1. Cloner le projet
bash
```
git clone https://github.com/Pittermanifique/ASCII_Convert.git
cd ASCII_Convert
2. Créer un environnement virtuel (optionnel)
```
bash
```
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```
3. Installer les dépendances
```
pip install -r requirements.txt
```
4. Installer FFmpeg
FFmpeg est nécessaire pour gérer l’audio dans les vidéos.
Sur Windows avec winget :
bash
```
winget install "FFmpeg (Essentials Build)"
Vérifier l’installation
ffmpeg -version
```
### Utilisation
Lancer le script principal
bash
```
python3 ascii_convert.py
```

### Dépendances :
```
Python 3.10+
OpenCV (opencv-python)
Pillow (Pillow)
tqdm (tqdm)
FFmpeg (externe) pour l’audio
```

### Conseils d’utilisation :

Toujours utiliser une police monospace pour un rendu correct.
Pour les vidéos longues, privilégiez une largeur de caractères raisonnable.
