#!/usr/bin/env python

import sys
try:
    import gtk
    import gtk.glade
    import gobject
    import pygame
    import os
    from time import sleep
    pygtk.require("2.0")
except:
    pass

class MainClass:

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def callback(self, widget, data):
        self.glade.get_object("buttonsLabel").set_text("Button %s was clicked" % data)

    def main(self):
        # Event loop
        while 1:
            self.draw()
            gtk.main_iteration(False)
            sleep(0.01)


    def __init__(self):
        #Set the Glade file
        self.gladefile = "PyGTK_Glade.glade" 
        self.glade = gtk.Builder()
        self.glade.add_from_file(self.gladefile)
        self.glade.connect_signals(self)

        # Connect the signal clicked of the buttons to a label to test the callback association
        # with Glade
        self.main_window = self.glade.get_object("window")
        self.main_window.show_all()
        self.glade.get_object("button1").connect("clicked", self.callback, "button1")
        self.glade.get_object("button2").connect("clicked", self.callback, "button2")

        # Set the drawing area created in Glade to wrap the PyGame canvas
        da = self.glade.get_object("drawing_area")
        da.set_size_request(640,480)    
        da.realize()

        # Force SDL to write on our drawing area
        os.putenv('SDL_WINDOWID', str(da.window.xid))

        # We need to flush the XLib event loop otherwise we can't
        # access the XWindow which set_mode() requires
        gtk.gdk.flush()

        pygame.init()
        pygame.display.set_mode((640, 480), 0, 0)

        #set up the pygame objects
        self.image = pygame.image.load("ball.bmp")
        self.background = pygame.image.load("background.jpg")
        self.x = 0
        self.y = 0
        self.screen = pygame.display.get_surface()

        self.screen.blit(self.background, [0, 0])
        gobject.idle_add(pygame.display.update)

        #collect key press events
        self.main_window.connect("key-press-event", self.key_pressed)

    def key_pressed(self, widget, event, data=None):
        if event.keyval == 65361:
            self.x -= 5
        elif event.keyval == 65362:
            self.y -= 5
        elif event.keyval == 65363:
            self.x += 5
        elif event.keyval == 65364:
            self.y += 5

    def draw(self):
        self.screen.blit(self.background, [0,0])
        rect = self.image.get_rect()
        rect.x = self.x
        rect.y = self.y
        self.screen.blit(self.image, rect)
        pygame.display.flip()
        return True

if __name__ == "__main__":
    base = MainClass()
    base.main()
