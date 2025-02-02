# PACEM - Plateau d'Ambiance Contrôlant l'Eclairage et la Musique

Overview

PACEM is an immersive ambiance system designed for tabletop role-playing games (TTRPGs) like Dungeons & Dragons. It dynamically adjusts background music and LED lighting based on the game master's descriptions. The system consists of:

A voice recognition program that analyzes the game master's descriptions and extracts keywords.

A database of over 80 tracks, categorized by mood and theme.

An Arduino-controlled LED strip (WS2812B) that adjusts colors and effects according to the scene.

A user-friendly tkinter interface for manual and automatic control.

Features

🎵 Dynamic Music Selection

Voice recognition identifies descriptive words in real-time.

A scoring system determines the most appropriate music track based on extracted keywords.

Music is stored on a USB drive to prevent excessive disk usage.

💡 Immersive Lighting Effects

LED colors and animations change according to scene context (e.g., red for battles, green for forests).

Smooth transitions using FastLED's blend() function.

Special effects for common situations (e.g., storms, fire, magic spells).

Adjustable brightness and animation speed via sliders in the GUI.

🖥 Customizable User Interface

Manual control for both lighting and music.

Color and animation customization with real-time preview.

Configurations can be saved and loaded in JSON format.

Installation

Prerequisites

Python 3.x

Arduino IDE (for LED control)

Required Python libraries: speech_recognition, tkinter, pyserial, fastled

An Arduino board compatible with WS2812B LED strips

Setup

Clone the repository:

git clone https://github.com/Ambition42/PACEM.git
cd PACEM

Install dependencies:

pip install -r requirements.txt

Upload the Arduino script to your board.

Run the program:

python main.py

Usage

Launch the PACEM software.

Press the Voice Recognition button to let the system analyze the game master's narration.

The system automatically selects a suitable music track and adjusts the LED lighting.

Use the manual controls for fine-tuning.

License

This project is licensed under Creative Commons Attribution - NonCommercial 4.0 International (CC BY-NC 4.0). See the LICENSE file for details.

Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

🎲 Bring your TTRPG sessions to life with PACEM!

