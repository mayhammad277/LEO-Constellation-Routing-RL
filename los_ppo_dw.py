import gym
import numpy as np
import heapq
import matplotlib.pyplot as plt
from datetime import datetime, timezone
from stable_baselines3 import A2C,PPO

import gym
import numpy as np
from collections import defaultdict
import matplotlib.pyplot as plt
from gym import spaces
from scipy.spatial import distance
import random
import datetime
from datetime import timezone
from datetime import datetime


import numpy as np
from datetime import datetime, timezone
def satellite_coverage_check(r1, r2, Re=6371, threshold=500):
        r1, r2 = np.array(r1), np.array(r2)
        d = np.linalg.norm(r1 - r2)
        d_min = np.linalg.norm(np.cross(r1, r2)) / d
        return d_min > Re - threshold  # relxing the constraint

def is_on_earth(position, epsilon=10):
    R_E = 6371  #
    distance_from_center = np.linalg.norm(position)
    return abs(distance_from_center - R_E) <= epsilon
def julian_date(utc_time):
    """Convert UTC time to Julian Date."""
    unix_epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
    delta_seconds = (utc_time - unix_epoch).total_seconds()
    julian_date = 2440587.5 + delta_seconds / 86400.0
    return julian_date

def gst_from_julian(julian_date):
    """Compute Greenwich Sidereal Time from Julian Date."""
    T = (julian_date - 2451545.0) / 36525.0
    # Compute GST in degrees, modulo 360 to stay within bounds
    GST = 280.46061837 + 360.98564736629 * (julian_date - 2451545.0) + 0.000387933 * T**2 - (T**3 / 38710000.0)
    GST = GST % 360.0  # Ensure GST is within [0, 360] degrees
    return np.radians(GST)



def geodetic_to_eci(lat_deg, lon_deg, altitude_km=0, utc_time=None):

      if utc_time is None:
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

      lat = np.radians(lat_deg)
      lon = np.radians(lon_deg)

      R_E = 6378.137

    # Compute the Julian Date from the given UTC time
      jd = julian_date(utc_time)

      gst = gst_from_julian(jd)

      lon_eci = lon + gst  # Longitude in the inertial frame (ECI)

      x = (R_E + altitude_km) * np.cos(lat) * np.cos(lon_eci)
      y = (R_E + altitude_km) * np.cos(lat) * np.sin(lon_eci)
      z = (R_E + altitude_km) * np.sin(lat)

      return x, y, z



def is_on_earth(position, epsilon=1e-3):#to check wether the current node is a sallite or a ground point while routing
    R_E = 6371
    distance_from_center = np.linalg.norm(position)
    return abs(distance_from_center - R_E) >= epsilon

"""
# Add ground stations to the dictionary
satellites_eci_DW_a[0] = cape_town_pos  #)
satellites_eci_DW_a[1] = berlin_pos
satellites_eci_DW_a[2] = new_york_pos
satellites_eci_DW_a[3] = tokyo_pos
satellites_eci_DW_a[4] = sydney_pos
satellites_eci_DW_a[5] = moscow_pos
satellites_eci_DW_a[6] = wellington_pos
satellites_eci_DW_a[7] = alert_pos
satellites_eci_DW_a[8] = south_pole_pos
"""


def geodetic_to_eci(lat_deg, lon_deg, altitude_km=0, utc_time=None):

      if utc_time is None:
        utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

      lat = np.radians(lat_deg)
      lon = np.radians(lon_deg)

      R_E = 6378.137

    # Compute the Julian Date from the given UTC time
      jd = julian_date(utc_time)

      gst = gst_from_julian(jd)

      lon_eci = lon + gst  # Longitude in the inertial frame (ECI)

      x = (R_E + altitude_km) * np.cos(lat) * np.cos(lon_eci)
      y = (R_E + altitude_km) * np.cos(lat) * np.sin(lon_eci)
      z = (R_E + altitude_km) * np.sin(lat)

      return x, y, z


Re=6371
new_york_pos = geodetic_to_eci(40.7128, -74.0060, 0)
tokyo_pos = geodetic_to_eci(35.6762, 139.6503, 0)
sydney_pos = geodetic_to_eci(-33.8688, 151.2093, 0)
moscow_pos = geodetic_to_eci(55.7558, 37.6173, 0)
wellington_pos = geodetic_to_eci(-41.2865, 174.7762, 0)  #

