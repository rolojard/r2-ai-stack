# Sequences Package

This folder contains **example** Event Stack sequences (JSON) you can load via the API:

- **VIP_Show_Sequence**: PhotoOp + Leia cinematic + PROUD mood  
- **Kid_Show_Sequence**: KidEvent + Jawa panic cinematic + HAPPY mood  
- **Stage_Show_Sequence**: Parade + Vader entrance cinematic + ALERT quick mood  

## Usage

Assuming your Flask API is running:

```bash
curl -X POST http://<orin-ip>:5000/r2/load_event_stack/VIP_Show_Sequence
