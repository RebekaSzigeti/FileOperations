import os
import shutil
import json
import logging

#when you group the folders, these should not end up in the FOLDERS named folder
directories = {"HTML", "IMAGES", "VIDEOS", "DOCUMENTS","ARCHIVES", "AUDIO", "PLAINTEXT", "PDF", "PYTHON", "EXE", "OTHER", "FOLDERS" }


class FileOrganizer:
    def __init__(self, path, configFile, dry_run=False, verbose=False):
        self.path = path
        self.configFile = configFile
        self.directories = set()
        self.dry_run = dry_run
        self.items_moved = 0
        self.folders_created = 0
        self.verbose = verbose
        self.error_count = 0

        logging.info(
            f"Organize started | Path: {self.path} | "
            f"Config: {self.configFile} | "
            f"Dry run: {self.dry_run}"
        )

    def organize(self):
         logging.debug("Starting organization process")
         for item in os.listdir(self.path):
            found = False
            src_path = os.path.join(self.path, item)

            if os.path.isfile(os.path.join(self.path, item)):
                _, ext = os.path.splitext(item)
                ext = ext.lower()
                if ext in self.extMatch:
                    folder = self.extMatch[ext]

                    if folder not in self.directories:
                       self.create_folder(folder)

                    dest_path = os.path.join(self.path, folder, item)
                    dest_path = self.get_unique_path(dest_path)
                    self.move_item(src_path, dest_path)
                    found = True

            elif os.path.isdir(os.path.join(self.path, item)) and item not in directories:
               
                if "FOLDERS" not in self.directories:
                       self.create_folder("FOLDERS")

                dest_path = os.path.join(self.path, "FOLDERS", item)
                dest_path = self.get_unique_path(dest_path)
                self.move_item(src_path, dest_path)
                found = True

            if not found and item not in directories:
                 if "OTHER" not in self.directories:
                       self.create_folder("OTHER")
                 
                 dest_path = os.path.join(self.path, "OTHER", item)
                 dest_path = self.get_unique_path(dest_path)
                 self.move_item(src_path, dest_path)

    def create_folder(self, folder):
         self.folders_created+=1
         os.mkdir(os.path.join(self.path, folder))
         logging.info(f"Created folder: {folder}")
         self.directories.add(folder)
         if self.verbose:
             print(f"{folder} named folder created")

    def create_ext_match_array(self):
        try:
            with open(self.configFile, "r") as file:
                content = json.load(file)
                self.extMatch = content
                logging.info("Configuration file loaded successfully")
        except FileNotFoundError:
            print("config.json was not found")

    def get_unique_path(self, dest_path):
        if not os.path.exists(dest_path):
            return dest_path

        base, ext = os.path.splitext(dest_path)
        counter = 1

        while True:
            new_path = f"{base}_{counter}{ext}"
            if not os.path.exists(new_path):
                logging.debug(f"Resolved filename collision: {new_path}")
                return new_path
            counter += 1

    def update_self_directories(self):
        items = os.listdir(self.path)
        for item in items:
            full_path = os.path.join(self.path, item)

            if os.path.isdir(full_path) and item in directories:
                self.directories.add(item)

    def print_summary(self):
        print("\n--- Summary ---")
        
        if self.dry_run:
            print(f"Items that would be moved: {self.items_moved}")
            logging.info(f"Dry run complete | Items: {self.items_moved}")
        else:
            print(f"Items moved: {self.items_moved}")
            print(f"Number of errors encountered: {self.error_count}")
            logging.info(
                f"Organize complete | Moved: {self.items_moved} | "
                f"Errors: {self.error_count}"
            )
        
        print(f"Folders created: {self.folders_created}")
        logging.info(f"Folders created: {self.folders_created}")


    def move_item(self, src_path, dest_path):
        filename = os.path.basename(src_path)
        dest_folder = os.path.basename(os.path.dirname(dest_path))

        if self.dry_run:
            print(f"[DRY RUN] Would move: {filename} -> {dest_folder}")
            logging.info(f"[DRY RUN] Would move: {filename} -> {dest_folder}")
            self.items_moved += 1
            return

        try:
            shutil.move(src_path, dest_path)
            self.items_moved += 1

            logging.info(f"Moved: {filename} -> {dest_folder}")

            if self.verbose:
                print(f"Moved: {filename} -> {dest_folder}")

        except PermissionError:
            logging.warning(f"Permission denied: {src_path}")
            print(f"Permission denied: {src_path}")
            self.error_count += 1

        except Exception as e:
            logging.error(f"Error moving {src_path}: {e}")
            print(f"Error moving {src_path}: {e}")
            self.error_count += 1



    def run(self):
        self.update_self_directories()
        self.create_ext_match_array()
        self.organize()
        self.print_summary()

