#todo Imports
#----------------------
import os
from pathlib import Path
import shutil


#todo Global Variable
#----------------------
PATH_DOWNLOADS = r"D:\DOWNLOADS"  # dev local
# PATH_DOWNLOADS =Path.home()/'DOWNLOADS'


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
def get_file_cat(filename):

    #* ignore sorting folders
    if filename.startswith('_'):
        return None

    #* folder
    filepath = os.path.join(PATH_DOWNLOADS, filename)
    if os.path.isdir(filepath):
        return None

    #* file (FIXED: use filename instead of file)
    file_extension = Path(filename).suffix.lower()

    # looking for category
    for cats, list_keywords in CATEGORIES.items():
        if file_extension in list_keywords:
            return cats

    # nicer output
    if file_extension == "":
        print(f"[INFO] No extension → {filename} assigned to _Others")
    else:
        print(f"[INFO] Unsupported extension {file_extension} → {filename} assigned to _Others")

    return '_Others'



#todo Read all the files
#----------------------
def sort_downloads():

    all_files = os.listdir(PATH_DOWNLOADS)
    folders = [f for f in all_files if os.path.isdir(os.path.join(PATH_DOWNLOADS, f)) and not f.startswith('_')]
    files = [f for f in all_files if not os.path.isdir(os.path.join(PATH_DOWNLOADS, f))]

    #*report to console
    print('\n' + '-' * 55)
    print("📂 Scanning Downloads Folder...")
    print(f"📁 Folders found : {len(folders)}")
    print(f"📄 Files found   : {len(files)}")
    print('-' * 55 + '\n')

    for file in os.listdir(PATH_DOWNLOADS):

        #*get file category(based on rules)
        dir_name = get_file_cat(file)
        # print(f"[CHECK] {file} → {dir_name}")

        if dir_name:

            #todo create Sorting folders
            dir_filepath = os.path.join(PATH_DOWNLOADS, dir_name)
            if not os.path.exists(dir_filepath):
                os.makedirs(dir_filepath)
                print(f"[CREATE] Folder created: {dir_name}")

            #todo Define OLD/NEW Paths
            old_path = os.path.join(PATH_DOWNLOADS, file)
            new_path = os.path.join(PATH_DOWNLOADS, dir_name, file)

            #todo Move files
            try:
                shutil.move(old_path, new_path)
                print(f"[MOVE] {file} → {dir_name}\n")

            except Exception as e:
                print(f"[ERROR] Could not move {file}: {e}\n")



#todo Main
if __name__ == '__main__':
    sort_downloads()
