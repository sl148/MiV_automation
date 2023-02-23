import os
import requests
from threading import Thread
import subprocess
import time
from open_ephys.control import OpenEphysHTTPServer


# Run shell script
t1 = Thread(target=subprocess.run, args=(["sh","./run_oe.sh"],))
t1.start()

# https
http_status = "http://localhost:37497/api/status"
http_recording = "http://localhost:37497/api/recording"
http_processors = "http://localhost:37497/api/processors"
http_load = "http://localhost:37497/api/load"
http_window = "http://localhost:37497/api/window"

server = OpenEphysHTTPServer()

def get_signal_chain():
    return requests.get(http_processors)

def get_status():
    return server.status()

def set_directory():
    return requests.put(http_recording, json={"parent_directory" : "./"})

def set_acquire():
    return server.acquire()

def set_record():
    return server.record()

def set_idle():
    return server.idle()

def set_signal_chain(path):
    print("Setting template: ", path)
    return requests.put(http_load, json={"path" : path})

def close():
    return requests.put(http_window, json={"command" : "quit"})

# Connect to server
r = None
while r is None:
    try:
        r = get_status()
    except:
        pass


recording_task_template = ["/home/lee/Parasol/automation/scripts/signal_chain_template_1.xml",\
                        "/home/lee/Parasol/automation/scripts/signal_chain_template_2.xml"]

for path in recording_task_template:
    r = set_signal_chain(path)
    print("Setting template: ", path)
    r = set_record()
    time.sleep(4)
    r = set_idle()
    time.sleep(1)

# Close the window
r = close()



