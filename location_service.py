import subprocess
import json
import urllib.request

def get_windows_native_gps():
    try:
        # Windows PowerShell ka native command jo location hardware sensor block ko access karta hai
        powershell_cmd = (
            "[void][Reflection.Assembly]::LoadWithPartialName('System.Device'); "
            "$watcher = New-Object System.Device.Location.GeoCoordinateWatcher; "
            "$watcher.Start(); "
            "Start-Sleep -s 2; "
            "if($watcher.Position.Location.IsUnknown -eq $false) { "
            "  Write-Output ($watcher.Position.Location.Latitude.ToString() + ',' + $watcher.Position.Location.Longitude.ToString()) "
            "}"
        )
        
        # Command execute karein background me
        result = subprocess.run(
            ["powershell", "-Command", powershell_cmd],
            capture_output=True, text=True, timeout=5
        )
        
        output = result.stdout.strip()
        if output and "," in output:
            return output  # Returns 'latitude,longitude'
    except Exception:
        pass
    return None

def get_live_location():
    # 1. Primary Route: Pure Hardware Triangulation via Windows PowerShell
    print("🛰️ Fetching Live Pinpoint Location from Windows Sensors...")
    gps_coords = get_windows_native_gps()
    
    if gps_coords:
        google_maps_url = f"https://www.google.com/maps?q={gps_coords}"
        return google_maps_url, "Device Precise GPS"

    # 2. Secondary Fallback: IP-Based Network Location
    try:
        url = "https://ipinfo.io/json"
        response = urllib.request.urlopen(url, timeout=5)
        data = json.loads(response.read().decode())
        if "loc" in data:
            lat_long = data["loc"]
            google_maps_url = f"https://www.google.com/maps?q={lat_long}"
            city = data.get("city", "Unknown City")
            return google_maps_url, f"{city} (IP Network)"
    except Exception:
        pass

    # 3. Third Fallback: Static Coordinates (Delhi)
    return "https://www.google.com/maps?q=28.6139,77.2090", "Delhi (Static Fallback)"