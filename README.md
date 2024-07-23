# KBACK (Arch Linux)

KBACK is a simple backup utility for Arch Linux x86_64 systems. It allows you to create tar.gz archives of specified files or folders, and manage these backups with ease.

## Author

Vinal Krush

## Features

- Backup and archive specified files or folders.
- Automatically skip symbolic links.
- Configurable backup directory via `/etc/kback/kback.conf`.
- List available backups.
- Progress bar to monitor archiving process.
- Ensures correct permissions on created archives.
- Failsafe mechanisms to check for root privileges and validate configurations.

## Requirements

- Arch Linux x86_64
- Python 3
- `tqdm` library for progress bar

## Installation
(Installing without the install script is not recommended)

```bash
git clone https://github.com/VinalKrush/kback.git
cd kback
sudo chmod +x ./install.sh
sudo ./install.sh
```

## Usage

### Command-Line Options

- `source`: Path to the file or folder to back up.
- `-b, --list-backups`: List backups in the backup directory.

### Examples

1. **Backup a file or folder:**

    ```bash
    sudo kback /path/to/source
    ```

    This command will create a tar.gz archive of the specified file or folder in the configured backup directory.

2. **List available backups:**

    ```bash
    sudo kback -b
    ```

    This command will list all backups available in the configured backup directory.

### Configuration

By default, the backup directory is `/var/backups`. You can change this by editing the configuration file located at `/etc/kback/kback.conf`.

```ini
[Settings]
backup_dir = /your/custom/backup/dir
```

# Important Notes

1. **Root Privileges:**
   The script requires root privileges to run. Ensure you execute it with sudo or as the root user.
   
2. **Symbolic Links:**
   The script automatically skips symbolic links during the backup process.
   
3. **Permissions:**
   The created archive will have read and write permissions for all users (rw-rw-rw-).

## Example Configuration

```ini
[Settings]
backup_dir = /var/backups
```

## Handling Missing Configuration

If the configuration file is missing, the script will default to using /var/backups as the backup directory. You will be prompted to confirm this action.

```bash
WARNING: The Config File For KBACK Does Not Exist.
The default location for backups is /var/backups
If this is not intended, please reinstall kback
Do you want to continue? [Y/n]
```

## Ensuring Backup Directory Exist

If the specified backup directory does not exist, the script will prompt you to create it:

```bash
Error: The backup directory '/your/custom/backup/dir' does not exist.
Would you like to create it? [Y/n]
```

# Current Goals

1. Adding a restore command allowing users to restore backups to a specified directory
