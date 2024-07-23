#!/usr/bin/env python3

import os
import tarfile
from datetime import datetime
import configparser
import argparse
import sys
from tqdm import tqdm

# Function to check if the script is running as root
def check_root():
    if os.geteuid() != 0:
        print("Error: You must run this command with sudo or be the root user.")
        sys.exit(1)

# Function to read the backup directory from the config file
def read_config():
    config_file = '/etc/kback/kback.conf'
    backup_dir = '/var/backups'

    if not os.path.isfile(config_file):
        print("WARNING: The Config File For KBACK Does Not Exist.")
        print("The default location for backups is /var/backups")
        print("If this is not intended, please reinstall kback")
        response = input("Do you want to continue? [Y/n] ").strip().lower()
        if response in ['', 'y', 'yes']:
            return backup_dir
        else:
            print("Exiting due to missing config file.")
            sys.exit(2)
    else:
        config = configparser.ConfigParser()
        try:
            config.read(config_file)
            backup_dir = config.get('Settings', 'backup_dir', fallback='/var/backups')
        except configparser.MissingSectionHeaderError:
            print(f"Error: The config file '{config_file}' is missing section headers.")
            sys.exit(3)
        except configparser.NoSectionError:
            print(f"Error: The config file '{config_file}' does not contain the '[Settings]' section.")
            sys.exit(4)
        except configparser.NoOptionError:
            print(f"Error: The config file '{config_file}' does not contain 'backup_dir' option.")
            sys.exit(5)
    
    return backup_dir

# Function to ensure the backup directory exists
def ensure_backup_dir_exists(backup_dir):
    if not os.path.isdir(backup_dir):
        print(f"Error: The backup directory '{backup_dir}' does not exist.")
        response = input("Would you like to create it? [Y/n] ").strip().lower()
        if response in ['', 'y', 'yes']:
            try:
                os.makedirs(backup_dir)
                print(f"Backup directory '{backup_dir}' created.")
            except Exception as e:
                print(f"Failed to create backup directory: {e}")
                sys.exit(6)
        else:
            print("Backup directory was not created. Exiting.")
                

# Function to create a tar archive of the specified file or folder with a progress bar
def create_archive(source_path, backup_dir):
    if not os.path.exists(source_path):
        print(f"Error: The specified file or folder '{source_path}' does not exist.")
        return

    if os.path.abspath(source_path) == "/":
        print("Error: You cannot backup the WHOLE system as this script is not intended for that.")
        print("You can look into system backup packages like Timeshift.")
        return

    # Prepare the archive name with a timestamp
    base_name = os.path.basename(source_path.rstrip('/'))
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_name = f"{base_name}_{timestamp}.tar.gz"
    archive_path = os.path.join(backup_dir, archive_name)

    # Create the tar archive with a progress bar
    with tarfile.open(archive_path, "w:gz") as tar:
        if os.path.isfile(source_path):
            # Archive a single file
            if os.path.islink(source_path):
                print("    ==> ERROR: KBACK Can't Archive Symbolic Links")
                sys.exit(7)
            file_size = os.path.getsize(source_path)
            with tqdm(total=file_size, unit='B', unit_scale=True, unit_divisor=1024, desc="Archiving") as pbar:
                tar.add(source_path, arcname=os.path.basename(source_path))
                pbar.update(file_size)
        else:
            # Archive a directory
            total_size = 0
            file_sizes = []
            for dirpath, _, filenames in os.walk(source_path):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    if os.path.islink(file_path):
                        print(f"    ==> WARNING: Skipping Symbolic Link: {file_path}")
                        continue
                    file_sizes.append(os.path.getsize(file_path))
                    total_size += os.path.getsize(file_path)

            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024, desc="Archiving") as pbar:
                for dirpath, _, filenames in os.walk(source_path):
                    for filename in filenames:
                        file_path = os.path.join(dirpath, filename)
                        if os.path.islink(file_path):
                            print(f"    ==> WARNING: Skipping Symbolic Link: {file_path}")
                            continue
                        tar.add(file_path, arcname=os.path.relpath(file_path, source_path))
                        pbar.update(os.path.getsize(file_path))

    # Change permissions of the archive to allow read and write for all users
    os.chmod(archive_path, 0o666)  # 0o666 corresponds to rw-rw-rw-

    print(f"Backup successful! Archive created at: {archive_path}")

# Function to list files in the backup directory
def list_backups(backup_dir):
    if not os.path.isdir(backup_dir):
        print(f"Error: The backup directory '{backup_dir}' does not exist.")
        sys.exit(8)

    backups = os.listdir(backup_dir)
    if not backups:
        print("There are no backups on this system.")
    else:
        print("Backups available:")
        for backup in backups:
            print(backup)

def main():
    check_root()

    parser = argparse.ArgumentParser(description="Backup and archive a file or folder.")
    parser.add_argument("source", help="Path to the file or folder to back up", nargs='?')
    parser.add_argument("-b", "--list-backups", action='store_true', help="List backups in the backup directory")
    args = parser.parse_args()

    backup_dir = read_config()

    if args.list_backups:
        list_backups(backup_dir)
    elif args.source:
        ensure_backup_dir_exists(backup_dir)
        create_archive(args.source, backup_dir)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()