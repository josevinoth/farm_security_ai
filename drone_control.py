from tellopy import Tello
import time

def move_to_coordinate(drone, x, y, z):
       # Set the coordinate target
    target_x = drone.get_pose().x + x
    target_y = drone.get_pose().y + y
    target_z = drone.get_pose().z + z

    # Move to the target location
    drone.go_xyz_speed(target_x, target_y, target_z, 30)

# Create a Tello object
tello = Tello()

try:
    # Connect to the drone
    tello.connect()

    # Takeoff
    tello.takeoff()

    # Move to the coordinate location (for example, move forward by 50 cm)
    move_to_coordinate(tello, 0, 50, 0)

    # Land
    tello.land()

except Exception as e:
    print(f"Error: {e}")

finally:
    # Disconnect from the drone
    tello.disconnect()