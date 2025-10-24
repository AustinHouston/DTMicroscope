# stem_client.py
# Austin Houston

import socket
import json
import numpy as np
from typing import Tuple, Any

from base_client import BaseProtocol

class STEMClient(BaseClientFactory):
    # wrappers to mirror STEMServer API
    def get_detectors(self):
        return self._call("get_detectors")

    def activate_device(self, device):
        return self._call("activate_device", {"device": device})

    def device_settings(self, device, **kwargs):
        return self._call("device_settings", {"device": device, **kwargs})

    def get_stage(self):
        return self._call("get_stage")

    def set_stage(self, stage_positions, relative=True):
        # allow dict or list
        params = {"stage_positions": stage_positions, "relative": relative}
        return self._call("set_stage", params)

    def acquire_image(self, device, **kwargs):
        result = self._call("acquire_image", {"device": device, **kwargs})
        # If the server returned serialized numpy (list, shape, dtype), reconstruct it
        if isinstance(result, (list, tuple)) and len(result) == 3:
            array_list, shape, dtype = result
            arr = np.array(array_list, dtype=dtype)
            arr = arr.reshape(shape)
            return arr
        return result

    def acquire_image_stack(self, device):
        return self._call("acquire_image_stack", {"device": device})

    def acquire_spectrum(self, device, **kwargs):
        return self._call("acquire_spectrum", {"device": device, **kwargs})

    def acquire_spectrum_points(self, device, points, **kwargs):
        return self._call("acquire_spectrum_points", {"device": device, "points": points, **kwargs})

    def set_beam_position(self, x, y):
        return self._call("set_beam_position", {"x": x, "y": y})

    def get_vacuum(self):
        return self._call("get_vacuum")

    def get_microscope_status(self):
        return self._call("get_microscope_status")

    def aberration_correction(self, order, **kwargs):
        return self._call("aberration_correction", {"order": order, **kwargs})

    def close(self):
        return self._call("close")


