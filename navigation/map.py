#! /usr/bin/env python
# -*- coding: latin-1

# Proyect libraries
import random
from city import City
from point import MapPoint
from Drawable_Objects.Line import Line
from Drawable_Objects.Route import Route
from Drawable_Objects.Drawable_Object_Storage import Drawable_Object_Storage
from Drawable_Objects.Dynamic_Object import Dynamic_Object
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

        # TODO: Ugly, try to improve this mechanism
        self.last_route_id = -1

        # Initialize the City backend part 
        # (Must be created before the Drawing Area)
        self.city = City()
        self.storage = Drawable_Object_Storage()

        # Create the PyGtk Interface
        self.create_window_interface()


    def create_window_interface(self):
        self.create_menu()
        # Zone 2 
        # TODO
        self.create_map()
        self.create_source_block_interface()
        self.create_dest_block_interface()
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
        hbox = Gtk.HBox(False, 0)
        da = Gtk.DrawingArea()
        da.set_size_request(WINDOW_SIZE[0], WINDOW_SIZE[1])

        hbox.pack_start(da, True, False, 0)
        self.vbox.pack_start(hbox, False, False, 0)

        da.connect("realize", self._realized)
        hbox.show_all()


    def create_source_block_interface(self):
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

        self.cb_source_street_1 = Gtk.ComboBoxText()        
        hbox_street_1.pack_start(label_street_1, False, False, 5)
        hbox_street_1.pack_start(self.cb_source_street_1, False, False, 0)

        # Street 2
        hbox_street_2 = Gtk.HBox(False, 5)
        label_street_2 = Gtk.Label()
        label_street_2.set_text("Calle Origen 2:   ")

        self.cb_source_street_2 = Gtk.ComboBoxText()
        hbox_street_2.pack_start(label_street_2, False, False, 5)
        hbox_street_2.pack_start(self.cb_source_street_2, False, False, 0)


        # Fill the combo box one (has all the street) and the second combo
        streets = self.city.get_streets()
        for street in streets.itervalues():
            self.cb_source_street_1.append_text(street.get_name())
        self.cb_source_street_1.set_active(random.randint(0, len(streets)-1))

        self.fill_second_combo_box(streets, 
                                   self.cb_source_street_1, 
                                   self.cb_source_street_2)

        # Add the signal for the comboboxes
        self.cb_source_street_1.connect("changed", 
                                        self.combobox_change, 
                                        self.cb_source_street_2)

        # Add the streets to the container
        vbox.pack_start(hseparator, False, False, 0)
        vbox.pack_start(hbox_main_label, False, False, 0)
        vbox.pack_start(hbox_street_1, False, False, 0)
        vbox.pack_start(hbox_street_2, False, False, 0)
        vbox.show_all()


    def create_dest_block_interface(self):
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

        self.cb_dest_street_1 = Gtk.ComboBoxText()

        hbox_street_1.pack_start(label_street_1, False, False, 5)
        hbox_street_1.pack_start(self.cb_dest_street_1, False, False, 0)

        # Street 2
        hbox_street_2 = Gtk.HBox(False, 5)
        label_street_2 = Gtk.Label()
        label_street_2.set_text("Calle Destino 2:   ")

        self.cb_dest_street_2 = Gtk.ComboBoxText()
        self.cb_dest_street_2.append_text("Avenida Independencia")
        self.cb_dest_street_2.set_active(0)
        hbox_street_2.pack_start(label_street_2, False, False, 5)
        hbox_street_2.pack_start(self.cb_dest_street_2, False, False, 0)

        # Fill the combo box one (has all the street) and the second combo
        streets = self.city.get_streets()
        for street in streets.itervalues():
            self.cb_dest_street_1.append_text(street.get_name())
        self.cb_dest_street_1.set_active(random.randint(0, len(streets)-1))

        self.fill_second_combo_box(streets, 
                                   self.cb_dest_street_1, 
                                   self.cb_dest_street_2)

        # Add the signal for the comboboxes
        self.cb_dest_street_1.connect("changed", 
                                      self.combobox_change, 
                                      self.cb_dest_street_2)

        # Add the streets to the container
        vbox.pack_start(hseparator, False, False, 0)
        vbox.pack_start(hbox_main_label, False, False, 0)
        vbox.pack_start(hbox_street_1, False, False, 0)
        vbox.pack_start(hbox_street_2, False, False, 0)
        vbox.show_all()


    def fill_second_combo_box(self, streets, combo1, combo2):
        # Fill the second combo box (has the streets that 
        # intersects with the street on the combo 1)
        street_one = streets[combo1.get_active_text()]
        intersection = self.city.get_streets_names_who_intersect_with_a_street(street_one)

        model = combo2.get_model()
        model.clear()
        combo2.set_model(model)

        for intersected_street in intersection:
            combo2.append_text(intersected_street)

        combo2.set_active(random.randint(0, len(intersection)-1))


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


    def combobox_change(self, widget, data):
        streets = self.city.get_streets()
        street_one = streets[widget.get_active_text()]
        self.fill_second_combo_box(streets, widget, data)


    def change_system_state(self, widget, data):
        if widget.get_active() == True:
            widget.set_label("Desactivar Sistema")

            # Get the intersections of the streets
            streets = self.city.get_streets()

            street1_source = streets[self.cb_source_street_1.get_active_text()]
            street2_source = streets[self.cb_source_street_2.get_active_text()]
            intersection_source = street1_source.intersect_street(street2_source)

            street1_dest = streets[self.cb_dest_street_1.get_active_text()]
            street2_dest = streets[self.cb_dest_street_2.get_active_text()]
            intersection_dest = street1_dest.intersect_street(street2_dest)

            # Draw the route
            try:
                route = self.city.get_route_between_intersections(list(intersection_source)[0],
                                                                  list(intersection_dest)[0])
                self.create_and_add_route(route)
            except:
                print "FATAL ERROR. Intersection not calculated properly"

            # Draw the ambulance
            if self.ambulance_id != -1:
                int_source = self.city.get_intersection(list(intersection_source)[0])
                ambulance = self.storage.get_object(self.ambulance_id)
                pos = int_source.point.convert_to_map_point().get_tuple()
                ambulance.set_pos(pos)
                ambulance.visible = True

        else:
            # TODO: Ugly, try to improve this mechanism
            if self.last_route_id != -1:
                self.storage.remove_object(self.last_route_id)

            if self.ambulance_id != -1:
                ambulance = self.storage.get_object(self.ambulance_id)
                ambulance.visible = False

            self.last_route_id = -1
            widget.set_label("Calcular Ruta Óptima")
        

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

        # Create an add an ambulance (make it invisible until someone clicked the toggle button)
        ambulance = Dynamic_Object(self.screen, (0,0), "Drawable_Objects/ambulance.jpg")
        ambulance.visible = False
        self.ambulance_id = ambulance.id()
        self.storage.add_object(ambulance)


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

        # TODO: Ugly, try to improve this mechanism
        if self.last_route_id != -1:
            self.storage.remove_object(self.last_route_id)

        self.last_route_id = route.id()
        self.storage.add_object(route)

        return route


if __name__ == "__main__":
    window = GameWindow()
    window.connect("destroy",Gtk.main_quit)
    window.show()
    Gtk.main()
