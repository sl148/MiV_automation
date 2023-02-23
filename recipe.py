import os
import requests
from threading import Thread
import multiprocessing
import subprocess
import time
from open_ephys.control import OpenEphysHTTPServer

local_host = "localhost"
# local_host = "MECHSE-MGAZZ-02:ad.uillinois.edu"
http_status = f"http://{local_host}:37497/api/status"
http_recording = f"http://{local_host}:37497/api/recording"
http_processors = f"http://{local_host}:37497/api/processors"
http_load = f"http://{local_host}:37497/api/load"
http_window = f"http://{local_host}:37497/api/window"


# Run shell script
class Server():
    def __init__(self):
        # https
        self.server = None

    def connect(self):
        self.server = OpenEphysHTTPServer()
        r = None
        while r is None:
            try:
                r = self.get_status()
            except:
                pass

    def get_signal_chain(self):
        return requests.get(http_processors)

    def get_status(self):
        return self.server.status()

    def set_directory(self):
        return requests.put(http_recording, json={"parent_directory" : "./"})

    def set_acquire(self):
        return self.server.acquire()

    def set_record(self):
        return self.server.record()

    def set_idle(self):
        return self.server.idle()

    def set_signal_chain(self,path):
        print("Setting template: ", path)
        return requests.put(http_load, json={"path" : path})

    def disconnect(self):
        requests.put(http_window, json={"command" : "quit"})


class GUI():
    def __init__(self):
        self.p = None

    def reset(self):
        self.p = multiprocessing.Process(target=subprocess.run, args=(["sh","./run_oe.sh"],))

    def start(self):
        self.p.start()
    
    def join(self):
        pass

    def terminate(self):
        self.p.terminate()
        self.p.join(timeout=0)
        while self.p.is_alive():
            print('alive')
            time.sleep(0.2)
            pass

    

gui = GUI()
server = Server()

# TODO: generate xml files that have user defined signal chain
recording_task_template = ["/home/lee/Parasol/automation/MiV_automation/signal_chain_acquisition_template_1.xml",\
                        # "/home/lee/Parasol/automation/MiV_automation/empty_template.xml",\
                        "/home/lee/Parasol/automation/MiV_automation/signal_chain_acquisition_template_2.xml"]


for path in recording_task_template:
    gui.reset()
    gui.start()
    server.connect()

    r = server.set_signal_chain(path)   
    r = server.set_record()
    time.sleep(3)
    r = server.set_idle()
    time.sleep(0.1)
    
    # Disconnect server
    server.disconnect()

    # Close the thread
    gui.terminate()


