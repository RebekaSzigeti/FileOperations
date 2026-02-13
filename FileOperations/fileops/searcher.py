import os
import shutil
import logging

class FileSearcher:

    def __init__(self, path, keyword, recursive=False, dry_run=False, verbose=False):
        self.path = path
        self.keyword = keyword.lower()
        self.recursive = recursive
        self.results_folder =  os.path.join(self.path, "SEARCH_RESULTS")
        self.dry_run = dry_run
        self.verbose = verbose
        self.copied_count = 0
        self.error_count = 0

        logging.info(f"Search started | Path: {self.path} | "
                     f"Keyword: '{self.keyword}' | "
                     f"Recursive: {self.recursive} | "
                     f"Dry run: {self.dry_run}")

    def search_and_copy(self):
         
         logging.debug("Running non-recursive search")

         for item in os.listdir(self.path):
            src_path = os.path.join(self.path, item)

            if os.path.isfile(src_path):

                if self.keyword in item.lower():
                    dest_path = os.path.join(self.results_folder, item)
                    dest_path = self.get_unique_path(dest_path)
                    self._copy_file(src_path, dest_path)

    def search_and_copy_recursive(self):
         
         logging.debug("Running recursive search")

         for root, dirs, files in os.walk(self.path):

            if "SEARCH_RESULTS" in dirs:
                dirs.remove("SEARCH_RESULTS")

            for file in files:
                if self.keyword in file.lower():
                    src_path = os.path.join(root, file)

                    dest_path = os.path.join(self.results_folder, file)
                    dest_path = self.get_unique_path(dest_path)
                    self._copy_file(src_path, dest_path)


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


    def _copy_file(self, src_path, dest_path):
        relative_src = os.path.relpath(src_path, self.path)
        relative_dest = os.path.relpath(dest_path, self.path)

        if self.dry_run:
            print(f"[DRY RUN] Would copy: {relative_src} -> {relative_dest}")
            logging.info(f"[DRY RUN] Would copy: {relative_src} -> {relative_dest}")
            self.copied_count += 1
            return

        try:
            shutil.copy2(src_path, dest_path)
            self.copied_count += 1
            logging.info(f"Copied: {relative_src} -> {relative_dest}")

            if self.verbose:
                print(f"Copied: {relative_src} -> {relative_dest}")

        except PermissionError:
            logging.warning(f"Permission denied: {relative_src}")
            print(f"Permission denied: {relative_src}")
            self.error_count += 1

        except Exception as e:
            logging.error(f"Unexpected error copying {relative_src}: {e}")
            print(f"Unexpected error copying {relative_src}: {e}")
            self.error_count += 1

    def print_statistics(self):
        print("\n--- Search Summary ---")

        if self.dry_run:
            print(f"\nFiles that would be copied: {self.copied_count}")
            logging.info(f"Dry run complete | Matches: {self.copied_count}")
        else:
            print(f"\nFiles copied: {self.copied_count}")
            print(f"Number of errors encountered: {self.error_count}")
            logging.info(f"Search complete | Copied: {self.copied_count} | "
                         f"Errors: {self.error_count}")


    def run(self):
         
         if not self.dry_run:
            if not os.path.exists(self.results_folder):
                os.mkdir(self.results_folder)
                logging.debug("Created SEARCH_RESULTS folder")

         if not self.recursive:
            self.search_and_copy()
         else:
             self.search_and_copy_recursive()

         self.print_statistics()

    