#!/usr/bin/env python

import os
import sys

import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk, GLib

dir_name = os.path.dirname(__file__)

gtk_theme_name = ""
gtk_icon_theme = None
search_entry = None
icon_info = None
btn_height = 0

result_wrapper_box = None
icon_names = []
result_scrolled_window = None


def on_search_changed(sb):
    global result_scrolled_window

    phrase = sb.get_text()
    if phrase and len(phrase) > 2:
        if result_scrolled_window:
            result_scrolled_window.destroy()
        scrolled_window = Gtk.ScrolledWindow.new(None, None)
        scrolled_window.set_propagate_natural_width(True)
        scrolled_window.set_propagate_natural_height(True)
        result_scrolled_window = scrolled_window
        result_wrapper_box.pack_start(scrolled_window, True, True, 0)
        lb = Gtk.ListBox.new()
        scrolled_window.add(lb)

        for name in icon_names:
            if phrase in name:
                row = IconListRow(name)
                lb.add(row)

        result_wrapper_box.show_all()
        return scrolled_window


class IconListRow(Gtk.ListBoxRow):
    def __init__(self, name):
        super().__init__()
        self.connect("focus-in-event", update_info, name)
        self.connect("activate", on_row_activate, name)

        eb = Gtk.EventBox.new()
        self.add(eb)
        eb.connect("button-press-event", update_info, name)
        box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
        eb.add(box)

        pixbuf = gtk_icon_theme.load_icon(name, 24,
                                          Gtk.IconLookupFlags.FORCE_SIZE |
                                          Gtk.IconLookupFlags.GENERIC_FALLBACK |
                                          Gtk.IconLookupFlags.USE_BUILTIN)
        img = Gtk.Image.new_from_pixbuf(pixbuf)
        box.pack_start(img, False, False, 6)

        lbl = Gtk.Label.new(name)
        box.pack_start(lbl, False, False, 0)


def update_info(ebox, ebtn, name):
    global icon_info
    icon_info.update(name)


class IconInfo(Gtk.Box):
    def __init__(self, name):
        super().__init__()
        self.set_orientation(Gtk.Orientation.VERTICAL)
        self.name = name

        self.button = Gtk.Button()
        self.button.set_always_show_image(True)
        self.button.set_image_position(Gtk.PositionType.TOP)
        self.button.set_label("nwg-icon-picker")
        self.button.set_tooltip_text("Click to pick the icon name")
        self.pack_start(self.button, False, False, 0)

        self.button.connect("clicked", on_button_clicked)

        self.lbl_filename = Gtk.Label()
        self.lbl_filename.set_line_wrap(True)
        self.lbl_filename.set_property("margin-top", 6)
        self.lbl_filename.set_selectable(True)
        self.pack_start(self.lbl_filename, False, False, 0)

        self.update(name)

    def update(self, name):
        info = gtk_icon_theme.lookup_icon(name, 96, 0)
        self.lbl_filename.set_text(info.get_filename())

        img = Gtk.Image.new_from_icon_name(name, Gtk.IconSize.DIALOG)
        self.button.set_image(img)
        self.button.set_label(name)

        global btn_height
        if btn_height > 0:
            self.button.set_size_request(0, btn_height)


def on_button_clicked(btn):
    print(btn.get_label())
    Gtk.main_quit()


def on_row_activate(row, name):
    print(name)
    Gtk.main_quit()


def main():
    GLib.set_prgname('nwg-icon-picker')

    window = Gtk.Window()
    window.connect("destroy", Gtk.main_quit)

    global gtk_theme_name
    gtk_settings = Gtk.Settings.get_default()
    gtk_theme_name = gtk_settings.get_property("gtk-icon-theme-name")

    global gtk_icon_theme
    gtk_icon_theme = Gtk.IconTheme.get_default()

    global icon_names
    icon_names = gtk_icon_theme.list_icons()
    print("Found {} icons".format(len(icon_names)), file=sys.stderr)
    icon_names.sort(key=str.casefold)

    hbox = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
    hbox.set_property("margin", 6)
    window.add(hbox)

    vbox = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
    hbox.pack_start(vbox, True, True, 0)

    global icon_info
    icon_info = IconInfo("nwg-icon-picker")
    vbox.pack_start(icon_info, False, False, 0)

    global search_entry
    search_entry = Gtk.SearchEntry()
    search_entry.connect("search-changed", on_search_changed)
    vbox.pack_start(search_entry, False, False, 0)

    global result_wrapper_box
    result_wrapper_box = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 0)
    vbox.pack_start(result_wrapper_box, False, False, 0)

    window.show_all()

    search_entry.grab_focus()

    # save the initial value and use later to preserve the window from floating on the icon height changed
    global btn_height
    btn_height = icon_info.button.get_allocated_height()

    Gtk.main()


if __name__ == '__main__':
    sys.exit(main())
