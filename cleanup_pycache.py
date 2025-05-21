import os
import shutil

def delete_pycache_folders(root_dir):
    deleted = 0
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if "__pycache__" in dirnames:
            pycache_path = os.path.join(dirpath, "__pycache__")
            shutil.rmtree(pycache_path)
            print(f"Deleted: {pycache_path}")
            deleted += 1
    if deleted == 0:
        print("No __pycache__ directories found.")
    else:
        print(f"Deleted {deleted} __pycache__ directories.")

if __name__ == "__main__":
    delete_pycache_folders(os.getcwd())



# python cleanup_pycache.py

# Test

# pytest test_folder/
# python cleanup_pycache.py
