# Attention Layer Package

**Provides real-time “attention” reactions** when R2 spots objects/faces.

## Files

- `attention_layer.py`  
  - Manages attention state, timers, and hooks for visuals & mood  
- `camera_detection_thread.py`  
  - Runs YOLOv5 detection in a background thread (GPU)  
  - Triggers `attention_layer.trigger_attention()`

## Installation

```bash
# from repo root
pip install torch torchvision opencv-python-headless
