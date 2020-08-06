import requests
import logging
import uuid
from paython.exceptions import MissingDataError
from paython.payway_exceptions import PaywayException

logger = logging.getLogger(__name__)


class Payway(object):

    def __init__(self, username, password, company_id, source_id, debug=False):
        self.username = username
        self.password = password
        self.company_id = company_id
        self.source_id = source_id
        if debug:
            self.BASE_URL = 'https://devedgilpayway.net/PaywayWS'
        else:
            self.BASE_URL = 'https://edgilpayway.net/PaywayWS'

    def get_token(self):
        response = requests.post(self.BASE_URL + '/Session', json={"request": "getPaywaySession",
                                                                   "companyId": self.company_id,
                                                                   "password": self.password,
                                                                   "userName": self.username})
        obj = response.json()
        return obj['paywaySessionToken']

    def capture(self, token, amount, credit_card=None):

        if not credit_card:
            debug_string = "paython.gateways.payway.capture()  -- No CreditCard object present. You passed in %s "\
                           % (credit_card)
            logger.debug(debug_string)
            raise MissingDataError('You did not pass a CreditCard object into the auth method')

        response = requests.post(self.BASE_URL + '/Payment/CreditCard',
                                 json=self.format_data(token, amount, credit_card))
        obj = response.json()

        if int(obj['paywayCode']) != 5000:
            raise PaywayException(int(obj['paywayCode']), obj['paywayMessage'])
        return obj

    def format_data(self, token, amount, credit_card):
        request = dict()
        request['accountInputMode'] = 'primaryAccountNumber'
        request['request'] = 'sale'
        request['paywaySessionToken'] = token
        request['cardAccount'] = {
            "accountNumber": credit_card.number,
            "expirationDate": credit_card.exp_date,
            "firstName": credit_card.full_name,
            "fsv": credit_card.verification_value
        }
        request['cardTransaction'] = {
            "amount": amount,
            "idSource": self.source_id,
            "name": "CLASSIFIED-{}".format(uuid.uuid4())
        }
        return request
