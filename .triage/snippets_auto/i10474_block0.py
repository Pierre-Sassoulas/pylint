"""
程序主窗口。
"""

from win32more.Microsoft.UI.Xaml import LaunchActivatedEventArgs, Window
from win32more.Microsoft.UI.Xaml.Markup import XamlReader
from win32more.Microsoft.UI.Xaml.Media import MicaBackdrop
from win32more.xaml import XamlApplication


class MainWindow(XamlApplication):
    """
    程序主窗口。
    """

    win: Window
    args: LaunchActivatedEventArgs

    def OnLaunched(self, args):
        self.win = Window()
        self.win.SystemBackdrop = MicaBackdrop()
        with open("page.xaml", "r", encoding="utf-8") as file:
            self.win.Content = XamlReader.Load(file.read())
        self.win.Activate()


XamlApplication.Start(MainWindow)

