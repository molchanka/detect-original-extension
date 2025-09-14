#!/usr/bin/env python3
import sys
import os
import argparse
from pathlib import Path
import puremagic


def detect_extension(file_path: Path) -> list | None:
    """
    Detects the extension of a file using puremagic
    :param file_path: Path to the file
    :return: List of possible extensions, or None if unknown
    """
    try:
        matches = puremagic.magic_file(str(file_path))
    except ValueError:
        print(f"Error analyzing file {file_path}: A file must be at least 1 byte in size.")
        return None
    except Exception as e:
        print(f"Error analyzing file: {e}.")
        return None

    if not matches:
        return [file_path.suffix]

    result = {matches[0].extension}

    # Scenario - There is more than one extension with equal confidence
    if len(matches) > 1:
        for m in matches[1:]:
            if m.confidence == matches[0].confidence and m.extension != matches[0].extension:
                result.add(m.extension)

    return list(result) if result else [file_path.suffix]


def scan_directory(directory: Path) -> list | None:
    """
    Scans a whole directory of files to present the user with the list of original extensions.
    :param directory: Path to the directory
    :return: List of sets of extensions with the filenames
    """
    try:
        children_paths = [child for child in directory.iterdir() if child.is_file()]

        # Error - Directory is empty
        if not children_paths:
            print(f"{directory} has no files.")
            return None

        children_results = []

        for child in children_paths:
            if detect_extension(child) is not None:
                children_results.append({child.name: detect_extension(child)})

    except Exception as e:
        print(f"Error analyzing directory: {e}")
        return None

    return children_results if children_results else None


def main():
    parser = argparse.ArgumentParser(
        description="Detect the original extension(s) of a file using puremagic."
    )
    parser.add_argument(
        "path",
        help="Path to a file or directory (if using -d)",
        type=Path
    )
    parser.add_argument(
        "-d", "--directory",
        action="store_true",
        help="Interpret the path as a directory and scan all files inside"
    )

    args = parser.parse_args()

    # Error - Path not found
    if not args.path.exists():
        print(f"Path not found: {args.path}")
        sys.exit(1)

    # Scenario - Directory argument used
    if args.directory:
        # Error - Path does not end in a directory
        if not args.path.is_dir():
            print(f"Expected a directory but got a file: {args.path}")
            sys.exit(1)

        results = scan_directory(args.path)

        if results:
            print(f"Detected extensions in directory '{args.path}':")
            for result in results:
                for file, ext_list in result.items():
                    if ext_list and ext_list[0] != '':
                        print(f"{file}: {', '.join(ext_list)}")
                    else:
                        print(f"{file}: unknown")
        else:
            print("No files to analyze.")

    # Scenario - No directory argument, single file scan
    else:
        # Error - Path does not end in a file
        if not args.path.is_file():
            print(f"Expected a file but got a directory: {args.path}")
            sys.exit(1)

        extension = detect_extension(args.path)

        if extension:
            if len(extension) > 1:
                print("Ambiguity detected. Possible original extensions:")
                print(*extension, sep=", ")
            if extension[0] == "":
                print("No extension detected.")
            else:
                print(f"The file's original extension is {extension[0]}")
        else:
            print("Could not determine file type")


if __name__ == "__main__":
    main()
