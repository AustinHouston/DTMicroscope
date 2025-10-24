# base_server.py
# Austin Houston

import json
from twisted.internet import protocol, defer



class BaseRPCProtocol(protocol.Protocol):
    """
    Handles JSON-RPC-style communication.
    Dispatches commands to factory methods named rpc_<command>.
    """
    def connectionMade(self):
        print(f"[{self.__class__.__name__}] Connection made: {self.transport.getPeer()}")

    def dataReceived(self, data):
        try:
            message = json.loads(data.decode('utf-8'))
            d = self.handle_message(message)
            if isinstance(d, defer.Deferred):
                d.addCallback(self._send_result, message)
                d.addErrback(self._send_error, message)
            else:
                self._send_result(d, message)
        except Exception as e:
            self._send_error(e, {"id": None})

    def handle_message(self, message):
        cmd = message.get("command")
        params = message.get("params", {})
        method = getattr(self.factory, cmd, None)
        if not method:
            raise ValueError(f"Unknown command: {cmd}")
        return method(**params)

    def _send_result(self, result, message):
        reply = {"id": message.get("id"), "result": result}
        self.transport.write((json.dumps(reply) + "\n").encode('utf-8'))

    def _send_error(self, error, message):
        reply = {"id": message.get("id"), "error": str(error)}
        self.transport.write((json.dumps(reply) + "\n").encode('utf-8'))

class BaseServerFactory(protocol.Factory):
    protocol = BaseRPCProtocol