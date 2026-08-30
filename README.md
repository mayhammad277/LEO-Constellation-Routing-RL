# 🛰️ Daptive LEO Satellite Routing and Constellation Design for Maximum Achievable LOS and Coverage  .
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository implements **reinforcement learning** and **heuristic search** for finding optimal communication paths in Low Earth Orbit (LEO) satellite constellations. The environment models Earth geometry, line-of-sight constraints, and realistic Walker-Delta orbits with parameters (planes, altitude, inclination) for minimized routing latency and maximized Line-of-Sight (LOS) connectivity.

## 📖 Overview

The project simulates a Delta Walker constellation and evaluates its performance by finding the shortest communication path between major global cities (e.g., Berlin to Cape Town, New York to Tokyo) using a **graph search algorithm** with heuristic guidance. A reinforcement learning agent explores the trade-offs between the number of orbital planes, satellites per plane, altitude, and inclination to maximize network efficiency.

### ✨ Key Features

- **Custom Gym Environment**: `SatelliteRoutingEnv` manages the state of the constellation and calculates rewards based on routing performance.
- **Delta Walker Constellation Generator**: Mathematically generates 3D satellite positions in Earth-Centered Inertial (ECI) coordinates.
- **Intelligent Routing**: Implements a shortest-path search with Line-of-Sight (LOS) constraints, ensuring inter-satellite links (ISL) are not obstructed by the Earth.
- **Multi-Algorithm Support**: Integration with Stable-Baselines3 for training reinforcement learning agents (on-policy and off-policy).
- **3D Visualization**: Comprehensive plotting tools to visualize the constellation, ground stations, and the active routing path.

The code originates from research on autonomous routing policies for space networks.

## ✨ Features

- 🌍 **Realistic Earth Geometry**: ECI coordinate conversions, line-of-sight checks, and great-circle distances.
- 🛰️ **Walker-Delta Constellations**: Generate `P` orbital planes with `S` satellites each.
- 🧭 **Heuristic Search Baseline**: Guaranteed shortest path using a satellite connectivity graph and an admissible heuristic.
- 🤖 **Reinforcement Learning**: Train an agent to make hop-by-hop routing decisions.
- 📊 **Visualization & Metrics**: Compare learned policies against optimal paths obtained from the baseline.


<img width="650" height="658" alt="download (9)" src="https://github.com/user-attachments/assets/e0216814-91d2-4e38-a63c-e5f1377f606b" />


 <br><br> <br><br> <br><br>
 <br><br> <br><br> <br><br>







<img width="650" height="658" alt="download (8)" src="https://github.com/user-attachments/assets/e85a4b3e-7a8c-4306-a0e7-4682d5e348ae" />



 <br><br> <br><br> <br><br>
 <br><br> <br><br> <br><br>




Multi-Shell Solution :


<img width="650" height="658" alt="download (5)" src="https://github.com/user-attachments/assets/246acd43-23bb-4a50-ad77-40863e954f6d" />


 <br><br> <br><br> <br><br>
 <br><br> <br><br> <br><br>


## 🔗 Simulation Page

For a live simulation or more interactive exploration, visit the [GitHub Simulation Page](https://github.com/yourusername/yourrepo).

<!-- Replace the above link with your actual simulation page URL -->
## 📈 Usage

### Training an Agent

To train a reinforcement learning agent on the environment, use any policy gradient algorithm from a library like Stable-Baselines3. Below is a generic example (replace `YourAlgorithm` with the actual algorithm class):

```python
from stable_baselines3 import YourAlgorithm  # e.g., an on-policy or off-policy RL algorithm
from los_ppo_dw import SatelliteRoutingEnv

env = SatelliteRoutingEnv()
model = YourAlgorithm("MlpPolicy", env, verbose=1, learning_rate=0.00001)
model.learn(total_timesteps=800000)
model.save("rl_satellite_routing")




