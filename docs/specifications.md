**Game Design Document: Civilization-Inspired Strategy Game**

---

## **Overview**

This document outlines the specifications for a strategy game inspired by the Civilization series. The game is developed using **Python and Pygame**, featuring **procedural map generation using Perlin noise**, **SQLite3 for persistent data storage**, and **configurable settings stored in INI files**.

---

## **Core Features**

### **1. User Interface (UI) & User Interaction**

- **Menu System**:
  - Start Screen with options: **Create New Game**, **Load Existing Game**, **Exit**.
  - When you create new game you have to give it a name, this allows multiple saved games to be kept
  - Load Existing Game first shows a list of saved games when the user selects the save the load button activates and once clicked it retrieves save data from SQLite3 and starts the game playing
- **In-Game UI**:
  - **Command Interface** on the left side of the screen, similar to games like **Age of Empires** and **Civilization VI**, displaying available actions for selected units or cities.
  - **Contextual UI** that changes dynamically based on selection, similar to **Total War**.
  - **Tooltips and pop-up notifications** provide hints and feedback.
  - **Minimap** in the bottom-right for quick navigation.
  - **Turn-based system** where players make strategic moves before ending their turn.
  - **Fog of War** obscuring unexplored regions, like in **StarCraft** and **Civ VI**.
  - **Right-click for movement and left-click for selection**, inspired by **Command & Conquer**.

---

## **2. Map Generation & Exploration**

- **Procedural terrain generation** using **Perlin noise**, akin to **Minecraft’s world generation**.
- **Map size is configurable** in an INI file.
- **Tile types**:
  - Grassland, Forest, Desert, Mountains, Water, Tundra, Swamp, and Hills.
- **Exploration Mechanics**:
  - Units can only move into tiles within their sight range.
  - Scout units have increased vision.
  - Enemy movement outside explored areas remains unknown unless units are present.

---

## **3. Game Mechanics**

### **Cities**

- **City Development**:
  - Settlers establish cities.
  - Cities require food to grow and resources to build structures and train units.
  - Growth is influenced by resource availability and trade routes.
  - Structures such as **Granaries**, **Workshops**, and **Factories** improve resource output.
- **Buildings & Upgrades**:
  - Housing: Increases population cap.
  - Barracks: Trains military units.
  - Universities: Boost research speed.
  - Factories: Improve production efficiency.
  - Walls & Fortifications: Improve city defense.

### **Resource Collection & Management**

- **Harvesting**:
  - Workers gather resources from nearby tiles.
  - Mines for metals and coal.
  - Farms for food production.
  - Lumber camps for wood.
  - Oil rigs and uranium extraction for late-game units.
- **Trade & Economy**:
  - Cities can **trade resources** via roads and harbors.
  - Gold is generated from commerce, taxes, and trade routes.
  - Marketplaces, Banks, and Stock Exchanges boost economic growth.

---

## **4. Unit Mechanics & Combat**

### **Unit Interaction & Movement**

- **Turn-based movement**, where units can move a set distance per turn.
- **Different terrains impact movement**:
  - Roads increase speed.
  - Forests slow down most units but offer defensive bonuses.
  - Mountains are impassable except for specialized units.
  - Water requires naval or air transport.

### **Combat Mechanics**

- **Turn-based combat**, influenced by terrain, unit positioning, and technological advancements.
- **Unit strengths and weaknesses**:
  - Cavalry excels against archers but is weak against spearmen.
  - Siege units are powerful against cities but weak against infantry.
  - Air units dominate late-game battles but require fuel upkeep.
- **Ranged vs. Melee**:
  - Ranged units can attack from a distance but are weak in close combat.
  - Melee units must engage directly but have higher defense.
- **Fortifications**:
  - Cities and forts provide defensive bonuses.
  - Units inside cities benefit from increased protection.

### **Unit Types by Age**

#### **1. Tribal Age**

- **Spearmen (Melee)**: Basic foot soldiers.
- **Canoes (Naval)**: Small transport vessels.

#### **2. Bronze Age**

- **Swordsmen (Melee)**: Stronger infantry.
- **Chariots (Mounted)**: Fast-moving but weak against spearmen.
- **Battering Rams (Siege)**: Destroys city walls.
- **Triremes (Naval)**: First combat ships.

#### **3. Iron Age**

- **Legionnaires (Melee)**: Heavy infantry.
- **Cavalry (Mounted)**: Faster, stronger mounted units.
- **Ballistae (Siege)**: Long-range attacks on fortifications.

#### **4. Steel Age**

- **Musketmen (Ranged)**: Early gunpowder units.
- **Dragoons (Mounted)**: Fast shock cavalry.
- **Cannons (Siege)**: High-damage against cities.
- **Frigates (Naval)**: Stronger combat ships.

#### **5. Steam Engine Age**

- **Riflemen (Ranged)**: Effective against all older units.
- **Steam Tanks (Heavy)**: Early armored vehicles.
- **Ironclads (Naval)**: Heavy warships.

#### **6. Combustion Engine Age**

- **Infantry (Ranged)**: Modern soldiers.
- **Armored Tanks (Heavy)**: Game-changing powerful units.
- **Battleships & Submarines (Naval)**: Control the seas.
- **Early Planes (Air)**: First air combat units.

#### **7. Jet Age**

- **Modern Infantry (Ranged)**: Final-tier soldiers.
- **Main Battle Tanks (Heavy)**: Most powerful land units.
- **Jet Fighters & Bombers (Air)**: Dominates the skies.
- **Aircraft Carriers & Nuclear Submarines (Naval)**: Ultimate naval power.

---

## **5. Technology Advancement**

- **Progression unlocks new units, buildings, and abilities.**
- **Tech Trees inspired by Civilization & Age of Empires**:
  - **Agriculture → Irrigation → Industrialized Farming**
  - **Bronze Working → Iron Working → Steelworking**
  - **Mathematics → Engineering → Robotics**
  - **Gunpowder → Rifles → Modern Firearms**
  - **Steam Power → Combustion Engines → Nuclear Power**
  - **Flight → Jet Propulsion → Space Exploration**
  - **Computing → AI & Cybernetics** (Future Expansion)

---

## **6. AI Players (Future Expansion)**

- AI-controlled civilizations expand, build, trade, and engage in diplomacy.
- Strategies include **military conquest, economic growth, and technological supremacy**.

---

## **7. Persistent Data (SQLite3) & Configuration**

- **Save/Load Game with SQLite3**.
- **Customizable settings stored in INI files**:
  - Map generation.
  - Unit stats.
  - Technological advancements.
  - Graphics & UI themes.

---

## **8. Graphics & Controls**

- **Mouse-driven UI** inspired by **Civilization VI & Age of Empires**.
- **Context-sensitive command menus**.
- **Placeholder images easily replaceable**.

---

## **Conclusion**

This design document ensures the Civilization-inspired strategy game is deeply engaging, customizable, and expandable with future updates.
