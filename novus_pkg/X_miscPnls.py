#!python
# -*- encoding: utf-8 -*-

# X_miscPnls.py

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
This module contains miscellanious panels classes used for the 
Novus Business and IT Training Program.
'''

import wx
import X_styles, X_utilities

class Report1_Row_Pnl(wx.Panel):
    '''This panel holds a row title and a value slot for all six years.'''
    def __init__(self, parent, *args, **kwargs):
        super(Report1_Row_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.title = wx.StaticText(self, -1, '')
        self.y1 = wx.StaticText(self, -1, '')
        self.y2 = wx.StaticText(self, -1, '')
        self.y3 = wx.StaticText(self, -1, '')
        self.y4 = wx.StaticText(self, -1, '')
        self.y5 = wx.StaticText(self, -1, '')
        self.y6 = wx.StaticText(self, -1, '')
        self.fields = [f for f in self.GetChildren() if f.GetClassName()=='wxStaticText']
        
        sizer.Add(self.title, 3, wx.RIGHT, 5)
        sizer.Add(self.y1, 1, wx.RIGHT, 5)
        sizer.Add(self.y2, 1, wx.RIGHT, 5)
        sizer.Add(self.y3, 1, wx.RIGHT, 5)
        sizer.Add(self.y4, 1, wx.RIGHT, 5)
        sizer.Add(self.y5, 1, wx.RIGHT, 5)
        sizer.Add(self.y6, 1)
        
        self.SetSizer(sizer)
        
    #----------------------------------------------------------------------
    def Init(self, rowList, bold=False, italic=False, big=False):
        '''Takes a field list of a title and six values and sets the values
        of the panel's static text objects.'''
        for i in range(7):
            self.fields[i].SetLabel(rowList[i])
        
        if bold:
            for i in range(7):
                self.fields[i].SetFont(self.styles.h4_b_font)
        elif italic:
            for i in range(7):
                self.fields[i].SetFont(self.styles.h4_i_font)
        else:
            for i in range(7):
                self.fields[i].SetFont(self.styles.h4_font)
                
        for i in range(7):
            if bold and big:
                self.fields[i].SetFont(self.styles.h3_b_font)
            elif big:
                self.fields[i].SetFont(self.styles.h3_font)
    
    #----------------------------------------------------------------------
    def AddVal(self, value, col, isCur = True, isPerc = False):
        '''Adds a value to the panel. If col == 1 then the value is
        added to the "forecast" StaticText object. Otherwise the value
        is added to the "actual" Static Text object. If isCur and not 
        isPerc, the value is added as a currency. If not isCur and
        isPerc,the value is added as a percent. Otherwise, the value is
        added as a comma separated integer.'''
        # Set the correct StaticText object for setting the label
        if col == 1:
            obj = self.y1
        elif col == 2:
            obj = self.y2
        elif col == 3:
            obj = self.y3
        elif col == 4:
            obj = self.y4
        elif col == 5:
            obj = self.y5
        else:
            obj = self.y6
        
        if isCur and not isPerc:
            value = int(value)
            obj.SetLabel('$ '+format(value, ',d'))
        elif isPerc and not isCur:
            obj.SetLabel("%.2f %%" % (value,))
        else:
            value = int(value)
            obj.SetLabel(format(value, ',d'))
            
        if value < 0:
            obj.SetForegroundColour(wx.RED)
        else:
            obj.SetForegroundColour(wx.BLACK)
            
    #----------------------------------------------------------------------
    def AddFloat(self, value, col):
        '''Adds a floating point number to the correct column.'''
        if col == 1:
            obj = self.y1
        elif col == 2:
            obj = self.y2
        elif col == 3:
            obj = self.y3
        elif col == 4:
            obj = self.y4
        elif col == 5:
            obj = self.y5
        else:
            obj = self.y6
            
        obj.SetLabel("%.2f" % (value,))

        if value < 0:
            obj.SetForegroundColour(wx.RED)
        else:
            obj.SetForegroundColour(wx.BLACK)
            
    #----------------------------------------------------------------------
    def UltraBig(self):
        '''Sets up the panel's Static Text objects to be of a large font 
        and bold.'''
        for x in self.fields:
            x.SetFont(self.styles.h2_b_font)
            
    #----------------------------------------------------------------------
    def ExportRow(self):
        '''Scrapes the current row and returns the values as floats.'''
        row = [self.title.GetLabel()]
        for x in self.fields[1:]:
            value = x.GetLabel()
            if '$' in value:
                value = value.split(' ')[-1]
            elif '%' in value:
                value = value.split(' ')[0]
            elif value == '-':
                value = '0.0'
            elif value == '':
                return row
                
            value = value.replace(',', '')
                
            try:
                value = float(value)
            except ValueError:
                pass
            finally:
                row.append(value)

        return row
    
    #----------------------------------------------------------------------
    def SetLabel(self, newTitle):
        '''Sets the row title.'''
        self.title.SetLabel(newTitle)
    
