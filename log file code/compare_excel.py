import pandas as pd


param_file = r"D:/ANAV/log file code/ardupilot_parameters.txt"
param_dict = {}

with open(param_file, 'r') as file:
    for line in file:
        if ':' not in line:
            continue
        key, value = line.strip().split(':', 1)
        param_dict[key.strip()] = float(value.strip())

# Step 2: Load reference Excel
reference_file = r"D:/ANAV/log file code/expected log.xlsx"  # Replace with actual filename
df = pd.read_excel(reference_file)


for idx, row in df.iterrows():
    param_name = row['Param_Name']
    
    if param_name in param_dict:
        actual_value = param_dict[param_name]
        min_val = row['Min_value']
        max_val = row['Max value']
        set_val = row['Set']

        # Step 4: Set the seen value in the Excel sheet
        df.at[idx, 'Seen Value'] = actual_value

        # Step 5: If actual_value is out of bounds, update it in the param_dict
        if not (min_val <= actual_value <= max_val):
            param_dict[param_name] = set_val


df.to_excel("validated_parameters.xlsx", index=False)
print("Excel with updated 'Seen Value' saved.")

# Step 7: Save updated parameter dictionary back to text file
with open('updated_ardupilot_parameters.txt', 'w') as f:
    for key, val in param_dict.items():
        f.write(f"{key}: {val}\n")

print("Updated parameters saved to 'updated_ardupilot_parameters.txt'.")
