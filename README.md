# SVG Multiplier
Custom Python tool for copying an SVG design with automatically edited text fields, simplifying the process of making e.g. a large number of name tags with a similar design.

## Notes
The script functionality has only been tested in a very limited number of cases, with compatability currently only verified for Inkscape (version 1.3.2) SVGs and Python 3.11!

## Usage
1. Create an SVG design in Inkscape (The only software currently supported.)
    - For automatically edited text fields, name the text fields in question as "txt_1", "txt_2", etc. with each number corresponding to a column of an input table of data.
2. Go to File -> Document properties... and select "Resize to content". This ensures margins are calculated appropriately.
3. Save the design as type "Inkscape SVG" into the same directory as the Python script.
4. Create a table of data to paste into the placeholder text fields, with each row corresponding to a new instance of the original SVG design. Save the table as a CSV file into the same directory as the Python script.
    - E.g. in Excel, this is done by making such a table and saving the file as a "CSV (Comma delimited)" file.
5. Run the Python script and follow the prompts.
    - E.g. in Windows, this is done by opening the script directory, right-clicking, selecting "Open in Terminal", and running the command "python svg_multiplier.py".

Example files are included for reference.
