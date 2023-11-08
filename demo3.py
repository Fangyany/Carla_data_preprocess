import carla
import time
import numpy as np
import cv2

actor_list = []


def img_process(image):
    img = np.array(image.raw_data)
    img = img.reshape((1080, 1920, 4))
    img = img[:, :, :3]
    cv2.imwrite("car.png", img)
    # cv2.imshow("", img)
    # cv2.waitKey(1)
    pass

def callback(event):
    print(event)


try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    world = client.load_world('Town01')

    map = world.get_map()

    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('model3')[0]
    spawn_point = carla.Transform(carla.Location(x=40, y=0, z=3), carla.Rotation(yaw=180))
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    actor_list.append(vehicle)

    # Find the blueprint of the sensor.
    blueprint = blueprint_library.find('sensor.camera.rgb')
    # Modify the attributes of the blueprint to set image resolution and field of view.
    blueprint.set_attribute('image_size_x', '1920')
    blueprint.set_attribute('image_size_y', '1080')
    blueprint.set_attribute('fov', '110')
    # Set the time in seconds between sensor captures
    blueprint.set_attribute('sensor_tick', '1.0')

    transform = carla.Transform(carla.Location(x=0.8, z=1.7))
    sensor = world.spawn_actor(blueprint, transform, attach_to=vehicle)
    actor_list.append(sensor)
    sensor.listen(lambda data: img_process(data))


    blueprint_collision = blueprint_library.find('sensor.other.collision')
    transform = carla.Transform(carla.Location(x=0.0, z=0.0))
    sensor_collision = world.spawn_actor(blueprint_collision, transform, attach_to=vehicle)
    actor_list.append(sensor_collision)
    sensor_collision.listen(callback)
 


    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    
    while True:
        # Nearest waypoint in the center of a Driving or Sidewalk lane.
        waypoint01 = map.get_waypoint(vehicle.get_location(),project_to_road=True, 
                                    lane_type=(carla.LaneType.Driving | carla.LaneType.Sidewalk))
        print("waypoint01", waypoint01)
        waypoints = waypoint01.next(2.0)
        waypoint02 = waypoints[0]
        print('waypoint02', waypoint02)

finally:
    for actor in actor_list:
        actor.destroy()
    print('All cleaned up!')