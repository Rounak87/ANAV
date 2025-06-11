import time
from pymavlink import mavutil

# Parameter Categories based on ArduPilot Tuning Screen
PARAM_CATEGORIES = {
    "Rate Roll": ["ATC_RAT_RLL_P", "ATC_RAT_RLL_I", "ATC_RAT_RLL_D", "ATC_RAT_RLL_IMAX", "ATC_RAT_RLL_FLTE", "ATC_RAT_RLL_FLTD", "ATC_RAT_RLL_FLTT"],
    "Rate Pitch": ["ATC_RAT_PIT_P", "ATC_RAT_PIT_I", "ATC_RAT_PIT_D", "ATC_RAT_PIT_IMAX", "ATC_RAT_PIT_FLTE", "ATC_RAT_PIT_FLTD", "ATC_RAT_PIT_FLTT"],
    "Rate Yaw": ["ATC_RAT_YAW_P", "ATC_RAT_YAW_I", "ATC_RAT_YAW_D", "ATC_RAT_YAW_IMAX", "ATC_RAT_YAW_FLTE", "ATC_RAT_YAW_FLTD", "ATC_RAT_YAW_FLTT"],
    "Throttle Accel": ["THR_ACCEL_P", "THR_ACCEL_I", "THR_ACCEL_D", "THR_ACCEL_IMAX"],
    "Throttle Rate": ["THR_RATE_P"],  # May need to check the exact name in ArduPilot
    "Altitude Hold": ["AH_P"],  # Replace with the appropriate parameter names
    "Waypoint Navigation": ["WPNAV_SPEED", "WPNAV_RADIUS", "WPNAV_SPEED_UP", "WPNAV_SPEED_DN", "WPNAV_LOITERSPEED"], #check these params
    "Stabilize Roll": ["STB_RLL_P"],
    "Stabilize Pitch": ["STB_PIT_P"],
    "Stabilize Yaw": ["STB_YAW_P"],

    "Position XY": ["POS_XY_P", "POS_XY_TC"],
    "Velocity XY": ["VEL_XY_P", "VEL_XY_I", "VEL_XY_D", "VEL_XY_IMAX"],

    # Filters
    "Basic Filters": ["GYRO_FILTER", "ACCEL_FILTER"],
    "Static Notch Filter": ["FLTR_ENABLE", "FLTR_FREQ", "FLTR_BW", "FLTR_ATT"],
    "Harmonic Notch Filter": ["HNTCH_ENABLE", "HNTCH_MODE", "HNTCH_REF",
                              "HNTCH_FREQ", "HNTCH_BW", "HNTCH_ATT",
                              "HNTCH_HMNCS"],
}

