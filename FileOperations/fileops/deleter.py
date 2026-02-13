import os
import logging

class FileDeleter:

    def __init__(self, path, keyword, recursive=False, dry_run=False, verbose=False, force = False):
        self.path = path
        self.keyword = keyword.lower()
        self.recursive = recursive
        self.dry_run = dry_run
        self.verbose = verbose
        self.deleted_count = 0
        self.force = force
        self.error_count = 0

        logging.info(
            f"Delete started | Path: {self.path} | "
            f"Keyword: '{self.keyword}' | "
            f"Recursive: {self.recursive} | "
            f"Dry run: {self.dry_run} | "
            f"Force: {self.force}"
        )

 
    def delete_files(self):
        logging.debug("Running non-recursive delete")
        for item in os.listdir(self.path):
            src_path = os.path.join(self.path, item)

            if os.path.isfile(src_path):
                if self.keyword in item.lower():
                    self._handle_delete(src_path)


    def delete_files_recursive(self):
        logging.debug("Running recursive delete")
        for root, dirs, files in os.walk(self.path):

            for file in files:
                if self.keyword in file.lower():
                    src_path = os.path.join(root, file)
                    self._handle_delete(src_path)

   
    def _handle_delete(self, src_path):
        relative_path = os.path.relpath(src_path, self.path)
        
        if self.dry_run:
            print(f"[DRY RUN] Would delete: {relative_path}")
            logging.info(f"[DRY RUN] Would delete: {relative_path}")
            self.deleted_count += 1
        else:
            isTherePermission = True

            if not self.force:
                response = input(f"Are you sure you want to delete this file: {relative_path}? (y/n): ")
                if response.lower() != "y" and response.lower() != "yes":
                    logging.info(f"Deletion cancelled by user: {relative_path}")
                    isTherePermission = False

            if isTherePermission:
                try:
                    os.remove(src_path)
                    logging.info(f"Deleted: {relative_path}")
                    self.deleted_count += 1
                    if self.verbose:
                        print(f"Deleted: {relative_path}")

                except PermissionError:
                    logging.warning(f"Permission denied: {relative_path}")
                    print(f"Permission denied: {src_path}")
                    self.error_count += 1

                except Exception as e:
                    logging.error(f"Unexpected error deleting {relative_path}: {e}")
                    print(f"Error deleting {src_path}: {e}")
                    self.error_count += 1


    def print_summary(self):
        print("\n--- Summary ---")
        
        if self.dry_run:
            print(f"Items that would be deleted: {self.deleted_count}")
            logging.info(f"Dry run complete | Matches: {self.deleted_count}")
        else:
            print(f"Items deleted: {self.deleted_count}")
            print(f"Number of errors encountered: {self.error_count}")
            logging.info(
                f"Delete complete | Deleted: {self.deleted_count} | "
                f"Errors: {self.error_count}"
            )

        

    def run(self):

        if not self.recursive:
            self.delete_files()
        else:
            self.delete_files_recursive()

        self.print_summary()

