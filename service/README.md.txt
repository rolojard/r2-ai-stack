# Service Package

This folder contains scripts to run your R2 AI Stack as a systemd service.

## Files

- `run_stack.sh`  
  - Starts the Flask API inside your Python venv  
  - Be sure to `chmod +x` it

- `r2ai-stack.service`  
  - Systemd unit file  
  - Copy to `/etc/systemd/system/`

## Installation

```bash
# 1. Copy the service file
sudo cp r2ai-stack.service /etc/systemd/system/

# 2. Reload systemd and enable
sudo systemctl daemon-reload
sudo systemctl enable r2ai-stack.service

# 3. Start the service
sudo systemctl start r2ai-stack.service

# 4. Check status/logs
sudo systemctl status r2ai-stack.service
journalctl -u r2ai-stack.service -f
