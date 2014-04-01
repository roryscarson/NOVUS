#!python

# setup.py

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

import os, sys, shutil
from glob import glob

#--------------------------------------------------------------------------
# PY2EXE Setup Script
#--------------------------------------------------------------------------
if 'py2exe' in sys.argv:
    from distutils.core import setup
    import py2exe
    
    shutil.rmtree('build', ignore_errors=True)
    shutil.rmtree('dist', ignore_errors=True)
     
    packages = ['novus_pkg']

    # Get Data Files
    #----------------------------------------------------------------------
    res = os.path.abspath(os.path.join(os.getcwd(), 'novus_pkg', 'resources'))
            
    paths = []
    for x in os.walk(res):
        paths.append(x[0])
    file_stuff = []
    for x in paths:
        file_stuff.append(glob(os.path.join(x, '*.*')))
    
    MyDataFiles = [('resources', file_stuff[0]),
                   ('resources/Armenian', file_stuff[1]),
                   ('resources/Armenian/howto', file_stuff[2]),
                   ('resources/Armenian/Year 1', file_stuff[3]),
                   ('resources/Armenian/Year 2', file_stuff[4]),
                   ('resources/Armenian/Year 3', file_stuff[5]),
                   ('resources/Armenian/Year 4', file_stuff[6]),
                   ('resources/Armenian/Year 5', file_stuff[7]),
                   ('resources/Armenian/Year 6', file_stuff[8]),
                   ('resources/English', file_stuff[9]),
                   ('resources/English/howto', file_stuff[10]),
                   ('resources/English/Year 1', file_stuff[11]),
                   ('resources/English/Year 2', file_stuff[12]),
                   ('resources/English/Year 3', file_stuff[13]),
                   ('resources/English/Year 4', file_stuff[14]),
                   ('resources/English/Year 5', file_stuff[15]),
                   ('resources/English/Year 6', file_stuff[16]),
                   ('resources/images', file_stuff[17]),
                   ('Microsoft.VC90.CRT', glob(r'C:/\Users/Greg Wilson/Documents/Computing/cPPdlls/*.*'))]
    
    setup(
        options = {"py2exe": {"compressed": 2,
                              "optimize": 2,
                              "packages": packages,
                              "bundle_files": 3,
#                              "excludes":['win32api'],
                              "dist_dir": "dist",
                              "xref": False,
                              "skip_archive": False,
                              "ascii": False,
                              "custom_boot_script": '',
                             }
                  },
        windows= [
                  {'script': 'Novus.py',
                   'icon_resources': [(1, 'C:/\Users/Greg Wilson/Documents/Peace Corps Projects/Novus/Novus Dev/images/novus.ico')]
                   }
                  ],
        zipfile = "lib/library.zip",
        packages = ['novus_pkg'],
        data_files = MyDataFiles
    )
    