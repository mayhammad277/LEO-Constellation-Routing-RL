# LEO-Constellation-Routing-RL
Reinforcement learning (PPO,SAC) for optimal routing in LEO satellite constellations, with A* baseline and Walker-Delta orbit modeling.



# 🛰️ LEO Satellite Routing with PPO and A* Baseline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository implements  **reinforcement learning (PPO & SAC)** and **A* search** for finding optimal communication paths in Low Earth Orbit (LEO) satellite constellations. The environment models Earth geometry, line-of-sight constraints, and realistic Walker-Delta orbits with parameters (planes, altitude, inclination) for minimized routing latency and maximized Line-of-Sight (LOS) connectivity.

## 📖 Overview

🛰️ Overview
The project simulates a Delta Walker constellation and evaluates its performance by finding the shortest communication path between major global cities (e.g., Berlin to Cape Town, New York to Tokyo) using an A Routing algorithm*. 
The RL agent explores the trade-offs between the number of orbital planes, satellites per plane, altitude, and inclination to maximize network efficiency.✨ Key FeaturesCustom Gym Environment: SatelliteRoutingEnv manages the state of the constellation and calculates rewards based on routing performance.Delta Walker Constellation 




Generator: Mathematically generates 3D satellite positions in Earth-Centered Inertial (ECI) coordinates.Intelligent Routing: 
Implements A* pathfinding with Line-of-Sight (LOS) constraints, ensuring inter-satellite links (ISL) are not obstructed by the Earth.Multi-Algorithm Support: Integration with Stable-Baselines3 for training PPO and A2C agents. 

3D Visualization: Comprehensive plotting tools to visualize the constellation, ground stations, and the active routing path.🛠️ Installation: Bash pip install gym numpy matplotlib scipy stable-baselines3 skyfield shimmy
The code originates from research on autonomous routing policies for space networks.

## ✨ Features

- 🌍 **Realistic Earth Geometry**: ECI coordinate conversions, line-of-sight checks, and great-circle distances.
- 🛰️ **Walker-Delta Constellations**: Generate `P` orbital planes with `S` satellites each.
- 🧭 **A* Baseline Routing**: Guaranteed shortest path using satellite connectivity graph.
- 🤖 **PPO Learning**: Train an RL agent to make hop-by-hop routing decisions.
- 📊 **Visualization & Metrics**: Compare learned policies against optimal A* paths.




🚀 Environment Design State Space. The agent observes the current constellation configuration:P: Number of orbital planes.S: Number of satellites per plane. Altitude: Orbital height (km).Inclination: Orbital tilt (degrees).Action SpaceA continuous Box space allowing the agent to fine-tune:$\Delta P$, $\Delta S$, $\Delta \text{Altitude}$, and $\Delta \text{Inclination}$.Reward Function:

The reward is a multi-objective function that penalizes latency and hops while rewarding successful LOS connectivity. Latency Penalty: High total path distance reduces reward.Hop Penalty: Minimizing the number of satellites in a path is prioritized.LOS Bonus: Successfully maintaining Line-of-Sight links between nodes.📈 Usage: Training an Agent.


To train a PPO agent on the environment: Python from stable_baselines3 import PPO
from los_ppo_dw import SatelliteRoutingEnv

env = SatelliteRoutingEnv()
model = PPO("MlpPolicy", env, verbose=1, learning_rate=0.00001)
model.learn(total_timesteps=800000)
model.save("ppo_satellite_routing")





Evaluation & VisualizationThe environment provides a built-in method to visualize the learned constellation and the resulting route: Pythonplot_constellation_with_route(env.satellites_eci, path_indices, env.A, env.B)



🗺️ Routing LogicThe system uses the Great Circle Distance for heuristic estimation in the A* algorithm. It checks for Line-of-Sight (LOS) between any two nodes to ensure the Earth's limb does not interfere with the signal.






📊 ResultsThe project includes scripts to compare PPO and A2C performance, providing automated plots of:Episode Reward Over Time.Average Latency vs. Constellation Density.Hyperparameter tuning results for different learning rates and gammas.Developed for research in Satellite Network Optimization and Reinforcement Learning.


<img width="650" height="658" alt="download (9)" src="https://github.com/user-attachments/assets/e0216814-91d2-4e38-a63c-e5f1377f606b" />


 


<img width="650" height="658" alt="download (8)" src="https://github.com/user-attachments/assets/e85a4b3e-7a8c-4306-a0e7-4682d5e348ae" />




<img width="650" height="658" alt="download (5)" src="https://github.com/user-attachments/assets/246acd43-23bb-4a50-ad77-40863e954f6d" />



📚 Dependencies
Python ≥ 3.8
NumPy
SciPy
Matplotlib
Gym
PyTorch (for PPO)
Jupyter (for notebooks)

See requirements.txt for exact versions.



📖 Background & References
Walker Delta Constellation: J. G. Walker, "Circular Orbit Patterns", 1984.

*A Search**: Hart, Nilsson, Raphael, 1968.

PPO: Schulman et al., "Proximal Policy Optimization Algorithms", 2017.





🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request for improvements, bug fixes, or new features.

📄 License
This project is licensed under the MIT License – see the LICENSE file for details.

