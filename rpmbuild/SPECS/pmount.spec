# rpmbuild/SPECS/pmount.spec

# --- Package Metadata ---
Name:           pmount
Version:        1.0
Release:        1%{?dist}
Summary:        Script to permanently mount filesystems via fstab using UUID 

License:        MIT
URL:            http://example.com/pmount
Source0:        pmount
Source1:        pmount.1

BuildArch:      noarch
# BuildRequires: # List packages needed to *build* the software (not needed for a script)

# --- Runtime Dependencies ---
# List packages required for your script to run on the target system
# bash, util-linux (provides blkid, mount, findmnt), grep
Requires:       bash, util-linux, grep

%description
This script automates adding a filesystem entry to /etc/fstab using the UUID
and attempts to mount it. Useful for making LVM or partition mounts persistent.
It requires root privileges to run and is intended for system administrators.

# --- Prepare Section (for extracting source - not needed for simple files) ---
%prep
# Nothing to do here for pre-built files, but the section must exist or be omitted carefully.
# We'll just ensure the build root is clean.
%{__rm} -rf %{buildroot}

# --- Build Section (for compiling - not needed for a script) ---
%build
# Nothing to do here for a script

# --- Install Section ---
# This section copies files from the build environment (or SOURCES)
# into the temporary installation root ($RPM_BUILD_ROOT)
%install
# Create the destination directories in the RPM build root
%{__mkdir_p} %{buildroot}/usr/local/bin
%{__mkdir_p} %{buildroot}/usr/local/share/man/man1

# Copy the script from SOURCES and set executable permissions in the build root
%{__cp} %{SOURCE0} %{buildroot}/usr/local/bin/pmount
%{__chmod} 0755 %{buildroot}/usr/local/bin/pmount # Ensure correct permissions for the executable

# Copy the man page from SOURCES and set standard permissions
%{__cp} %{SOURCE1} %{buildroot}/usr/local/share/man/man1/pmount.1
%{__chmod} 0644 %{buildroot}/usr/local/share/man/man1/pmount.1 # Standard man page permissions

# --- Files Section ---
# This section lists the files that will be included in the final RPM
# from the installation root (%{buildroot}), mapped to their final destinations
# %attr(permissions, user, group) target_path
%files
%attr(0755,root,root) /usr/local/bin/pmount
%attr(0644,root,root) /usr/local/share/man/man1/pmount.1


# --- Changelog Section ---
# Record changes to the package
%changelog
* Sun May 18 2025 Hrishikesh Mishra mishrarishikesh0@gmail.com - 1.0-1
- Initial package creation
