# 🔐  PSWD - A Simple CLI Password Manager

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)  
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  

PSWD is a lightweight **command-line password manager** written in Python (Based on Windows and Linux Filesystem).  
It allows you to **add, unlock, get, reset, and list** your stored credentials, all with session-based security.  

Passwords are encrypted using [Fernet (cryptography)](https://cryptography.io/en/latest/) and stored locally.  
Your session automatically expires after inactivity, requiring you to unlock again for safety.  

---

## Features :
- Secure password storage with encryption  
- Session lock system (auto-expires after inactivity)  
- Simple and intuitive CLI commands  
- JSON storage for easy management  

## 📦 Installation :

<img src = "https://www.logo.wine/a/logo/Linux/Linux-Logo.wine.svg"
width = "auto"
height = "50"
style="vertical-align:middle;" />
1. clone this repo anywhere
2. Give executable permission
3. create a Symlink of this repo to ~/.local/bin
```
> git clone https://VigneshwaranK08//PSWD.git
> chmod +x main.py # ( after > cd PSWD)
> sudo ln -s <path where u cloned>/PSWD/main.py ~/.local/bin/pswd
```
<img src= "https://www.logo.wine/a/logo/Microsoft_Windows/Microsoft_Windows-Logo.wine.svg"
height="70"
width="auto"
style="vertical-align:middle;" />
1. Clone this repo anywhere

```
git clone https://github.com/VigneshwaranK08/PSWD.git
```

## How to Use :

Note : Add python3 before pswd in every command (For <img src= "https://www.logo.wine/a/logo/Microsoft_Windows/Microsoft_Windows-Logo.wine.svg"
height="70"
width="auto"
style="vertical-align:middle;" />)

```
> pswd add <ServiceName> -f <AnyField> -p <Password>  # add a Password

> pswd list # View all the services

> pswd get <ServiceName> # Get the password for the specified ServiceName

> pswd unlock # Unlock with Master Password to continue using the app

> pswd reset # Caution ! Deletes all the passwords (including Master password) and all the Service's

```

## Project Structure 📂:

```
pswd/
|-- Encryption/
|   |-- Decoding.py
|   |-- Encoding.py
|   |-- key.key
|   |-- KeyGen.py
|-- main.py
|-- README.md
|-- .gitignore
|-- LICENSE
```
