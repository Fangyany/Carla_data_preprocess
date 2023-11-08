import carla
import time

actor_list = []
try:
    client = carla.Client('localhost', 2000)
    client.set_timeout(5.0)

    world = client.load_world('Town05')
    # world = client.load_world('Town02_Opt', carla.MapLayer.Buildings | carla.MapLayer.ParkedVehicles)
    # world.unload_map_layer(carla.MapLayer.Buildings)
    # world.unload_map_layer(carla.MapLayer.ParkedVehicles)

    # world.load_map_layer(carla.MapLayer.Buildings)


    blueprint_library = world.get_blueprint_library()
    vehicle_bp = blueprint_library.filter('model3')[0]
    spawn_point = carla.Transform(carla.Location(x=40, y=0, z=3), carla.Rotation(yaw=180))
    vehicle = world.spawn_actor(vehicle_bp, spawn_point)
    actor_list.append(vehicle)
    vehicle.apply_control(carla.VehicleControl(throttle=1.0, steer=0.0))
    time.sleep(5)

finally:
    for actor in actor_list:
        actor.destroy()
    print('All cleaned up!')