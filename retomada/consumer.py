import os
import datetime
import re

def get_folders_with_date_format(directory):
    folder_paths = []
    for root, directories, files in os.walk(directory):
        for directory in directories:
            # Verifica se o nome da pasta corresponde ao formato AAAA-MM-DD
            if re.match(r"\d{4}-\d{2}-\d{2}$", directory):
                folder_path = os.path.join(root, directory)
                folder_paths.append(folder_path)
    return folder_paths

if __name__ == "__main__":
    folder_paths = get_folders_with_date_format(PATH_DIR)
    print("Pastas no formato AAAA-MM-DD:")
    for folder_path in folder_paths:
        print(folder_path)
