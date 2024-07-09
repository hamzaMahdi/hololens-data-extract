import os
import json
import pandas as pd

# Define the directory containing the .state files
directory = os.getcwd()

# Prepare a list to store the data
data = []

# Define the labels of interest for measurements
labels_of_interest = [
    "Neck Diameter", "Height", "Width", "Volume",
    "Proximal Vessel Diameter", "Distal Vessel Diameter"
]

# Loop through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.state'):
        filepath = os.path.join(directory, filename)
        
        # Extract parts of the filename based on the given format
        parts = filename.split()
        participant = parts[0].split('-')[0][11:]  # Assuming 'Participant' is the prefix in the filename
        subtype = parts[0].split('-')[1]
        id_ = parts[1]
        date = parts[2]
        time = parts[3].replace('_', ':')[:-6]  # Removing file extension and converting time format

        # Read JSON content from file
        with open(filepath, 'r') as file:
            content = json.load(file)

        # Initialize a dictionary to store all data
        file_data = {
            'Participant': participant,
            'Subtype': subtype,
            'ID': id_,
            'Date': date,
            'Time': time
        }

        # Extract measurements from the JSON content
        measurements = content.get('inVolumeSaveData', {}).get('savedMeasurements', [])
        for measurement in measurements:
            if measurement['label'] in labels_of_interest:
                label = measurement['label'].replace(" ", "_")  # Convert spaces to underscores for column names
                measured_value = measurement['measuredValue']
                file_data[label] = measured_value

        # Handle projection data
        projections = content.get('workingProjectionSaveDatas', [])
        for i, proj in enumerate(projections, 1):
            prefix = f'Projection{i}_'
            file_data[prefix + 'PictureFileName'] = proj.get('pictureFileName', '')
            file_data[prefix + 'Angulation'] = proj.get('angluation', '').replace('°', '')
            file_data[prefix + 'Rotation'] = proj.get('rotation', '').replace('°', '')

        # Append the file data dictionary to the data list
        data.append(file_data)

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
csv_file_path = os.path.join(directory, 'output.csv')
df.to_csv(csv_file_path, index=False)

print(f"Data has been successfully written to {csv_file_path}")
