#!/usr/bin/env python3
"""Filter history entries to keep only those with matching SVG files"""
import json
from pathlib import Path
from datetime import datetime

# Load history
with open("monkey_data/history.json", "r") as f:
    history = json.load(f)

# Get list of available SVG files
svg_dir = Path("monkey_evolution")
svg_files = {f.name for f in svg_dir.glob("*_monkey.svg")}

print(f"Total history entries: {len(history['entries'])}")
print(f"Available SVG files: {len(svg_files)}")

# Filter entries - keep only those that match an SVG file
def get_svg_filename(timestamp):
    """Calculate the expected SVG filename from a timestamp"""
    date = datetime.fromisoformat(timestamp)
    return f"{date.year}-{date.month:02d}-{date.day:02d}_{date.hour:02d}-{date.minute:02d}_monkey.svg"

kept_entries = []

for entry in history['entries']:
    expected_svg = get_svg_filename(entry['timestamp'])
    if expected_svg in svg_files:
        # Add svg_filename to the entry
        entry['svg_filename'] = expected_svg
        kept_entries.append(entry)
        print(f"✅ KEEP: {entry['timestamp']} -> {expected_svg}")
    else:
        print(f"❌ REMOVE: {entry['timestamp']} -> {expected_svg}")

print(f"\nKept: {len(kept_entries)} | Removed: {len(history['entries']) - len(kept_entries)}")

# Save filtered history
history['entries'] = kept_entries
with open("monkey_data/history.json", "w") as f:
    json.dump(history, f, indent=2)

print(f"✅ Saved {len(kept_entries)} entries to history.json")
