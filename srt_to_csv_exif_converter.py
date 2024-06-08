import re
import csv

# Define the input and output file paths
input_file = 'DJI_20231125134955_0002_D.SRT'
output_file = 'output.csv'

# Open the input file
with open(input_file, 'r') as file:
    lines = file.readlines()

# Initialize a list to hold the extracted data
data = []

# Define a refined regular expression to extract the needed information
pattern = re.compile(
    r'FrameCnt: (\d+), DiffTime: \d+ms\n(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\n\[.*?\[latitude: ([\d.]+)\] \[longitude: ([\d.]+)\] \[rel_alt: ([\d.]+)'
)

# Variable to accumulate lines of each subtitle entry
current_entry = []

# Process the file line by line
for line in lines:
    if line.strip() == '':
        # Join the accumulated lines and search with the regex
        entry = '\n'.join(current_entry)
        print(f'Processing entry: {entry}')  # Debugging: print the entry being processed
        match = pattern.search(entry)
        if match:
            frame_nb = f"frame_{int(match.group(1)):04d}"
            time = match.group(2)
            latitude = match.group(3)
            longitude = match.group(4)
            altitude = match.group(5)
            # Append the extracted data to the list
            data.append([frame_nb, longitude, latitude, altitude, time])
            print(f'Match found: {match.groups()}')  # Debugging: print matched groups
        else:
            print(f'No match found for entry: {entry}')  # Debugging: indicate no match was found
        # Reset the current entry accumulator
        current_entry = []
    else:
        # Add line to the current entry accumulator
        current_entry.append(line.strip())

# Handle any remaining entry after the loop
if current_entry:
    entry = '\n'.join(current_entry)
    print(f'Processing final entry: {entry}')  # Debugging: print the final entry being processed
    match = pattern.search(entry)
    if match:
        frame_nb = f"frame_{int(match.group(1)):04d}"
        time = match.group(2)
        latitude = match.group(3)
        longitude = match.group(4)
        altitude = match.group(5)
        # Append the extracted data to the list
        data.append([frame_nb, longitude, latitude, altitude, time])
        print(f'Match found: {match.groups()}')  # Debugging: print matched groups
    else:
        print(f'No match found for final entry: {entry}')  # Debugging: indicate no match was found

# Write the data to a CSV file
with open(output_file, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header
    csvwriter.writerow(['name(frame_nb)', 'long(longitude)', 'lat(latitude)', 'H (altitude)', 'time'])
    # Write the data rows
    csvwriter.writerows(data)

print(f'Data has been extracted and saved to {output_file}')

# Debugging: Print the data to check
for row in data:
    print(row)
