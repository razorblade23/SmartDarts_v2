# SmartDarts

SmartDarts is a web-based application designed to bring smart functionality to electronic dartboards. It is built to run on single-board computers (SBCs) like Raspberry Pi and interfaces with the physical dartboard via GPIO pins to accurately register hits. The project aims to make local dart games more engaging and interactive.

---

## Features

### Current Capabilities:
- **Dartboard Integration**:
  - Uses GPIO pins to connect and interact with physical electronic dartboards.
  - Configurable for various dartboard models via a guided initialization process. This allows you to map specific pins to numbers on the dartboard.

- **Player Support**:
  - Supports up to 8 players in a single game session.

- **Game Modes**:
  1. **X01**: 
     - Popular game modes such as 301, 501, 701, and more.
  2. **Cricket**:
     - Full support for this strategic dart game.

### Work in Progress:
- Enhanced user interface.
- Additional game modes.
- Advanced analytics and scoring breakdowns.
- Remote game hosting and multiplayer support.

---

## Getting Started

### Prerequisites
To use SmartDarts, you will need:
- A single-board computer (e.g., Raspberry Pi).
- A compatible electronic dartboard.
- Basic wiring to connect the dartboard's output pins to the SBC's GPIO pins.

### Installation
1. Clone this repository to your SBC:
   ```bash
   git clone https://github.com/your-repo/smartdarts.git
   cd smartdarts
   ```
2. Install the necessary dependencies:
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3 python3-pip
   pip3 install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python3 app.py
   ```
4. Access the SmartDarts interface by navigating to `http://<your-sbc-ip>:8000` in your browser.

---

## Usage

### Initial Setup
1. Power up your SBC and connect it to the local network.
2. Launch the application and follow the guided initialization process to map the dartboard pins to the respective numbers.
3. Once configured, you can select a game mode and add players to begin playing.

---

## Contributing
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a branch for your feature or bug fix:
   ```bash
   git checkout -b feature/my-feature
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add my feature"
   ```
4. Push to your branch and submit a pull request.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgements
- The Raspberry Pi community for GPIO libraries and support.
- Dart enthusiasts worldwide for game inspiration.

---

Enjoy playing darts with SmartDarts!
