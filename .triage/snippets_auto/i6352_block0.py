"""
The main window of the application.
"""

from typing import Tuple

import gi
gi.require_version("Gtk", "3.0")
# pylint: disable=wrong-import-position
from gi.repository import Gtk
# pylint: enable=wrong-import-position

class MainWindow(Gtk.Window):
    """
    The main window of the application.
    """

    WINDOW_SIZE: Tuple[int, int] = (500, 250)
    MAIN_PADDING_PX: int = 10
    FRAMES_VERTICAL_SPACE_PX: int = 10

    INPUT_FILE_FRAME_LABEL: str = "Input file"
    INPUT_FILE_BUTTON_LABEL: str = "Choose input file"

    def __init__(self, title: str):
        super().__init__(title=title)
        self.set_size_request(*self.WINDOW_SIZE)

        # --- Add widgets --- #

        # Main container
        main_box: Gtk.Box = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL,
                                        spacing=self.FRAMES_VERTICAL_SPACE_PX)
        self.add(main_box)
        MainWindow.__pad_on_all_sides(main_box, self.MAIN_PADDING_PX)

        # Input file picker
        input_file_frame: Gtk.Frame = Gtk.Frame.new(label=self.INPUT_FILE_FRAME_LABEL)
        main_box.pack_start(child=input_file_frame, expand=True, fill=True, padding=0)

        hbox: Gtk.Box = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL)
        input_file_frame.add(hbox)

        self.input_file_button = Gtk.Button.new(label=self.INPUT_FILE_BUTTON_LABEL)

        # --- Connect and show --- #
        self.connect("destroy", Gtk.main_quit)
        self.show_all()

    @staticmethod
    def __pad_on_all_sides(widget: Gtk.Widget, padding: int) -> None:
        widget.set_margin_bottom(padding)
        widget.set_margin_top(padding)
        widget.set_margin_left(padding)
        widget.set_margin_right(padding)

