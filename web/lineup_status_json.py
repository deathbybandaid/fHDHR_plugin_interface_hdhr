from flask import Response
import json


class Lineup_Status_JSON():
    endpoints = ["lineup_status.json"]
    endpoint_name = "hdhr_lineup_status_json"

    def __init__(self, fhdhr):
        self.fhdhr = fhdhr

    def __call__(self, *args):
        return self.get(*args)

    def get(self, *args):

        tuners_scanning = 0
        for origin in self.fhdhr.origins.valid_origins:

            tuner_status = self.fhdhr.device.tuners.status(origin)

            for tuner_number in list(tuner_status.keys()):
                if tuner_status[tuner_number]["status"] == "Scanning":
                    tuners_scanning += 1

        if tuners_scanning:
            jsonlineup = self.scan_in_progress()
        else:
            jsonlineup = self.not_scanning()
        lineup_json = json.dumps(jsonlineup, indent=4)

        return Response(status=200,
                        response=lineup_json,
                        mimetype='application/json')

    def scan_in_progress(self):
        jsonlineup = {
                      "ScanInProgress": "true",
                      "Progress": 99,
                      "Found": 1
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
