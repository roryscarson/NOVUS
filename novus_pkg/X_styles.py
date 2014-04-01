#!python
# -*- encoding: utf-8 -*-

# X_styles.py

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
This class contains the style attributes for the Novus program,
including color and font.
'''

import wx

class NovusStyle(wx.Object):
    '''This class contains the style attributes used for the Novus
    program.'''
    def __init__(self, parent, *args, **kwargs):
        self.h1_font = wx.Font(25, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.h1_b_font = wx.Font(25, wx.SWISS, wx.NORMAL, wx.BOLD)
        
        self.h2_font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.h2_b_font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.BOLD)
        
        self.h3_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.h3_b_font = wx.Font(12, wx.SWISS, wx.NORMAL, wx.BOLD)
        
        self.h4_font = wx.Font(11, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.h4_b_font = wx.Font(11, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.h4_i_font = wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL)
        self.h4_bi_font = wx.Font(11, wx.SWISS, wx.ITALIC, wx.BOLD)
        self.h4_iu_font = wx.Font(11, wx.SWISS, wx.ITALIC, wx.NORMAL, 
                                 underline=True)
        
        self.h5_font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.NORMAL)
        self.h5_b_font = wx.Font(9, wx.SWISS, wx.NORMAL, wx.BOLD)
        self.h5_i_font = wx.Font(9, wx.SWISS, wx.ITALIC, wx.NORMAL)
        self.h5_iu_font = wx.Font(9, wx.SWISS, wx.ITALIC, wx.NORMAL, 
                                 underline=True)
        
        self.darkGreen = wx.Colour(80, 118, 66)
        self.lightGreen = wx.Colour(134, 148, 42)
        self.brown = wx.Colour(163, 123, 69)
        self.darkGrey = wx.Colour(204, 207, 188)
        self.lightGrey = wx.Colour(243, 244, 236)