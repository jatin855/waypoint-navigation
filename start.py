from dronekit import connect, VehicleMode, LocationGlobalRelative
import time
import math

# ---------------------------
# Connect to Vehicle (SITL)
# ---------------------------
print("Connecting to vehicle...")
vehicle = connect('udp:127.0.0.1:1451', wait_ready=True)

# ---------------------------
# Arm and takeoff function
# ---------------------------
def arm_and_takeoff(target_altitude):
    print("Arming motors...")
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialize...")
        time.sleep(1)

    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        time.sleep(1)

    print(f"Taking off to {target_altitude} meters")
    vehicle.simple_takeoff(target_altitude)

    # Wait until the vehicle reaches the target altitude
    while True:
        alt = vehicle.location.global_relative_frame.alt
        print(f" Altitude: {alt:.1f} m")
        if alt >= target_altitude * 0.95:
            print("Reached target altitude")
            break
        time.sleep(1)

# ---------------------------
# Function to offset location by meters
# ---------------------------
def get_location_offset_meters(original_location, dNorth, dEast, alt):
    earth_radius = 6378137.0  # meters
    dLat = dNorth / earth_radius
    dLon = dEast / (earth_radius * math.cos(math.pi * original_location.lat / 180))

    newlat = original_location.lat + (dLat * 180 / math.pi)
    newlon = original_location.lon + (dLon * 180 / math.pi)
    return LocationGlobalRelative(newlat, newlon, alt)

# ---------------------------
# Fly to a waypoint function
# ---------------------------
def fly_to(dNorth, dEast, alt, sleep_time=20):
    target_location = get_location_offset_meters(vehicle.location.global_relative_frame, dNorth, dEast, alt)
    vehicle.simple_goto(target_location)
    print(f"Flying to N:{dNorth} E:{dEast} Alt:{alt}")
    time.sleep(sleep_time)  # wait to reach

# ---------------------------
# Mission Execution
# ---------------------------

# 1. Takeoff to 10 m
arm_and_takeoff(10)

# Save home location
home_location = vehicle.location.global_relative_frame

# 2. Fly 100 m North
fly_to(50, 0, 10, sleep_time=30)

# 3. Fly 100 m East
fly_to(0, 50, 10, sleep_time=30)

# 4. Return to Home
print("Returning to Launch...")
vehicle.mode = VehicleMode("RTL")

# Wait until landed
while vehicle.armed:
    print(f" Altitude: {vehicle.location.global_relative_frame.alt:.1f} m")
    time.sleep(1)

print("Landed and disarmed")
vehicle.close()
