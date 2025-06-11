import time
import pandas as pd
from pymavlink import mavutil

# === STEP 1: Connect to Pixhawk and Get Parameters ===
print("Connecting to Pixhawk...")
connection = mavutil.mavlink_connection('COM7', baud=115200)
connection.wait_heartbeat()
print("Heartbeat received!")

# Request all parameters
print("Requesting parameters...")
connection.mav.param_request_list_send(connection.target_system, connection.target_component)

parameters = {}
while True:
    msg = connection.recv_match(type='PARAM_VALUE', blocking=True, timeout=5)
    if msg is None:
        break
    param_id = msg.param_id.decode('utf-8').strip() if isinstance(msg.param_id, bytes) else msg.param_id
    parameters[param_id] = msg.param_value
    print(f"{param_id}: {msg.param_value}")

# Save raw parameters to file
with open('ardupilot_parameters.txt', 'w') as f:
    for key, val in parameters.items():
        f.write(f"{key}: {val}\n")
print("\nParameters saved to 'ardupilot_parameters.txt'.")

# === STEP 2: Load Reference Excel and Compare ===
reference_file = "expected_log.xlsx"  # <-- replace with your actual Excel filename
df = pd.read_excel(reference_file)

for idx, row in df.iterrows():
    param_name = row['Param_Name']
    if param_name in parameters:
        actual_value = parameters[param_name]
        min_val = row['Min_value']
        max_val = row['Max value']
        set_val = row['Set']

        # Update Seen Value column in Excel
        df.at[idx, 'Seen Value'] = actual_value

        # If the parameter is out of bounds, update in the dictionary
        if not (min_val <= actual_value <= max_val):
            print(f"[!] {param_name} is out of range ({actual_value} not in [{min_val}, {max_val}]) → setting to {set_val}")
            parameters[param_name] = set_val

            # === STEP 3 (Optional): Upload to Pixhawk ===
            connection.mav.param_set_send(
                connection.target_system,
                connection.target_component,
                param_name.encode('utf-8'),
                float(set_val),
                mavutil.mavlink.MAV_PARAM_TYPE_REAL32
            )
            time.sleep(0.1)

# Save updated Excel
df.to_excel("validated_parameters.xlsx", index=False)
print("Excel with updated 'Seen Value' saved to 'validated_parameters.xlsx'.")

# Save updated parameter list
with open('updated_ardupilot_parameters.txt', 'w') as f:
    for key, val in parameters.items():
        f.write(f"{key}: {val}\n")
print("Updated parameters saved to 'updated_ardupilot_parameters.txt'.")