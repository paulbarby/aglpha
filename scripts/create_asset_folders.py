import os
import json
import glob
from pathlib import Path

def create_asset_folders():
    """
    Reads all JSON files in data/tiles directory and creates the necessary
    folders for the assets based on the paths in the JSON files.
    """
    # Get the project root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    # Path to the tiles JSON files
    tiles_dir = os.path.join(project_root, "data", "tiles")
    
    # Path to the assets directory
    assets_dir = os.path.join(project_root, "assets")
    
    print(f"Scanning JSON files in {tiles_dir}...")
    
    # List to store all unique directories that need to be created
    dirs_to_create = set()
    
    # Read each JSON file in the tiles directory
    for json_file in glob.glob(os.path.join(tiles_dir, "*.json")):
        print(f"Processing {os.path.basename(json_file)}")
        
        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
                
            # Add the base image directory
            if 'base_image' in data and data['base_image']:
                image_path = data['base_image']
                dir_path = os.path.dirname(os.path.join(project_root, image_path))
                dirs_to_create.add(dir_path)
                
            # Add directories for all variant images
            if 'variants' in data and isinstance(data['variants'], dict):
                for variant, image_path in data['variants'].items():
                    if image_path:
                        dir_path = os.path.dirname(os.path.join(project_root, image_path))
                        dirs_to_create.add(dir_path)
        
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON file {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")
    
    # Create all the directories
    print("\nCreating directories:")
    for dir_path in sorted(dirs_to_create):
        try:
            Path(dir_path).mkdir(parents=True, exist_ok=True)
            print(f"Created: {os.path.relpath(dir_path, project_root)}")
        except Exception as e:
            print(f"Error creating directory {dir_path}: {str(e)}")
    
    print("\nFolder creation complete!")
    print(f"Created {len(dirs_to_create)} directories for your tile assets.")

if __name__ == "__main__":
    create_asset_folders()
