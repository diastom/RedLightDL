import sys
import os
import multiprocessing

# Necessary for PyInstaller 
if sys.platform.startswith('win'):
    multiprocessing.freeze_support()

# Add the current directory to sys.path to ensure RedLight package is found
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

sys.path.append(base_path)

from RedLight.server import app

if __name__ == '__main__':
    print("Starting RedLight Server...", flush=True)
    app.run(host='127.0.0.1', port=5000, debug=False)
