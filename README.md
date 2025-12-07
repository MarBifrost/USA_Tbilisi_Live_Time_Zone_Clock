# USA & Tbilisi Live Time Zone Clock ⏰

A clean and simple **Tkinter desktop app** that shows current time in all major US time zones + Tbilisi (Georgia), with a search feature to get the exact local time and abbreviation (EST/EDT, CST/CDT, etc.) for any city in the United States.

## Features

- Real-time clock for all major US time zones:
  - Eastern (EST/EDT)
  - Central (CST/CDT)
  - Mountain (MST/MDT)
  - Pacific (PST/PDT)
  - Alaska (AKST/AKDT)
  - Hawaii (HST)
  - Arizona (MST – no DST)
  - Guam & American Samoa
- Current time in **Tbilisi, Georgia** (Asia/Tbilisi)
- Search any US city → instantly shows:
  - Local time with AM/PM
  - Correct abbreviation (e.g., **EDT** in summer, **EST** in winter)
  - Full IANA timezone name (e.g., `America/New_York`)
- **Refresh Now** button for instant update
- Auto-refreshes every 60 seconds
- Works offline after first launch (except city search needs internet)

## Requirements

- Python 3.9–3.13
- Internet connection (only for city search via OpenStreetMap/Nominatim)

## Installation & Run

1. Clone or download this repository
   ```
   git clone https://github.com/MarBifrost/usa-tbilisi-timezone-app.git
   cd usa-tbilisi-timezone-app
    ```
2. Create and activate a virtual environment
    ```
    python -m venv .venv
    .Windows
    .venv\Scripts\activate
    macOS / Linux
    source .venv/bin/activate
    ```
3. Install dependencies
    ```
    pip install -r requirements.txt
    If TimezoneFinder fails on windows:
    pip install timezonefinder --no-build-isolation
    ```
4.
    ```
    python main.py
    ```
Project Structure
```
├── main.py              ← Main application (everything is here)
├── requirements.txt     ← Python dependencies
├── screenshot.png       ← (optional) Add a screenshot
└── README.md            ← This file
```

## License
Apache License
