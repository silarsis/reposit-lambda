#!/usr/bin/env python
"""
Simple client
"""

from __future__ import print_function
from os  import environ
import swagger_client

class Deployment:
    " A deployment is essentially a house, I think "
    def __init__(self, userkey, api):
        self._userkey = userkey
        self._api = api

    @property
    def capacity(self):
        " Return battery capacity "
        resp = self._api.deployments_userkey_battery_capacity_get(self._userkey)
        return resp.to_dict()['battery_capacity']

    @property
    def battery_historical_soc(self):
        " Historical state of charge information - list of [timestamp, charge]"
        resp = self._api.deployments_userkey_battery_historical_soc_get(self._userkey)
        soc = resp.to_dict()['battery_soc']
        soc.sort()
        return soc

    @property
    def charge(self):
        " Return the current battery charge "
        return self.battery_historical_soc[-1][1]

    @property
    def charge_percent(self):
        " Percent charged "
        resp = self._api.deployments_userkey_battery_historical_soc_get(self._userkey)
        cap = resp.to_dict()['battery_capacity']
        soc = resp.to_dict()['battery_soc']
        soc.sort()
        return (soc[-1][1] / cap) * 100

    @property
    def charging(self):
        " Return true if currently charging, false otherwise "
        soc = self.battery_historical_soc
        return soc[-1][1] > soc[-2][1]

    @property
    def feeding_grid(self):
        " Return true if we're feeding power to the grid "
        resp = self._api.deployments_userkey_meter_historical_p_get(self._userkey)
        soc = resp.to_dict()['meter_p']
        soc.sort()
        return soc[-1][1] < 0

    @property
    def status(self):
        " Return whether we're feeding the grid, charging, using battery, or flat and using power "
        soc = self.battery_historical_soc
        if soc[-1][1] > soc[-2][1]:
            return "charging"
        if soc[-1][1] < soc[-2][1]:
            return "discharging"
        if self.feeding_grid:
            return "feeding"
        return "flat"

class Reposit:
    """
    Basic class to login and do some stuff

    Note: connection is shared across instances of the class
    """
    _username = environ.get('reposit_user')
    _password = environ.get('reposit_pass')
    _api = None

    def __init__(self):
        " Instantiate a Reposit client object, and login "
        swagger_client.configuration.username = self._username
        swagger_client.configuration.password = self._password
        self._api = swagger_client.DefaultApi()
        self._token = self._api.auth_login_get().to_dict()['rp_token']
        swagger_client.configuration.api_key['Authorization'] = "RP-TOKEN %s" % self._token

    def deployment(self, userkey):
        " Return a deployment "
        return Deployment(userkey, self._api)

    @property
    def token(self):
        " Return the token "
        return self._token

    def logout(self):
        " Log this token out "
        self._api.auth_logout_get()

    @property
    def userkeys(self):
        " Return a list of user keys "
        return self._api.userkeys_get().to_dict().get('user_keys', [])

def test():
    " Brief method to test some stuff "
    client = Reposit()
    for key in client.userkeys:
        print("Your battery is %0.2f%% full" % (client.deployment(key).charge_percent))
        print("You are currently %s" % client.deployment(key).status)
    client.logout()

def status():
    " Return a status for the alexa skill "
    client = Reposit()
    key = client.userkeys[-1]
    answer = "Your battery is " + str(client.deployment(key).charge_percent) \
        + "%% full. You are currently " + client.deployment(key).status
    print("Reposit status message: " + answer)
    client.logout()
    return answer

if __name__ == '__main__':
    test()
