import os
import shutil
import glob
import argparse

def process_objaverse_data(input_dir, output_dir):
    """
    Filters and reorganizes directories from the Objaverse dataset.

    This script finds directories under the BASE_DIR that do NOT contain
    an 'info/tabletop_pose.json' file and moves them to a new, sequentially
    numbered directory structure within the OUTPUT_DIR.
    """
    # Base directory where the '000-009', '010-019', etc. folders are located.
    # Please adjust this path if your data is located elsewhere.
    base_dir = input_dir

    # Directory to place the newly organized data.
    output_dir = os.path.join(base_dir, "organized")
    
    # Counter for the new sequential directory names.
    count = 0

    # Check if the base directory exists.
    if not os.path.isdir(base_dir):
        print(f"Error: Base directory '{base_dir}' not found.")
        return

    # Create the output directory if it doesn't exist.
    os.makedirs(output_dir, exist_ok=True)
    print(f"Output will be saved to: {output_dir}")

    print("Scanning for directories to process...")

    # Construct the search pattern for the hash-named directories
    # e.g., objaverse/hf-objaverse-v1/processed_data/*/*
    search_pattern = os.path.join(base_dir, "*", "*")
    
    # Find all potential data directories
    for dir_path in glob.glob(search_pattern):
        # We only care about actual directories
        if not os.path.isdir(dir_path):
            continue
            
        # Define the path to the file we are checking for
        tabletop_pose_file = os.path.join(dir_path, "info", "tabletop_pose.json")

        # Check if the tabletop_pose.json file exists.
        if  os.path.exists(tabletop_pose_file):
            # Format the new directory name with leading zeros (e.g., 0000, 0001).
            new_name = f"{count:04d}"
            new_path = os.path.join(output_dir, new_name)

            print(f"Processing '{dir_path}' -> Moving to '{new_path}'")

            # Move and rename the directory.
            try:
                shutil.move(dir_path, new_path)
                # Increment the counter only on successful move.
                count += 1
            except Exception as e:
                print(f"Error moving '{dir_path}': {e}")
        else:
            print(f"Skipping '{dir_path}' (tabletop_pose.json notfound).")

    print(f"Processing complete. Total directories moved: {count}.")
    print(f"Organized data is in: {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Objaverse dataset.")
    parser.add_argument("--input_dir", type=str, default="objaverse/hf-objaverse-v1/processed_data",
                        help="Base directory where the processed data is located.")
    parser.add_argument("--output_dir", type=str, default="objaverse/hf-objaverse-v1/processed_data/organized",
                        help="Output directory for the organized data.")
    args = parser.parse_args()

    process_objaverse_data(args.input_dir, args.output_dir)
