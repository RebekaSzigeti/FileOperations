import argparse
from fileops.organizer import FileOrganizer
from fileops.searcher import FileSearcher
from fileops.deleter import FileDeleter
import logging
import os


def main():

    logging.basicConfig(
        filename="filetool.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    parser = argparse.ArgumentParser(description="File Organizer Tool")

    subparsers = parser.add_subparsers(dest="command")

    # organize command
    organize_parser = subparsers.add_parser(
        "organize",
        help="Organize files in a directory based on extension rules"
    )
    organize_parser.add_argument(
        "--path",
        type=str,
        default= os.getcwd(),
        help="Path to organize (default: current directory)"
    )

    organize_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Simulate file operations without making changes"
   )

    organize_parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to config file"
    )

    organize_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output"
    )




     # search command
    search_parser = subparsers.add_parser(
        "search",
        help="Search files by name and copy them to SEARCH_RESULTS folder"
    )

    search_parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="Directory to search in (default: current directory)"
    )

    search_parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Keyword to search for in file names (case-insensitive)"
    )

    search_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Search recursively in subdirectories"
    )

    search_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be copied without actually copying files"
    )

    search_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output about the search and copy process"
    )


     # delete command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete files if their name contain a given string"
    )

    delete_parser.add_argument(
        "--path",
        type=str,
        default=os.getcwd(),
        help="Directory to delete in (default: current directory)"
    )

    delete_parser.add_argument(
        "--name",
        type=str,
        required=True,
        help="Keyword to search for in file names (case-insensitive)"
    )

    delete_parser.add_argument(
        "--recursive",
        action="store_true",
        help="Delete recursively in subdirectories"
    )

    delete_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting files"
    )

    delete_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed output about the deletion process"
    )

    delete_parser.add_argument(
        "--force",
        action="store_true",
        help="Will not ask for permission before the deletion of a file"
    )


    args = parser.parse_args()

    if args.command == "organize":
        organizer = FileOrganizer(args.path, args.config, args.dry_run, args.verbose)
        organizer.run()

    if args.command == "search":
         searcher = FileSearcher(args.path, args.name, args.recursive, args.dry_run, args.verbose)
         searcher.run()
    
    if args.command == "delete":
         deleter = FileDeleter(args.path, args.name, args.recursive, args.dry_run, args.verbose, args.force)
         deleter.run()

    if not args.command:
        parser.print_help()
        return


    logging.info("========== RUN END ==========")
    
    logging.info("")




if __name__ == "__main__":
    main()
