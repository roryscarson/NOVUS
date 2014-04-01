

# novus_lang_xml.py

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
This script is used to create the Novus Entrepreneurship Training Program
Language XML sheet.
'''

import csv
import sys

from xml.etree import ElementTree as ET

class NovusLangUtil():
    '''This class is used to edit, search, and export the translation
    table for the Novus Entrepreneurship Training application. The 
    class requires that the file 'Program Translation.csv' be located
    in the same directory as the script.'''
    def __init__(self):
        # Read the CSV file and create a lang_table --
        print 'Started...'
        file_name = 'resources/Program Translation.csv'
        try:
            file = open(file_name, 'rb')
        except IOError, e:
            print 'The file "Program Tranlation.csv" must be located in the same directory as this script!.'''
            sys.exit()
            
        self.lang_table = []
        for line in csv.reader(file, dialect='excel'):
            self.lang_table.append(line)
        file.close()

        # Make a list of the column headers, starting with 'XML Tag'
        self.column_titles = []
        for x in self.lang_table[2]:
            if x != '': self.column_titles.append(x)
        
        # Crop the self.lang_table to only include tags and translations    
        self.CropTable()
        self.ClearBlankColumns()
        
        self.MakeXML()
        print "Here"
        
    #-----------------------------------------------------------------
    def CropTable(self):
        '''This method crops out the title and the column headers.'''
        self.lang_table = self.lang_table[3:]

    #-----------------------------------------------------------------
    def ClearBlankColumns(self):
        '''Takes a language table and ensures that only columns with
        data are included.'''
        column_count = len(self.column_titles)
        for x in range(len(self.lang_table)):
            self.lang_table[x] = self.lang_table[x][:column_count]
    
    #-----------------------------------------------------------------  
    def FindDuplicates(self, column=0):
        '''This method finds duplicate data and prints out the offending
        data and its index positions in the self.lang_table list.'''
        if column > len(self.column_titles):
            print 'That column is not included in the translation table!'
        else:
            print 'Scanning ', self.column_titles[column], 'for duplicates'
        
        # Make a list of tags --
        tag_list = []
        for x in self.lang_table:
            tag_list.append(x[0])
            
        # Count the number of instances of each word, stdout repeats--
        duplicate_count = 0
        for x in tag_list:
            if self.lang_table.count(x) > 1:
                print 25 * '-'
                print 'REPEAT TAG >', x, 
                print 'ROWS >', self.GetTagIndex(x)
                print
                duplicate_count += 1
        
        print 25 * '='
        print 'Scan Complete'
        print 'Duplicates Found >', duplicate_count
        print
    
        return duplicate_count
    
    #-----------------------------------------------------------------
    def FindAllDuplicates(self):
        '''Runs through each column in the table and reports 
        duplicates.'''
        duplicate_count = 0
        for x in range(len(self.column_titles)):
            duplicate_count += self.FindDuplicates(x)
        return duplicate_count
        
    #-----------------------------------------------------------------
    def GetTagIndex(self, tag):
        '''This method returns all of the indexes in a list matching
        the supplied tag.'''
        index_list = []
        for x in range(len(self.lang_table)):
            if self.lang_table[x] == tag:
                index_list.append(x)
        return x

    #-----------------------------------------------------------------
    def TestPrint(self, n_lines = 5):
        '''Prints out n_lines lines of the self.lang_table list 
        attribute.'''
        for x in self.lang_table[:n_lines]:
            print x
            
    #-----------------------------------------------------------------
    def GetTag(self, phrase):
        '''Takes and English phrase or word in the program, checks to
        see if it's in the lang_table, and if so returns the XML 
        tag.'''
        english_list = []
        for x in self.lang_table:
            english_list.append(x[1])
            
        if phrase in english_list:
            i = english_list.index(phrase)
            tag = self.lang_table[i][0]
            x = 'The XML Tag for %s is... %s \n'
            print x % (phrase, tag,)
        else:
            print '%s is not in the self.lang_table! \n' % (phrase,)
            
    #-----------------------------------------------------------------
    def MakeXML(self):
        '''This takes the language table and creates a XML file with
        the contents.'''
        
        # Create the Element Tree Object
        root = ET.Element('root')
        
        for row in self.lang_table:
            tag_attr = row[0]
            for col in row[1:]:
                lang_attr = self.column_titles[row.index(col)]
                x = ET.SubElement(root, tag_attr, 
                                  attrib={'lang': lang_attr})
                x.text = unicode(col, encoding='utf8')
        
        file = open('resources/novus.xml', 'w')
        ET.ElementTree(root).write(file)
        file.close()
        
    #-----------------------------------------------------------------
    def PullText(self, tag, language='English'):
        '''If the novus.xml file is present, this will search for 
        an element with the matching tag and language attribute.'''
        try:
            x = ET.parse('resources/novus.xml').getroot()
        except:
            print 'You haven\'t created the "novus.xml" file yet!'
            return False
        
        for i in x:
            tag_attr = i.tag
            lang_attr = i.attrib['lang']
            if tag_attr == tag and lang_attr == language:
                return i.text
        print 'No objects met the search criteria.'
            
    #-----------------------------------------------------------------
    def PullTag(self, text, language='English'):
        '''If the novus.xml file is present, this will search for
        an element with the corresponding text and language 
        and will return the tag.'''
        try:
            x = ET.parse('resources/novus.xml').getroot()
        except:
            print 'You haven\'t created the "novus.xml" file yet!'
            return False
        
        for i in x:
            text_attr = i.text
            lang_attr = i.attrib['lang']
            if text_attr == text and lang_attr == language:
                return i.tag
        print 'No objects met the search criteria.'
        
#=====================================================================
if __name__ == '__main__':
    x = NovusLangUtil()
    
    