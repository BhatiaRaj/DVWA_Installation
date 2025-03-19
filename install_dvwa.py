import subprocess
import os
import re

def run_command(command, shell=False, capture_output=True):
    """Runs a shell command and handles potential errors."""
    try:
        result = subprocess.run(
            command,
            shell=shell,
            check=True,
            capture_output=capture_output,
            text=True,
        )
        if capture_output:
          return result.stdout.strip()
        else:
          return ""

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        exit(1)  # Exit on error
    except FileNotFoundError:
        print(f"Command not found: {command[0] if isinstance(command, list) else command.split()[0]}")
        exit(1)
    except Exception as ex:
        print(f"An unexpected error occurred: {ex}")
        exit(1)

def check_prerequisites():
    """Checks if necessary tools (git, mysql, apache2) are installed."""
    required_tools = ["git", "mysql", "apache2"]
    for tool in required_tools:
        try:
            subprocess.run([tool, "--version"], check=True, capture_output=True, text=True)
        except FileNotFoundError:
            print(f"Error: {tool} is not installed. Please install it before proceeding.")
            print(f"  On Debian/Ubuntu: sudo apt install {tool}")
            print(f"  On CentOS/RHEL: sudo yum install {tool}")
            exit(1)

def install_dvwa():
    """Installs and configures DVWA."""
    check_prerequisites()

    # 1. Change directory
    os.chdir("/var/www/html")

    # 2. Git clone
    run_command(["git", "clone", "https://github.com/digininja/DVWA.git"])

    # 3. Check download (ls is not strictly necessary for automation)

    # 4. Change permissions
    run_command(["chmod", "-R", "777", "DVWA"])

    # 5. Change directory
    os.chdir("DVWA/config")

    # 6. Check for config.inc.php.dist (ls is not strictly necessary here either)

    # 7. Copy config file
    run_command(["cp", "config.inc.php.dist", "config.inc.php"])

    # 8 & 9.  Modify config file (using more robust file manipulation)
    config_file_path = "config.inc.php"
    try:
        with open(config_file_path, "r") as f:
            config_content = f.read()

        config_content = re.sub(r"\$_DVWA\['db_user'\]\s*=\s*'.*?';", r"$_DVWA['db_user'] = 'admin';", config_content)
        config_content = re.sub(r"\$_DVWA\['db_password'\]\s*=\s*'.*?';", r"$_DVWA['db_password'] = 'password';", config_content)
        #ReCaptcha Key
        config_content = re.sub(r"\$_DVWA\['recaptcha_public_key'\]\s*=\s*'.*?';", r"$_DVWA['recaptcha_public_key'] = '';", config_content)
        config_content = re.sub(r"\$_DVWA\['recaptcha_private_key'\]\s*=\s*'.*?';", r"$_DVWA['recaptcha_private_key'] = '';", config_content)

        with open(config_file_path, "w") as f:
            f.write(config_content)

    except FileNotFoundError:
        print(f"Error: Could not find config file at {config_file_path}")
        exit(1)
    except Exception as e:
        print(f"Error modifying config file: {e}")
        exit(1)

    # 10. Start MySQL service
    run_command(["service", "mysql", "start"])

    # 11 - 15. Configure database (using a single multi-command string)
    mysql_commands = [
        "CREATE DATABASE dvwa;",
        "CREATE USER 'admin'@'127.0.0.1' IDENTIFIED BY 'password';",
        "GRANT ALL PRIVILEGES ON dvwa.* TO 'admin'@'127.0.0.1';",
        "FLUSH PRIVILEGES;"  # Important: Apply the changes immediately
    ]
    # Construct the mysql command with multiple statements.  "-e" allows executing commands.
    full_mysql_command = "mysql -u root -e \"" +  "; ".join(mysql_commands) + "\""
    run_command(full_mysql_command, shell=True)



    # 16. Start Apache2 service
    run_command(["service", "apache2", "start"])

    # 17-22.  Modify php.ini (more robust path handling and file modification)
    php_version = None
    try:
      php_version_output = run_command(["php", "-v"])
      match = re.search(r"PHP (\d+\.\d+)", php_version_output) # Use regex for more robust version extraction

      if match:
        php_version = match.group(1)
        print(f"Detected PHP version: {php_version}")
      else:
        print("Could not determine PHP version.  Defaulting to 8.2.  You may need to adjust the path manually.")
        php_version = "8.2" #Default php version
    except Exception as e:
      print(f"Could not determine PHP version, defaulting to 8.2: {e}")
      php_version = "8.2"


    php_ini_path = f"/etc/php/{php_version}/apache2/php.ini"
    try:
        with open(php_ini_path, "r") as f:
            php_ini_content = f.read()
        php_ini_content = php_ini_content.replace("allow_url_fopen = Off", "allow_url_fopen = On")
        php_ini_content = php_ini_content.replace("allow_url_include = Off", "allow_url_include = On")

        with open(php_ini_path, "w") as f:
            f.write(php_ini_content)
    except FileNotFoundError:
        print(f"Error: Could not find php.ini file at {php_ini_path}")
        print("Please check your PHP version and installation path.")
        exit(1)
    except Exception as e:
        print(f"Error modifying php.ini file: {e}")
        exit(1)

    # 22. Reload Apache
    run_command(["service", "apache2", "reload"])

    print("\nDVWA installation complete (except for manual database creation).")
    print("Please visit http://127.0.0.1/DVWA in your browser, log in with admin/password,")
    print("go to the 'Setup' page, and click 'Create / Reset Database'.")
    print("Then, log in again to start using DVWA.")
if __name__ == "__main__":
    install_dvwa()
