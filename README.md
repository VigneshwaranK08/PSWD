# 🔐  PSWD - A Simple CLI Password 

PSWD is a lightweight **command-line password manager** written in Python (Based on Linux Filesystem).  
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

clone this repo at ~/.local/bin/

```
> git clone https://VigneshwaranK08//pswd.git
> cd pswd/
> mv pswd.py ~/.local/bin/pswd  
> cd ..
> chmod +x pswd 
```
## How to Use :

```
> pswd add <ServiceName> -f <AnyField> -p <Password>  # add a Password

> pswd list # View all the services

> pswd get <ServiceName> # Get the password for the specified ServiceName

> pswd unlock # Unlock with Master Password to continue using the app

> pswd reset # Caution ! Deletes all the passwords (including Master password) and all the Service's

```