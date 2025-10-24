# base_client.py
# Austin Houston

import json
from twisted.internet import reactor, protocol, defer

# client should add away rpc_ prefix
# server should strip away rpc_ prefix
class BaseClientProtocol(protocol.Protocol):
    def __init__(self):
        self._pending = {}
        self._next_id = 1

    # need to send other types than Deferred
    def send_command(self, command, params=None):
        msg_id = self._next_id
        self._next_id += 1
        d = defer.Deferred()
        self._pending[msg_id] = d
        msg = json.dumps({"id": msg_id, "command": command, "params": params or {}}).encode()
        self.transport.write(msg)
        return d

    def dataReceived(self, data):
        for line in data.split(b"\n"):
            if not line:
                continue
            msg = json.loads(line.decode('utf-8'))
            d = self._pending.pop(msg["id"], None)
            if not d:
                continue
            if "error" in msg:
                d.errback(Exception(msg["error"]))
            else:
                d.callback(msg["result"])

class BaseClientFactory(protocol.ClientFactory):
    protocol = BaseClientProtocol
    def __init__(self):
        self.proto = None

    def buildProtocol(self, addr):
        self.proto = self.protocol()
        return self.proto


