# Intrusion Detection System Alert

This project provides a notification system that alerts users via visual notifications or emails when Suricata or Snort detects an intrusion. The script prompts the user to disable the internet connection in response to potential threats.

## Features

- **Real-time Alerts**: Monitors Suricata and Snort alert logs for any changes.
- **Notification Options**: Sends visual alerts and plays notification sounds using `mpg123`.
- **User Prompt**: Asks the user whether to disable the internet connection upon detecting an intrusion.

## Installation

To set up the Intrusion Detection System Alert, follow these steps:

1. **Install Required Packages**:
   ```bash
   pip3 install -r requirements.txt
   sudo apt install mpg123 -y  # Required for notification sound

