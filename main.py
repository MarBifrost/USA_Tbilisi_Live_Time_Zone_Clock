# =============================================================================
# USA + Tbilisi + Worldwide Time Zone App (Your Favorite Design + Input Validation)
# Apache License 2.0
# =============================================================================

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import pytz
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import re

# =============================================================================
# Fixed zones
# =============================================================================
US_TIMEZONES = {
    "Eastern (EST/EDT)":     "US/Eastern",
    "Central (CST/CDT)":     "US/Central",
    "Mountain (MST/MDT)":    "US/Mountain",
    "Pacific (PST/PDT)":     "US/Pacific",
    "Alaska (AKST/AKDT)":    "US/Alaska",
    "Hawaii (HST)":          "US/Hawaii",
    "Arizona (MST)":         "US/Arizona",
}
TBILISI_TZ = "Asia/Tbilisi"

# =============================================================================
# Friendly name (EST/EDT, +04, etc.)
# =============================================================================
def get_friendly_tz_name(iana_tz: str) -> str:
    if not iana_tz:
        return "Unknown"
    try:
        tz = pytz.timezone(iana_tz)
        now = datetime.now(tz)
        is_dst = now.dst() != datetime.timedelta(0)

        mapping = {
            "US/Eastern": "EDT" if is_dst else "EST",
            "US/Central": "CDT" if is_dst else "CST",
            "US/Mountain": "MDT" if is_dst else "MST",
            "US/Pacific": "PDT" if is_dst else "PST",
            "US/Alaska": "AKDT" if is_dst else "AKST",
            "US/Hawaii": "HST",
            "US/Arizona": "MST",
            "Asia/Tbilisi": "+04",
        }
        if iana_tz in mapping:
            return mapping[iana_tz]

        offset = now.utcoffset()
        if offset is not None:
            hours = int(offset.total_seconds() // 3600)
            mins = int(abs(offset.total_seconds() % 3600) // 60)
            sign = "+" if hours >= 0 else "-"
            return f"UTC{sign}{abs(hours):02d}" + (f":{mins:02d}" if mins else "")
        return iana_tz.split("/")[-1]
    except:
        return iana_tz.split("/")[-1]

# =============================================================================
# Helpers
# =============================================================================
def get_current_time(tz_str: str) -> str:
    return datetime.now(pytz.timezone(tz_str)).strftime("%I:%M:%S %p")

def get_city_timezone(city_name: str):
    geolocator = Nominatim(user_agent="timezone_app_secure")
    try:
        location = geolocator.geocode(city_name, exactly_one=True, timeout=10)
        if not location:
            return None
        tf = TimezoneFinder()
        return tf.timezone_at(lng=location.longitude, lat=location.latitude)
    except:
        return None

# =============================================================================
# Input validation: only letters + spaces + hyphens allowed
# =============================================================================
def validate_city_name(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z\s\-]+$", name.strip()))

# =============================================================================
# Your beautiful UI (unchanged!)
# =============================================================================
class TimeZoneApp:
    def __init__(self, root):
        self.root = root
        self.root.title("USA + Tbilisi Live Clock")
        self.root.geometry("540x660")
        self.root.configure(bg="#f0f0f0")

        tk.Label(root, text="Live Time Zones", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

        # USA zones
        usa_frame = tk.LabelFrame(root, text=" United States Time Zones ", font=("Arial", 12, "bold"), padx=10, pady=10)
        usa_frame.pack(padx=20, pady=10, fill="x")
        self.usa_labels = {}
        for name, tz in US_TIMEZONES.items():
            row = tk.Frame(usa_frame)
            row.pack(fill="x", pady=2)
            tk.Label(row, text=f"{name}:", width=22, anchor="w", font=("Courier", 11)).pack(side="left")
            lbl = tk.Label(row, text="Loading...", font=("Courier", 11, "bold"))
            lbl.pack(side="left")
            self.usa_labels[name] = lbl

        # Tbilisi
        tbilisi_frame = tk.LabelFrame(root, text=" Georgia ", font=("Arial", 12, "bold"), padx=10, pady=8)
        tbilisi_frame.pack(padx=20, pady=10, fill="x")
        self.tbilisi_label = tk.Label(tbilisi_frame, text="Tbilisi: Loading...", font=("Courier", 13, "bold"))
        self.tbilisi_label.pack()

        # Search + buttons
        control_frame = tk.Frame(root, bg="#f0f0f0")
        control_frame.pack(pady=15)
        tk.Label(control_frame, text="Search any city:", bg="#f0f0f0", font=("Arial", 10)).pack(side="left")
        self.city_entry = tk.Entry(control_frame, width=22, font=("Arial", 10))
        self.city_entry.pack(side="left", padx=8)
        self.city_entry.bind("<Return>", lambda e: self.search_city_time())
        # Optional: block typing digits in real-time
        self.city_entry.bind("<KeyRelease>", self.filter_input)

        tk.Button(control_frame, text="Search", bg="#2196F3", fg="white", command=self.search_city_time).pack(side="left", padx=5)
        tk.Button(control_frame, text="Refresh Now", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.manual_refresh).pack(side="left", padx=12)

        self.result_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#d35400", bg="#f0f0f0")
        self.result_label.pack(pady=12)

        self.update_times()
        self.root.after(60000, self.update_times)

    # =============================================================================
    # NEW: Block numbers while typing (optional but nice)
    # =============================================================================
    def filter_input(self, event=None):
        current = self.city_entry.get()
        cleaned = re.sub(r"[^A-Za-z\s\-]", "", current)  # remove anything not letter/space/-
        if cleaned != current:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, cleaned)

    # =============================================================================
    def search_city_time(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showwarning("Empty field", "Please type a city name")
            return

        if not validate_city_name(city):
            self.result_label.config(text="", fg="red")
            messagebox.showwarning("Invalid input", "City name cannot contain numbers or symbols")
            return

        tz_str = get_city_timezone(city)
        if tz_str:
            time_str = get_current_time(tz_str)
            friendly = get_friendly_tz_name(tz_str)
            self.result_label.config(text=f"{city.title()}:  {time_str}  →  {friendly}", fg="#006400")
        else:
            self.result_label.config(text="", fg="red")
            messagebox.showerror("Not found", "There is no such city")

    def manual_refresh(self):
        self.update_times()
        if self.city_entry.get().strip() and validate_city_name(self.city_entry.get()):
            self.search_city_time()

    def update_times(self):
        for name, tz in US_TIMEZONES.items():
            self.usa_labels[name].config(text=get_current_time(tz))
        self.tbilisi_label.config(text=f"Tbilisi: {get_current_time(TBILISI_TZ)}")
        self.root.after(60000, self.update_times)

# =============================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = TimeZoneApp(root)
    root.mainloop()