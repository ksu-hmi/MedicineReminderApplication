 # Medicine Reminder Application
Simple medicine reminder app using python

To build an APK for Android from your Kivy application, we will use Buildozer, a tool that automates the process of packaging Kivy applications for Android. Below is a step-by-step guide to help you through this process.

## Features

- Set reminders with medication name and interval (in hours).
- View a list of all active reminders.
- Edit or delete existing reminders.
- Receive notifications with medication details.

## Installation

### Prerequisites

- Python 3.6+
- Git
- Buildozer (Python tool to package the application)
- Java JDK (for compiling the application)
- Android SDK (Android development tools)

### Step 1: Set Up Your Environment

#### On Ubuntu (or other Debian-based distributions):

```sh
sudo apt update
sudo apt install -y python3-pip python3-dev build-essential git \
    python3-venv libffi-dev libssl-dev liblzma-dev zlib1g-dev \
    libgdbm-dev libsqlite3-dev libreadline-dev libncurses5-dev libbz2-dev \
    openjdk-11-jdk
```

### On MacOS

```sh
brew install caskroom/cask/brew-cask
brew install automake autoconf libtool pkg-config
brew install gnu-sed wget
brew install openssl
```

### Step 4: Initialize the Buildozer Project
Navigate to your project directory and initialize Buildozer:

```sh
cd your_project_directory
buildozer init
```

This command will create a buildozer.spec file in your project directory. This file contains all the configurations required to build the APK.

### Step 5: Configure Buildozer
Open the buildozer.spec file in a text editor and modify it as needed. Here are some important fields you should configure:

```ini
title = Medicine Reminder
package.name = medicinereminder
package.domain = org.example
source.include_exts = py,kv
source.include_patterns = assets/*, images/*, *.png
requirements = python3,kivy,kivymd,plyer,schedule,sqlite3
android.permissions = INTERNET, VIBRATE
```


### Step 6: Build the APK
Once your buildozer.spec file is configured, you can build the APK. In your project directory, run:

```sh
buildozer -v android debug
```
This command will download the necessary tools, compile your application, and package it into an APK file. The -v flag provides verbose output.