PARAM_NAME_MAPPING = {
    "ATC_RAT_RLL_P": "Rate Roll: P Gain",
    "ATC_RAT_RLL_I": "Rate Roll: I Gain",
    "ATC_RAT_RLL_D": "Rate Roll: D Gain",
    "ATC_RAT_RLL_IMAX": "Rate Roll: IMAX",
    "ATC_RAT_RLL_FLTE": "Rate Roll: FLTE",
    "ATC_RAT_RLL_FLTD": "Rate Roll: FLTD",
    "ATC_RAT_RLL_FLTT": "Rate Roll: FLTT",

    "ATC_RAT_PIT_P": "Rate Pitch: P Gain",
    "ATC_RAT_PIT_I": "Rate Pitch: I Gain",
    "ATC_RAT_PIT_D": "Rate Pitch: D Gain",
    "ATC_RAT_PIT_IMAX": "Rate Pitch: IMAX",
    "ATC_RAT_PIT_FLTE": "Rate Pitch: FLTE",
    "ATC_RAT_PIT_FLTD": "Rate Pitch: FLTD",
    "ATC_RAT_PIT_FLTT": "Rate Pitch: FLTT",

    "ATC_RAT_YAW_P": "Rate Yaw: P Gain",
    "ATC_RAT_YAW_I": "Rate Yaw: I Gain",
    "ATC_RAT_YAW_D": "Rate Yaw: D Gain",
    "ATC_RAT_YAW_IMAX": "Rate Yaw: IMAX",
    "ATC_RAT_YAW_FLTE": "Rate Yaw: FLTE",
    "ATC_RAT_YAW_FLTD": "Rate Yaw: FLTD",
    "ATC_RAT_YAW_FLTT": "Rate Yaw: FLTT",

    "THR_ACCEL_P": "Throttle Accel: P Gain",
    "THR_ACCEL_I": "Throttle Accel: I Gain",
    "THR_ACCEL_D": "Throttle Accel: D Gain",
    "THR_ACCEL_IMAX": "Throttle Accel: IMAX",
     "THR_RATE_P": "Throttle Rate: P Gain",
    "AH_P": "Altitude Hold: P Gain",
    "WPNAV_SPEED": "Waypoint Navigation: Speed",
    "WPNAV_RADIUS": "Waypoint Navigation: Radius",
    "WPNAV_SPEED_UP": "Waypoint Navigation: Speed Up",
    "WPNAV_SPEED_DN": "Waypoint Navigation: Speed Dn",
    "WPNAV_LOITERSPEED": "Waypoint Navigation: Loiter Speed",

}
PARAM_NAME_MAPPING.update({
    # Stabilize Parameters
    "STB_RLL_P": "Stabilize Roll: P Gain",
    "STB_PIT_P": "Stabilize Pitch: P Gain",
    "STB_YAW_P": "Stabilize Yaw: P Gain",

    # Position XY
    "POS_XY_P":  "Position XY: P Gain",
    "POS_XY_TC":  "Position XY: Time Constant",

    # Velocity XY
    "VEL_XY_P":  "Velocity XY: P Gain",
    "VEL_XY_I":  "Velocity XY: I Gain",
    "VEL_XY_D":  "Velocity XY: D Gain",
    "VEL_XY_IMAX":  "Velocity XY: IMAX",

    # Basic Filters
    "GYRO_FILTER":  "Gyro Filter",
    "ACCEL_FILTER":  "Accel Filter",

    # Static Notch Filter
    'FLTR_ENABLE': 'Static Notch Filter Enable',
    'FLTR_FREQ': 'Static Notch Filter Frequency',
    'FLTR_BW': 'Static Notch Filter Bandwidth',
    'FLTR_ATT': 'Static Notch Filter Attenuation',

    # Harmonic Notch Filter
    'HNTCH_ENABLE': 'Harmonic Notch Filter Enable',
    'HNTCH_MODE': 'Harmonic Notch Filter Mode',
    'HNTCH_REF': 'Harmonic Notch Filter Reference',
    'HNTCH_FREQ': 'Harmonic Notch Filter Frequency',
    'HNTCH_BW': 'Harmonic Notch Filter Bandwidth',
    'HNTCH_ATT': 'Harmonic Notch Filter Attenuation',
    'HNTCH_HMNCS': 'Harmonic Notch Filter Harmonics'
})


def get_user_friendly_name(param_id):
   
    return PARAM_NAME_MAPPING.get(param_id, param_id)


connection = mavutil.mavlink_connection('COM6', baud=115200)


print("Waiting for heartbeat...")
connection.wait_heartbeat()
print("Heartbeat received!")


print("Requesting parameters...")
connection.mav.param_request_list_send(connection.target_system, connection.target_component)

parameters = {}


while True:
    message = connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
    if message is None:
        break  # No more parameters to receive

    param_id = message.param_id
    if isinstance(param_id, bytes):
        param_id = param_id.decode('utf-8').strip()

    param_value = message.param_value
    parameters[param_id] = param_value


categorized_params = {}
for category in PARAM_CATEGORIES:  # Loop through categories in the order you defined
    categorized_params[category] = {}
    for param_id in PARAM_CATEGORIES[category]:
        if param_id in parameters:
            categorized_params[category][param_id] = parameters[param_id]
            
output_file = 'categorized_ardupilot_parameters1.txt'
with open(output_file, 'w') as file:
    file.write("Parameters by Category:\n")
    for category, params in categorized_params.items():
        file.write(f"\n--- {category} ---\n")
        for param_id, param_value in params.items():
            user_friendly_name = get_user_friendly_name(param_id)
            file.write(f"{user_friendly_name}: {param_value}\n")

print(f"Categorized parameters saved to '{output_file}'.")