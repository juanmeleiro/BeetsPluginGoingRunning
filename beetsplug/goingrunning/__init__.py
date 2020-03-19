#  Copyright: Copyright (c) 2020., Adam Jakab
#
#  Author: Adam Jakab <adam at jakab dot pro>
#  Created: 2/19/20, 11:30 AM
#  License: See LICENSE.txt
#
import os

from beets.plugins import BeetsPlugin
from beets.util.confit import ConfigSource, load_yaml

from beetsplug.goingrunning import common as GRC
from beetsplug.goingrunning.command import GoingRunningCommand


class GoingRunningPlugin(BeetsPlugin):
    _default_plugin_config_file_name_ = 'config_default.yml'

    def __init__(self):
        super(GoingRunningPlugin, self).__init__()
        config_file_path = os.path.join(os.path.dirname(__file__), self._default_plugin_config_file_name_)
        source = ConfigSource(load_yaml(config_file_path) or {}, config_file_path)
        self.config.add(source)

    def commands(self):
        return [GoingRunningCommand(self.config)]

    # fixme: This creates conflict with the acousticbrainz plugin because of a bug in beets/plugins.py:340
    # @property
    # def item_types(self):
    #     """Declare FLOAT types for numeric flex attributes so that query parser will correctly use NumericQuery for
    #     them
    #     """
    #     t = {}
    #     for attr in GRC.KNOWN_NUMERIC_FLEX_ATTRIBUTES:
    #         t[attr] = types.FLOAT
    #
    #     return t
