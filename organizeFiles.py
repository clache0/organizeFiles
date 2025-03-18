import os
import shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

def get_exif_datetime(file_path):
    """Extracts the 'Date Taken' from image metadata if available."""
    try:
        with Image.open(file_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if tag_name == "DateTimeOriginal":
                        return datetime.datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f"Skipping {file_path}: {e}")
    
    return None

def get_file_datetime(file_path):
    """Gets Date Taken from EXIF or falls back to file modification date."""
    dt = get_exif_datetime(file_path)
    if dt is None:
        timestamp = os.path.getmtime(file_path)
        dt = datetime.datetime.fromtimestamp(timestamp)
    return dt.year, dt.month, dt.day, dt.strftime('%H-%M-%S')

def organize_files_by_date(base_folder):
    if not os.path.isdir(base_folder):
        print("Invalid folder path.")
        return

    for root, _, files in os.walk(base_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Skip directories or hidden files
            if file.startswith('.'):
                continue
            
            year, month, day, time = get_file_datetime(file_path)
            
            # Create year and month folders
            year_folder = os.path.join(base_folder, str(year))
            month_folder = os.path.join(year_folder, f'{month:02d}')
            os.makedirs(month_folder, exist_ok=True)
            
            # Move file to organized folder
            new_file_path = os.path.join(month_folder, file)
            shutil.move(file_path, new_file_path)
            print(f'Moved {file} to {new_file_path}')

if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    organize_files_by_date(folder_path)
