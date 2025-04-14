# passwdpwn

A flexible, powerful password cracking toolkit designed for CTFs, cybersecurity training, and forensic investigations. This script helps you generate *massive*, intelligently crafted wordlists based on user-defined inputs (names, places, dates, keywords, or existing lists) and cracks hashes using common algorithms like MD5, SHA1, and SHA256.

## Features

- Accepts **custom word categories** from the user
- Supports **importing existing wordlists**
- Automatically generates:
  - Case variants (lower, upper, capitalized)
  - Leetspeak variants (e.g., `a` → `@`, `4`)
  - Word + special character combos (e.g., `Name!`, `#Place`)
  - Full pairwise and triple-word combinations
- Cracks hashes in **MD5**, **SHA1**, and **SHA256**
- Outputs all combinations to `MegaGigaWordlist.txt`
- Designed for **Capture the Flag (CTF)** and forensic memory dump challenges
- Optional GUI mode

## Requirements

- Python 3.6+
- Works on Linux, macOS, and Windows

## Usage

Run the script and follow the prompts:

```bash
python generate_wordlist.py
