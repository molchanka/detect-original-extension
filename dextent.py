#!/usr/bin/env python3
import sys
import os
from pathlib import Path

import puremagic


def detect_extension(file_path: Path) -> list | None:
    """
    Detects the extension of a file using puremagic
    :param file_path: Path to the file
    :return: Extension of the file (".gif"), or None if unknown
    """
    try:
        matches = puremagic.magic_file(str(file_path))
    except Exception as e:
        print(f"Error analyzing file: {e}")
        return None

    if not matches:
        return None

    result = {matches[0].extension}

    if len(matches) > 1: # Addressing possible signatures with same or similar magic numbers
        for m in matches[1:]:
            if m.confidence == matches[0].confidence:
                if m.extension != matches[0].extension:
                    result.add(m.extension)

    return list(result) if result else None

def scan_directory(directory: Path) -> list | None:
    """
    Scans a whole directory of files to present the user with the list of original extensions.
    :param directory: Path to the directory
    :return: List of sets of extensions with the filenames
    """
    # if Path.is_dir(directory) -- needs to be checked, perhaps at the main()
    try:
        with open(str(directory), 'r') as directory:
            for file in directory:

    except Exception as e:
        print(f"Error analyzing directory: {e}")
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: python dextent.py <file_path>")
        sys.exit(1)
    file_path = Path(sys.argv[1])
    if not file_path.exists() or not file_path.is_file():
        print(f"File not found: {file_path}")
        sys.exit(1)
    extension = detect_extension(file_path)
    if extension:
        if len(extension) > 1:
            print(f"Ambiguity detected. Possible original extensions: ")
            print(*extension, sep=", ")
        else:
            print(f"The file's original extension is {extension[0]}")
    else:
        print("Could not determine file type")


if __name__ == "__main__":
    main()
