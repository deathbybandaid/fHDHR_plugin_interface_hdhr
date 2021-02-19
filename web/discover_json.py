from flask import Response, request
import json


class Discover_JSON():
    endpoints = ["/discover.json", "/hdhr/discover.json"]
    endpoint_name = "hdhr_discover_json"

    def __init__(self, fhdhr, plugin_utils):
        self.fhdhr = fhdhr
        self.plugin_utils = plugin_utils
        self.interface = self.fhdhr.device.interfaces[self.plugin_utils.namespace]

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        base_url = request.url_root[:-1]

        origindiscover_list = []
        for origin in self.fhdhr.origins.valid_origins:
            origindiscover = self.interface.get_discover_dict(origin, base_url)
            origindiscover_list.append(origindiscover)

        return Response(status=200,
                        response=json.dumps(origindiscover_list, indent=4),
                        mimetype='application/json')

        origindiscover = {}
        if self.interface.source in self.fhdhr.origins.valid_origins:
            origindiscover = self.interface.get_discover_dict(self.interface.source, base_url)

        return Response(status=200,
                        response=json.dumps(origindiscover, indent=4),
                        mimetype='application/json')
