#!python
# -*- encoding: utf-8 -*-

# C_LessonList_pnl.py

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
The module contains the code for the Lesson List Panel for the
Novus program.
'''

import wx
import wx.lib.scrolledpanel as scrolled
from wx.lib.wordwrap import wordwrap
import X_styles
import Q_data
from Q_language import GetPhrase

class LessonList_Pnl(scrolled.ScrolledPanel):
    '''This class allows the user to select the lesson.'''
    def __init__(self, parent):
        scrolled.ScrolledPanel.__init__(self, parent, -1)
        
        # Attributes ------------------------------------------------------
        self.year = 0
        
        # Data ------------------------------------------------------------
        self.data = Q_data.Data(None)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        self.SetBackgroundColour(self.styles.darkGreen)
        
        # Labels ----------------------------------------------------------
        lang = self.data.GetData1()[1][1]
        
        self.lessonSelect_lbl = GetPhrase('lessonSelect_lbl', lang)
        self.year_lbl = GetPhrase('year_lbl', lang)
        self.lessonList_lbl = GetPhrase('lessonList_lbl', lang)
        self.lesson_lbl = GetPhrase('lesson_lbl', lang)
        self.back_lbl = GetPhrase('back_lbl', lang)
        self.decisions_lbl = GetPhrase('decisions_lbl', lang)
        
        self.y1l1_lbl = GetPhrase('y1l1_lbl', lang)
        self.y1l2_lbl = GetPhrase('y1l2_lbl', lang)
        self.y1l3_lbl = GetPhrase('y1l3_lbl', lang)
        self.y1l4_lbl = GetPhrase('y1l4_lbl', lang)
        self.y1l5_lbl = GetPhrase('y1l5_lbl', lang)
        self.y1l6_lbl = GetPhrase('y1l6_lbl', lang)
        self.y1_lessonList = [self.y1l1_lbl, self.y1l2_lbl, self.y1l3_lbl,
                              self.y1l4_lbl, self.y1l5_lbl, self.y1l6_lbl]
        self.y2l1_lbl = GetPhrase('y2l1_lbl', lang)
        self.y2l2_lbl = GetPhrase('y2l2_lbl', lang)
        self.y2l3_lbl = GetPhrase('y2l3_lbl', lang)
        self.y2l4_lbl = GetPhrase('y2l4_lbl', lang)
        self.y2l5_lbl = GetPhrase('y2l5_lbl', lang)
        self.y2l6_lbl = GetPhrase('y2l6_lbl', lang)
        self.y2_lessonList = [self.y2l1_lbl, self.y2l2_lbl, self.y2l3_lbl,
                              self.y2l4_lbl, self.y2l5_lbl, self.y2l6_lbl]
        self.y3l1_lbl = GetPhrase('y3l1_lbl', lang)
        self.y3l2_lbl = GetPhrase('y3l2_lbl', lang)
        self.y3l3_lbl = GetPhrase('y3l3_lbl', lang)
        self.y3l4_lbl = GetPhrase('y3l4_lbl', lang)
        self.y3l5_lbl = GetPhrase('y3l5_lbl', lang)
        self.y3l6_lbl = GetPhrase('y3l6_lbl', lang)
        self.y3_lessonList = [self.y3l1_lbl, self.y3l2_lbl, self.y3l3_lbl,
                              self.y3l4_lbl, self.y3l5_lbl, self.y3l6_lbl]
        self.y4l1_lbl = GetPhrase('y4l1_lbl', lang)
        self.y4l2_lbl = GetPhrase('y4l2_lbl', lang)
        self.y4l3_lbl = GetPhrase('y4l3_lbl', lang)
        self.y4l4_lbl = GetPhrase('y4l4_lbl', lang)
        self.y4l5_lbl = GetPhrase('y4l5_lbl', lang)
        self.y4l6_lbl = GetPhrase('y4l6_lbl', lang)
        self.y4_lessonList = [self.y4l1_lbl, self.y4l2_lbl, self.y4l3_lbl,
                              self.y4l4_lbl, self.y4l5_lbl, self.y4l6_lbl]
        self.y5l1_lbl = GetPhrase('y5l1_lbl', lang)
        self.y5l2_lbl = GetPhrase('y5l2_lbl', lang)
        self.y5l3_lbl = GetPhrase('y5l3_lbl', lang)
        self.y5l4_lbl = GetPhrase('y5l4_lbl', lang)
        self.y5l5_lbl = GetPhrase('y5l5_lbl', lang)
        self.y5l6_lbl = GetPhrase('y5l6_lbl', lang)
        self.y5_lessonList = [self.y5l1_lbl, self.y5l2_lbl, self.y5l3_lbl,
                              self.y5l4_lbl, self.y5l5_lbl, self.y5l6_lbl]
        self.y6l1_lbl = GetPhrase('y6l1_lbl', lang)
        self.y6l2_lbl = GetPhrase('y6l2_lbl', lang)
        self.y6l3_lbl = GetPhrase('y6l3_lbl', lang)
        self.y6l4_lbl = GetPhrase('y6l4_lbl', lang)
        self.y6l5_lbl = GetPhrase('y6l5_lbl', lang)
        self.y6l6_lbl = GetPhrase('y6l6_lbl', lang)
        self.y6_lessonList = [self.y6l1_lbl, self.y6l2_lbl, self.y6l3_lbl,
                              self.y6l4_lbl, self.y6l5_lbl, self.y6l6_lbl]
        
        # Sizer
        #------------------------------------------------------------------
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        #--#
        self.lessonSelect_st = wx.StaticText(self, -1, self.lessonSelect_lbl + ' -')
        self.lessonSelect_st.SetFont(self.styles.h1_font)
        self.lessonSelect_st.SetForegroundColour(self.styles.lightGrey)
        sizer.Add(self.lessonSelect_st, 0, wx.LEFT|wx.TOP, 15)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        
        #--#
        self.lessonYear_st = wx.StaticText(self, -1, self.year_lbl+': ')
        self.lessonYear_st.SetFont(self.styles.h2_font)
        self.lessonYear_st.SetForegroundColour(self.styles.lightGrey)
        sizer.Add(self.lessonYear_st, 0, wx.LEFT, 45)
        
        #--#
        sizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND|wx.ALL, 10)
        sizer.Add((-1, 10)) 
        
        self.lesson1_btn = wx.Button(self, wx.ID_FILE1, self.lesson_lbl, size=(420, 65))
        self.lesson2_btn = wx.Button(self, wx.ID_FILE2, self.lesson_lbl, size=(420, 65))
        self.lesson3_btn = wx.Button(self, wx.ID_FILE3, self.lesson_lbl, size=(420, 65))
        self.lesson4_btn = wx.Button(self, wx.ID_FILE4, self.lesson_lbl, size=(420, 65))
        self.lesson5_btn = wx.Button(self, wx.ID_FILE5, self.lesson_lbl, size=(420, 65))
        self.lesson6_btn = wx.Button(self, wx.ID_FILE6, self.lesson_lbl, size=(420, 65))
        
        self.btnList = [b for b in self.GetChildren() if b.GetClassName()=='wxButton']
        for btn in self.btnList:
            btn.SetBackgroundColour(self.styles.brown)
            btn.SetForegroundColour(self.styles.lightGrey)
            btn.SetFont(self.styles.h3_b_font)
            sizer.Add(btn, 0, wx.LEFT, 40)
            sizer.Add((-1, 15))
        
        # Back and Decisions Buttons --------------------------------------
        a_box = wx.BoxSizer(wx.HORIZONTAL)
        self.back_btn = wx.Button(self, wx.ID_BACKWARD, self.back_lbl, size=(200, 50))
        self.back_btn.SetBackgroundColour(self.styles.lightGrey)
        self.back_btn.SetForegroundColour(self.styles.brown)
        self.back_btn.SetFont(self.styles.h3_b_font)
        self.decisions_btn = wx.Button(self, wx.ID_FORWARD, self.decisions_lbl, size=(200, 50))
        self.decisions_btn.SetBackgroundColour(self.styles.lightGreen)
        self.decisions_btn.SetForegroundColour(self.styles.lightGrey)
        self.decisions_btn.SetFont(self.styles.h3_b_font)
        a_box.Add(self.back_btn, 0, wx.RIGHT, 20)
        a_box.Add(self.decisions_btn, 0)
        sizer.Add(a_box, 0, wx.LEFT, 40)
        sizer.Add((-1, 20))
        
        # Method Calls ----------------------------------------------------
        self.SetSizer(sizer)
        self.SetupScrolling()
        
    #---------------------------------------------------------------------
    def Init(self, year):
        '''Sets up the labels and buttons so the year and lesson titles are
        correct.'''
        self.year = year
        
        self.lessonYear_st.SetLabel(self.year_lbl + ' ' + unicode(year) + ' '+self.lessonList_lbl)
        
        if year==1:
            lessonList = self.y1_lessonList
        elif year==2:
            lessonList = self.y2_lessonList
        elif year==3:
            lessonList = self.y3_lessonList
        elif year==4:
            lessonList = self.y4_lessonList
        elif year==5:
            lessonList = self.y5_lessonList
        else:
            lessonList = self.y6_lessonList
        
        #--#
        for x in range(6):
            try:
                self.btnList[x].SetLabel(wordwrap(lessonList[x], 350, wx.ClientDC(self)))
            except AttributeError, e:
                pass
            