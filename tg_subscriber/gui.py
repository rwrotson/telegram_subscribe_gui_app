import os
import string
from pathlib import Path

import wx
from wxasync import AsyncBind

from tg_subscriber.telegram_api import follow_channels
from tg_subscriber.constants import (
    PREFS_FOLDER, USER_FILE_PATH, CHANNEL_FILE_PATH
)


class UpperTextCtrl(wx.TextCtrl):
    """
    Make all the text in text inputs upper case
    """
    def __init__(self, *args, **kwargs):
        super(UpperTextCtrl, self).__init__(*args, **kwargs)
        self.Bind(wx.EVT_CHAR, self.on_char)

    def on_char(self, event):
        key = event.GetKeyCode()
        text_ctrl = event.GetEventObject()
        if chr(key) in string.ascii_letters:
            text_ctrl.AppendText(chr(key).upper())
            return
        event.Skip()


class Window(wx.Frame):
    def __init__(self, pos=(200, 100)):
        super().__init__(
            parent=None, title='follow / unfollow', size=(400, 500), pos=pos,
            style=wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX
            )
        self.panel = wx.Panel(self)
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        self.vbox.AddStretchSpacer()
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        """
        Add a picture to the background
        """
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap('images/background.bmp')
        dc.DrawBitmap(bmp, 0, 0)


class MainWindow(Window):
    def __init__(self, pos=(200, 100)):
        super().__init__(pos)

        self.make_main_control_buttons()
        self.make_main_layout()
        self.make_binds()

    def make_main_control_buttons(self):
        self.readme_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/readme.bmp'), size=(300, 50)
            )
        self.user_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/user.bmp'), size=(140, 50)
            )
        self.channels_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/channels.bmp'), size=(140, 50)
            )
        self.follow_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/follow.bmp'), size=(300, 50)
            )
        self.unfollow_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/unfollow.bmp'), size=(300, 50)
            )

    def make_main_layout(self):
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.readme_button, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.user_button, proportion=0)
        hbox.AddSpacer(20)
        hbox.Add(self.channels_button, proportion=0)
        self.vbox.Add(hbox, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.follow_button, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.unfollow_button, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)

    def make_binds(self):
        self.readme_button.Bind(wx.EVT_BUTTON, self.OnReadmeClick)
        self.user_button.Bind(wx.EVT_BUTTON, self.OnUserClick)
        self.channels_button.Bind(wx.EVT_BUTTON, self.OnChannelsClick)
        AsyncBind(wx.EVT_BUTTON, self.OnFollowClick, self.follow_button)
        AsyncBind(wx.EVT_BUTTON, self.OnUnfollowClick, self.unfollow_button)

    def OnReadmeClick(self, evt):
        position = self.GetPosition()
        readme_window = ReadMeWindow(position)
        self.Close()
        readme_window.Show()

    def OnUserClick(self, evt):
        position = self.GetPosition()
        user_window = UserWindow(position)
        self.Close()
        user_window.Show()

    def OnChannelsClick(self, evt):
        position = self.GetPosition()
        channels_window = ChannelsWindow(position)
        self.Close()
        channels_window.Show()

    async def OnFollowClick(self, evt):
        await follow_channels()

    async def OnUnfollowClick(self, evt):
        await follow_channels(follow=False)


class SideWindow(Window):
    def __init__(self, pos):
        super().__init__(pos)

        self.panel.SetBackgroundColour('white')
        self.font_large = wx.Font(
            16, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Trattatello'
            )
        self.font_small = wx.Font(
            12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Trattatello'
            )
        self.font_smallest = wx.Font(
            10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False, 'Trattatello'
            )

        self.back_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/back.bmp'), size=(140, 50)
            )
        self.back_button.Bind(wx.EVT_BUTTON, self.OnBackClick)

    def make_save_button(self):
        self.save_button = wx.BitmapButton(
            self.panel, -1, wx.Bitmap('images/save.bmp'), size=(140, 50)
            )
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSaveClick)

    def OnBackClick(self, evt):
        position = self.GetPosition()
        main_window = MainWindow(position)
        self.Close()
        main_window.Show()

    def OnSaveClick():
        pass


