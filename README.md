# pmount(Permanent Mount)

This repository contains the source files and RPM .spec file for the pmount utility.
The pmount script is a command-line tool designed for Linux system administrators to simplify the process of making a filesystem mount persistent across reboots. 

It automatically detects the filesystem's UUID and type and adds the correct entry to /etc/fstab, then attempts to mount the filesystem.
It is particularly useful after creating new block devices like LVM Logical Volumes or partitions.

## NAME

pmount - add a filesystem entry to /etc/fstab using UUID and mount it
## INSTALLATION
Download .rpm file

`yum install <rpm-file>.rpm`

Example: `yum install pmount-1.0-1.amzn2023.noarch.rpm`

## SYNOPSIS

`pmount` [`OPTIONS`] *device_path* *mount_point_directory*

## DESCRIPTION

`pmount` is a shell script that automates the process of making a filesystem mount persistent across reboots. It is typically used by a system administrator after creating and formatting a new block device, such as an LVM Logical Volume or a partition, and wants to ensure it's mounted automatically on boot.

The script performs the following steps:

* Validates that it is run with root privileges.
* Handles `--version`, `--help`, and `-h` options if provided as the sole argument.
* Validates that exactly two arguments, representing the block device path and the mount point directory, are provided for the main functionality.
* Validates that the specified block device path exists and is a block device.
* Validates that the specified mount point directory exists and is a directory.
* Uses the `blkid(8)` command to reliably find the filesystem UUID and type of the block device. Exits if no filesystem UUID is found (i.e., the device is not formatted).
* Checks if an entry for the found UUID (`UUID=...`) or the specified mount point already exists in `/etc/fstab`. If an entry is found, the script exits with an error to prevent duplicates or unintended modifications.
* If no existing entry is found, it adds a new entry to `/etc/fstab` using the found UUID, the specified mount point, the determined filesystem type (or 'auto' as a fallback), and default mount options (`defaults 0 0`).
* Attempts to mount all filesystems listed in `/etc/fstab` using `mount -a(8)` to verify the syntax of the new entry and the availability of the device.
* Provides informative messages throughout the process and a success message if all steps complete without error.

This script requires root privileges to modify `/etc/fstab` and execute the `mount` command.

## OPTIONS

* `--version`: Show the script version number and exit.
* `--help`, `-h`: Show a brief help message including usage and options, and exit.

## ARGUMENTS

* *device_path*: The absolute path to the block device containing the filesystem to be permanently mounted (e.g., /dev/sda1, /dev/mapper/myvg-mydata, /dev/disk/by-uuid/... ).
* *mount_point_directory*: The absolute path to the existing directory where the filesystem should be mounted (e.g., /mnt/data, /srv/appdata). This directory must exist and be a directory before running the script.

## EXAMPLES

* `sudo pmount /dev/myvg/mydata /mnt/appdata`: Adds an /etc/fstab entry for the Logical Volume /dev/myvg/mydata using its UUID, setting the mount point to /mnt/appdata with default options, and attempts to mount it.
* `sudo pmount /dev/sdb1 /var/lib/mysql`: Adds an /etc/fstab entry for the partition /dev/sdb1 using its UUID, setting the mount point to /var/lib/mysql with default options, and attempts to mount it.
* `pmount --version`: Display the script version.
* `pmount --help`: Display the help message.

## EXIT STATUS

* **0**: Success. The /etc/fstab entry was added and the mount attempt (mount -a) was successful.
* **1**: Failure. An error occurred due to:
    * Incorrect number of arguments or invalid argument used.
    * Insufficient privileges (not run as root).
    * Invalid device path or mount point (doesn't exist, wrong type).
    * Inability to find a filesystem UUID for the device.
    * An entry for the UUID or mount point already exists in `/etc/fstab`.
    * A failure during the attempt to write the entry to `/etc/fstab`.
    * A failure during the `mount -a` attempt (e.g., syntax error in fstab, device temporarily unavailable, filesystem issues).

Error messages are printed to standard error.

## BUGS

The script exits if an entry for the UUID or mount point already exists. It does not attempt to update or modify existing entries. Manual editing of `/etc/fstab` is required in such cases.

Error messages from the final `mount -a` command might be generic; check system logs for details if it fails.

## AUTHOR

Hrishikesh Mishra
