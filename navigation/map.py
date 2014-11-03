#!/usr/bin/env python
# -*- coding: latin-1

# Proyect libraries
import random
from city import City
from point import MapPoint
from Drawable_Objects.Line import Line
from Drawable_Objects.Route import Route
from Drawable_Objects.Drawable_Object_Storage import Drawable_Object_Storage

# Pygame libraries
import os
import pygame
from pygame.locals import *
from gi.repository import GObject
from gi.repository import Gtk
from gi.repository import GdkX11

# Miscellaneous constants.
MAP_FILE = "city/map.png"
WINDOW_SIZE = 1006, 397
WINDOW_CAPTION = "Sistema de Navegacion para Emergencias"
DEFAULT_LINE_COLOR = pygame.Color(70, 70, 125)

class GameWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        vbox = Gtk.VBox(False, 2)
        vbox.show()
        self.add(vbox)

        #create the menu
        file_menu = Gtk.Menu()

        accel_group = Gtk.AccelGroup()
        self.add_accel_group(accel_group)

        dialog_item = Gtk.MenuItem()
        dialog_item.set_label("Dialog")
        dialog_item.show()
        dialog_item.connect("activate",self.show_dialog)
        file_menu.append(dialog_item)
        dialog_item.show()

        quit_item = Gtk.MenuItem()
        quit_item.set_label("Quit")
        quit_item.show()
        quit_item.connect("activate",self.quit)
        file_menu.append(quit_item)
        quit_item.show()

        menu_bar = Gtk.MenuBar()
        vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        file_item = Gtk.MenuItem()
        file_item.set_label("_File")
        file_item.set_use_underline(True)
        file_item.show()

        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)

        # City part (Must be created before the Drawing Area)
        self.city = City()
        self.storage = Drawable_Object_Storage()
        self.init_point = None
        self.end_point = None
        
        #create the drawing area
        da = Gtk.DrawingArea()
        da.set_size_request(WINDOW_SIZE[0], WINDOW_SIZE[1])
        vbox.pack_end(da, False, False, 0)
        da.connect("realize", self._realized)
        da.show()

        #collect key press events
        self.connect("key-press-event", self.key_pressed)


    def key_pressed(self, widget, event, data=None):
        # Draws a random route taken from the navigation module.
        if self.init_point == None:
            self.init_point = self.city.get_random_intersection()
            self.end_point = self.city.get_random_intersection()
        else:
            self.init_point = self.end_point
            self.end_point = self.city.get_random_intersection()

        self.create_and_add_route( 
            self.city.get_route_between_intersections(self.init_point, 
                                                      self.end_point))
        

    def show_dialog(self, widget, data=None):
        #prompts.info("A Pygtk Dialog", "See it works easy")
        title = "PyGame embedded in Gtk Example"
        dialog = Gtk.Dialog(title, 
                            None, 
                            Gtk.DialogFlags.MODAL,(Gtk.STOCK_CANCEL, 
                                                   Gtk.ResponseType.CANCEL, 
                                                   Gtk.STOCK_OK, 
                                                   Gtk.ResponseType.OK))

        content_area = dialog.get_content_area()
        label = Gtk.Label("See, it still works")
        label.show()
        content_area.add(label)
        response = dialog.run()
        dialog.destroy()


    def quit(self, widget, data=None):
        self.destroy()


    def draw(self):
        self.screen.blit(self.background,[0,0])
        self.storage.draw_objects()
        pygame.display.flip()
        return True


    def _realized(self, widget, data=None):
        # pygame.display.set_caption(WINDOW_CAPTION)
        os.putenv('SDL_WINDOWID', str(widget.get_window().get_xid()))        
        pygame.init()
        pygame.display.set_mode(WINDOW_SIZE, 0, 0)
        self.background = pygame.image.load(MAP_FILE).convert()
        self.screen = pygame.display.get_surface()
        GObject.timeout_add(10, self.draw)


    def create_and_add_route(self, route, line_color=None):
        lines = []

        for i in range(len(route) - 1):
            map_prev = route[i].point.convert_to_map_point().get_tuple()
            map_current = route[i + 1].point.convert_to_map_point().get_tuple()

            if line_color is None:
                line_color = pygame.Color(random.randint(0,255),
                                          random.randint(0,255),
                                          random.randint(0,255))

            lines.append(Line(self.screen, map_prev, map_current, 5, line_color))

        route = Route(self.screen, lines)
        self.storage.add_object(route)

        return route


if __name__ == "__main__":
    window = GameWindow()
    window.connect("destroy",Gtk.main_quit)
    window.show()
    Gtk.main()
