# This work is licensed under a Creative Commons Attribution - NonCommercial 4.0 International License

from collections import defaultdict  # Optimizes the code by creating indexes
import json  # Loads the file containing the musics
import random  # Simulates randomness
import tkinter  # Displays the user interface

import pygame  # Controls the music
import serial  # Allows communication with the Arduino board
import speech_recognition as sr  # Handles vocal recognition


class Music:
    def __init__(self, adjectives, source, score=0):
        self.adjectives = adjectives
        self.source = source
        self.score = score


class MusicLibrary:
    def __init__(self, adjectives_index):
        self.adjectives_index = adjectives_index

    def add_music(self, music):
        for adj in music.adjectives:
            self.adjectives_index[adj].append(music)

    def search_by_adjectives(self, description):
        matching_musics = []

        for adj in description:
            matching_musics.extend(self.adjectives_index[adj])

        return list({music.source: music for music in matching_musics}.values())

    def load_from_json(self, json_path):
        # The function returns all the musics from the JSON file
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            adjectives = item["adjectives"]
            source = item["source"]
            self.add_music(Music(adjectives, source))


def choose_music(description, music_list):
    global current_music
    global pause

    arduino.write(" ".join(description).encode())  # The final description is transmitted to Arduino

    for Song in music_list:
        Song.score = 0  # The score is reset
        for word in Song.adjectives:
            if word in description:
                Song.score += 1
            else:
                Song.score -= 0.5
        for word in description:
            if word in Song.adjectives:
                Song.score += 1
            else:
                Song.score -= 0.5

    random.shuffle(music_list)
    sorted_musics = sorted(music_list, key=lambda x: x.score, reverse=True)
    # Musics are sorted by decreasing order according to their score

    next_music = sorted_musics[0].source

    if current_music is not None:
        pygame.mixer.music.fadeout(2000)  # If there was another music playing, it fades out

    current_music = next_music
    pygame.mixer.music.load(next_music)

    pause = False
    pygame.mixer.music.play(loops=-1)  # The music is played indefinitely


def detect_speech():
    root.geometry("200x150")
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio, language="fr-FR")
            return text
        except sr.UnknownValueError:
            error_text.config(text="Répétez plus clairement...")
            root.geometry("200x200")  # The window gets bigger to make the message fit in the interface
            error_text.pack(pady=10, side="bottom")
            return False
        except sr.RequestError:
            error_text.config(text=f"Erreur de service :\nVérifiez votre connexion Internet")
            root.geometry("200x200")
            error_text.pack(pady=10, side="bottom")
            return False


