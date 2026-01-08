
# PSINT 

A modular Open Source Intelligence (OSINT) automation tool designed for security analysts. It unifies breach lookups, metadata extraction, and digital footprint mapping into a single asynchronous CLI.

##  Features

### 1. Breach Detection (`breach`)
Checks if an email address has been compromised in known public data breaches using the LeakCheck API.
* **Function:** Queries public databases to see if your data was exposed.
* **Output:** Returns the source of the breach (e.g., "LinkedIn", "Adobe") and the specific data types leaked (e.g., "Email, Password, IP Address").

### 2. Digital Footprint Tracker (`footprint`)
Analyzes a user's digital presence starting from a UPI ID or username.
* **UPI Validation:** Validates the UPI ID format and identifies the banking provider (e.g., `user@oksbi` -> Google Pay/SBI).
* **Active Recon:** Automatically checks if the username exists on developer-friendly platforms like *GitHub*, *Reddit*, and *Vimeo*.
* **Passive Recon:** Generates "Google Dork" links to manually check walled gardens like *LinkedIn*, *Facebook*, and *Instagram* without triggering anti-bot defenses.

### 3. Metadata Forensics (`metadata`)
Extracts hidden EXIF data and information from local files.
* **Images:** Extracts camera model, software version, and date. Crucially, if GPS data exists, it **decrypts the coordinates** and generates a clickable **Google Maps link** to the exact location where the photo was taken.
* **PDFs:** Extracts author, creator tool, and creation dates.

---

##  Installation

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/osint-tool.git](https://github.com/yourusername/osint-tool.git)
    cd osint-tool
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configuration (Optional)**
    Create a `.env` file in the root directory to use a paid API key for more detailed results. If left blank, the tool uses the free public tier.
    ```ini
    LEAKCHECK_API_KEY=your_key_here
    ```

---

##  Usage Guide

Run the tool using `python main.py` followed by the command you want to use.

### 1. Check for Breaches
Scan an email address to see if it has been leaked.

```bash
python main.py breach user@example.com

```

### 2. Check Metadata

Analyze a file (Image or PDF) to find hidden details and location data.

```bash
python main.py metadata evidence.jpg

```

### 3. Trace Digital Footprint

Scan a UPI ID (or username) to map banking providers and social media accounts.

```bash
python main.py footprint user@oksbi

```

---

## 🛡️ Disclaimer

This tool is designed for educational purposes, security research, and authorized defensive testing only. The author is not responsible for any misuse of this tool.


## side note - the canon.jpg file is just for testing, please ignore it. it'll be removed in a later version.


