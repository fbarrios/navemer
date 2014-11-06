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
WINDOW_CAPTION = "NAVEMER - Sistema de Navegacion para Emergencias (Interfaz Vehículo)"
DEFAULT_LINE_COLOR = pygame.Color(70, 70, 125)

class GameWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        self.vbox = Gtk.VBox(False, 5)
        self.vbox.show()

        self.set_title(WINDOW_CAPTION)
        self.add(self.vbox)

        # Initialize the City backend part (Must be created before the Drawing Area)
        self.city = City()
        self.storage = Drawable_Object_Storage()
        self.init_point = None
        self.end_point = None

        self.create_window_interface()

        # Add some buttons
        '''
        hbox = Gtk.HBox(2, False)
        combo = Gtk.ComboBoxText()
        combo.append_text("BIRD")
        combo.append_text("IS")
        combo.set_active(0)
        vbox.pack_end(hbox, False, False, 0)

        self.button = Gtk.Button("Toggle Draw Area")
        self.button.connect("clicked", self.button_clicked, None)
        hbox.pack_end(combo, False, False, 0)
        hbox.pack_end(self.button, False, False, 0)
        hbox.show_all()
        '''
    

    def create_window_interface(self):
        # Zone 1
        self.create_menu()

        # Zone 2 
        # TODO

        # Zone 3
        self.create_map()

        # Zone 4
        self.create_origin_block_interface()

        # Zone 5
        self.create_destination_block_interface()

        # Zone 6
        self.create_toggle_button()


    def create_menu(self):
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
        self.vbox.pack_start(menu_bar, False, False, 0)
        menu_bar.show()

        file_item = Gtk.MenuItem()
        file_item.set_label("_File")
        file_item.set_use_underline(True)
        file_item.show()

        file_item.set_submenu(file_menu)
        menu_bar.append(file_item)


    def create_map(self):
        #create the drawing area
        da = Gtk.DrawingArea()
        da.set_size_request(WINDOW_SIZE[0], WINDOW_SIZE[1])
        self.vbox.pack_start(da, False, False, 0)
        da.connect("realize", self._realized)
        da.show()


    def create_origin_block_interface(self):
        vbox = Gtk.VBox(False, 5)
        self.vbox.pack_start(vbox, False, False, 0)

        hseparator = Gtk.HSeparator()
        main_label = Gtk.Label()
        hbox_main_label = Gtk.HBox(False, 5)
        main_label.set_text("Ingrese dirección de origen:")
        main_label.set_use_underline(True)
        hbox_main_label.pack_start(main_label, False, False, 5)

        # Street 1
        hbox_street_1 = Gtk.HBox(False, 5)
        label_street_1 = Gtk.Label()
        label_street_1.set_text("Calle Origen 1:   ")

        cb_street_1 = Gtk.ComboBoxText()
        cb_street_1.append_text("Campillo")
        cb_street_1.set_active(0)
        hbox_street_1.pack_start(label_street_1, False, False, 5)
        hbox_street_1.pack_start(cb_street_1, False, False, 0)

        # Street 2
        hbox_street_2 = Gtk.HBox(False, 5)
        label_street_2 = Gtk.Label()
        label_street_2.set_text("Calle Origen 2:   ")

        cb_street_2 = Gtk.ComboBoxText()
        cb_street_2.append_text("Torrent")
        cb_street_2.set_active(0)
        hbox_street_2.pack_start(label_street_2, False, False, 5)
        hbox_street_2.pack_start(cb_street_2, False, False, 0)

        # Add the streets to the container
        vbox.pack_start(hseparator, False, False, 0)
        vbox.pack_start(hbox_main_label, False, False, 0)
        vbox.pack_start(hbox_street_1, False, False, 0)
        vbox.pack_start(hbox_street_2, False, False, 0)
        vbox.show_all()


    def create_destination_block_interface(self):
        vbox = Gtk.VBox(False, 5)
        self.vbox.pack_start(vbox, False, False, 0)

        hseparator = Gtk.HSeparator()
        main_label = Gtk.Label()
        hbox_main_label = Gtk.HBox(False, 5)
        main_label.set_text("Ingrese dirección de destino:")
        main_label.set_use_underline(True)
        hbox_main_label.pack_start(main_label, False, False, 5)

        # Street 1
        hbox_street_1 = Gtk.HBox(False, 5)
        label_street_1 = Gtk.Label()
        label_street_1.set_text("Calle Destino 1:   ")

        cb_street_1 = Gtk.ComboBoxText()
        cb_street_1.append_text("Avenida Paseo Colon")
        cb_street_1.set_active(0)
        hbox_street_1.pack_start(label_street_1, False, False, 5)
        hbox_street_1.pack_start(cb_street_1, False, False, 0)

        # Street 2
        hbox_street_2 = Gtk.HBox(False, 5)
        label_street_2 = Gtk.Label()
        label_street_2.set_text("Calle Destino 2:   ")

        cb_street_2 = Gtk.ComboBoxText()
        cb_street_2.append_text("Avenida Independencia")
        cb_street_2.set_active(0)
        hbox_street_2.pack_start(label_street_2, False, False, 5)
        hbox_street_2.pack_start(cb_street_2, False, False, 0)

        # Add the streets to the container
        vbox.pack_start(hseparator, False, False, 0)
        vbox.pack_start(hbox_main_label, False, False, 0)
        vbox.pack_start(hbox_street_1, False, False, 0)
        vbox.pack_start(hbox_street_2, False, False, 0)
        vbox.show_all()


    def create_toggle_button(self):
        vbox = Gtk.VBox(False, 5)
        self.vbox.pack_start(vbox, False, False, 0)

        hseparator = Gtk.HSeparator()
        hbox = Gtk.HBox(False, 0)

        toggle_button = Gtk.ToggleButton("Calcular Ruta Optima")
        toggle_button.connect("clicked", self.change_system_state, None)

        hbox.pack_start(toggle_button, True, False, 0)
        vbox.pack_start(hseparator, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        vbox.show_all()


    def change_system_state(self, widget, data):
        if widget.get_active() == True:
            widget.set_label("Desactivar Sistema")
        else:
            widget.set_label("Calcular Ruta Optima")


    '''
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
    '''
        

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
