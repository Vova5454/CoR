import os


save_folder = os.environ.get("LOCALAPPDATA")
if not save_folder:
    save_folder = os.path.join(os.path.expanduser("~"), "AppData", "Local")
save_folder = os.path.join(save_folder, "CoR")
os.makedirs(save_folder, exist_ok=True)