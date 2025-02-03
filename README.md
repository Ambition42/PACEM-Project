# PACEM Project

## Overview
The PACEM is an immersive ambiance system designed for tabletop role-playing games (TTRPGs) like Dungeons & Dragons. It dynamically adjusts background music and LED lighting based on the game master's descriptions. The system consists of:

 - A voice recognition program that analyzes the game master's descriptions and extracts keywords.

 - A database of over 90 tracks, categorized by mood and theme.

 - An Arduino-controlled LED strip (WS2812B) that adjusts colors and effects according to the scene.

 - A user-friendly tkinter interface for manual and automatic control.

## Installation
Prerequisites :
- Python 3.x
- Arduino IDE
- Required Python libraries : speech_recognition, pygame, random, tkinter, serial, json, collections, defaultdict
- Required Arduino library : FastLED

First, clone the repository :
```bash 
git clone https://github.com/Ambition42/PACEM-Project.git
```

Upload the Arduino script to your board. 

Run the Python script. You should see a graphical interface appear. 

You can now start using the PACEM to enhance your roleplay game nights !

## Language
The name "PACEM" comes from the french acronym Plateau d'Ambiance Contrôlant l'Eclairage et la Musique.
For now, the PACEM can only understand descriptions in french. Our team is currently working on an improved version to allow users to choose the language they want.


