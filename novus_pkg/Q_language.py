#! python
# -*- encoding: utf-8 -*-

# Q_language.py

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
This module contains the methods for pulling words and phrases
from the novus.xml file.
'''

import os
import sys
from xml.etree import ElementTree as ET
import Q_data
import X_utilities

def GetPhrase(tag, language):
    # Get the currently selected language
    
    # Read the 'novus.xml' file and create the element tree
    filepath = X_utilities.ResourceFP('novus.xml')
    try:
        x = ET.parse(filepath).getroot()
    except:
        return False
    
    # Find and return the phrase that matches the supplied tag
    for i in x:
        tag_attr = i.tag
        lang_attr = i.attrib['lang']
        if tag_attr == tag and lang_attr == language:
            return unicode(i.text)
    
    # If nothing is found, return False
    return False

        
if __name__ == '__main__':
    GetPhrase('Ale')