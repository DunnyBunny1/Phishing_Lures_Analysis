from lures import LureNotifier
import os


def main():
    # Read in our domains file
    file_name: str = 'domains.txt'
    directory: str = os.getcwd()
    file_path: str = os.path.join(directory, file_name)
    with open(file_path, 'rt') as f:  # Open the file in read - text mode
        lines: [] = f.readlines()

if __name__ == '__main__':
    main()
