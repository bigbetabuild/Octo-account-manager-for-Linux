# Roblox Account Manager for Linux

A powerful multi-instance account manager for Roblox on Linux, designed to work seamlessly with Roblox Sober.

## Features

✅ **Multi-Instance Support** - Launch multiple Roblox accounts simultaneously  
✅ **Account Management** - Add, edit, delete, and organize accounts  
✅ **Session Persistence** - Remember login sessions across sessions  
✅ **Secure Credentials** - Encrypted password storage using keyring  
✅ **Quick Launch** - One-click account switching and launching  
✅ **Profile Management** - Organize accounts into profiles  
✅ **Activity Logging** - Track account activity and logins  

## Requirements

- Linux (Ubuntu 20.04+, Fedora, Arch, etc.)
- Python 3.8+
- Roblox Sober (Vulkan-based Roblox client for Linux)
- pip3

## Installation

1. Clone the repository:
```bash
git clone https://github.com/bigbetabuild/Octo-account-manager-for-Linux.git
cd Octo-account-manager-for-Linux
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Ensure Roblox Sober is installed:
```bash
# Roblox Sober installation instructions at: https://github.com/RobloxLabs/roblox-sober
```

4. Run the application:
```bash
python3 main.py
```

## Usage

### Adding an Account
1. Click "Add Account" button
2. Enter username and password
3. (Optional) Assign to a profile
4. Click "Save"

### Launching an Account
1. Select an account from the list
2. Click "Launch" to start Roblox Sober with that account
3. Multiple instances can be launched simultaneously

### Managing Sessions
- View active sessions in the "Active Sessions" tab
- Monitor CPU/Memory usage per instance
- Kill individual instances or all instances

## Configuration

Configuration files are stored in `~/.config/roblox-account-manager/`:
- `accounts.json` - Encrypted account data
- `profiles.json` - Profile configurations
- `settings.json` - Application settings

## Project Structure

```
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── ui/                 # GUI components
│   │   ├── main_window.py
│   │   ├── account_dialog.py
│   │   ├── session_monitor.py
│   │   └── styles.py
│   ├── core/               # Core functionality
│   │   ├── account_manager.py
│   │   ├── session_manager.py
│   │   ├── launcher.py
│   │   └── config_manager.py
│   ├── utils/              # Utilities
│   │   ├── crypto.py
│   │   ├── logger.py
│   │   └── validators.py
│   └── resources/          # Resources
│       ├── icons/
│       └── styles/
├── tests/                  # Unit tests
├── docs/                   # Documentation
└── .desktop                # Desktop launcher file
```

## License

GNU General Public License v3.0

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss proposed changes.

## Support

For issues, questions, or suggestions, please open a GitHub issue.

---

**Note:** This project is independent and not affiliated with Roblox Corporation or the Roblox Sober project.
