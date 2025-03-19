# DVWA Installation Script

This script automates the installation and configuration of Damn Vulnerable Web Application (DVWA) on macOS, Linux, and Windows (via WSL). It checks for prerequisites, clones the DVWA repository, configures database settings, modifies necessary configurations, and starts required services.

## Prerequisites

### macOS & Linux:
Ensure the following are installed:
- Git
- MySQL (MariaDB recommended)
- Apache2
- PHP

For Debian-based systems:
```sh
sudo apt update && sudo apt install git mysql-server apache2 php php-mysql libapache2-mod-php -y
```

For RedHat-based systems:
```sh
sudo yum install git mariadb-server httpd php php-mysql -y
```

For macOS (using Homebrew):
```sh
brew install git mysql apache2 php
```

### Windows (via WSL):
Install Windows Subsystem for Linux (WSL) and follow the Linux setup above.

## Installation

### Clone and Run Script
```sh
git clone https://github.com/your-repo/dvwa-setup.git
cd dvwa-setup
chmod +x install_dvwa.py
python3 install_dvwa.py
```

## Manual Setup Steps
1. Navigate to `http://127.0.0.1/DVWA` in your browser.
2. Log in with:
   - **Username:** `admin`
   - **Password:** `password`
3. Go to the **Setup** page and click **Create / Reset Database**.
4. Log in again to start using DVWA.

## Troubleshooting
- **Command Not Found Errors:** Ensure required packages are installed.
- **Permission Issues:** Run with `sudo` if necessary.
- **MySQL Connection Errors:** Ensure MySQL is running (`sudo service mysql start`).


