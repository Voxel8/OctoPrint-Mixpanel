# coding=utf-8
from __future__ import absolute_import

import sys

import octoprint.plugin
from mixpanel import Mixpanel
from netifaces import ifaddresses, AF_LINK


class MixpanelPlugin(octoprint.plugin.SettingsPlugin,
                     octoprint.plugin.AssetPlugin,
                     octoprint.plugin.EventHandlerPlugin):

    def on_event(self, event, payload):
        if event not in [
            'Startup',
            'ClientOpened',
            'ClientClosed',
            'Connected',
            'Disconnected',
            'Error',
            'Upload',
            'PrintStarted',
            'PrintDone',
            'PrintCancelled',
            'PrintPaused',
            'PrintResumed',
            ]:
            return

        if not hasattr(self, 'mp'):
            ethernet = 'en0' if sys.platform == 'darwin' else 'eth0'
            token = self._settings.get(['token'])
            self.mp = Mixpanel(token)
            self.mac = ifaddresses(ethernet)[AF_LINK][0]['addr']
        self.mp.track(self.mac, event, payload)

    ##~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            token='',
        )

    ##~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            #js=["js/mixpanel.js"],
            #css=["css/mixpanel.css"],
            #less=["less/mixpanel.less"]
        )

    ##~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            mixpanel=dict(
                displayName="Mixpanel Plugin",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_commit",
                user="Voxel8",
                repo="OctoPrint-Mixpanel",
                current=self._plugin_version,
                branch="master",

                # update method: pip
                pip="https://github.com/jminardi/OctoPrint-Mixpanel/archive/{target_version}.zip"
            )
        )


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Mixpanel Plugin"

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = MixpanelPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

