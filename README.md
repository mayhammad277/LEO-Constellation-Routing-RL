# LEO-Constellation-Routing-RL
Reinforcement learning (PPO,SAC) for optimal routing in LEO satellite constellations, with A* baseline and Walker-Delta orbit modeling.



# 🛰️ LEO Satellite Routing with PPO and A* Baseline

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

This repository implements and compares **reinforcement learning (PPO)** and **A* search** for finding optimal communication paths in Low Earth Orbit (LEO) satellite constellations. The environment models Earth geometry, line-of-sight constraints, and realistic Walker-Delta orbits.

## 📖 Overview

Efficient routing in mega-constellations (e.g., Starlink, OneWeb) is challenging due to dynamic topologies and Earth occlusion. This project provides:

- A **Gym-style environment** for satellite network routing.
- **A* heuristic search** as an optimal baseline (shortest-path with great-circle distances).
- **Proximal Policy Optimization (PPO)** agent that learns to select next-hop satellites to minimize total path delay.
- **Walker-Delta constellation generator** for customizable orbit configurations.

The code originates from research on autonomous routing policies for space networks.

## ✨ Features

- 🌍 **Realistic Earth Geometry**: ECI coordinate conversions, line-of-sight checks, and great-circle distances.
- 🛰️ **Walker-Delta Constellations**: Generate `P` orbital planes with `S` satellites each.
- 🧭 **A* Baseline Routing**: Guaranteed shortest path using satellite connectivity graph.
- 🤖 **PPO Learning**: Train an RL agent to make hop-by-hop routing decisions.
- 📊 **Visualization & Metrics**: Compare learned policies against optimal A* paths.

## 📁 Repository Structure
.
├── environment/

│ ├── satellite_env.py # Gym environment for routing
│ ├── constellation.py # Walker-Delta orbit generation
│ └── routing_utils.py # A, coverage checks, coordinate transforms

├── agents/
│ ├── ppo_agent.py # PPO implementation (actor-critic)
  └── a_star_baseline.py # A search wrapper

├── notebooks/
└── Los_reward_ppo_DW_5th_updates_gym_learning_initial_final_def.ipynb # Main experimentation notebook


├── train.py # Training script for PPO agent
├── eval.py # Evaluation and comparison
├── requirements.txt
└── README.md


## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mayhammad277/LEO-Constellation-Routing-RL
   cd LEO-Constellation-Routing-RL

   
Create and activate a virtual environment (optional):
bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
Install dependencies:


bash
pip install -r requirements.txt



🧪 Usage

Generate a Walker-Delta Constellation

   
from environment.constellation import delta_walker_constellation

satellites = delta_walker_constellation(P=12, S=24, altitude=550, inclination=53.0)


Train a PPO Agent


python train.py --config configs/ppo_config.yaml
4. Evaluate and Compare
bash
python eval.py --checkpoint runs/ppo_best.pth --episodes 100





📈 Results
Method	Avg. Path Length (km)	Avg. Hops	Success Rate
A* (optimal)	12,450	8.2	100%
PPO (trained)	12,820	8.5	98%
*Example results for a 300‑satellite Walker‑Delta constellation (P=12, S=25).*



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

