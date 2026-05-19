#!/usr/bin/env python3

import subprocess
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
import re
from typing import List, Tuple

# ----------------------------
# CONFIGURATION - Change THIS
# ----------------------------
PRTG_URL_BASE = "http://IP:5050/TOKEN?content="

# ----------------------------

def get_temperatures() -> List[Tuple[str, float]]:
    try:
        result = subprocess.run(
            ["sysctl", "-a"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error: sysctl failed: {e.stderr.strip()}", file=sys.stderr)
        return []

    temps = []
    for line in result.stdout.splitlines():
        if "temperature" in line and ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.upper().endswith("C"):
                try:
                    temp = float(val[:-1].strip())
                    temps.append((key, temp))
                except ValueError:
                    print(f"Warning: skipped invalid line: '{line}'", file=sys.stderr)
    return temps

def build_prtg_xml(temps: List[Tuple[str, float]]) -> str:
    root = ET.Element("prtg")
    for channel_name, value in temps:
        result = ET.SubElement(root, "result")
        channel = re.sub(r'[^a-zA-Z0-9_.\-]', ' ', channel_name).strip() or "Temperature"
        # Round to integer
        int_value = int(round(value))
        ET.SubElement(result, "channel").text = channel
        ET.SubElement(result, "value").text = str(int_value)
        ET.SubElement(result, "unit").text = "Temperature"
        ET.SubElement(result, "mode").text = "Average"
    return ET.tostring(root, encoding="unicode", method="xml")

def send_to_prtg(xml_data: str) -> None:
    encoded = urllib.parse.quote(xml_data, safe="")
    full_url = PRTG_URL_BASE + encoded
    try:
        with urllib.request.urlopen(full_url, timeout=10) as response:
            print(f"Success — HTTP {response.getcode()}: {response.read().decode().strip()}")
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} — {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    temps = get_temperatures()
    if not temps:
        print("ERROR: No temperatures found.", file=sys.stderr)
        sys.exit(1)
    xml_data = build_prtg_xml(temps)
    print("=== DEBUG XML (all values rounded to integers) ===")
    print(xml_data)
    print("=== END XML ===")
    send_to_prtg(xml_data)

if __name__ == "__main__":
    main()
