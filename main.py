import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from data import fe
import pywintypes
from time import sleep
from win10toast import ToastNotifier
import stat

toast = ToastNotifier()
toast.show_toast("Folder Manager", "The process has been started", duration=8)
os.chdir("C:/Users/petar/python_projects/folder_manager")

downloads = 'C:/Users/petar/Downloads'
desktop = 'C:/Users/petar/Desktop'

def cleandir(path):   
    for file in os.listdir(path):
        movefile(file, path)

def movefile(file, path):
    if os.path.splitext(file)[1] != '':
        ext = os.path.splitext(file)[1].lower()
        for file_ext in fe:
            if ext in fe[file_ext]["ext"]:
                try:
                    os.rename(os.path.join(path, file), os.path.join(fe[file_ext]["path"], file))
                    print(f'{file} was moved to {os.path.join(fe[file_ext]["path"])}')
                except FileExistsError:
                    try:
                        os.remove(os.path.join(path, file))
                    except PermissionError:
                        os.chmod(os.path.join(path, file), stat.S_IWRITE)
                        os.remove(os.path.join(path, file))
                except FileNotFoundError:
                    pass

# cleandir(desktop)

def on_modified(event):
    if os.path.splitext(event.src_path)[1] not in [".crdownload", ".tmp"]:
        sleep(3)
        file = os.path.basename(event.src_path)
        dir = os.path.dirname(event.src_path)
        movefile(file, dir)

def on_created(event):
    file = os.path.basename(event.src_path)
    dir = os.path.dirname(event.src_path)
    print(f"{file} was created!")
    movefile(file, dir)

if __name__ == "__main__":

    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_created
    event_handler.on_modified = on_modified
    observer = Observer()
    observer.schedule(event_handler, downloads, recursive=False)
    observer.schedule(event_handler, desktop, recursive=False)
    observer.start()

    print("Watching Download and Desktop directories...")

    try:
        while observer.is_alive():
            observer.join(1)
    finally:
        observer.stop()
        observer.join()