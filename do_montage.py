# coding: utf-8
import os

from src import file_parsing, audio_file_editing

pwd = os.path.dirname(os.path.realpath(__file__))
input_folder_path = os.path.join(pwd, "input")
output_folder_path = os.path.join(pwd, "output")

mon_decoupage = file_parsing.ParseCutFile(
    os.path.join(input_folder_path, "decoupage_disque.txt")
)
mon_disque = mon_decoupage.parse_file("chantres")
print("lecture fichier")
manips_disque = audio_file_editing.EditAudioFile(
    os.path.join(input_folder_path, "CHOEURS V4.wav")
)
print("fin lecture fichier")

print("création des pistes")
manips_disque.make_disk(
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
