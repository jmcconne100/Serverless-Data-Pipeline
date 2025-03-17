#!/bin/bash

# Define messages
MSG_PYTHON_CHECK="Checking if Python3 is installed..."
MSG_PYTHON_INSTALL="Python3 is not installed. Installing..."
MSG_PYTHON_INSTALLED="Python3 is already installed."

MSG_PIP_CHECK="Checking if pip3 is installed..."
MSG_PIP_INSTALL="pip3 is not installed. Installing..."
MSG_PIP_INSTALLED="pip3 is already installed."

MSG_FAKER_CHECK="Checking if Faker library is installed..."
MSG_FAKER_INSTALL="Faker library not found. Installing..."
MSG_FAKER_INSTALLED="Faker library is already installed."

MSG_OS_DETECT="Detecting OS..."
MSG_OS_UNSUPPORTED="Unsupported OS. Exiting."

# Detect OS type
echo "$MSG_OS_DETECT"
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
    echo "Detected OS: $OS"
else
    echo "$MSG_OS_UNSUPPORTED"
    exit 1
fi

# Check if Python3 is installed
echo "$MSG_PYTHON_CHECK"
if ! command -v python3 &> /dev/null; then
    echo "$MSG_PYTHON_INSTALL"
    if [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
        sudo apt update && sudo apt install -y python3 python3-pip
    elif [[ "$OS" == "rhel" || "$OS" == "fedora" || "$OS" == "centos" || "$OS" == "amzn" ]]; then
        sudo yum update -y && sudo yum install -y python3 python3-pip
    else
        echo "$MSG_OS_UNSUPPORTED"
        exit 1
    fi
else
    echo "$MSG_PYTHON_INSTALLED"
fi

# Check if pip3 is installed
echo "$MSG_PIP_CHECK"
if ! command -v pip3 &> /dev/null; then
    echo "$MSG_PIP_INSTALL"
    pip3 install --upgrade pip --user
else
    echo "$MSG_PIP_INSTALLED"
fi

# Check if Faker library is installed
echo "$MSG_FAKER_CHECK"
if ! python3 -c "import faker" &> /dev/null; then
    echo "$MSG_FAKER_INSTALL"
    pip3 install faker --user
else
    echo "$MSG_FAKER_INSTALLED"
fi

echo "Setup completed. You can now run your Python scripts."
