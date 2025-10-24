# stem_server.py
# Austin Houston

from twisted.internet import reactor
from base_server import BaseServerFactory
import numpy as np

import sys
sys.path.insert(0, "C:\\AE_future\\autoscript_1_14\\")
import autoscript_tem_microscope_client as auto_script


class STEMServer(BaseServerFactory):
    def __init__(self):
        self.detectors = {"flu_camera": {"size": 512, "exposure": 0.1}}
        self.microscope = auto_script.TemMicroscopeClient()
        self.microscope.connect(ip = "127.0.0.1", port = 9095)
        
    def get_detectors(self):
        return list(self.detectors.keys())

    def activate_device(self, device):
        if device in self.detectors:
            print(f"{device} activated")
            return 1
        else:
            raise ValueError(f"Device {device} not found")

    def acquire_image(self, device):
        if device not in self.detectors:
            raise ValueError(f"Device {device} not found")
        print(f"Acquiring image from {device}")
        image = np.zeros((512, 512), dtype=np.uint16)
        return image.tolist()

def main():
    reactor.listenTCP(9093, STEMServer())
    print("STEM Server running on port 9093")
    reactor.run()

if __name__ == "__main__":
    main()