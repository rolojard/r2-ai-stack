#!/usr/bin/env python3
import os
import json
import threading
import time
import cv2

from flask import Flask, jsonify, request, send_from_directory
from flask import Response, stream_with_context
from flask_cors import CORS

from r2_profile_manager      import ProfileManager
from r2_mood_manager         import MoodManager
from r2_cinematic_manager    import CinematicManager
from r2_event_stack_manager  import EventStackManager
from camera_detection_thread import CameraDetectionThread
from attention_layer         import AttentionLayer

# New QA imports
from r2_qa.qa_module         import QAModule
from r2_qa.tts_driver        import TTSDriver

app = Flask(__name__, static_folder=None)
CORS(app)

# Initialize core managers
profile_manager     = ProfileManager()
mood_manager        = MoodManager()
cinematic_manager   = CinematicManager(profile_manager)
event_stack_manager = EventStackManager(profile_manager, mood_manager, cinematic_manager)
attention_layer     = AttentionLayer(profile_manager, mood_manager)
camera_thread       = CameraDetectionThread(profile_manager, attention_layer)

# Initialize QA & TTS
qa  = QAModule(api_key=os.getenv("OPENAI_API_KEY", None))
tts = TTSDriver()
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Start background threads as daemons
camera_thread.start()
event_stack_manager.start()

recent_actions = []

def log_action(msg: str):
    timestamp = time.strftime('%H:%M:%S')
    entry = f"{timestamp} - {msg}"
    recent_actions.insert(0, entry)
    # keep only latest 10
    del recent_actions[10:]
    
def mjpeg_generator():
    """Yield JPEG frames in multipart response."""
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
        # encode to JPEG
        ret2, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 60])
        if not ret2:
            continue
        # yield frame
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        time.sleep(1/5)  # 5 fps

@app.route('/')
def dashboard():
    return send_from_directory('..', 'dashboard/r2_operator_dashboard.html')

@app.route('/r2/status', methods=['GET'])
def get_status():
    return jsonify({
        'profile':   profile_manager.get_profile(),
        'mood':      mood_manager.get_mood(),
        'heartbeat': int(time.time())
    })

@app.route('/r2/set_profile/<profile_name>', methods=['POST'])
def set_profile(profile_name):
    profile_manager.set_profile(profile_name)
    log_action(f"Set Profile: {profile_name}")
    return jsonify({'status': 'ok'})

@app.route('/r2/set_mood/<mood_name>', methods=['POST'])
def set_mood(mood_name):
    mood_manager.set_mood(mood_name)
    log_action(f"Set Mood: {mood_name}")
    return jsonify({'status': 'ok'})

@app.route('/r2/trigger_cinematic/<cinematic_name>', methods=['POST'])
def trigger_cinematic(cinematic_name):
    cinematic_manager.run_cinematic_sequence(cinematic_name)
    log_action(f"Triggered Cinematic: {cinematic_name}")
    return jsonify({'status': 'ok'})

@app.route('/r2/trigger_quick_mood/<mood_name>', methods=['POST'])
def trigger_quick_mood(mood_name):
    event_stack_manager.add_event('quick_mood', mood_name)
    log_action(f"Triggered Quick Mood: {mood_name}")
    return jsonify({'status': 'ok'})

@app.route('/r2/add_event', methods=['POST'])
def add_event():
    data = request.get_json() or {}
    if 'event_type' not in data or 'event_data' not in data:
        return jsonify({'status':'error','message':'Missing fields'}), 400
    event_stack_manager.add_event(data['event_type'], data['event_data'])
    log_action(f"Added Event: {data['event_type']}/{data['event_data']}")
    return jsonify({'status': 'ok'})

@app.route('/r2/event_stack', methods=['GET'])
def get_event_stack():
    return jsonify({'event_stack': event_stack_manager.get_current_stack()})

@app.route('/r2/clear_event_stack', methods=['POST'])
def clear_event_stack():
    event_stack_manager.stop_stack()
    log_action("Cleared Event Stack")
    return jsonify({'status': 'ok'})

@app.route('/r2/recent_actions', methods=['GET'])
def get_recent_actions():
    return jsonify({'recent_actions': recent_actions})

@app.route('/r2/stop_all', methods=['POST'])
def stop_all():
    profile_manager.set_profile('LargeCon')
    mood_manager.set_mood('FRIENDLY')
    event_stack_manager.stop_stack()
    attention_layer.force_clear_attention()
    log_action("Force Stop All")
    return jsonify({'status': 'ok'})

@app.route('/r2/attention_state', methods=['GET'])
def attention_state():
    return jsonify({
        'attention_enabled': camera_thread.enabled,
        'attention_active':  attention_layer.attention_active,
        'attention_target':  attention_layer.attention_target
    })

@app.route('/r2/load_event_stack/<sequence_name>', methods=['POST'])
def load_event_stack(sequence_name):
    try:
        seq_path = os.path.join('..', 'sequences', f"{sequence_name}.json")
        with open(seq_path, 'r') as f:
            seq = json.load(f)
        for e in seq:
            event_stack_manager.add_event(e['event_type'], e['event_data'])
        log_action(f"Loaded Sequence: {sequence_name}")
        return jsonify({'status': 'ok'})
    except FileNotFoundError:
        return jsonify({'status':'error','message':'Sequence not found'}), 404
    except Exception as e:
        return jsonify({'status':'error','message':str(e)}), 500

@app.route('/r2/attention_enable', methods=['POST'])
def attention_enable():
    camera_thread.enable()
    return jsonify({'status':'ok','enabled':True})

@app.route('/r2/attention_disable', methods=['POST'])
def attention_disable():
    camera_thread.disable()
    return jsonify({'status':'ok','enabled':False})
    
@app.route('/video_feed')
def video_feed():
    return Response(stream_with_context(mjpeg_generator()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    
# NEW: Ask R2 endpoint
@app.route('/r2/ask', methods=['POST'])
def ask_r2():
