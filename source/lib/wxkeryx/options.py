# -*- coding: utf-8 -*-
#
# Author: Chris Oliver (excid3@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import os.path
import shutil
import wx
import wx.lib.buttons as buttons
import  wx.lib.colourselect as  csel

from lib import consts, plugins

class optionDialog(wx.Dialog):
    def __init__(self, *args, **kwds):
        kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        wx.Dialog.__init__(self, *args, **kwds)
        self.SetTitle(_("Options"))
        self.SetIcon(wx.Icon(consts.fileIco, wx.BITMAP_TYPE_ICO))
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Add notebook
        self.notebook = wx.Notebook(self)
        self.notebook_il = wx.ImageList(16, 16)
        self.notebook_il.Add(wx.Bitmap(consts.icon_layout))
        self.notebook_il.Add(wx.Bitmap(consts.icon_download))
        self.notebook_il.Add(wx.Bitmap(consts.icon_plugin))
        self.notebook.SetImageList(self.notebook_il)
        sizer.Add(self.notebook, 1, wx.EXPAND|wx.TOP|wx.RIGHT|wx.LEFT, 5)

        # Add line
        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.LEFT|wx.TOP, 5)

        # Add buttons
        btnsizer = wx.StdDialogButtonSizer()
        btn = wx.Button(self, wx.ID_OK)
        btn.SetDefault()
        btnsizer.AddButton(btn) 
        btn = wx.Button(self, wx.ID_CANCEL)
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer, 0, wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT|wx.ALL, 5)

        self.addTabs()
        self.SetSizer(sizer)
        self.Fit()
        
    def addTabs(self):
        pane = wx.Panel(self.notebook, -1, style=wx.TAB_TRAVERSAL)
        vert = wx.BoxSizer(wx.VERTICAL)

        txt = wx.StaticText(pane, -1, _("All directories should be relative paths."))
        vert.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)

        sizer = wx.BoxSizer()
        txt = wx.StaticText(pane, -1, _("Log Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.logCtrl = wx.TextCtrl(pane, -1, consts.LogPath, size=wx.Size(250,-1))
        sizer.Add(self.logCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer()
        txt = wx.StaticText(pane, -1, _("Locale Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.localeCtrl = wx.TextCtrl(pane, -1, consts.LocalePath)
        sizer.Add(self.localeCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        #sizer = wx.BoxSizer()
        #txt = wx.StaticText(pane, -1, _("Packages Directory:"))
        #sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        #self.packagesCtrl = wx.TextCtrl(pane, -1, consts.PackagesPath)
        #sizer.Add(self.packagesCtrl, 1, wx.ALL, 3)
        #vert.Add(sizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Plugins Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.pluginsCtrl = wx.TextCtrl(pane, -1, consts.PluginsPath)
        sizer.Add(self.pluginsCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Projects Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.projectsCtrl = wx.TextCtrl(pane, -1, consts.ProjectsPath)
        sizer.Add(self.projectsCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Themes Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.pixmapsCtrl = wx.TextCtrl(pane, -1, consts.PixmapsPath)
        sizer.Add(self.pixmapsCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Themes Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.themesCtrl = wx.TextCtrl(pane, -1, consts.ThemesPath)
        sizer.Add(self.themesCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Default Theme Directory:"))
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.defaultThemeCtrl = wx.TextCtrl(pane, -1, consts.ThemeDefaultPath)
        sizer.Add(self.defaultThemeCtrl, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        pane.SetSizer(vert)
        self.notebook.AddPage(pane, _("Directories"), False, 0)
        
        ### Second page ### THIS PAGE IS USED FOR THE PROXY
        pane = wx.Panel(self.notebook, -1, style=wx.TAB_TRAVERSAL)
        vert = wx.BoxSizer(wx.VERTICAL)
        # vert keeps track of the vertical objects in the page (rows)

        self.proxyCheckBox= wx.CheckBox(pane, -1, "Enable proxy support")
        self.proxyCheckBox.SetValue(consts.proxy_enabled) # Set proxy value
        vert.Add(self.proxyCheckBox, 0, wx.ALL, 3)

        # Make a bold font.
        bold_font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)#, False, u'Comic Sans MS')
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Add the "URL:" static text.
        url = wx.StaticText(pane, -1, _("URL: "))
        url.SetFont(bold_font)
        sizer.Add(url, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        # Add the "http://" static text.
        http = wx.StaticText(pane, -1, _("http://"))
        sizer.Add(http, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        # Add the URL text box.
        self.proxy_url = wx.TextCtrl(pane, -1, '')
        sizer.Add(self.proxy_url, 1, wx.ALL, 3)
        # Add the ":" static text.
        colon = wx.StaticText(pane, -1, _(":"))
        sizer.Add(colon, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        # Add the port text box.
        self.proxy_port = wx.TextCtrl(pane, -1, '')
        sizer.Add(self.proxy_port, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Username:"))
        txt.SetFont(bold_font)
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.proxy_username = wx.TextCtrl(pane, -1, consts.proxy_username)
        sizer.Add(self.proxy_username, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        txt = wx.StaticText(pane, -1, _("Password:"))
        txt.SetFont(bold_font)
        sizer.Add(txt, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 3)
        self.proxy_password = wx.TextCtrl(pane, -1, consts.proxy_password, style=wx.TE_PASSWORD)
        sizer.Add(self.proxy_password, 1, wx.ALL, 3)
        vert.Add(sizer, 0, wx.EXPAND)

        pane.SetSizer(vert)
        self.notebook.AddPage(pane, _("Download Options"), False, 1)

        self.LoadProxy()
        self.OnChecked(None) # Enable/Disable proxy textbox based on checkbox status
        self.Bind(wx.EVT_CHECKBOX, self.OnChecked, self.proxyCheckBox)

        ### Third page ###
        pane = wx.Panel(self.notebook, -1, style=wx.TAB_TRAVERSAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        txt = wx.StaticText(pane, -1, _("Loaded plugins:"))
        txt.SetFont(wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.BOLD, 0, ""))
        sizer.Add(txt, 0, wx.ALL, 3)

        self.pluginList = wx.ListBox(pane)
        sizer.Add(self.pluginList, 1, wx.EXPAND, 0)

        self.fill()

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.disableBtn = buttons.GenBitmapTextButton(pane, -1, wx.Bitmap(consts.icon_plugin_disable), _("Disable"))#, size=(120, 25))
        sizer2.Add(self.disableBtn, 0, wx.ALL, 3)
        self.Bind(wx.EVT_BUTTON, self.OnDisable, self.disableBtn)

        #bmp = wx.Bitmap(os.path.join(consts.dirPixmaps, 'plugin_go.png'))
        #self.disableBtn = buttons.GenBitmapTextButton(pane, -1, bmp, _("Start"))#, size=(120, 25))
        #sizer2.Add(self.disableBtn, 0, wx.ALL, 3)
                
        self.addBtn = buttons.GenBitmapTextButton(pane, -1, wx.Bitmap(consts.icon_plugin_add), _("Add"))#, size=(120, 25))
        sizer2.Add(self.addBtn, 0, wx.ALL, 3)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, self.addBtn)
        
        #bmp = wx.Bitmap(os.path.join(consts.dirPixmaps, 'plugin_edit.png'))
        #self.disableBtn = buttons.GenBitmapTextButton(pane, -1, bmp, _("Edit"))#, size=(120, 25))
        #sizer2.Add(self.disableBtn, 0, wx.ALL, 3)
        
        #bmp = wx.Bitmap(os.path.join(consts.dirPixmaps, 'plugin_delete.png'))
        #self.disableBtn = buttons.GenBitmapTextButton(pane, -1, bmp, _("Delete"))#, size=(120, 25))
        #sizer2.Add(self.disableBtn, 0, wx.ALL, 3)

        sizer.Add(sizer2)
        pane.SetSizer(sizer)
        self.notebook.AddPage(pane, _("Plugins"), False, 2)

    def OnChecked(self, evt):
        if self.proxyCheckBox.GetValue():
            self.proxy_url.Enable()
            self.proxy_port.Enable()
            self.proxy_username.Enable()
            self.proxy_password.Enable()
        else:
            self.proxy_url.Disable() 
            self.proxy_port.Disable() 
            self.proxy_username.Disable()
            self.proxy_password.Disable()

    def LoadProxy(self):
        """So right here, we've got to grab the value from the config and set it in the interface"""
        try:
            url = consts.http_proxy['http']
            (url, port) = (url.split(':')[1][2:], url.split(':')[-1])
            self.proxy_url.SetValue(url)
            self.proxy_port.SetValue(port)
        except: 
            pass

    def fill(self): # Fill plugin list
        self.pluginList.Clear()
        for item in plugins.OSPluginList: self.pluginList.Append(item[0])
        for item in plugins.InterfacePluginList: self.pluginList.Append(item[0])

    def OnAdd(self, evt):
        dlg = wx.FileDialog(self, message=_("Choose a file"),
                            defaultDir = consts.cwd, 
                            defaultFile = "",
                            wildcard = consts.wildcard_plugin,
                            style=wx.OPEN | wx.CHANGE_DIR)

        # Show the dialog and retrieve the user response. If it is the OK response, 
        # process the data
        if dlg.ShowModal() == wx.ID_OK:
            file = dlg.GetPaths()
            dlg.Destroy()
            if file[0]:
                # Copy the file to the plugins directory
                shutil.copyfile(file[0], os.path.join(consts.dirPlugins, os.path.basename(file[0]))) 
        else: 
            return

        wx.MessageBox(_("Plugin installed successfully. Restart Keryx to load the plugin."), _("Install Successful"))

    def OnDisable(self, evt):
        def disable(instance):
            try:
                instance.cleanup()
                wx.MessageBox(_("Plugin disabled successfully."))
                return True
            except: return False

        temp = []
        for item in plugins.OSPluginList: 
            if item[0] == self.pluginList.Items[self.pluginList.GetSelection()]:
                if disable(item[1]): # Successfully disabled
                    temp = []
                    for i in plugins.OSPluginList:
                        if i[0] != item[0]: temp.append(i)
                    plugins.OSPluginList = temp
                    self.fill()
                    return
                
        for item in plugins.InterfacePluginList: 
            if item[0] == self.pluginList.Items[self.pluginList.GetSelection()]:
                if disable(item[1]): # Successfully disabled
                    for i in plugins.InterfacePluginList:
                        if i[0] != item[0]: temp.append(i)
                    plugins.InterfacePluginList = temp
                    self.fill()
                    return
                
        wx.MessageBox(_("Unable to find plugin."))
        return False
        
# end of class optionDialog