class UserWindow(SideWindow):
    def __init__(self, pos):
        super().__init__(pos)
        self.make_save_button()
        self.make_info_texts()
        self.make_inputs()
        self.fill_inputs()
        self.make_layout()

    def make_info_texts(self):
        self.info_text = wx.StaticText(self.panel)
        self.info_text.SetFont(self.font_large)
        self.info_text.SetLabel('ВВЕДИТЕ ДАННЫЕ ПОЛЬЗОВАТЕЛЯ')
        self.id_text = wx.StaticText(self.panel, size=(120, 40))
        self.id_text.SetFont(self.font_large)
        self.id_text.SetLabel('*API_APP_ID')
        self.hash_text = wx.StaticText(self.panel, size=(120, 40))
        self.hash_text.SetFont(self.font_large)
        self.hash_text.SetLabel('*API_APP_HASH')
        self.phone_text = wx.StaticText(self.panel, size=(120, 40))
        self.phone_text.SetFont(self.font_large)
        self.phone_text.SetLabel('*PHONE NUMBER')

    def make_inputs(self):
        self.id_input = UpperTextCtrl(self.panel, size=(180, 40))
        self.id_input.SetFont(self.font_large)
        self.hash_input = UpperTextCtrl(self.panel, size=(180, 40))
        self.hash_input.SetFont(self.font_large)
        self.phone_input = UpperTextCtrl(self.panel, size=(180, 40))
        self.phone_input.SetFont(self.font_large)

    def fill_inputs(self):
        if os.path.exists(USER_FILE_PATH):
            with open(USER_FILE_PATH, 'r') as file:
                user, hash, phone = file.read().split(', ')
            self.id_input.WriteText(user)
            self.hash_input.WriteText(hash)
            self.phone_input.WriteText(phone)

    def make_layout(self):
        self.vbox.Add(self.info_text, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(self.id_text, proportion=0)
        hbox1.Add(self.id_input, proportion=0)
        self.vbox.Add(hbox1, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2.Add(self.hash_text, proportion=0)
        hbox2.Add(self.hash_input, proportion=0)
        self.vbox.Add(hbox2, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3.Add(self.phone_text, proportion=0)
        hbox3.Add(self.phone_input, proportion=0)
        self.vbox.Add(hbox3, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        hbox4 = wx.BoxSizer(wx.HORIZONTAL)
        hbox4.Add(self.back_button, proportion=0)
        hbox4.AddSpacer(20)
        hbox4.Add(self.save_button, proportion=0)
        self.vbox.Add(hbox4, flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)

    def OnSaveClick(self, evt):
        """
        Save user's info into file
        """
        os.makedirs(PREFS_FOLDER, exist_ok=True)
        with open(USER_FILE_PATH, 'w') as f:
            user_id = self.id_input.GetValue().strip(' ')
            user_hash = self.hash_input.GetValue().strip(' ')
            user_phone = self.phone_input.GetValue().strip(' ')
            f.write(f'{user_id}, {user_hash}, {user_phone}')
        self.OnBackClick(evt)


class ChannelsWindow(SideWindow):
    def __init__(self, pos):
        super().__init__(pos)

        self.make_save_button()
        self.make_info_and_inputs()
        self.fill_inputs()
        self.make_layout()

    def make_info_and_inputs(self):
        self.text = wx.StaticText(self.panel)
        self.text.SetFont(self.font_large)
        self.text.SetLabel('ВВЕДИТЕ НАЗВАНИЯ КАНАЛОВ')

        self.channels_input = UpperTextCtrl(
            self.panel, size=(300, 350), style=wx.TE_MULTILINE
            )
        self.channels_input.SetFont(self.font_small)

    def fill_inputs(self):
        if os.path.exists(CHANNEL_FILE_PATH):
            with open(CHANNEL_FILE_PATH, 'r') as f:
                channels = f.read()
            self.channels_input.WriteText(channels)

    def make_layout(self):
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.text,  flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.channels_input,  flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.back_button, proportion=0)
        hbox.AddSpacer(20)
        hbox.Add(self.save_button, proportion=0)

        self.vbox.Add(hbox,  flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)

    def OnSaveClick(self, evt):
        """
        Save channels info into file
        """
        os.makedirs(PREFS_FOLDER, exist_ok=True)
        with open(CHANNEL_FILE_PATH, 'w') as file:
            channels = self.channels_input.GetValue()
            # turn into upper case
            channels = channels.upper()
            # reduce options to one form of string
            channels = channels.replace('HTTPS://T.ME/', '')
            channels = channels.replace('T.ME/', '')
            channels = channels.replace('@', '')
            # remove duplicate channels
            channels_list = channels.split(', ')
            clean_channels_list = []
            [clean_channels_list.append(x) for x in channels_list
                if x not in clean_channels_list]
            channels = ', '.join(clean_channels_list)
            file.write(channels)
        self.OnBackClick(evt)


class ReadMeWindow(SideWindow):
    def __init__(self, pos):
        super().__init__(pos)

        self.make_readme_text()
        self.make_layout()

    def make_readme_text(self):
        txt = str(Path('texts/readme.txt').read_text().upper())
        self.text = wx.StaticText(self.panel)
        self.text.SetFont(self.font_smallest)
        self.text.SetLabel(txt)
        self.text.Wrap(300)

    def make_layout(self):
        self.vbox.AddStretchSpacer()
        self.vbox.Add(self.text,  flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()

        self.vbox.Add(self.back_button,  flag=wx.ALIGN_CENTER, proportion=0)
        self.vbox.AddStretchSpacer()
        self.panel.SetSizer(self.vbox)
