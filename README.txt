Program: Novus 1.0

Date: 8/11/2012

Progam Design and Programming: Greg Wilson
Simulator Design: Austin Sherwindt, Greg Wilson

Contact: gwilson.sq1@gmail.com

Novus is part of the Public Domain

Novus is distributed under the GNU General Public License, version 3

#--------------------------------------#
#            CHANGE LOG                #
#--------------------------------------#

__UPDATES 1.0 -__
* Finished lite version with links to vimeo vids for all lessons
* Updated lesson titles
* Omitted Dialog for lesson video source selection
* Omitted PW for game reset
* Excluded Language menu from menubar

__UPDATES 0.2.4 -__

* Updated the Market Summary content

__UPDATES 0.2.3 -__

* Added the language switcher functions
* Fixed a bug in the best case HR calculation
* Changed the team storage file storage method to not rely on tags

__UPDATES 0.2.2 -__

* Changed all wxComboBox widgets (drop down menus) read only
* Fixed a reset error in the total descretionary spending total 
calculation
* Tried to prevent index errors when calling for the 
novus_pkg.Q_data.CombineData method by not allowing the call when
the year is 7. 
* Changed the video file search algorithm to avoid having to load the
win32api module. This process is now handled with a series of dialogs.

__UPDATES 0.2.1 -__

* Changed the Lesson Select button layout
* Added label text wrapping to the Lesson Select button layout
* Added a "Game Overview" button to the How-To video list
* Added a "Total Capital Expenditure" on the finance panel for rounds 1 and 4
* Changed the Market Summary html files for blank decisions panels to notify
users that they will not have to make a decision for that year. I haven't found
an elegant solution to hide these panels, so this is a workaround. 
* When the number of production cycles are changed, the feedback below
now also shows the corresponding market share. 


__UPDATES 0.2 -__

* Added the Market Summary Content to the game
* Added the General Information and Instructional Videos 
* Fixed a glitch in the best case scenario for round 6
* Added word wrapping to the lesson titles
* Added 'Teacher Mode', which will display the actual results along
side the forecast results

---

__UPDATES 0.1.5 -__

* Fixed a calculation error in Interest Income
* Changed the product scoring methods for price and packaging
* Changed the BSC scoring methodology 
* Changed STB draw Static Text object to bold font
* The LTD interest rate in round four now factor in the team's 
past emergency Line of Credit draws
* Readjusted Scoring - Made it much more severe, mostly driven by the
need to adversly impact teams that price themselves out of the market
* The export function now uses only result panel attributes for titles
and sheet names
* Modified the Economies of Scale function to replicate the financial
model
* Changed the weighting of the BSC Managerial Effectiveness score.

---

__UPDATES 0.1.4 -__

* Fixed Short term borrowing interest expense calculation error
* Revised scoring method for products
* All windows scroll to top upon submission of decisions

---

__UPDATES 0.1.3 -__

* Packaging excesses in the spin controls will no longer carry over 
to the following round, and the warning will be re-hidden.
* Fixed a glitch in the WCM scoring function
* The Managment Effectiveness score is now calculated with previously 
generated data, lowering the processing time for calculating round
results
* Added the first version of the "Export Results" function, that will 
generate a timestamped Excel spreadsheet in the "Novus Data" directory 
with the current team results.

---

__UPDATES 0.1.2 -__

* Updated Splash version number
* Edited all instances of the game's full title to read Novus
Entrepreneurship Training Program
* Fixed the scrolling bug on the HR panel
* Changed the quantity spin controls on the HR panel to initialize with
last year's hiring quantity
* Fixed the price control fields to enforce minimum and maximum values and 
to allow writing decimals without a value in the 1's column
* Round 4 total packaging equipment total now excludes the prices of machines
purchased in the first round. 
* Fixed the glitch in the HR score on the Balanced Score Card (BSC). The 
score now also is partly determined by production and sales scores.
* Changed the BCS to include the different determinants of the Brand Strength
score.
* Changed the methods for scoring the Key Financial ratios. The individual
components are now scored based on their unilateral deviation away from the
best case ratios and the industry standards.
* Began adding the export results function

---

__UPDATES 0.1.1 -__

* Round 6 decisions can be submitted
* After Round 6 decisions, the game reverts to a stable end state
* Added "Export Results" and "Reset Game" buttons on the game panel
* Fixed the data_file glitch in the setup.py script
* Added a "Busy" dialog for the results processing
* HR Per Person costs now correctly update
* Added a Market Information panel for general market information

---

__UPDATES 0.1.0 -__

* Original Release


