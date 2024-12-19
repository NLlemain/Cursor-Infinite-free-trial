import os
import shutil
import ctypes

def secure_delete(file_path, passes=3):
    try:
        long_path = f"\\\\?\\{file_path}"
        if os.path.isfile(long_path):
            with open(long_path, 'ba+', buffering=0) as f:
                length = f.tell()
                for _ in range(passes):
                    f.seek(0)
                    f.write(os.urandom(length))
            os.remove(long_path)
            print(f"Securely deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")

def delete_directory(directory_path):
    try:
        long_path = f"\\\\?\\{directory_path}"
        if os.path.exists(long_path):
            shutil.rmtree(long_path)
            print(f"Deleted directory: {directory_path}")
    except Exception as e:
        print(f"Error deleting {directory_path}: {e}")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def wipe_cursor_traces():
    cursor_paths = [
        os.path.expandvars(r"%APPDATA%\\Cursor"),
        os.path.expandvars(r"%LOCALAPPDATA%\\Programs\\Cursor"),
        os.path.expandvars(r"%LOCALAPPDATA%\\Cursor"),
        os.path.expandvars(r"%TEMP%\\Cursor"),
        os.path.expandvars(r"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Cursor")
    ]

    for path in cursor_paths:
        if os.path.isdir(path):
            delete_directory(path)
        elif os.path.isfile(path):
            secure_delete(path)

def main():
    if not is_admin():
        print("This script requires administrative privileges to run.")
        return

    print("Wiping Cursor app traces...")
    wipe_cursor_traces()
    print("Done.")

if __name__ == "__main__":
    main()
