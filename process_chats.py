import csv

def process_chats(file_path):
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Initialize variables
    participants = {}
    
    # Process each line
    for line in lines:
        line = line.strip()
        if ':' in line:
            name, message = line.split(':', 1)
            name = name.strip()
            message = message.strip()

            # Store message under participant's name
            if name in participants:
                participants[name].append(message)
            else:
                participants[name] = [message]

    # Prepare CSV output
    output_file = 'chats_output.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write header
        header = ['Participant'] + [f'Message {i+1}' for i in range(max(len(msgs) for msgs in participants.values()))]
        writer.writerow(header)
        
        # Write data rows
        for participant, messages in participants.items():
            row = [participant] + messages + [''] * (len(header) - len(messages) - 1)
            writer.writerow(row)

    print(f'Processed data written to {output_file}')

# Example usage:
file_path = 'editing.txt'  # Replace with your file path
process_chats(file_path)