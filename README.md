# Email Downloader

A simple Python script to download emails via IMAP from all folders. Each folder is processed synchronously, while emails within each folder are downloaded asynchronously.

## Requirements

- Python 3.12+ (might be working on earlier versions, but not tested)
- [python-dotenv](https://www.google.com/search?q=python-dotenv+installation)

## Setup

* Create and enable a virtual environment

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

1. Install the required package:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the same directory as the script with the following content:

   ```
   IMAP_SERVER=mail.example.com
   USERNAME=user@example.com
   PASSWORD=your_password
   SAVE_DIR=./emails
   ```

   Replace the values with your actual IMAP server details and credentials.

## Usage

Run the script:

```bash
python src/main.py
```

The script will:

- Connect to your IMAP server.
- Retrieve a list of folders.
- For each folder, download all emails asynchronously.
- Save each email as an `.eml` file in a folder-specific directory under `SAVE_DIR`.
