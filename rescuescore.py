#!/usr/bin/env python2
from __future__ import division

import pygtk

from rescuetime_wrapper import get_efficiency


pygtk.require('2.0')
import gtk
from gtk import gdk

gtk.gdk.threads_init()
import gobject
import cairo
#Parameters


class RescueScore:
    def __init__(self):
        self.initialize_text_tray()
        self.icon = gtk.StatusIcon()
        efficiency, _ = get_efficiency()
        p = self.text_to_pixbuf(str(efficiency) + " ")
        self.icon.set_from_pixbuf(p)
        self.icon.set_tooltip("Idle")
        self.minute_milliseconds = 6000  #number of milliseconds in a minute
        self.icon.connect('activate', self.icon_click)
        self.icon.set_visible(True)
        self.old_hour = ""

    def initialize_text_tray(self):
        self.traySize = 19
        self.trayPixbuf = gdk.Pixbuf(gdk.COLORSPACE_RGB, True, 8, self.traySize, self.traySize)
        self.trayPixbuf.fill(0x00000000)

        self.pixmap = self.trayPixbuf.render_pixmap_and_mask(alpha_threshold=127)[0]
        self.cr = self.pixmap.cairo_create()
        self.cr.select_font_face("Georgia", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        self.color_seen = (1, 1, 1, 1)
        self.cr.set_source_rgba(*self.color_seen)
        default_font_size = 20
        self.cr.set_font_size(default_font_size)
        self.trayPixbuf.get_from_drawable(self.pixmap, self.pixmap.get_colormap(),
                                          0, 0, 0, 0, self.traySize, self.traySize)
        self.trayPixbuf = self.trayPixbuf.add_alpha(True, 0x00, 0x00, 0x00)

    def text_to_pixbuf(self, text):
        self.cr.set_operator(cairo.OPERATOR_CLEAR)
        self.cr.paint()
        self.cr.set_operator(cairo.OPERATOR_SOURCE)
        color = self.color_seen
        self.cr.set_source_rgba(*color)
        self.cr.move_to(0, 16)
        self.cr.set_font_size(15)
        self.cr.show_text(text)
        self.trayPixbuf.get_from_drawable(self.pixmap, self.pixmap.get_colormap(), 0, 0, 0, 0,
                                          self.traySize, self.traySize)
        p = self.trayPixbuf.add_alpha(True, 0x00, 0x00, 0x00)
        return p

    def icon_click(self, dummy):
        self.update()

    def update(self):
        """This method is called everytime a tick interval occurs"""

        #Get this hour efficiency
        efficiency, hour = get_efficiency()
        if hour == self.old_hour:
            pass
        else:
            self.old_hour = hour
            p = self.text_to_pixbuf(str(efficiency) + " ")
            self.icon.set_from_pixbuf(p)
        source_id = gobject.timeout_add(self.minute_milliseconds * 10, self.update)
        # return True

    def main(self):
        # All PyGTK applications must have a gtk.rescuetime_wrapper.py(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).

        pass
        source_id = gobject.timeout_add(self.minute_milliseconds, self.update)
        gtk.main()

# If the program is run directly or passed as an argument to the python
# interpreter then create a RescueScore instance and show it
if __name__ == "__main__":
    app = RescueScore()
    app.main()
