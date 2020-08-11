class PaywayException(Exception):
    """ This is the master class for all the exceptions that can occur at the payway background processment """

    def __init__(self, code, msg):
        self.code = code
        self.msg = msg

    def __str__(self):
        return repr('{}: {}'.format(self.code, self.msg))
