#!/usr/bin/env python
"""
Simple client
"""

from __future__ import print_function
from os  import environ
import time
import threading
import swagger_client
from expiringdict import ExpiringDict

class Deployment:
    " A deployment is essentially a house, I think "
    def __init__(self, userkey, api):
        self._userkey = userkey
        self._api = api
        self._cache = ExpiringDict(max_len=10, max_age_seconds=150)

    def _get(self, key):
        resp = self._cache.get(key)
        if not resp:
            now = int(time.time())
            resp = self._cache[key] \
                = getattr(self._api, 'deployments_userkey_%s_get' % key)(
                    self._userkey, start=now-300)
            print("%s: %s" % (key, str(resp)))
        dresp = resp.to_dict()
        # Horrible hack because specifying a start seems to generate a 0 on the end for now
        internal_key = key.replace('_historical', '')
        del(dresp[internal_key][-1])
        return dresp

    @property
    def battery_historical_soc(self):
        " Historical state of charge information - list of [timestamp, charge]"
        return self._get('battery_historical_soc')

    @property
    def meter_historical_p(self):
        " Return true if we're feeding power to the grid "
        return self._get('meter_historical_p')

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
    def discharging(self):
        " Return true if currently using battery power, false otherwise "
        charge = self.battery_historical_soc['battery_soc']
        return charge[-1][1] < charge[-2][1]

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
        if self.charging:
            return "charging your battery"
        if self.discharging:
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
        self._token = self._api.auth_login_post().to_dict()['access_token']
        swagger_client.configuration.api_key['Authorization'] = "Bearer %s" % self._token
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
