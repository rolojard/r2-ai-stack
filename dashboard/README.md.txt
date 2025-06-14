# Operator Dashboard Package

This folder holds your **Operator Dashboard**—a real-time web UI to monitor R2’s:

- **Profile** (LargeCon, PhotoOp, etc.)  
- **Mood** (HAPPY, MAD, etc.)  
- **Heartbeat** (timestamp)  
- **Attention State** (Idle, Active, Disabled)  
- **Recent Actions** (last 10 commands)

## Files

- `r2_operator_dashboard.html`  
- `static/r2_dashboard.css`

## Usage

1. **Ensure** your Flask server (`core_api/app.py`) is running on port **5000**.  
2. **Place** this `dashboard/` folder next to your `core_api/` folder.  
3. **Open** in a browser: `http://<orin-ip>:5000/`  

The page will auto-refresh every 2 seconds.

## Customization

- Modify CSS in `static/r2_dashboard.css` for your color scheme.  
- Extend the HTML to display additional data (e.g., event stack).

