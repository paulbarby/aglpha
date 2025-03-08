# Civilization Game

A civilization-style strategy game built with Python and Pygame.

## 🎮 Game Overview

This turn-based strategy game allows players to build and manage civilizations, explore procedurally generated maps, manage units and cities, research technologies, and engage in diplomacy and warfare with AI-controlled opponents.

## ✨ Features

- **Procedurally Generated Maps**: Unique gameplay experience with each new game
- **Multiple Terrain Types**: Including grasslands, forests, mountains, deserts, and more
- **City Management**: Build and improve cities, manage resources and production
- **Unit Systems**: Military, civilian, and special units with unique abilities
- **Tech Tree**: Research new technologies to advance your civilization
- **Save/Load System**: Persistent game state using SQLite
- **AI Opponents**: Strategic computer-controlled civilizations
- **Dynamic Audio System**: Context-aware music and sound effects

## 🚀 Installation

### Prerequisites

- Python 3.8+
- Pygame

### Setup

1. Clone the repository:

   ```
   git clone https://github.com/paulbarby/aglpha.git
   cd aglpha
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the game:
   ```
   python game.py
   ```

## 🎯 How to Play

1. **Start a New Game**: From the main menu, select "New Game" to create a new civilization
2. **Game Controls**:

   - Mouse: Select units, cities, and interface elements
   - Arrow Keys: Scroll the map
   - Space: End turn
   - ESC: Access game menu

3. **Gameplay Loop**:
   - Build and expand cities
   - Train units for exploration and combat
   - Research technologies
   - Manage resources
   - Interact with other civilizations

## 🏗️ Technical Architecture

The game is built with a modular architecture consisting of:

- **Engine**: Core game mechanics and state management
- **Map System**: Procedural terrain generation and pathfinding
- **Unit System**: Movement, combat, and special abilities
- **City System**: Building, production, and population management
- **Player System**: Human and AI player management
- **UI System**: Game interface and animations
- **Storage System**: Saving and loading game state
- **Event System**: Game event handling and dispatching

## 📚 Documentation

For more detailed information, see the documentation in the `docs/` directory:

- [Game Specifications](docs/specifications.md)
- [Technical Specifications](docs/technical-specs.md)
- [Asset Guidelines](docs/asset-prompt.txt)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
