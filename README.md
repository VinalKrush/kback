# KBACK (Arch Linux)

KBACK is a simple backup utility for Arch Linux x86_64 systems. It allows you to create tar.gz archives of specified files or folders, and manage these backups with ease.

## Author

Vinal Krush

## Features

- Backup and archive specified files or folders.
- Configurable backup directory via `/etc/kback/kback.conf`.
- List available backups.

## Requirements

- Arch Linux x86_64
- Python 3
- `tqdm` library for progress bar

## Installation
(Installing without the install script is not recommended)

**Install Script:**
```bash
git clone https://github.com/VinalKrush/kback.git
cd kback
sudo chmod +x ./install.sh
sudo ./install.sh
```

**Manual Install**
```bash
# Git clone the repo
git clone https://github.com/VinalKrush/kback.git
cd kback
```

```bash
# Move the script to /usr/bin
sudo touch /usr/bin/kback
sudo cp kback.py /usr/bin/kback
sudo chmod +x /usr/bin/kback
```

```bash
# Making config file
sudo mkdir -p /etc/kback
sudo touch /etc/kback/kback.conf
sudo cp kback.conf /etc/kback/kback.conf
```

## Usage

### Command-Line Options

- `source`: Path to the file or folder to back up.
- `-b, --list-backups`: List backups in the backup directory.

### Examples

- **Backup a file or folder:**

    ```bash
    sudo kback /path/to/source
    ```
    This command will create a tar.gz archive of the specified file or folder in the configured backup directory.

- **List available backups:**

    ```bash
    sudo kback -b
    ```

    This command will list all backups available in the configured backup directory.
    **Note**
    If you create backups and then change the backup directory, This command will only list backups in the new directory

### Configuration

By default, the backup directory is `/var/backups`. You can change this by editing the configuration file located at `/etc/kback/kback.conf`.

```ini
[Settings]
backup_dir = /your/custom/backup/dir
```

# Important Notes

- **Root Privileges:**
   The script requires root privileges to run. Ensure you execute it with sudo or as the root user.
   
- **Symbolic Links:**
   The script automatically skips symbolic links during the backup process. (I have it do this because symlinks cannot be added to archives as it will return with an error)
   
- **Permissions:**
   The created archive will have read and write permissions for all users (rw-rw-rw-).

- **Progess Bar Freezes:**
   On older or slower hardware, it may seem like the progress bar is frozen but I promise KBACK is still working.

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
(Biggest goal is to become a all in one backup manager)

- Adding a restore command allowing users to restore backups to a specified directory

- Adding a delete command allowing users to delete backups

- Adding a uninstall script to make the uninstall process easy

- Maybe in the future add a command-line option to not archive the backup so symlinks can be backed up
