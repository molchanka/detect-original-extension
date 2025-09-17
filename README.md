# detect-original-extension

## Detect Original File Extension
This project is a Python tool that detects the real or original file extension of a file using the [puremagic](https://pypi.org/project/puremagic) module. It is useful when files have been renamed or disguised and you want to recover their actual type, or in case you have suspicions about a file that is not properly opening on your system/shows up as corrupted.

## Features
+ Detects the file type based on magic numbers (file signatures)
+ Handles cases where multiple file types share the same or similar signatures
+ Returns one or more possible extensions
+ Can scan directories and report all detected file types
+ Clean Python code with error handling

## Upcoming Features
+ Returning a file to its original extension
+ A report/statistic on scanned directory
+ Nice-looking CLI
+ GUI version

## Compatibility
+ Python 3.12+
This repository requires you to have the python **puremagic** module in order for dextent.py to work, and a version of Python 3.12 or higher.

### Clone the repository to desired location
```
git clone https://github.com/molchanka/detect-original-extension
```

### Install puremagic from pypy
```
pip install puremagic
```

### Install exact puremagic version from requirements.txt
```
pip install -r requirements.txt
```

## Usage
The tool can be used either on a single file or on a whole directory.

### Single File
Go into the cloned repository directory and run the script from the command line, using the path (global or relative) to the file you want to check:
```
python dextent.py <file_path>
```

**Example**
```
python dextent.py disguised.png
The file's original extension is .zip
```

### Directory Scan
Go into the cloned repository directory and run the script from the command line, using **-d** option and the path (global or relative) to the directory you want to check:
```
python dextent.py -d /path/to/files
Detected extensions in '/path/to/files':
file1.exe: .txt
file2: unknown
image.png: .png
archive: .zip
```