#--------------------------------------------------------------------------
class Report2_Row_Pnl(wx.Panel):
    '''This panel holds a row title and a value slot the forecasted 
    and actual financial reports.'''
    def __init__(self, parent, *args, **kwargs):
        super(Report2_Row_Pnl, self).__init__(parent, *args, **kwargs)
        
        # Style -----------------------------------------------------------
        self.styles = X_styles.NovusStyle(None)
        
        # Sizer -----------------------------------------------------------
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.title = wx.StaticText(self, -1, '')
        self.forecast = wx.StaticText(self, -1, '')
        self.actual = wx.StaticText(self, -1, '')
        self.fields = [f for f in self.GetChildren() if f.GetClassName()=='wxStaticText']
        
        sizer.Add(self.title, 2, wx.RIGHT, 5)
        sizer.Add(self.forecast, 1, wx.RIGHT, 5)
        sizer.Add(self.actual, 1)
        
        self.SetSizer(sizer)
        
    #----------------------------------------------------------------------
    def Init(self, rowList, bold=False, italic=False):
        '''Takes a field list of a title, forecast, and actual results 
        and sets the field labels accordingly.'''
        for i in range(3):
            self.fields[i].SetLabel(rowList[i])
        
        if bold:
            for i in range(3):
                self.fields[i].SetFont(self.styles.h4_b_font)
        elif italic:
            for i in range(3):
                self.fields[i].SetFont(self.styles.h4_i_font)
        else:
            for i in range(3):
                self.fields[i].SetFont(self.styles.h4_font)
                
    #----------------------------------------------------------------------
    def AddVal(self, value, col, isCur = True, isPerc = False):
        '''Adds a value to the panel. If col == 1 then the value is
        added to the "forecast" StaticText object. Otherwise the value
        is added to the "actual" Static Text object. If isCur and not 
        isPerc, the value is added as a currency. If not isCur and
        isPerc,the value is added as a percent. Otherwise, the value is
        added as a comma separated integer.'''
        # Set the correct StaticText object for setting the label
        if col == 1:
            obj = self.forecast
        else:
            obj = self.actual
        
        if isCur and not isPerc:
            value = int(value)
            obj.SetLabel('$ '+format(value, ',d'))
        elif isPerc and not isCur:
            obj.SetLabel("%.2f %%" % (value,))
        else:
            value = int(value)
            obj.SetLabel(format(value, ',d'))
            
        if value < 0:
            obj.SetForegroundColour(wx.RED)
        else:
            obj.SetForegroundColour(wx.BLACK)
            
    #----------------------------------------------------------------------
    def AddFloat(self, value, col):
        '''Adds a floating point number to the correct column.'''
        if col == 1:
            obj = self.forecast
        else:
            obj = self.actual
        obj.SetLabel("%.2f" % (value,))
        
        if value < 0:
            obj.SetForegroundColour(wx.RED)
        else:
            obj.SetForegroundColour(wx.BLACK)
            
    #----------------------------------------------------------------------
    def ShowActual(self):
        '''Sets up teacher mode, which shows the Actual results column.'''
        if not self.actual.IsShown():
            self.actual.Show()
        self.Layout()
        
    #----------------------------------------------------------------------
    def HideActual(self):
        '''Turns off teacher mode, which will hide the Actual results colulmn.'''
        if self.actual.IsShown():
            self.actual.Hide()
        self.Layout()
        
    #----------------------------------------------------------------------
    def SetLabel(self, newTitle):
        '''Sets the row label.'''
        self.title.SetLabel(newTitle)
        
    #----------------------------------------------------------------------
    def ExportRow(self):
        '''Scrapes the current row and returns the values as floats.'''
        row = [self.title.GetLabel()]
        for x in self.fields[1:]:
            value = x.GetLabel()
            if '$' in value:
                value = value.split(' ')[-1]
            elif '%' in value:
                value = value.split(' ')[0]
            elif value == '-':
                value = '0.0'
            elif value == '':
                return row
                
            value = value.replace(',', '')
                
            try:
                value = float(value)
            except ValueError:
                pass
            finally:
                row.append(value)

        return row
    
#--------------------------------------------------------------------------
class Currency_TC(wx.TextCtrl):
    '''Allows only numbers that can be converted to a currency amount
    to be entered.'''
    def __init__(self, parent, *args, **kwargs):
        super(Currency_TC, self).__init__(parent, style=wx.TE_CENTER|wx.BORDER)
        
        self.min = 0
        self.max = 100
        
        self.styles = X_styles.NovusStyle(None)
        self.SetFont(self.styles.h4_font)
        
        self.Bind(wx.EVT_KEY_UP, self.OnKey)
        self.Bind(wx.EVT_KILL_FOCUS, self.OnKill)
    
    #----------------------------------------------------------------------
    def OnKey(self, evt):
        input = self.GetValue()
        if input != '.':
            rslt = X_utilities.ValidateLastFloat(input)
            if X_utilities.ValidateConvertFloat(rslt):
                self.SetValue(rslt)
            else:
                self.SetValue('')
            self.SetInsertionPointEnd()
            
    #----------------------------------------------------------------------
    def OnKill(self, evt):
        try:
            input = float(self.GetValue())
            self.SetValue("%.2f" % (input,))
        except ValueError, e:
            self.SetValue('0.00')
        finally:
            input = float(self.GetValue())
            if input < self.min:
                self.SetValue("%.2f" % (self.min,))
            elif input > self.max:
                self.SetValue("%.2f" % (self.max,))
        
    #----------------------------------------------------------------------
    def SetRange(self, min, max):
        '''Sets the minimum and maximum price attributes for the object.'''
        self.min = min 
        self.max = max 
            
        