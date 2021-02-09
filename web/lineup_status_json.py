from flask import Response
import json


class Lineup_Status_JSON():
    endpoints = ["/hdhr/<devicekey>/lineup_status.json"]
    endpoint_name = "hdhr_lineup_status_json"

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, devicekey, *args):
        return self.get(devicekey, *args)

    def get(self, devicekey, *args):

        if devicekey.startswith(self.fhdhr.config.dict["main"]["uuid"]):
            origin = devicekey.split(self.fhdhr.config.dict["main"]["uuid"])[-1]

            tuner_status = self.fhdhr.device.tuners.status(origin)
            tuners_scanning = 0
            for tuner_number in list(tuner_status.keys()):
                if tuner_status[tuner_number]["status"] == "Scanning":
                    tuners_scanning += 1

            channel_count = len(list(self.fhdhr.device.channels.list[origin].keys()))

            if tuners_scanning:
                jsonlineup = self.scan_in_progress(origin)
            elif not channel_count:
                jsonlineup = self.scan_in_progress(origin)
            else:
                jsonlineup = self.not_scanning()
            lineup_json = json.dumps(jsonlineup, indent=4)

        else:
            lineup_json = {}

        return Response(status=200,
                        response=lineup_json,
                        mimetype='application/json')

    def scan_in_progress(self, origin):

        channel_count = len(list(self.fhdhr.device.channels.list[origin].keys()))

        jsonlineup = {
                      "ScanInProgress": "true",
                      "Progress": 99,
                      "Found": channel_count
                      }
        return jsonlineup

    def not_scanning(self):
        jsonlineup = {
                      "ScanInProgress": "false",
                      "ScanPossible": "true",
                      "Source": self.fhdhr.config.dict["hdhr"]["reporting_tuner_type"],
                      "SourceList": [self.fhdhr.config.dict["hdhr"]["reporting_tuner_type"]],
                      }
        return jsonlineup
