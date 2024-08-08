import csv

# Function to process contact numbers from a block of text
def process_contacts(text):
    # Split the text into lines and remove any extra whitespace
    lines = text.strip().split('\n')
    return [line.strip() for line in lines if line.strip()]

# Collect a block of text input from the user
print("Paste all contact numbers in one go (each on a new line).")
print("Press Enter twice to end input.")
user_input = ""
while True:
    try:
        line = input()
        if line == "":
            break
        user_input += line + "\n"
    except EOFError:
        break

# Process the input to get a list of contacts
contacts = process_contacts(user_input)

# Path to save the CSV file
csv_file_path = 'contacts.csv'

# Write contacts to CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Contact Number'])  # Header row
    for contact in contacts:
        writer.writerow([contact])

print(f"Contacts have been exported to {csv_file_path}")
