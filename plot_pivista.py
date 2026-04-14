import pyvista as pv
import numpy as np

def visualize_path_3d(path, satellite_positions):

    if len(path) < 2:
        print("Path is too short to visualize.")
        return
    

    plotter = pv.Plotter()
    plotter = pv.Plotter(window_size=[1300, 900])
    

    R_E = 6371  # re
    earth = pv.Sphere(radius=R_E, center=(0, 0, 0))
    plotter.add_mesh(earth, color='blue', opacity=0.5, show_edges=False, label='Earth')    
    

    for idx, position in satellite_positions.items():
        plotter.add_mesh(pv.Sphere(radius=200, center=position), color="black", label=f"Satellite {idx}")
    
    # Add the path
    if len(path) < 1:
        resolution = len(path) - 1
    else:
        resolution = 1  # Minimum resolution
        line = pv.Line(path[0], path[1], resolution=resolution)
        plotter.add_mesh(line, color="red", line_width=4, label="Path")
        line = pv.Line(path[1], path[2], resolution=resolution)
        plotter.add_mesh(line, color="red", line_width=4, label="Path")
        line = pv.Line(path[2], path[-1], resolution=resolution)
        plotter.add_mesh(line, color="red", line_width=4, label="Path")

    # Set camera and display
    plotter.show_grid()
    plotter.show()



satellite_positions = {0: (3880.9488138870834, 19.388492360987545, 5061.47132572352), -1: (5269.713468711807, 489.35167063654364, -3559.6750541154174), 1: (3584.410916031797, 2570.950270421302, 5342.4053929687625), 2: (4243.869867206002, 5379.648068073109, 1023.7370290593066), 3: (-2757.13302931726, 6310.747419726175, 756.152599569856), 4: (4021.304286035935, -255.8438895488513, 5635.844039188675), 5: (971.1046592461447, 6299.012454525057, 2716.335790968715), 6: (-2939.902218412336, 5523.274765034484, 2974.809759779018), 7: (33.734506578301946, 922.0427160395394, -6866.424215239934), 8: (-6895.934950464513, -549.4662362908879, 378.48422015628825), 9: (2379.0224257996683, 6297.293422361468, 1638.1178654157452), 10: (-6414.177295552094, 516.1119573257138, 2567.302155862929), 11: (1811.9991236890535, -6626.843457274395, 894.8112981509761), 12: (5623.361535121263, 3409.7023197951135, -2179.636994196845), 13: (-2115.1316097560843, -5704.4521121894295, 3314.2912762636297), 14: (5572.49108869816, -1753.5251474024585, 3724.456324697039), 15: (1146.7656686681848, -3408.575219028432, 5921.623575351467), 16: (6024.240776255638, -123.82166355243933, 3419.3966655103022), 17: (110.80667326226622, 1019.0980734155439, 6851.87881450703), 18: (-972.8057398482969, -4498.125683929464, 5178.764004553722)}

path = [satellite_positions[0], satellite_positions[16], satellite_positions[12],satellite_positions[16]]
visualize_path_3d(path, satellite_positions)
