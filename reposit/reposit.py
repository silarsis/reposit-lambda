#!/usr/bin/env python
"""
Simple client
"""

from __future__ import print_function
from os  import environ
import time
import swagger_client
from expiringdict import ExpiringDict

class Deployment:
    " A deployment is essentially a house, I think "
    def __init__(self, userkey, api):
        self._userkey = userkey
        self._api = api
        self._cache = ExpiringDict(max_len=10, max_age_seconds=150)

    @property
    def battery_historical_soc(self):
        " Historical state of charge information - list of [timestamp, charge]"
        resp = self._cache.get('battery_soc')
        if not resp:
            now = int(time.time())
            resp = self._cache['battery_soc'] \
                = self._api.deployments_userkey_battery_historical_soc_get(
                    self._userkey, start=now-600)
            print("battery_historical_soc: %s" % str(resp))
            # Horrible hack because specifying a start seems to generate a 0 on the end for now
            if resp['battery_soc'][-1][1] == 0:
                del(resp['battery_soc'][-1])
        return resp.to_dict()

    @property
    def meter_historical_p(self):
        " Return true if we're feeding power to the grid "
        resp = self._cache.get('meter_historical_p')
        if not resp:
            now = int(time.time())
            resp = self._cache['meter_historical_p'] \
                = self._api.deployments_userkey_meter_historical_p_get(
                    self._userkey, start=now-600)
            print("meter_historical_p: %s" % str(resp))
        return resp.to_dict()

    @property
    def capacity(self):
        " Return battery capacity "
        return self.battery_historical_soc['battery_capacity']

    @property
    def charge(self):
        " Return the current battery charge "
        return self.battery_historical_soc['battery_soc'][-1][1]

    @property
    def charging(self):
        " Return true if currently charging, false otherwise "
        charge = self.battery_historical_soc['battery_soc']
        return charge[-1][1] > charge[-2][1]

    @property
    def charge_percent(self):
        " Percent charged "
        return (self.charge / self.capacity) * 100

    @property
    def feeding_grid(self):
        " Return true if we're feeding power to the grid "
        feed = self.meter_historical_p['meter_p']
        return feed[-1][1] < 0

    @property
    def status(self):
        " Return whether we're feeding the grid, charging, using battery, or flat and using power "
        soc = self.battery_historical_soc['battery_soc']
        if self.charge:
            return "charging your battery"
        if soc[-1][1] < soc[-2][1]:
            return "using battery power"
        if self.feeding_grid:
            return "feeding power to the grid"
        return "running off grid power"

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
        self._deployments = [Deployment(key, self._api) for key in self.userkeys]

    @property
    def deployments(self):
        " Return a list of deployment objects "
        return self._deployments

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
    for deployment in client.deployments:
        print("Your battery is %0.2f%% full" % (deployment.charge_percent))
        print("Your house is %s" % deployment.status)
    client.logout()

def status():
    " Return a status for the alexa skill "
    client = Reposit()
    percent = "%.0f" % client.deployments[-1].charge_percent
    answer = "Your battery is " + percent \
        + "% full. Your house is " + client.deployments[-1].status
    print("Reposit status message: " + answer)
    client.logout()
    return answer

if __name__ == '__main__':
    test()
