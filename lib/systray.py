#!/usr/bin/env python

import plugin
import os
if os.name == "nt":
    import winsystray as ossystray
    import subprocess
import time


icon = "lib/systrayicon.ico"
hover_text = "NMControl"

httpGuiUrl = "http://127.0.0.2"  # should be scraped from serviceHTTP.py or moved to common.py

def launch_httpGui(sti):
    if os.name == "nt":  # windows
        subprocess.call(["cmd", "/c", "start", httpGuiUrl])
    else:
        os.system(httpGuiUrl)  # untestet, probably wrong

class SystrayThread(plugin.PluginThread):
    name = 'systray'
    def __init__(self, app):
        self.app = app
        self.menu_options = (('httpGui', None, launch_httpGui),)  # menu icons should somehow be possible via the middle option
        plugin.PluginThread.__init__(self)

    def pStart(self):
        if self.app['debug']: print "Systray.py: Plugin %s parent start" %(self.name)
        self.sti = ossystray.SysTrayIcon(icon, hover_text, self.menu_options, on_quit=self.do_quit, default_menu_index=None)
        self.running = 1
        while 1:
            self.sti.pump()
            if not self.running:
                break
            time.sleep(0.1)

    def pStop(self, arg = []):
        if self.app['debug']: print "Plugin %s parent stop" %(self.name)
        self.running = False
        self.sti.do_quit()
        return True

    def do_quit(self, sti):
        if self.app['debug']: print "Systray.py: do_quit"
        self.app['plugins']['main'].stop()  # will bail if already shutting down
