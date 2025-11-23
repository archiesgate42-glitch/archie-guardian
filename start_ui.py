#!/usr/bin/env python
"""
Start script voor Archie Guardian UI
Initialiseert guardian.py backend en start Flask UI server
"""

import sys
import os
import threading
import time

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import guardian to initialize it
print("=" * 60)
print("🚀 Starting Archie Guardian UI")
print("=" * 60)
print("\n[1/3] Initializing Guardian backend...")

try:
    # Import guardian module to initialize widgets and orchestrator
    import guardian
    
    # Wait a moment for initialization
    time.sleep(1)
    
    print("   ✅ Guardian backend initialized")
    print(f"   ✅ Widgets available: {len(guardian.AVAILABLE_WIDGETS)}")
    print(f"   ✅ Orchestrator: {'Available' if guardian.ORCHESTRATOR_AVAILABLE else 'Not available'}")
    
except Exception as e:
    print(f"   ⚠️  Warning: Could not fully initialize guardian: {e}")
    print("   UI will run in limited mode")

print("\n[2/3] Starting Flask API server...")

# Now import and start the API
try:
    from guardian_api import app
    
    print("   ✅ Flask API ready")
    print("\n[3/3] Starting web server...")
    print("=" * 60)
    print("🌐 Open http://localhost:5000 in your browser")
    print("=" * 60)
    print("\n⚠️  Note: Keep this window open while using the UI")
    print("   Press Ctrl+C to stop the server\n")
    
    # Start Flask server
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    
except KeyboardInterrupt:
    print("\n\n🛑 Shutting down...")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