def simplify_text(basic_text):
    vocabulary = {
        "bibliothèque": ["livre", "livres", "grimoire", "grimoires", "parchemin", "parchemins", "érudit", "érudite",
                         "érudits"],
        "château": ["bastion", "citadelle", "forteresse", "palais"],
        "désert": ["aride", "dune", "dunes", "sable"],
        "donjon": ["temple"],
        "église": ["cathédrale", "chapelle", "religieux", "religieuse", "religion", "moine", "moines", "cloître",
                   "abbaye", "abbayes", "divin", "divine", "divins", "divines", "bénédiction"],
        "enfer": ["enfers", "infernal"],
        "forêt": ["arbres", "bois", "clairière"],
        "jungle": ["tropical", "tropicale", "liane", "lianes"],
        "laboratoire": ["alchimie", "apothicaire", "chaudron", "chaudrons", "fiole", "fioles", "potion", "potions"],
        "labyrinthe": ["dédale", "labyrinthesque"],
        "marais": ["bayou", "bayous", "marécage", "marécages", "tourbière", "tourbières"],
        "marché": ["brocante", "marchand", "marchands"],
        "montagne": ["mont", "monts", "montagnes"],
        "océan": ["coquillage", "coquillages", "flots", "île", "îles", "mer", "plage", "vague", "vagues"],
        "plaine": ["champ", "champs", "plaines", "prairie", "prairies", "pré", "prés", "colline", "collines"],
        "prison": ["geôle", "geôles", "cachot", "cachots", "bagne", "incarcération", "carcéral"],
        "rivière": ["berge", "fleuve", "ruisseau"],
        "lac": ["étang"],
        "souterrain": ["caverne", "cavernes", "égout", "égouts", "grotte", "grottes", "souterrains", "tunnel",
                       "tunnels"],
        "taverne": ["auberge", "gargotte", "restaurant"],
        "village": ["cité", "ville"],

        "sinistre": ["araignée", "araignées", "effrayant", "effrayante", "effrayants", "effrayantes", "fantôme",
                     "fantômes", "inquiétant", "inquiétante", "inquiétants", "inquiétantes", "lugubre", "macabre",
                     "oppressant", "oppressante", "menaçant", "menaçante", "menaçants", "menaçantes", "terreur",
                     "terreurs", "effroi", "sang", "sanglant", "sanglante", "sanglants", "sanglantes", "sinistres",
                     "terrifiant", "terrifiante", "cadavre", "cadavres", "cadavérique", "squelette", "squelettes",
                     "cimetière", "cimetières", "tombale", "tombales", "malaise", "maléfique",
                     "horreur", "horreurs", "catacombes", "horrible", "horribles", "affreux", "affreuse", "affreuses",
                     "abominable", "atroce", "ténébreux", "ténébreuse", "ténébreuses", "spectral", "spectrale",
                     "spectrales", "maudit", "maudite", "maudits", "maudites"],
        "puissant": ["grandiose", "magnifique", "puissance", "grandeur", "grand", "majestueux", "prestige",
                     "puissante", "prestigieux", "impérial", "domination"],
        "tranquille": ["paisible", "paisiblement", "calme", "repos", "reposez", "reposer", "dormez", "dormir",
                       "sommeil", "couchez", "coucher"],
        "mystérieux": ["ésotérique", "mystérieuse", "intriguant", "intrigant", "intrigante", "brume", "brouillard",
                       "mystère"],
        "ancien": ["ancienne", "temps", "millénaire", "ancestral", "ancestrale", "archaïque", "immémorial",
                   "immémoriaux"],
        "bizarre": ["étrange", "étranges", "anormal", "anormale", "suspect", "suspecte", "suspects", "suspectes"],
        "émouvant": ["nostalgie", "émotion", "nostalgique"],
        "austère": ["rude", "rudes", "désolé", "désolée", "désolées", "aride", "arides"],
        "exploration": ["explores", "explore", "explorez", "explorer", "engouffrez", "engouffrer"],
        "voyage": ["voyagez", "traversez", "périple", "aventure", "chevauchée", "marche", "randonnée", "odyssée",
                   "expédition", "caravane", "caravanes"],
        "bruyant": ["assourdissant", "sonore", "tapageur", "bruyante", "assourdissante"],
        "magie": ["magique", "féérique", "merveilleux", "merveilleuse", "ensorcelé", "ensorcelée", "ensorcelés",
                  "ensorcelées", "sortilège"],
        "surprise": ["soudain", "soudainement", "brusquement", "subitement"],
        "piège": ["piégé", "piégés", "piège", "pièges"],

        "combat": ["bataille", "bagarre", "mêlée", "assaut", "attaque", "conflit", "affrontement",
                   "combattre", "affronter", "attaquer", "défendre", "duel", "escarmouche", "baston",
                   "belligérant", "belligérants"],
        "feu": ["flamme", "feux", "incendie", "incendies", "brasier", "brasiers", "crépitement", "crépitements"],
        "nuit": ["noir", "obscurité", "lune", "étoiles", "ténèbre", "ténèbres"],
        "jour": ["soleil"],
        "pluie": ["goutte", "gouttes", "pleut", "bruine", "averse", "torrentiel", "torrentielle", "déluge"],
        "orage": ["tempête", "ouragan", "tornade", "cyclone"],
        "hiver": ["neige", "froid", "enneigé", "enneigée", "glacial"],

        "boss": ["dragon", "dragons", "géant", "géants", "hydre", "hydres", "démon", "démons", "diable", "diables",
                 "liche", "liches", "chimère", "chimères", "sphinx", "basilic", "basilics"],
        "ennemi moyen": ["gobelin", "gobelins", "orque", "orques", "troll", "trolls", "ogre", "ogres", "araignée",
                         "araignées", "assassin", "assassins", "cyclope", "fantôme", "fantômes", "zombie", "zombies"]
    }

    simplified_text = []

    # Multi-words expressions
    if "ciel d'encre" in basic_text:
        simplified_text.append("nuit")
    if "tout se passe bien" in basic_text or "tout va bien" in basic_text:
        simplified_text.append("tranquille")
    if "trop calme" in basic_text:
        simplified_text.append("bizarre")
    if "tout à coup" in basic_text:
        simplified_text.append("surprise")

    separated_text = basic_text.split()

    for word in separated_text:
        for key, synonyms_list in vocabulary.items():
            if word in synonyms_list or word == key:
                simplified_word = key
                simplified_text.append(simplified_word)
                break
    if not simplified_text:
        error_text.config(text="Aucune musique associée\nà votre description...")
        error_text.pack(pady=10, side="bottom")
        root.geometry("200x200")
    return simplified_text


def activate_voice_recognition():
    error_text.forget()
    root.geometry("200x150")
    speech = detect_speech()
    if isinstance(speech, str) and speech:  # Verifies if speech is a non-empty string
        final_simplified_text = simplify_text(speech)
        if final_simplified_text:
            matching_musics = library.search_by_adjectives(final_simplified_text)
            choose_music(final_simplified_text, matching_musics)


def manual_control():
    error_text.forget()
    root.geometry("200x200")
    controle_button.pack_forget()
    text_area.pack(pady=10)
    validate_button.pack()


def validate_manual_control():
    root.geometry("200x150")
    content = text_area.get().strip()
    if content:
        final_simplified_text = simplify_text(content)
        if final_simplified_text:
            matching_musics = library.search_by_adjectives(final_simplified_text)
            choose_music(final_simplified_text, matching_musics)

    text_area.delete(0, tkinter.END)
    text_area.pack_forget()
    validate_button.pack_forget()
    controle_button.pack(pady=10)


def stop_music():
    global pause
    if pause is False:
        arduino.write(" ".join(["pause"]).encode())
        pygame.mixer.music.pause()
        pause = True
    else:
        arduino.write(" ".join(["play"]).encode())
        pygame.mixer.music.unpause()
        pause = False


library = MusicLibrary(defaultdict(list))
library.load_from_json("music_data.json")

pygame.mixer.init()

arduino = serial.Serial('/dev/tty.usbserial-1420', 9600)

root = tkinter.Tk()
root.geometry("200x150")
root.title("PACEM Controller")

current_music = None
pause = False

# Initialization of the interface buttons
voice_recognition_button = tkinter.Button(root, text="Détection de parole", command=activate_voice_recognition)
controle_button = tkinter.Button(root, text="Contrôle manuel", command=manual_control)
validate_button = tkinter.Button(root, text="Valider le texte", command=validate_manual_control)
play_button = tkinter.Button(root, text="Play/Pause", command=stop_music)
text_area = tkinter.Entry(root, width=35)
error_text = tkinter.Label(root, text="")

voice_recognition_button.pack(pady=10)
controle_button.pack(pady=10)
play_button.pack(pady=10)
error_text.pack(pady=10, side="bottom")

root.mainloop()
