[![build](https://github.com/razorblade23/SmartDarts_v2_sbc/actions/workflows/python-app.yml/badge.svg?branch=master&event=push)](https://github.com/razorblade23/SmartDarts_v2_sbc/actions/workflows/python-app.yml)


# SmartDarts 🎯

SmartDarts is a web-based application designed to bring smart functionality to electronic dartboards. It is built to run on single-board computers (SBCs) like Raspberry Pi and interfaces with the physical dartboard via GPIO pins to accurately register hits. The project aims to make local dart games more engaging and interactive.

---

# WARNING ⚠️
THIS IS A WORK IN PROGRESS AND LOTS OF FEATURES ARE MISSING.

---

## Features ✨

### Current Capabilities: 🚀
- **Dartboard Integration**:
  - Uses GPIO pins to connect and interact with physical electronic dartboards. (currently only RPi supported, contributers welcome)
  - Configurable for various dartboard models via a guided initialization process. This allows you to map specific pins to numbers on the dartboard. (not fully finished)

- **Player Support**:
  - Supports up to 8 players in a single game session. (X01 game (single out) only for now)
  -- WARNING: Lacks proper boundaries and will go beyond zero

- **Game Modes**:
  1. **X01**: 
     - Popular game modes such as 301, 501, 701, and more. (only "Single Out" mode for now implemented)

- **Simulation Mode**:
  - Its possible to run the application in simulation mode. ** This DOES NOT require hardware components, wiring and physical dartboard, and is used for testing the application logic.

  - A script in root dir called `sim_cli.py` can be used to simulate throwing darts in specified game. Game must be initialized, players added and game started.

### Work in Progress: 🛠️
- Enhanced user interface.
- Additional game modes and options.
- Advanced analytics and scoring breakdowns.
- Remote game hosting and multiplayer support.
- Better README with more information on the topic

---

## Dartboard GPIO Connections 🔌

### Overview
The dartboard connects to the GPIO pins of the SBC in a matrix configuration. Each dartboard segment (e.g., specific numbers, doubles, and triples) corresponds to a row and column connection. 

### INFO: Detailed schematic will be provided soon

### Wiring Explanation
1. **Matrix Layout**:
   - The dartboard uses a matrix system where rows and columns correspond to specific GPIO pins.
   - When a dart hits a segment, it closes the circuit at the intersection of the respective row and column.

2. **Resistors**:
   - Each column is connected via pull-down resistors to prevent floating signals and ensure stable readings.

---

## Getting Started 🏁

### Prerequisites
To use SmartDarts (as intended), you will need:
- A single-board computer (e.g., Raspberry Pi) with GPIO support
- A compatible electronic dartboard. (nearly any can be used)
- Basic understanding of electronics
- Some thin wire (0.50 - 0.75mm)
- Some resistors
- Small solderboard (or breadboard for prototyping)
- Basic soldering skills (if using solderboard)

### Installation
Installation has 2 methods, using standard pip or using uv (https://docs.astral.sh/uv/)
Both methods are fine


1. Clone this repository to your SBC:
   ```bash

   git clone https://github.com/razorblade23/SmartDarts_v2_sbc
   cd SmartDarts_v2_sbc
   
   ```

### Installation -> Method: 1 💻
Install the necessary dependencies:
   ```bash

   sudo apt-get update
   sudo apt-get install -y python3 python3-pip
   python3 -m venv .venv
   source .venv/bin/activate
   pip install pip-tools
   pip-compile pyproject.toml
   pip install -r requirements.txt

   ```
### Installation -> Method: 2 🖥️
#### Requires `uv` to be installed
Install the necessary dependencies:
   ```bash

   uv sync
   
   ```

3. Run the application:
   ```bash

   uv run run.py

   ```

4. Access the SmartDarts interface by navigating to `http://<your-sbc-ip>:5000` in your browser.

---

## Usage 🕹️

### Initial Setup 🔧
1. Power up your SBC and connect it to the local network.
2. Launch the application and configure your dartboard with guided proccess.
3. Once configured, you can select a game mode and add players to begin playing.

### Initial setup without SBC (Simulation mode)
- A script in root dir called `sim_cli.py` can be used to simulate throwing darts in specified game. 
- You can simulate throwing darts by entering `game ID` which is shown on the playfield
- Darts are entered in format: [`M:S`] -> where `M` is multiplier and `S` is score
-- Examples: `D:8`, `T:10`, `S:25`, `D18`, `T17`, etc...
- You can enter only one dart at a time (to simulate real darts game)

---

## Contributing 🤝
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a branch for your feature or bug fix:
3. Commit your changes:
4. Push to your branch and submit a pull request.

---

## License 📜
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements 🙏
- The Raspberry Pi community for GPIO libraries and support.
- Dart enthusiasts worldwide for game inspiration.

---

Enjoy playing darts with SmartDarts!
