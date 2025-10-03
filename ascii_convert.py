import sys
import time

import gen_ascii

def video():
    print("presser la touche entrée pour les paramètres par défaut")
    video_path = input("fichier video : ")
    output_final = input("fichier final : ")
    new_width = input("nombre de caractères de large : ")
    new_width = int(new_width) if new_width.strip() != "" else None
    font_size = input("taille de la police : ")
    font_size = int(font_size) if font_size.strip() != "" else None
    font_path = input("fichier de la police : ")
    with_audio = input("avec audio ??? (y/n) : ")
    if with_audio.lower() == "y":
        gen_ascii.video_to_ascii(
            video_path,
            output_final=output_final,
            new_width=new_width,
            font_size=font_size,
            font_path=font_path,
        )
    elif with_audio.lower() == "n":
        gen_ascii.video_to_ascii(
            video_path,
            output_final=output_final,
            new_width=new_width,
            font_size=font_size,
            font_path=font_path,
            with_audio=False
        )

def image():
    print("presser la touche entrée pour les paramètres par défaut")
    input_image = input("fichier image : ")
    output_image = input("fichier final : ")
    new_width = input("nombre de caractères de large : ")
    new_width = int(new_width) if new_width.strip() != "" else None
    font_size = input("taille de la police : ")
    font_size = int(font_size) if font_size.strip() != "" else None
    font_path = input("fichier de la police : ")
    gen_ascii.image_to_ascii(
        input_image,
        output_image,
        new_width,
        font_size,
        font_path
    )


def video_live():
    print("Presser la touche entrée pour utiliser les paramètres par défaut")
    video_path = input("Fichier vidéo : ")
    new_width = input("Nombre de caractères de large (max 200) : ")
    new_width = int(new_width) if new_width.strip() != "" else 150
    font_size = input("Taille de la police : ")
    font_size = int(font_size) if font_size.strip() != "" else 12
    font_path = input("Fichier de police : ")
    font_path = font_path if font_path.strip() != "" else r"fonts\cour.ttf"
    print("Presser la touche q pour quitter la vidéo")
    time.sleep(3)

    gen_ascii.video_to_ascii_window(
        video_path,
        new_width=new_width,
        font_size=font_size,
        font_path=font_path,
    )

def main():
    while True:
        art = r"""
                                       __  __                                                                      __           
                                      /  |/  |                                                                    /  |          
          ______    _______   _______ $$/ $$/         _______   ______   _______   __     __  ______    ______   _$$ |_         
         /      \  /       | /       |/  |/  |       /       | /      \ /       \ /  \   /  |/      \  /      \ / $$   |        
         $$$$$$  |/$$$$$$$/ /$$$$$$$/ $$ |$$ |      /$$$$$$$/ /$$$$$$  |$$$$$$$  |$$  \ /$$//$$$$$$  |/$$$$$$  |$$$$$$/         
         /    $$ |$$      \ $$ |      $$ |$$ |      $$ |      $$ |  $$ |$$ |  $$ | $$  /$$/ $$    $$ |$$ |  $$/   $$ | __       
        /$$$$$$$ | $$$$$$  |$$ \_____ $$ |$$ |      $$ \_____ $$ \__$$ |$$ |  $$ |  $$ $$/  $$$$$$$$/ $$ |        $$ |/  |      
        $$    $$ |/     $$/ $$       |$$ |$$ |______$$       |$$    $$/ $$ |  $$ |   $$$/   $$       |$$ |        $$  $$/       
         $$$$$$$/ $$$$$$$/   $$$$$$$/ $$/ $$//      |$$$$$$$/  $$$$$$/  $$/   $$/     $/     $$$$$$$/ $$/          $$$$/        
                                             $$$$$$/                                                                            
        
        """
        print(art)
        print("1-convertir une image")
        print("2-convertir une vidéo")
        print("3-lire une vidéo en convertion direct (peut de fps a cause du traitement lant de l'image)")
        print("4-exit")
        choice = input("votre choix : ")
        if choice == "1":
            image()
        elif choice == "2":
            video()
        elif choice == "3":
            video_live()
        elif choice == "4":
            sys.exit()
        else:
            print("❌ Choix invalide")

if __name__ == "__main__":
    main()