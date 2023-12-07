
import os

def split_file(input_file, output_prefix, max_events_per_file, output_folder):
    event_count = 0
    file_count = 1
    current_output = None

    def format_file_number(number):
        return f"_{number:04d}"

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with open(input_file, 'r') as infile:
        for line in infile:
            if line.startswith("EVENT"):
                if event_count >= max_events_per_file:
                    current_output.close()
                    file_count += 1
                    event_count = 0
                if event_count == 0:
                    formatted_file_number = format_file_number(file_count)
                    current_output = open(os.path.join(output_folder, f"{output_prefix}{formatted_file_number}.out"), 'w')
            if current_output is not None:
                current_output.write(line)
                if line.startswith("EVENT"):
                    event_count += 1
        if current_output is not None:
            current_output.close()

# Usage
input_file = 'test.tx'  # Replace with your large file name
output_prefix = 'slight_FeedDownY2S'  # Prefix for the output files
max_events_per_file = 1000  # Maximum number of events per smaller file
output_folder = 'splitFiles'  # Name of the output folder

split_file(input_file, output_prefix, max_events_per_file, output_folder)