alert_pos = geodetic_to_eci(82.5018, -62.3481, 0)  # Alert, Nunavut
south_pole_pos = geodetic_to_eci(-90, 0, 0)
berlin_pos = geodetic_to_eci(52.52, 13.405, 0)
cape_town_pos = geodetic_to_eci(-33.9249, 18.4241, 0)


start_end_pairs = [
    (berlin_pos,cape_town_pos),
    (new_york_pos, tokyo_pos),    #2,3
    (sydney_pos, moscow_pos), #4,5
    (berlin_pos, new_york_pos),#5,6
    (cape_town_pos, sydney_pos),#7,8
    (berlin_pos, wellington_pos),#9,10
    (alert_pos,south_pole_pos) #11,12
]











class SatelliteRoutingEnv(gym.Env):
    def __init__(self):
        super(SatelliteRoutingEnv, self).__init__()
        self.R_E = 6371
        self.num_satellites = 3
        self.state_space_var = 3  # lat, long, h
        self.P = 4
        self.inclination = 20
        self.S = 5
        self.altitude = 500
        self.state = self._generate_random_state()

        self.satellites_eci = self.delta_walker_constellation(int(self.state[0]),int(self.state[1]),int(self.state[2]),int(self.state[3]))


        self.current_time = datetime.utcnow()
        self.A = self.geodetic_to_eci(52.52, 13.41)  # berl
        self.B = self.geodetic_to_eci(-33.92, 18.42)  # Cape

        self.A_ecef=self.geodetic_to_ecef(52.52, 13.41)
        self.B_ecef=self.geodetic_to_ecef(-33.92, 18.42)
        self.elevation_threshold = 5.0  # deg
        self.start_end_pairs=start_end_pairs
       ##################################################################
        self.satellites_eci[1] = self.A
        self.satellites_eci[0] = self.B



        # act space: multi-disc actions
        self.delta_height_range = [-100, 0, 100]
        self.delta_angle_range = [-5, 0, 5]

        self.observation_space = spaces.Box(
            low=np.array([2, 2, 100, 10]),
            high=np.array([10, 12, 1000, 90]),
            dtype=np.float32
        )

        """
        self.action_space = spaces.MultiDiscrete([
            3,  # delta P: [-1, 0, 1]
            3,  # delta in S: [-1, 0, 1]
            3,  #  delta h: [-50, 0, 50]
            3   # delta inc: [-5, 0, 5] deg
        ])
        """
        self.action_space = spaces.Box(
        low=np.array([-3, -3, -50, -5]),
        high=np.array([3, 3, 50, 5]),
        dtype=np.float32
                        )
    
    
    
    def _generate_random_state(self):
        return np.array([
            self.np_random.uniform(self.P-2, self.P+2), # x,
            self.np_random.uniform(self.S-4, self.S+4),
            self.np_random.uniform(self.altitude-200, self.altitude+200),
            self.np_random.uniform(self.inclination-20, self.inclination+20)
        ], dtype=np.float32)

    def reset(self):

        self.state = self._generate_random_state()

        
        # reg the constellation with the new parameters
        self.satellites_eci = self.delta_walker_constellation(
            int(self.state[0]),  # P
            int(self.state[1]),  # S
            self.state[2],       # alt
            self.state[3]        # inc
        )
        self.satellites_eci[1] = self.B
        self.satellites_eci[0] = self.A
        
        return np.array(self.state, dtype=np.float32)
    def compute_reward(self, distance, num_visited, path_length,has_los_to_1,has_los):
        #  reward function
        #coverage = self.calculate_coverage(self.state[2], int(self.state[0] * self.state[1]))
        latency = distance / 299792.458
        los_1_penalty = 1 if not has_los_to_1 else 0
        los_2_penalty = 1 if not has_los else 0

        print("los_1_penalty",los_1_penalty) if  has_los_to_1 else None

        reward =  (latency * 10) - (path_length * 5) - (los_1_penalty * 10) - (los_2_penalty * 10)

        return reward
    def compute_reward2(self, state,distance, path):
        reward = 0.0
        terminated = False
        truncated = False
 
        valid_los_links = 0
        path_exists = len(path) > 0
        loop_penalty = 0

        if path_exists:
          print("yes",len(path))
        # LoS link ratio
          total_hops = len(path)-1
          for i in range(total_hops):
            sat1 = self.satellites_eci[path[i]]
            sat2 = self.satellites_eci[path[i+1]]
            try :
                self.satellite_coverage_check(sat1, sat2)
                valid_los_links += 1
                #chk for loops
                if i > 0 and path[i] == path[i-1]:
                 loop_penalty -= 2.0
            except:
                continue

          los_ratio = valid_los_links / total_hops if total_hops > 0 else 0

          distance_km = distance
          latency = distance_km / 299792.458 * 1000
          latency_reward = 1 - (latency / 300)  # 300ms max expected
          los_reward = valid_los_links / total_hops

          #reward = 5.0 * los_reward + 3.0 * latency_reward
          reward= 500* valid_los_links - 50*latency
          """
          reward += (
            5.0 * los_ratio +                  # max LoS link
            2.0 * (1 / (hop_count + 1e-6)) +   # min hops
            1.5 * (1 / (latency + 1e-6)) +     # min latency
            0.5 * (1 / (distance_km + 1e-6))   # min  dis
          )
          """


        else:
         print("No path ")
         #  penalty for no path
         reward -= 1000000000000.0
         return reward ,True ,False
        return reward, terminated, truncated
    
    def compute_reward23(self, state, distance, path):
      reward = 0.0
      terminated = False
      truncated = False      
    
      optimal_hops = 3  #path with 3 hops
      max_los_ratio = 1.0
      min_distance = 5_000.0   # min path lenth 

      distance_km = distance
      latency = distance_km / 299792.458 * 1000
      latency_reward = 1 - (latency / 300)  # 300ms max expected      
    
      has_win = (
        len(path) == optimal_hops and
        self.calculate_los_ratio(path) == max_los_ratio and
        distance <= min_distance
      )
    
      if has_win:
        terminated =True 
        truncated=False 
        return 100000.0 ,True,False # mx reward
    
      standard_reward = (
        500 * self.calculate_los_ratio(path) -
        0.05 * distance -
        50 * len(path)  # penalty per hop
        -50*latency
       )
      return standard_reward,True, truncated
    def compute_reward24(self, state, distance, path):
      reward = 0.0
      terminated = False
      truncated = False

      optimal_hops = 4          
      max_los_ratio = 1.0
      min_distance = 5000.0     #  min total path  

      distance_km = max(distance, 1e-6)   
      latency = distance_km / 299792.458 * 1000  

      safe_hops = max(len(path) - 1, 1)
      los_ratio = self.calculate_los_ratio(path)  
      if not np.isfinite(los_ratio):
        los_ratio = 0.0

      has_win = (
        len(path) == optimal_hops and
        abs(los_ratio - max_los_ratio) < 1e-5 and  # handle floating-point
        distance <= min_distance
        )

      if has_win:
        terminated = True
        truncated = False 
        return 100_000.0, terminated, truncated  # max reward

      standard_reward = (
        500.0 * los_ratio
        - 0.05 * distance_km
        - 50.0 * len(path)    # penalty per hop
        - 50.0 * latency      # penalty for high latency
      )

      # Cs
      std_reward = np.clip(standard_reward, -1e6, 1e6)
      if not np.isfinite(std_reward):
        std_reward = -1e6

      return std_reward, terminated, truncated       

    def calculate_los_ratio(self, path):
      valid_los = 0
      for i in range(len(path)-1):
        if self.satellite_coverage_check(self.satellites_eci[path[i]], self.satellites_eci[path[i+1]]):
            valid_los += 1
      return valid_los / (len(path)-1) if len(path) > 1 else 0

    def step(self, action):
        # apply  action to  DW parms

        delta_P, delta_S, delta_alt, delta_inc = action 

        #new_P = np.clip(self.state[0] + delta_P, 4, 10)
        #new_S = np.clip(self.state[1] + delta_S, 6, 12)
        #new_altitude = np.clip(self.state[2] + delta_alt * 50, 500, 1000)
        #new_inclination = np.clip(self.state[3] + delta_inc * 5, 60, 90)

        new_P=max(self.state[0] + delta_P,1)

        new_S=max(self.state[1] + delta_S,1)
        new_altitude=self.state[2] + delta_alt
        new_inclination=self.state[3] + delta_inc


        self.state = np.array([new_P, new_S, new_altitude, new_inclination], dtype=np.float32)
        #print("self.state in step",self.state)

        #  constellation with new params
        self.satellites_eci = self.delta_walker_constellation(
            int(new_P), int(new_S), new_altitude, new_inclination
        )
        #print(self.satellites_eci.keys())
        #print("self.satellites_eci in step",self.satellites_eci)
        #self.satellites_eci[0] = self.B

        #self.satellites_eci[1] = self.A
        #print("self.start_end_pairs",type(self.start_end_pairs))

        last_sat_index = max(self.satellites_eci.keys()) if self.satellites_eci else -1
        current_index = last_sat_index + 1

        for start_pos, end_pos in self.start_end_pairs:
          self.satellites_eci[current_index] = start_pos
          current_index += 1 # Increment for the next entry
    
          self.satellites_eci[current_index] = end_pos
          current_index += 1 # Increment for the next entry





        rand_point=np.random.randint(0,len(self.start_end_pairs))

        #random start and end----------------------------------
        (self.A,self.B)=self.start_end_pairs[rand_point] 




        distance, visited_sats, path = self.a_star_routing(self.A, self.B, self.satellites_eci)
        #print("distance in step",distance)

        #gs changes every step either a or b
        gs = self.B_ecef if np.random.rand() < 0.5 else self.A_ecef#


        #has_los_1=self.satellite_coverage_check_all(self.satellites_eci,self.A,path, Re=6371,threshold=500)
        #has_los_2=self.satellite_coverage_check_all(self.satellites_eci,self.B,path, Re=6371,threshold=500)

        #  reward
        #reward = self.compute_reward(distance, len(visited_sats), len(path),has_los_1,has_los_2)
        reward,terminated,truncated=self.compute_reward24(self.state,distance, path)
        print("reward in step",reward)

        terminated = False  #  termination
        return self.state, reward, terminated, {"distance": distance, "path_length": len(path)}



    def calculate_coverage(self, altitude, num_satellites):
        #  coverage  based on h and  # sats

        return 1 - np.exp(-num_satellites * altitude / (2 * (self.R_E + altitude)))

    def eci_to_lat_lon(self, eci_coords, R_E=6371):
        x, y, z = eci_coords
        r = np.sqrt(x**2 + y**2 + z**2)

        lat = np.arcsin(z / r)
        lat_deg = np.degrees(lat)

        lon = np.arctan2(y, x)
        lon_deg = np.degrees(lon)

        return lat_deg, lon_deg

    def delta_walker_constellation(self, P, S, altitude, inclination, R_E=6371):
        satellites = {}
        index = 0

        inclination_rad = np.radians(inclination)

        a = R_E + altitude

        delta_omega = 360 / P  # RAAN separation - planes
        delta_nu = 360 / S     # true anomaly separation - sats

        for plane in range(P):
            omega = plane * delta_omega  # RAAN curr plane
            for sat in range(S):
                nu = sat * delta_nu  # true anom

                x = a * (np.cos(np.radians(omega)) * np.cos(np.radians(nu)) -
                    np.sin(np.radians(omega)) * np.sin(np.radians(nu)) * np.cos(inclination_rad))
                y = a * (np.sin(np.radians(omega)) * np.cos(np.radians(nu)) +
                    np.cos(np.radians(omega)) * np.sin(np.radians(nu)) * np.cos(inclination_rad))
                z = a * (np.sin(np.radians(nu)) * np.sin(inclination_rad))
                satellites[index] = np.array([x, y, z])
                index += 1

        return satellites

    def a_star_routing(self, source, target, satellite_positions, R_E=6371.8):
        # A*
        position_to_index = {tuple(v): k for k, v in satellite_positions.items()}

        if tuple(source) not in position_to_index or tuple(target) not in position_to_index:
            raise ValueError("src or tgt position not in satellite_positions.")

        open_set = []
        heapq.heappush(open_set, (0, source))  # (f_cost, current_node)

        g_cost = {tuple(pos): float('inf') for pos in satellite_positions.values()}
        g_cost[tuple(source)] = 0

        came_from = {}
        visited_sats = set()

        def edge_cost(current, neighbor):
            return self.great_circle_distance(np.array(current), np.array(neighbor))

        def heuristic_cost_estimate(current, goal):
            return self.great_circle_distance(np.array(current), np.array(goal))

        def get_neighbors(current, satellite_positions):
            neighbors = []
            current_pos = np.array(current)
            for pos in satellite_positions.values():
                if self.satellite_coverage_check(current_pos, pos):
                    neighbors.append(tuple(pos))
            return neighbors

        def reconstruct_path(came_from, current):
            path = [current]
            while current in came_from:
                current = came_from[current]
                path.insert(0, current)
            hop_distances = [edge_cost(path[i], path[i + 1]) for i in range(len(path) - 1)]
            total_distance = sum(hop_distances)
            return [position_to_index[tuple(p)] for p in path], total_distance

        while open_set:
            _, current = heapq.heappop(open_set)
            visited_sats.add(position_to_index[tuple(current)])

            if np.array_equal(current, target):
                path_indices, distance = reconstruct_path(came_from, tuple(current))
                if distance > R_E:
                    print("Total distance is greater than Earth's radius: the path involves multiple hops.")
                return distance, list(visited_sats), path_indices

            for neighbor in get_neighbors(current, satellite_positions):
                if tuple(neighbor) in visited_sats:
                    continue
                tentative_g_cost = g_cost[tuple(current)] + edge_cost(current, neighbor)

                if tentative_g_cost < g_cost[tuple(neighbor)]:
                    g_cost[tuple(neighbor)] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic_cost_estimate(neighbor, target)
                    heapq.heappush(open_set, (f_cost, neighbor))
                    came_from[tuple(neighbor)] = tuple(current)

        return float('inf'), list(visited_sats), []  # No valid path

    def great_circle_distance(self, pos1, pos2, R_E=6371.8):
        #  great-circle  between  points
        lat1 = np.arcsin(pos1[2] / np.linalg.norm(pos1))
        lon1 = np.arctan2(pos1[1], pos1[0])
        lat2 = np.arcsin(pos2[2] / np.linalg.norm(pos2))
        lon2 = np.arctan2(pos2[1], pos2[0])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = np.sin(dlat / 2) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2) ** 2
        c = 2 * np.arcsin(np.sqrt(a))
        return R_E * c

    def satellite_coverage_check(self,r1, r2, Re=6371, threshold=500):
        r1, r2 = np.array(r1), np.array(r2)
        d = np.linalg.norm(r1 - r2)
        #print(r1,"r1",r2,"r2","d",d)
        d_min = np.linalg.norm(np.cross(r1, r2)) / d
        return d_min > Re - threshold  # relxing constraint

    def satellite_coverage_check_all(self,satellites_eci,gs,path, Re=6371,threshold=500):
      for idxs in path:
        sat_eci = satellites_eci[idxs]
        r1, r2 = np.array(sat_eci), np.array(gs)
        d = np.linalg.norm(r1 - r2)
        d_min = np.linalg.norm(np.cross(r1, r2)) / d
        return d_min > Re - threshold  # relxing constraint




    def geodetic_to_eci(self, lat_deg, lon_deg, altitude_km=0, utc_time=None):
        if utc_time is None:
            utc_time = datetime.utcnow().replace(tzinfo=timezone.utc)

        lat = np.radians(lat_deg)
        lon = np.radians(lon_deg)
        R_E = 6371.8

        jd = self.julian_date(utc_time)
        gst = self.gst_from_julian(jd)
        lon_eci = lon + gst  # long  (ECI)

        x = (R_E + altitude_km) * np.cos(lat) * np.cos(lon_eci)
        y = (R_E + altitude_km) * np.cos(lat) * np.sin(lon_eci)
        z = (R_E + altitude_km) * np.sin(lat)

        return x, y, z

    def julian_date(self, utc_time):

        unix_epoch = datetime(1970, 1, 1, 0, 0, 0, tzinfo=timezone.utc)
        delta_seconds = (utc_time - unix_epoch).total_seconds()
        return 2440587.5 + delta_seconds / 86400.0

    def gst_from_julian(self, julian_date):
        T = (julian_date - 2451545.0) / 36525.0
        GST = 280.46061837 + 360.98564736629 * (julian_date - 2451545.0) + 0.000387933 * T ** 2 - (T ** 3 / 38710000.0)
        GST = GST % 360.0  # Kn 0 to 360
        return np.radians(GST)
    def geodetic_to_ecef(self, lat_deg, lon_deg, alt_km=0):
        lat = np.radians(lat_deg)
        lon = np.radians(lon_deg)
        x = (self.R_E + alt_km) * np.cos(lat) * np.cos(lon)
        y = (self.R_E + alt_km) * np.cos(lat) * np.sin(lon)
        z = (self.R_E + alt_km) * np.sin(lat)
        return np.array([x, y, z])

    def gmst(self, dt):
        jd = (dt - datetime(2000, 1, 1, 12)).total_seconds() / 86400.0 + 2451545.0
        T = (jd - 2451545.0) / 36525
        gmst_deg = 280.46061837 + 360.98564736629 * (jd - 2451545) + \
                   0.000387933 * T**2 - (T**3) / 38710000
        return np.radians(gmst_deg % 360)

    def eci_to_ecef(self, r_eci, dt):

        theta = self.gmst(dt)
        rot = np.array([
            [np.cos(theta), np.sin(theta), 0],
            [-np.sin(theta), np.cos(theta), 0],
            [0, 0, 1]
        ])
        return rot @ r_eci

    def has_line_of_sight_to_gs(self, satellites_eci: dict, gs_ecef,dt: datetime) -> dict:

        #gs_ecef = self.A_ecef
        result = {}

        for sat_id, sat_eci in satellites_eci.items():
            sat_ecef = self.eci_to_ecef(sat_eci, dt)
            vec = sat_ecef - gs_ecef
            vec_norm = np.linalg.norm(vec)
            gs_norm = np.linalg.norm(gs_ecef)

            cos_theta = np.dot(vec, gs_ecef) / (vec_norm * gs_norm)
            cos_theta = np.clip(cos_theta, -1.0, 1.0)
            theta_rad = np.arccos(cos_theta)
            elevation_deg = np.degrees(np.pi / 2 - theta_rad)

            result[sat_id] = elevation_deg > self.elevation_threshold

        return result
    def has_line_of_sight_to_both_gs(self, satellites_eci: dict, dt: datetime) -> dict:

      result = {}

      for sat_id, sat_eci in satellites_eci.items():
        sat_ecef = self.eci_to_ecef(sat_eci, dt)

        #  LOS to gs  A
        vec_a = sat_ecef - self.A_ecef
        cos_theta_a = np.dot(vec_a, self.A_ecef) / (np.linalg.norm(vec_a) * np.linalg.norm(self.A_ecef))
        elevation_deg_a = np.degrees(np.pi / 2 - np.arccos(np.clip(cos_theta_a, -1.0, 1.0)))

        #  LOS to  gs B
        vec_b = sat_ecef - self.B_ecef
        cos_theta_b = np.dot(vec_b, self.B_ecef) / (np.linalg.norm(vec_b) * np.linalg.norm(self.B_ecef))
        elevation_deg_b = np.degrees(np.pi / 2 - np.arccos(np.clip(cos_theta_b, -1.0, 1.0)))

        #  LOS to both gss
        result[sat_id] = (elevation_deg_a > self.elevation_threshold) and (elevation_deg_b > self.elevation_threshold)

      return result



