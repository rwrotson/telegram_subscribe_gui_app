import time
from pathlib import Path

import wx


class PopUpWindow(wx.Frame):
    def __init__(self, pos=(500, 400)):
        super().__init__(
            parent=None, size=(300, 200),
            pos=pos, style=wx.CLOSE_BOX
            )
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour('white')
        self.font = wx.Font(
            12, wx.DEFAULT, wx.NORMAL,
            wx.NORMAL, False, 'Trattatello'
            )
        self.font_large = wx.Font(
            16, wx.DEFAULT, wx.NORMAL,
            wx.NORMAL, False, 'Trattatello'
            )
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.AddStretchSpacer()

    def make_ok_button(self):
        self.ok_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/ok.bmp'), size=(70, 50)
            )
        self.Bind(wx.EVT_BUTTON, self.OnOKClick)

    def make_cancel_button(self):
        self.cancel_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/cancel.bmp'), size=(70, 50)
            )
        self.Bind(wx.EVT_BUTTON, self.OnCancelClick)

    def OnOKClick(self, evt):
        self.Close()

    def OnCancelClick(self, evt):
        self.Close()


class OKWindow(PopUpWindow):
    def __init__(self, pos=(500, 400)):
        super().__init__(pos)
        self.make_ok_button()
        self.make_text()
        self.set_text()
        self.make_layout()

    def make_text(self):
        self.info_text = wx.StaticText(self.panel, size=(100, 50))
        self.info_text.SetFont(self.font)

    def set_text(self):
        self.info_text.SetLabel('ОПЕРАЦИЯ ПРОШЛА УСПЕШНО!')

    def make_layout(self):
        self.vbox.Add(self.info_text, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.ok_button, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)


class ErrorWindow(OKWindow):
    def __init__(self, pos=(500, 400)):
        super().__init__(pos)
        self.set_text()

    def set_text(self):
        txt = str(Path('texts/error.txt').read_text().upper())
        self.info_text.SetLabel(txt)


class EnterCodeWindow(PopUpWindow):
    def __init__(self, pos=(500, 400)):
        super().__init__(pos)
        self.make_elements()
        self.make_ok_button()
        self.make_cancel_button()
        self.make_layout()

    def make_elements(self):
        self.code_text = wx.StaticText(self.panel)
        self.code_text.SetFont(self.font)
        self.code_text.SetLabel('ВВЕДИТЕ КОД, ОТПРАВЛЕННЫЙ ВАМ В TELEGRAM')
        self.code_input = wx.TextCtrl(self.panel, size=(100, 40))
        self.code_input.SetFont(self.font_large)

    def make_layout(self):
        self.vbox.Add(self.code_text, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.code_input, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.cancel_button, proportion=0)
        hbox.AddSpacer(20)
        hbox.Add(self.ok_button, proportion=0)
        self.vbox.Add(hbox, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)

    def OnOKClick(self, evt):
        self.code_value = self.code_input.GetValue().strip(' ')
        self.Close()

    def OnCancelClick(self, evt):
        self.Close()


def show_ok():
    ok_window = OKWindow()
    ok_window.Show()


def show_error():
    error_window = ErrorWindow()
    error_window.Show()


def enter_code():
    code_window = EnterCodeWindow()
    code_window.Show()
    while hasattr(code_window, 'code_value') is False:
        print(code_window)
        time.sleep(0.5)
    return code_window.code_value