#todo Imports
#----------------------
import os
from pathlib import Path
import shutil

#todo Global Variable
#----------------------
DEFAULT_PATH = r"D:\DOWNLOADS"

#todo Define Sorting rules
#----------------------
CATEGORIES = {
    '_Images': [".jpg", ".jpeg", ".png"],
    '_GIF': ['.gif'],
    '_Videos': ['.mp4', '.avi', '.mkv', '.mov'],
    '_Docs': ['.pdf', '.txt', '.docx'],
    '_ZIPs': ['.zip', '.rar', '.7z'],
    '_Installers': ['.exe', '.msi'],
    '_Code': ['.py', '.js', '.html', '.css', '.md'],
    '_Data': ['.csv', '.xlsx'],
    '_PPTs': ['.pptx'],
    "System": [".ini", ".dll"]
}


#todo Functions
#----------------------
def get_file_cat(filename, base_path):

    #* ignore sorting folders
    if filename.startswith('_'):
        return None

    #* folder
    filepath = os.path.join(base_path, filename)
    if os.path.isdir(filepath):
        return None

    #* file
    file_extension = Path(filename).suffix.lower()

    # looking for category
    for cats, list_keywords in CATEGORIES.items():
        if file_extension in list_keywords:
            return cats

    # fallback return
    return '_Others'



#todo Read all the files
#----------------------
def sort_downloads(target_path=DEFAULT_PATH, log_callback=print):
    """
    Sorts files in target_path.
    log_callback: function that accepts a string message. defaults to print.
    """
    
    if not os.path.exists(target_path):
        log_callback(f"[ERROR] Path not found: {target_path}")
        return

    all_files = os.listdir(target_path)
    folders = [f for f in all_files if os.path.isdir(os.path.join(target_path, f)) and not f.startswith('_')]
    files = [f for f in all_files if not os.path.isdir(os.path.join(target_path, f))]

    #*report
    log_callback('\n' + '-' * 55)
    log_callback("📂 Scanning Folder: " + target_path)
    log_callback(f"📁 Folders found : {len(folders)}")
    log_callback(f"📄 Files found   : {len(files)}")
    log_callback('-' * 55 + '\n')

    for file in os.listdir(target_path):

        #*get file category(based on rules)
        dir_name = get_file_cat(file, target_path)

        if dir_name:

            #todo create Sorting folders
            dir_filepath = os.path.join(target_path, dir_name)
            if not os.path.exists(dir_filepath):
                os.makedirs(dir_filepath)
                log_callback(f"[CREATE] Folder created: {dir_name}")

            #todo Define OLD/NEW Paths
            old_path = os.path.join(target_path, file)
            new_path = os.path.join(target_path, dir_name, file)

            #todo Move files
            try:
                shutil.move(old_path, new_path)
                log_callback(f"[MOVE] {file} → {dir_name}")

            except Exception as e:
                log_callback(f"[ERROR] Could not move {file}: {e}")
        
        elif dir_name == '_Others':
             # Only log this if specific verbosity/debug needed, or just let it slide to avoid noise
             # For now, we mimic original behavior which didn't explicitly blocking-print everything unless it was weird
             pass


#todo Main
if __name__ == '__main__':
    sort_downloads()
