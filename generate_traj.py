import carla
import random
import csv
import time
import os

def record_vehicle_trajectories(world, vehicle_blueprints, output_dir, duration, map_name):
    output_dir = os.path.join(output_dir, f'{map_name}_duration_{duration}')
    os.makedirs(output_dir, exist_ok=True)

    spawn_points = world.get_map().get_spawn_points()
    vehicles = []

    for _ in range(100):
        blueprint = random.choice(vehicle_blueprints)
        spawn_point = random.choice(spawn_points)
        vehicle = world.try_spawn_actor(blueprint, spawn_point)

        if vehicle is not None:
            vehicle.set_autopilot(True)
            vehicles.append(vehicle)

    trajectories = {vehicle.id: [] for vehicle in vehicles}

    timestamp = 0  # 添加时间戳

    while timestamp <= duration:
        for vehicle in vehicles:
            location = vehicle.get_location()
            vehicle_id = vehicle.id
            x, y = location.x, location.y
            frame = carla.Timestamp.frame
            trajectories[vehicle_id].append((vehicle_id, frame, x, y))

        world.tick()
        time.sleep(1)
        timestamp += 1

    # 存储轨迹数据
    for vehicle_id, trajectory in trajectories.items():
        filename = os.path.join(output_dir, f'vehicle_{vehicle_id}_trajectory.csv')
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(trajectory)

if __name__ == '__main__':
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(5.0)

        record_duration = 60
        map_name = 'Town05'

        world = client.load_world(map_name)
        vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')
        output_dir = 'trajectories'
        record_vehicle_trajectories(world, vehicle_blueprints, output_dir, record_duration, map_name)

    finally:
        pass