"""
epochs = 0
env = SatelliteRoutingEnv()
rewards = []
obs = env.reset()
print("Observation Shape:", obs.shape)

# ppo
model = PPO("MlpPolicy", env, learning_rate=0.00001, verbose=1,gamma=0.997)
model.learn(total_timesteps=800000)
model.save("ppo_satellite_routing")

# eval
done = False
while epochs < 800:
    action, _states = model.predict(obs)
    obs, reward, terminated, _ = env.step(action)
    rewards.append(reward)
    epochs += 1
    print(f"Action: {action}, Reward: {reward}")
mean_r = np.mean(rewards)

#
plt.figure(figsize=(10, 6)) ##

plt.plot(rewards, "g-o", label="Episode Reward", alpha=0.7)

plt.axhline(y=mean_r, color='r', linestyle='--', label=f'Mean Reward ({mean_r:.2f})')

plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("PPO Reward Over Time")
plt.legend() #
plt.grid(True) #
plt.show()
"""
# #######################
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_constellation_with_route(satellites_eci, path_indices, start,end,R_E=6371):

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    #  earth
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]
    x = R_E * np.cos(u) * np.sin(v)
    y = R_E * np.sin(u) * np.sin(v)
    z = R_E * np.cos(v)
    ax.plot_surface(x, y, z, color='blue', alpha=0.1)

    #  all sats
    for idx, pos in satellites_eci.items():
        if idx in path_indices:
            #  sats -- optimal route
            ax.scatter(pos[0], pos[1], pos[2], color='red', s=100, label='Optimal point' if idx == path_indices[0] else "")
        else:
            #  other sats
            ax.scatter(pos[0], pos[1], pos[2], color='gray', s=50, alpha=0.5)

    #  optimal route
    route_positions = [satellites_eci[idx] for idx in path_indices]
    route_x = [pos[0] for pos in route_positions]
    route_y = [pos[1] for pos in route_positions]
    route_z = [pos[2] for pos in route_positions]
    ax.plot(route_x, route_y, route_z, color='green', marker='o', markersize=8, label='Optimal Route')
    #------------------------berlin capetown
    ax.scatter(start[0],start[1],start[2], color='yellow',s=50 ,marker='*',  label='start')

    ax.scatter(end[0],end[1],end[2], color='black',s=50, marker='*', label='end ')

    # Add labels and legend
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title('Satellite Constellation with Optimal Route')
    plt.legend()
    plt.show()



