# R2-AI-Stack

**A modular, production-ready AI Personality & Show Stack for R2-D2**  
- Profile & Mood Managers  
- Cinematic & Event Stack Managers  
- Attention Layer + YOLO detection  
- Operator Dashboard (Flask + HTML/CSS)  
- Optional “Ask R2” QA module with TTS  
- systemd auto-start service

---

## Quickstart

```bash
git clone https://github.com/YourUser/r2-ai-stack.git
cd r2-ai-stack

# create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# install core deps
pip install -r core_api/requirements.txt

# run the server
python3 core_api/app.py
