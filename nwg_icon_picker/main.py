#!/usr/bin/env python

import os

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib

from nwg_icon_picker.tools import *

dir_name = os.path.dirname(__file__)

gtk_theme_name = ""
gtk_icon_theme = None
contexts = []
search_entry = None
result_label = None
button = None

grid = None
icon_names = []
icon_list = None


def build_context_listbox():
    listbox = Gtk.ListBox.new()
    for context in contexts:
        row = ContextListRow(context)
        listbox.add(row)

    return listbox


class ContextListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super().__init__()
        eb = Gtk.EventBox.new()
        self.add(eb)
        eb.connect("button-press-event", build_icon_list, name)
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        eb.add(box)
        lbl = Gtk.Label.new(name)
        box.pack_start(lbl, False, False, 0)


def on_search_changed(sb):
    global icon_list, grid, result_label

    phrase = sb.get_text()
    if phrase and len(phrase) > 2:
        if icon_list:
            icon_list.destroy()
        scrolled_window = Gtk.ScrolledWindow.new(None, None)
        scrolled_window.set_propagate_natural_width(True)
        scrolled_window.set_propagate_natural_height(True)
        icon_list = scrolled_window
        grid.attach(scrolled_window, 1, 1, 1, 1)
        lb = Gtk.ListBox.new()
        scrolled_window.add(lb)

        for name in icon_names:
            if phrase in name:
                row = IconListRow(name)
                lb.add(row)

        grid.show_all()
        return scrolled_window


def build_icon_list(ebox, ebtn, context=None):
    global icon_list, grid, result_label
    if icon_list:
        icon_list.destroy()

    scrolled_window = Gtk.ScrolledWindow.new(None, None)
    scrolled_window.set_propagate_natural_width(True)
    scrolled_window.set_propagate_natural_height(True)
    grid.attach(scrolled_window, 1, 1, 1, 1)

    if context:
        icon_names_in_ctx = gtk_icon_theme.list_icons(context)
        icon_names_in_ctx.sort(key=str.casefold)

        icon_list = scrolled_window
        lb = Gtk.ListBox.new()
        scrolled_window.add(lb)
        for name in icon_names_in_ctx:
            row = IconListRow(name)
            lb.add(row)

        result_label.set_markup("{} icons in <b>{}</b>".format(len(icon_names_in_ctx), context))

    grid.show_all()

    return scrolled_window


class IconListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super().__init__()
        eb = Gtk.EventBox.new()
        self.add(eb)
        eb.connect("button-press-event", update_button, name)
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        eb.add(box)
        """pixbuf = gtk_icon_theme.load_icon(name, 16,
                                          Gtk.IconLookupFlags.FORCE_SIZE |
                                          Gtk.IconLookupFlags.FORCE_SYMBOLIC)"""
        pixbuf = gtk_icon_theme.load_icon(name, 16,
                                          Gtk.IconLookupFlags.FORCE_SIZE |
                                          Gtk.IconLookupFlags.GENERIC_FALLBACK |
                                          Gtk.IconLookupFlags.USE_BUILTIN)
        img = Gtk.Image.new_from_pixbuf(pixbuf)
        box.pack_start(img, False, False, 6)
        lbl = Gtk.Label.new(name)
        box.pack_start(lbl, False, False, 0)


def update_button(ebox, ebtn, name):
    global button
    img = Gtk.Image.new_from_icon_name(name, Gtk.IconSize.DIALOG)
    button.set_image(img)
    button.set_label(name)



def main():
    GLib.set_prgname('nwg-icon-picker')

    window = Gtk.Window()
    window.connect("destroy", Gtk.main_quit)

    global gtk_theme_name
    gtk_settings = Gtk.Settings.get_default()
    gtk_theme_name = gtk_settings.get_property("gtk-icon-theme-name")
    eprint("Icon theme: {}".format(gtk_theme_name))

    global gtk_icon_theme
    gtk_icon_theme = Gtk.IconTheme.get_default()

    global contexts
    contexts = gtk_icon_theme.list_contexts()

    global icon_names
    icon_names = gtk_icon_theme.list_icons()

    # print(gtk_icon_theme.lookup_icon("foot", 48, 0).get_filename())

    hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
    hbox.set_property("margin", 6)
    window.add(hbox)

    vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
    hbox.pack_start(vbox, True, True, 0)

    global button
    button = Gtk.Button.new_from_icon_name("nwg-icon-picker", Gtk.IconSize.DIALOG)
    button.set_always_show_image(True)
    button.set_image_position(Gtk.PositionType.TOP)
    button.set_label("nwg-icon-picker")
    button.connect("clicked", Gtk.main_quit)
    vbox.pack_start(button, False, False, 0)

    global grid
    grid = Gtk.Grid.new()
    grid.set_column_spacing(6)
    grid.set_row_spacing(6)

    vbox.pack_start(grid, True, True, 0)

    global search_entry
    search_entry = Gtk.SearchEntry()
    search_entry.connect("search-changed", on_search_changed)
    grid.attach(search_entry, 0, 0, 1, 1)

    global result_label
    result_label = Gtk.Label()
    result_label.set_property("halign", Gtk.Align.START)
    grid.attach(result_label, 1, 0, 1, 1)

    lb = build_context_listbox()
    grid.attach(lb, 0, 1, 1, 1)

    window.show_all()
    search_entry.grab_focus()
    Gtk.main()


if __name__ == '__main__':
    sys.exit(main())
