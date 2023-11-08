import carla

def get_all_lane_ids(world_map):
    lane_ids = set()
    for waypoint in world_map.generate_waypoints(1.0):
        lane_id = waypoint.lane_id
        lane_ids.add(lane_id)
    return lane_ids

if __name__ == '__main':
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    world = client.load_world('Town05')
    world_map = world.get_map()

    all_lane_ids = get_all_lane_ids(world_map)

    for lane_id in all_lane_ids:
        print(f"Lane ID: {lane_id}")
