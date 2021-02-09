
from .discover_json import Discover_JSON
from .discover_json_origin import Discover_JSON_Origin

from .lineup_json import Lineup_JSON
from .lineup_json_origin import Lineup_JSON_Origin

from .lineup_xml import Lineup_XML

from .lineup_status_json import Lineup_Status_JSON

from .lineup_post import Lineup_Post
from .device_xml import HDHR_Device_XML

from .auto import Auto
from .tuner import Tuner


class Plugin_OBJ():

    def __init__(self, fhdhr, plugin_utils):
        self.fhdhr = fhdhr
        self.plugin_utils = plugin_utils

        self.lineup_post = Lineup_Post(fhdhr)

        self.device_xml = HDHR_Device_XML(fhdhr)

        self.auto = Auto(fhdhr)
        self.tuner = Tuner(fhdhr)

        self.lineup_xml = Lineup_XML(fhdhr)

        self.lineup_status_json = Lineup_Status_JSON(fhdhr)

        self.discover_json = Discover_JSON(fhdhr)
        self.discover_json_origin = Discover_JSON_Origin(fhdhr)

        self.lineup_json = Lineup_JSON(fhdhr)
        self.lineup_json_origin = Lineup_JSON_Origin(fhdhr)
