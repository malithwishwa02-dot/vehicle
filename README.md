# CHRONOS-MULTILOGIN

Method 4: Time-Shifted Injection implementation for synthetic browser profile aging using Multilogin API.

## Directory Structure

```
CHRONOS-MULTILOGIN/
│
├── core/
│   ├── __init__.py
│   ├── chronos.py          # System time manipulation via kernel32.dll
│   ├── mla_handler.py      # Multilogin API controller
│   └── forensics.py        # NTFS MFT scrubbing operations
│
├── config/
│   ├── __init__.py
│   └── settings.py         # Configuration parameters
│
├── utils/
│   ├── __init__.py
│   ├── logger.py          # Logging utilities
│   └── validators.py      # Input validation & privilege checks
│
├── profiles/              # Multilogin profile storage
│   └── .gitkeep
│
├── logs/                  # Operation logs
│   └── .gitkeep
│
├── main.py               # Primary orchestration logic
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Requirements

- Windows 10/11
- Administrator privileges
- Python 3.10+
- Multilogin installed with Local API enabled (port 35000)
- Chrome WebDriver compatible with Multilogin's Chrome version

## Usage

```bash
# Run with administrator privileges
python main.py --profile-id <MLA_PROFILE_ID> --journey standard
```