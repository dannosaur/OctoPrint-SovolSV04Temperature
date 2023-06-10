import octoprint.plugin
import re


class SovolSV04TemperaturePlugin(octoprint.plugin.OctoPrintPlugin):
    pattern = re.compile(
        r'^ T\d:\d+\.\d+ /\d+\.\d+ '
        r'B:(?P<bed_actual>\d+\.\d+) /(?P<bed_set>\d+\.\d+) '
        r'T0:(?P<tool0_actual>\d+\.\d+) /(?P<tool0_set>\d+\.\d+) '
        r'T1:(?P<tool1_actual>\d+\.\d+) /(?P<tool1_set>\d+\.\d+) '
        r'(?P<extra>.*)$'
    )

    def parse_temperature_line(self, comm_instance, line, *args, **kwargs):
        matches = self.pattern.match(line)
        if matches:
            tool0_set = matches.group('tool0_set')
            tool0_actual = matches.group('tool0_actual')
            tool1_set = matches.group('tool1_set')
            tool1_actual = matches.group('tool1_actual')
            bed_set = matches.group('bed_set')
            bed_actual = matches.group('bed_actual')
            extra = matches.group('extra')
            sane = f' T0:{tool0_actual} /{tool0_set}' \
                   f' T1:{tool1_actual} /{tool1_set}' \
                   f' B:{bed_actual} /{bed_set}' \
                   f' {extra}'
            return sane
        return line

    def get_update_information(self):
        return {
            "SovolSV04Temperature": {
                "displayName": "Sovol SV04 Temperature",
                "displayVersion": self._plugin_version,

                # version check: github repository
                "type": "github_release",
                "user": "dannosaur",
                "repo": "OctoPrint-SovolSV04Temperature",
                "current": self._plugin_version,

                # update method: pip
                "pip": "https://github.com/dannosaur/OctoPrint-SovolSV04Temperature/archive/{target_version}.zip",
            }
        }


__plugin_name__ = "Sovol SV04 Temperature"
__plugin_pythoncompat__ = ">=3,<4"


def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = SovolSV04TemperaturePlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        'octoprint.comm.protocol.gcode.received': __plugin_implementation__.parse_temperature_line,
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
