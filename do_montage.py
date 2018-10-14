# coding: utf-8
"""
This is the main file of the project.
It searches for the input files:
- the .wav file to open
- the .txt file describing the cuts
- an optionnal jpg file to add to the disk
It instantiate the classes that do the montage and launches it.
"""
import os
import glob

from src import file_parsing, audio_file_editing

#TODO: Ne pas mettre en dur les métadonnées du fichier


def do_stuff():
    # Get the input and output folders
    pwd = os.path.dirname(os.path.realpath(__file__))
    input_folder_path = os.path.join(pwd, "input")
    output_folder_path = os.path.join(pwd, "output")

    for folder in [input_folder_path, output_folder_path]:
        if not os.path.isdir(folder):
            os.makedirs(folder)

    # Search for the file describing the track cuts
    cut_file_paths = glob.glob(os.path.join(input_folder_path, "*.txt"))
    if len(cut_file_paths) == 0:
        print("ERREUR: pas de fichier txt pour le découpage du son."
              " Arret du programme")
        return 1
    cut_file_path = cut_file_paths[0]
    if len(cut_file_paths) > 1:
        print("ATTENTION: plusieurs potentiels fichiers txt pour le découpage "
              "du son. Le fichier choisi arbitrairement "
              "est %s." % cut_file_path)
    else:
        print("fichier de découpage: %s" % cut_file_path)
    mon_decoupage = file_parsing.ParseCutFile(cut_file_path)
    mon_disque = mon_decoupage.parse_file("chantres")

    # Search for the input wav file containting the sound
    sound_file_paths = glob.glob(os.path.join(input_folder_path, "*.wav"))
    if len(sound_file_paths) == 0:
        print("ERREUR: pas de fichier wav contenant le son trouvé."
              " Arret du programme")
        return 1
    sound_file_path = sound_file_paths[0]
    if len(sound_file_paths) > 1:
        print("ATTENTION: plusieurs potentiels fichiers wav pour le contenu "
              "du son. Le fichier choisi arbitrairement "
              "est %s." % sound_file_path)
    else:
        print("fichier contenant le son: %s" % sound_file_path)

    print("lecture fichier")
    disk_manipulation = audio_file_editing.EditAudioFile(sound_file_path)
    print("fin lecture fichier")
    print()

    print("création des pistes")
    disk_manipulation.make_disk(
        mon_disque,
        output_folder=output_folder_path,
        tags={
            "album": "Дуси и души праведных восхвалят Тя, Господи",
            "artist": "Православные русские певчие",
            "year": "2018",
            "genre": "Духовное песнопение",
        },
        cover="chantres.jpg",
    )
    print("Fini !")


if __name__ == '__main__':
    do_stuff()
