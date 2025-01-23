import zipfile
import os
import shutil

# Function to extract all XML files from zip files in a directory
def extract_xmls_from_zips(zip_folder):
    # Create a new folder named 'extracted_xmls'
    output_folder = os.path.join(zip_folder, 'extracted_xmls')
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the zip folder
    for root, _, files in os.walk(zip_folder):
        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        # Extract only XML files
                        for member in zip_ref.namelist():
                            if member.lower().endswith('.xml'):
                                # Ensure subdirectories are handled
                                member_path = os.path.join(output_folder, os.path.basename(member))
                                with open(member_path, 'wb') as output_file:
                                    output_file.write(zip_ref.read(member))
                except zipfile.BadZipFile:
                    print(f"Skipping invalid zip file: {zip_path}")

# Define the folder containing zip files
zip_folder = "File_path"

# Run the extraction function
extract_xmls_from_zips(zip_folder)

print(f"All XML files have been extracted to: {os.path.join(zip_folder, 'extracted_xmls')}")
