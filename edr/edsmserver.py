from __future__ import absolute_import

import json

from edrconfig import EDRConfig
from edrlog import EDRLog

import requests


EDRLOG = EDRLog()

class EDSMServer(object):

    SESSION = requests.Session()

    def __init__(self):
        config = EDRConfig()
        self.EDSM_API_KEY = config.edsm_api_key()
        self.EDSM_SERVER = config.edsm_server()

    def system(self, system_name):
        params = {"systemName": system_name, "showCoordinates": 1, "showInformation":1, "showId": 1}
        endpoint = "{}/api-v1/systems".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve system {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None
        
        return json.loads(resp.content)

    def bodies(self, system_name):
        params = {"systemName": system_name}
        endpoint = "{}/api-system-v1/bodies".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve bodies for {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None
        
        system_and_bodies = json.loads(resp.content)
        return system_and_bodies.get("bodies", None)

    def systems_within_radius(self, system_name, radius):
        params = {"systemName": system_name, "showCoordinates": 1, "radius": radius, "showInformation": 1, "showId": 1, "showPermit": 1}
        endpoint = "{}/api-v1/sphere-systems".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve system {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None

        results = json.loads(resp.content)
        if not results:
            EDRLOG.log(u"Empty systems within radius.", "INFO")
            return []
        sorted_results = sorted(results, key=lambda t: t["distance"])
        return sorted_results

    def stations_in_system(self, system_name):
        params = {"systemName": system_name}
        endpoint = "{}/api-system-v1/stations".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve system {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None

        results = json.loads(resp.content)
        if not results or not results.get('stations', None):
            EDRLOG.log(u"No stations in system {}.".format(system_name), "INFO")
            return []
        sorted_results = sorted(results['stations'], key=lambda t: t["distanceToArrival"])
        return sorted_results

    def factions_in_system(self, system_name):
        params = {"systemName": system_name}
        endpoint = "{}/api-system-v1/factions".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve state for system {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None

        return json.loads(resp.content)

    def deaths(self, system_name):
        params = {"systemName": system_name}
        endpoint = "{}/api-system-v1/deaths".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve deaths info for {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None
        
        return json.loads(resp.content)

    def traffic(self, system_name):
        params = {"systemName": system_name}
        endpoint = "{}/api-system-v1/traffic".format(self.EDSM_SERVER)
        resp = EDSMServer.SESSION.get(endpoint, params=params)

        if resp.status_code != requests.codes.ok:
            EDRLOG.log(u"Failed to retrieve traffic info for {} from EDSM: {}.".format(system_name, resp.status_code), "ERROR")
            return None
        
        return json.loads(resp.content)