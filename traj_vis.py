import carla
import random
import csv
import time
import os
import matplotlib.pyplot as plt

# 地图中心线坐标列表
map_center_line_x = []
map_center_line_y = []

# 地图边界线坐标列表
map_boundaries_x = []
map_boundaries_y = []

def get_map_center_line(world_map, map_center_line_x, map_center_line_y):
    for waypoint in world_map.generate_waypoints(1.0):
        if waypoint.lane_type == carla.LaneType.Driving:
            x = waypoint.transform.location.x
            y = waypoint.transform.location.y
            map_center_line_x.append(x)
            map_center_line_y.append(y)

def get_map_boundaries(world_map, map_boundaries_x, map_boundaries_y):
    for waypoint in world_map.generate_waypoints(1.0):
        x = waypoint.transform.location.x
        y = waypoint.transform.location.y
        map_boundaries_x.append(x)
        map_boundaries_y.append(y)

try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    map_name = 'Town05'
    record_duration = 60  # 保存轨迹持续时间

    world = client.load_world(map_name)
    world_map = world.get_map()

    get_map_center_line(world_map, map_center_line_x, map_center_line_y)
    get_map_boundaries(world_map, map_boundaries_x, map_boundaries_y)

    plt.figure(figsize=(10, 10))


    # plt.scatter(map_center_line_x, map_center_line_y, color='black', s=5, label='Map Center Line')
    plt.scatter(map_boundaries_x, map_boundaries_y, color='lightgray', s=5, label='Map Boundaries')

    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    trajectories_dir = f'trajectories/{map_name}_duration_{record_duration}'  # 更新轨迹文件夹名
    if not os.path.exists(trajectories_dir):
        print("Trajectories directory not found.")
        exit()

    trajectory_files = [file for file in os.listdir(trajectories_dir) if file.endswith('.csv')]
    # traj_all = []
    for i, trajectory_file in enumerate(trajectory_files):
        x = []
        y = []
        with open(os.path.join(trajectories_dir, trajectory_file), 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                x_val = float(row[0])
                y_val = float(row[1])
                if x_val != 0.0 and y_val != 0.0:  # 跳过0值
                    x.append(x_val)
                    y.append(y_val)
            if x and y:  # 只有 x 和 y 非空才绘制
                color = colors[i % len(colors)]  # 获取下一个颜色
                plt.plot(x, y, label=f'Trajectory {i}', c=color)
                # traj_all.append((x, y))

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axis('equal')
    plt.title(f'Carla Map {map_name} and Trajectories ({record_duration} seconds)')
    plt.grid(True)


    # output_filename = f'figure/carla_visualization_{map_name}_{record_duration}.png'
    # plt.savefig(output_filename, format='png')
    # print(f'Image saved as {output_filename}')



    # save trajectories
    # import pickle

    # traj_all_output_filename = f'traj_all_{map_name}_duration_{record_duration}.pkl'
    # with open(traj_all_output_filename, 'wb') as file:
    #     pickle.dump(traj_all, file)

    # with open(output_filename, 'rb') as file:
    #     loaded_traj_all = pickle.load(file)


except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pass
