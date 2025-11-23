"""
Flask API voor Archie Guardian UI
REST API endpoints voor widget management, chat, logs, en status
"""

from flask import Flask, jsonify, request, Response, stream_with_context, render_template, send_from_directory
from flask_cors import CORS
import json
import logging
from functools import wraps
from datetime import datetime
import time
import os
import sys
import subprocess
import requests

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import GuardianBridge
try:
    from services.guardian_bridge import GuardianBridge
except ImportError as e:
    print(f"Warning: Could not import GuardianBridge: {e}")
    GuardianBridge = None

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bridge (optional, for backward compatibility)
if GuardianBridge:
    bridge = GuardianBridge()
else:
    bridge = None
    print("⚠️  GuardianBridge not available - Using state file method")

# Widget CLI commands mapping
WIDGET_COMMANDS = {
    'file_integrity': 'file_integrity',
    'process_monitor': 'process_monitor',
    'network_sniffer': 'network_sniffer',
    'windows_defender': 'windows_defender',
    'rrnc': 'rrnc',
    'ollama_chat': 'ollama_chat'
}

def read_guardian_state():
    """Read guardian state from JSON file"""
    try:
        if os.path.exists('guardian_state.json'):
            with open('guardian_state.json', 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error reading guardian state: {e}")
    
    # Fallback if file doesn't exist
    return {
        'status': 'offline',
        'widgets': {name: {'enabled': False, 'status': 'idle'} for name in WIDGET_COMMANDS}
    }


# ============================================================================
# Error Handling Decorator
# ============================================================================

def handle_errors(f):
    """Decorator voor error handling op alle endpoints."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ConnectionError as e:
            logger.error(f"Connection error: {e}")
            return jsonify({
                'error': 'connection_error',
                'message': 'Could not connect to Guardian backend',
                'details': str(e)
            }), 503
        except ValueError as e:
            logger.error(f"Validation error: {e}")
            return jsonify({
                'error': 'validation_error',
                'message': 'Invalid input data',
                'details': str(e)
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error: {e}", exc_info=True)
            return jsonify({
                'error': 'internal_error',
                'message': 'An unexpected error occurred',
                'details': str(e) if app.debug else 'Contact support'
            }), 500
    return decorated_function


# ============================================================================
# Widget Management Endpoints
# ============================================================================

@app.route('/api/widgets', methods=['GET'])
@handle_errors
def get_widgets():
    """Get all widgets and their status from state file"""
    state = read_guardian_state()
    widgets_list = []
    
    for widget_name, widget_data in state.get('widgets', {}).items():
        widgets_list.append({
            'name': widget_name,
            'status': 'active' if widget_data.get('enabled') else 'idle',
            'active': widget_data.get('enabled', False),
            'model': widget_data.get('model') if widget_name == 'ollama_chat' else None
        })
    
    return jsonify(widgets_list)


@app.route('/api/widgets/<name>/start', methods=['POST'])
@handle_errors
def start_widget(name):
    """Start widget via CLI command to guardian.py"""
    if name not in WIDGET_COMMANDS:
        return jsonify({'error': 'Unknown widget'}), 404
    
    try:
        # Get guardian.py path
        guardian_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guardian.py')
        
        # Call guardian.py CLI with enable command
        result = subprocess.run([
            sys.executable, guardian_path,
            '--action', 'enable_widget',
            '--widget', name
        ], capture_output=True, text=True, timeout=10, cwd=os.path.dirname(guardian_path))
        
        if result.returncode == 0:
            # Wait a bit for state file to update
            time.sleep(0.5)
            state = read_guardian_state()
            widget_status = state.get('widgets', {}).get(name, {})
            
            return jsonify({
                'success': True,
                'widget': name,
                'status': 'active' if widget_status.get('enabled') else 'idle',
                'message': f'Widget {name} started'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to start widget',
                'details': result.stderr or result.stdout
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Command timeout'}), 504
    except Exception as e:
        logger.error(f"Error starting widget {name}: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/widgets/<name>/stop', methods=['POST'])
@handle_errors
def stop_widget(name):
    """Stop widget via CLI command to guardian.py"""
    if name not in WIDGET_COMMANDS:
        return jsonify({'error': 'Unknown widget'}), 404
    
    try:
        # Get guardian.py path
        guardian_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guardian.py')
        
        # Call guardian.py CLI with disable command
        result = subprocess.run([
            sys.executable, guardian_path,
            '--action', 'disable_widget',
            '--widget', name
        ], capture_output=True, text=True, timeout=10, cwd=os.path.dirname(guardian_path))
        
        if result.returncode == 0:
            # Wait a bit for state file to update
            time.sleep(0.5)
            state = read_guardian_state()
            widget_status = state.get('widgets', {}).get(name, {})
            
            return jsonify({
                'success': True,
                'widget': name,
                'status': 'idle',
                'message': f'Widget {name} stopped'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to stop widget',
                'details': result.stderr or result.stdout
            }), 500
    
    except subprocess.TimeoutExpired:
        return jsonify({'success': False, 'error': 'Command timeout'}), 504
    except Exception as e:
        logger.error(f"Error stopping widget {name}: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/widgets/<name>/status', methods=['GET'])
@handle_errors
def get_widget_status(name):
    """Get specific widget status from state file"""
    state = read_guardian_state()
    widget_status = state.get('widgets', {}).get(name)
    
    if not widget_status:
        return jsonify({'error': 'Widget not found'}), 404
    
    return jsonify({
        'name': name,
        'enabled': widget_status.get('enabled', False),
        'status': 'active' if widget_status.get('enabled') else 'idle',
        'model': widget_status.get('model') if name == 'ollama_chat' else None
    })


# ============================================================================
# Live Data Streaming (SSE)
# ============================================================================

@app.route('/api/stream/logs', methods=['GET'])
@handle_errors
def stream_logs():
    """SSE voor CLI output (audit.log)."""
    def generate():
        if not bridge:
            yield f"data: {json.dumps({'type': 'error', 'message': 'GuardianBridge not available', 'timestamp': datetime.now().isoformat()})}\n\n"
            return
        
        last_position = int(request.args.get('last_position', 0))
        
        # Send initial connection message
        yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.now().isoformat()})}\n\n"
        
        # Stream logs
        for log_entry in bridge.stream_logs(last_position):
            yield f"data: {log_entry}\n\n"
            time.sleep(0.1)  # Small delay to prevent overwhelming
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )


@app.route('/api/stream/widgets', methods=['GET'])
@handle_errors
def stream_widgets():
    """SSE voor widget status updates."""
    def generate():
        if not bridge:
            yield f"data: {json.dumps({'type': 'error', 'message': 'GuardianBridge not available', 'timestamp': datetime.now().isoformat()})}\n\n"
            return
        
        # Send initial connection message
        yield f"data: {json.dumps({'type': 'connected', 'timestamp': datetime.now().isoformat()})}\n\n"
        
        while True:
            try:
                widgets = bridge.get_all_widgets_status()
                yield f"data: {json.dumps({'type': 'status_update', 'widgets': widgets, 'timestamp': datetime.now().isoformat()})}\n\n"
                time.sleep(2)  # Update every 2 seconds
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'message': str(e), 'timestamp': datetime.now().isoformat()})}\n\n"
                time.sleep(5)
    
    return Response(
        stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',
            'Connection': 'keep-alive'
        }
    )


# ============================================================================
# Chat Interface
# ============================================================================

@app.route('/api/chat', methods=['POST'])
@handle_errors
def send_chat():
    """Send message naar Ollama."""
    if not bridge:
        return jsonify({'error': 'GuardianBridge not available'}), 503
    
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({
            'error': 'validation_error',
            'message': 'Missing "message" field'
        }), 400
    
    message = data['message'].strip()
    if not message:
        return jsonify({
            'error': 'validation_error',
            'message': 'Message cannot be empty'
        }), 400
    
    result = bridge.send_chat_message(message)
    
    if result.get('success'):
        return jsonify({
            'response': result.get('response'),
            'timestamp': result.get('timestamp')
        }), 200
    else:
        return jsonify({
            'error': 'chat_error',
            'message': result.get('error', 'Unknown error')
        }), 400


@app.route('/api/chat/history', methods=['GET'])
@handle_errors
def get_chat_history():
    """Haal chat geschiedenis op."""
    if not bridge:
        return jsonify([]), 200
    limit = int(request.args.get('limit', 50))
    history = bridge.get_chat_history(limit)
    return jsonify(history)


# ============================================================================
# System Status
# ============================================================================

@app.route('/api/status', methods=['GET'])
@handle_errors
def get_status():
    """Overall system health."""
    if not bridge:
        return jsonify({'status': 'disconnected', 'message': 'GuardianBridge not available'}), 503
    status = bridge.get_system_status()
    return jsonify(status)


@app.route('/api/config', methods=['GET'])
@handle_errors
def get_config():
    """Current configuration."""
    if not bridge:
        return jsonify({'version': '1.0', 'error': 'GuardianBridge not available'}), 503
    # Return basic config info
    config = {
        'version': '1.0',
        'permission_level': bridge.get_permission_level().get('permission_level'),
        'available_widgets': [w['name'] for w in bridge.get_all_widgets_status()]
    }
    return jsonify(config)


@app.route('/api/config', methods=['POST'])
@handle_errors
def update_config():
    """Update configuration (bijv. model wissel)."""
    if not bridge:
        return jsonify({'error': 'GuardianBridge not available'}), 503
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'validation_error',
            'message': 'No data provided'
        }), 400
    
    # For now, only support permission level updates
    if 'permission_level' in data:
        result = bridge.set_permission_level(data['permission_level'])
        if result.get('success'):
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    return jsonify({
        'error': 'validation_error',
        'message': 'Unsupported config update'
    }), 400


# ============================================================================
# Permissions (OrchB integratie)
# ============================================================================

@app.route('/api/permissions', methods=['GET'])
@handle_errors
def get_permissions():
    """Huidige permission level."""
    if not bridge:
        return jsonify({'permission_level': 'observe', 'error': 'GuardianBridge not available'}), 503
    perms = bridge.get_permission_level()
    return jsonify(perms)


@app.route('/api/permissions', methods=['POST'])
@handle_errors
def update_permissions():
    """Update permission level."""
    if not bridge:
        return jsonify({'error': 'GuardianBridge not available'}), 503
    
    data = request.get_json()
    
    if not data or 'permission_level' not in data:
        return jsonify({
            'error': 'validation_error',
            'message': 'Missing "permission_level" field'
        }), 400
    
    result = bridge.set_permission_level(data['permission_level'])
    
    if result.get('success'):
        return jsonify(result), 200
    else:
        return jsonify(result), 400


# ============================================================================
# Health Check
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'bridge_connected': bridge.is_connected() if bridge else False
    })


# ============================================================================
# Frontend Routes
# ============================================================================

@app.route('/', methods=['GET'])
def index():
    """Serve main UI page."""
    return render_template('index.html')


@app.route('/assets/<path:filename>')
def serve_assets(filename):
    """Serve assets from assets folder."""
    import os
    assets_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
    return send_from_directory(assets_dir, filename)


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 ARCHIE GUARDIAN UI API")
    print("=" * 60)
    if bridge:
        print(f"✅ GuardianBridge initialized: {bridge.is_connected()}")
    else:
        print("⚠️  GuardianBridge not available")
    print("📡 Starting Flask server on http://localhost:5000")
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)

