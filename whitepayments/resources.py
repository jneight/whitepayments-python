# coding=utf-8

import requests

from . import WHITE_API_KEY
from . import WHITE_OPEN_API_KEY
from . import base


class Customer(base.ResourceBase):
    url_base = 'https://api.whitepayments.com/customers/'

    def __init__(self, data=None):
        super(Customer, self).__init__(data=data)
        self.card = None

    @classmethod
    def create(cls, name, email, card=None, description=None):
        request = Request()
        data={
            'email': email,
            'name': name,
            'description': description,
            'card': card,
        }
        if isinstance(card, dict):
            data.update(card)
        response, status_code = request.post(cls.url_base, headers={}, data=data)
        if status_code == requests.codes.created:
            return (cls(data=response), status_code)
        return cls._handle_error(response)

    @classmethod
    def retrieve(cls, id):
        request = Request()
        response, status_code = request.get(cls.url_base + id, headers={})
        if status_code == requests.codes.ok:
            return (cls(data=response), status_code)
        return cls._handle_error(response)

    def update(self):
        request = Request()
        response, status_code = request.put(
            self.url_base + self.id, headers={}, data={'card': self.card})
        if status_code == requests.codes.ok:
            self._data = response
            return (self, status_code)
        return self._handle_error(response)


class Charge(base.ResourceBase):
    url_base = 'https://api.whitepayments.com/charges/'

    @classmethod
    def create(cls, customer, amount, currency, description=None, capture=True):
        request = Request()
        data = {
            'customer_id': customer,
            'amount': amount,
            'currency': currency,
            'description': description,
            'capture': capture,
            }
        response, status_code = request.post(cls.url_base, headers={}, data=data)
        if status_code == requests.codes.created:
            return (cls(data=response), status_code)
        return cls._handle_error(response)

    def capture(self):
        request = Request()
        response, status_code = request.get(
            self.url_base + self.id + '/capture/', headers={})
        if status_code in [requests.codes.created, requests.codes.ok, requests.codes.accepted]:
            self._data = response
            return (self, status_code)
        return self._handle_error(response)


class Token(base.ResourceBase):
    url_base = 'https://api.whitepayments.com/tokens/'

    @classmethod
    def create(cls, number, exp_month, exp_year, cvc, name=None):
        request = Request(api_key=WHITE_OPEN_API_KEY)
        data = {
            'number': number,
            'exp_month': exp_month,
            'exp_year': exp_year,
            'cvc': cvc,
            'name': name,
            }
        response, status_code = request.post(cls.url_base, headers={}, data=data)
        if status_code == requests.codes.created:
            return (cls(data=response), status_code)
        return cls._handle_error(response)