def plot_satellite_constellation(satellite_positions):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [pos[0] for pos in satellite_positions.values()]
    y = [pos[1] for pos in satellite_positions.values()]
    z = [pos[2] for pos in satellite_positions.values()]

    ax.scatter(x, y, z, c='b', marker='o')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_title('Satellite Constellation')

    plt.show()



def plot_routing_paths(satellite_positions, path_indices):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = [pos[0] for pos in satellite_positions.values()]
    y = [pos[1] for pos in satellite_positions.values()]
    z = [pos[2] for pos in satellite_positions.values()]
    ax.scatter(x, y, z, c='b', marker='o')

    for i in range(len(path_indices) - 1):
        start = satellite_positions[path_indices[i]]
        end = satellite_positions[path_indices[i + 1]]
        ax.plot([start[0], end[0]], [start[1], end[1]], [start[2], end[2]], c='r')

    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_zlabel('Z Position')
    ax.set_title('Satellite Routing Paths')

    plt.show()


"""
model = PPO.load("ppo_satellite_routing")

epochs = 0
rewards = []
obs = env.reset()
while epochs < 20:  # eval  10 episodes
    action, _states = model.predict(obs)
    obs, reward, terminated, info = env.step(action)
    rewards.append(reward)
    epochs += 1
    print(f"Episode: {epochs}, Reward: {reward}, Path Length: {info['path_length']}, Distance: {info['distance']}")


    if epochs == 1:
        #plot_satellite_constellation(env.satellites_eci)
        distance, visited_sats, path_indices = env.a_star_routing(env.A, env.B, env.satellites_eci)
        #plot_routing_paths(env.satellites_eci, path_indices)

        plot_constellation_with_route(env.satellites_eci, path_indices, env.A,env.B,R_E=6371)
    if epochs == 10:
        #plot_satellite_constellation(env.satellites_eci)
        distance, visited_sats, path_indices = env.a_star_routing(env.A, env.B, env.satellites_eci)
        #plot_routing_paths(env.satellites_eci, path_indices)

        plot_constellation_with_route(env.satellites_eci, path_indices, env.A,env.B,R_E=6371)
mean_r = np.mean(rewards)

plt.figure(figsize=(10, 6)) 

plt.plot(rewards, "g-o", label="Episode Reward", alpha=0.7) 

plt.axhline(y=mean_r, color='r', linestyle='--', label=f'Mean Reward ({mean_r:.2f})')

plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("PPO Reward Over Time")
plt.legend() 
plt.grid(True) 
plt.show()

"""


if __name__ == "__main__":



  epochs = 0
  env = SatelliteRoutingEnv()
  rewards = []
  obs = env.reset()
  print("Observation Shape:", obs.shape)

# ppo
  model = PPO("MlpPolicy", env, learning_rate=0.00001, verbose=1,gamma=0.997)
  model.learn(total_timesteps=800000)
  model.save("ppo_satellite_routing")

# eval
  done = False
  while epochs < 800:
    action, _states = model.predict(obs)
    obs, reward, terminated, _ = env.step(action)
    rewards.append(reward)
    epochs += 1
    print(f"Action: {action}, Reward: {reward}")
  mean_r = np.mean(rewards)

#
  plt.figure(figsize=(10, 6)) ##

  plt.plot(rewards, "g-o", label="Episode Reward", alpha=0.7)

  plt.axhline(y=mean_r, color='r', linestyle='--', label=f'Mean Reward ({mean_r:.2f})')

  plt.xlabel("Episode")
  plt.ylabel("Reward")
  plt.title("PPO Reward Over Time")
  plt.legend() #
  plt.grid(True) #
  plt.show()





