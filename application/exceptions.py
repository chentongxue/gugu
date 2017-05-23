

class WebsocketRPCConnectError(IOError):
    """
    Raised when a rpc websocket connect fails.
    """
    def __init__(self, message='', *args, **kwargs):
        IOError.__init__(self, message, *args, **kwargs)
