#!python
# -*- encoding: utf-8 -*-

# Q_about_dlg.py

# Greg Wilson, 2012
# gwilson.sq1@gmail.com
# This software is part of the Public Domain.

#    This file is part of the NOVUS Entrepreneurship Training Program.

#    NOVUS is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    NOVUS is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with NOVUS.  If not, see <http://www.gnu.org/licenses/>.

'''
The module contains the code for the "About" dialog for the Novus 
Entrepreneurship Training Program.
'''

import wx
import os
import webbrowser
import wx.html 
import X_styles, X_utilities

class About_Dlg(wx.Dialog):
    '''This class is for the About dialog for the Novus program.'''
    def __init__(self, parent, *args, **kwargs):
        super(About_Dlg, self).__init__(parent, id=-1, size=(530, 530))
        
        # Styles ----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.li_html = wxHTML(self)
        self.li_html.SetFonts('Constantia', 'serif', 
                                  [12, 12, 12, 13, 14, 15, 16])
        
        path = os.path.dirname(X_utilities.ResourceFP(''))
        path = os.path.join(path, 'about.html')
        self.li_html.LoadFile(path)
        sizer.Add(self.li_html, 1, wx.EXPAND)
        
        
        self.sl = wx.StaticLine(self, -1)
        sizer.Add(self.sl, 0, wx.EXPAND)
        
        self.ok = wx.Button(self, -1, 'OK')
        sizer.Add(self.ok, 0, wx.ALIGN_RIGHT|wx.ALL, 10)
        
        self.SetSizer(sizer)
    
        self.ok.Bind(wx.EVT_BUTTON, self.OnOK)
        
    def OnOK(self, evt):
        self.Destroy()
        
class wxHTML(wx.html.HtmlWindow):
     def OnLinkClicked(self, link):
         webbrowser.open(link.GetHref())
