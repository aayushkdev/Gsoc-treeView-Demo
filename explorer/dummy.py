import random
import string
import json

def generate_random_string(length=8):
    """Generate a random string of a given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_file_tree(depth=1, max_children=500, num_files=100000):
    """Generate a random file tree structure."""
    tree = {}
    file_count = 0

    def add_folder(path, current_depth):
        nonlocal file_count
        if current_depth > depth or file_count >= num_files:
            return

        folder_name = generate_random_string(8)
        # Use the folder name directly as the key in the parent folder dictionary
        folder_path = folder_name
        folder = {}  # This will hold files and subfolders for this folder

        # Add files to the folder
        num_files_in_folder = random.randint(1, max_children)
        for _ in range(num_files_in_folder):
            if file_count >= num_files:
                break
            file_name = generate_random_string(8) + ".txt"
            folder[file_name] = None
            file_count += 1
        
        # Add subfolders to the folder
        num_subfolders = random.randint(1, max_children)
        for _ in range(num_subfolders):
            if file_count >= num_files:
                break
            add_folder(folder_path + "/" + generate_random_string(8), current_depth + 1)

        # Assign the generated folder (which contains files and subfolders) to the parent folder
        if folder:
            tree[folder_path] = folder

    # Start with the root folder
    add_folder("", 0)
    return tree

def generate_dummy_data(num_entries=10000):
    """Generate dummy file data in the required format."""
    return json.dumps(generate_file_tree(num_files=num_entries), indent=4)

# Generate 10,000 dummy entries
dummy_data = generate_dummy_data(num_entries=100000)

# Save the data to a JSON file
with open('dummy_data.json', 'w') as f:
    f.write(dummy_data)

print("Dummy data generated and saved to 'dummy_data.json'")
