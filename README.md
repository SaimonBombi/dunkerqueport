# dunkerqueport
Web spider and generation report of ships movement in Dunkerque Port

## Description

This script utilizes Scrapy in order to extract the necessary data of the Dunkerque Port web (http://www.dunkerque-port.fr/fr/activites-commerciales/navires-entree-transit.html). It extracts the name of the ship, estimated date of arrival (ETA), and the origin and destination. With this data writes a report including if there is a new ship, or an ETA change, and what is the origin and destination.

## Install and run

This is a python script. You will need a version of python 3.x installed in your system. The following libraries are also needed. If there are not installed the script will try to install them. 
- Scrapy
- Pandas
The script will run by simply typing python followed by the file name of the script. In this case python bordeauxport.py.

## Output

In order to keep it as simple as possible, the script generates a .csv file with this new gathered data, and it compares it with the historic .csv file generated in previous runs of the script. 
It generates a report that is saved at dunkerqueportreport.txt stating the following data:
- Date and time of the report generated
- If there is a new ship, print: "NEW SHIP! name: " and the name of the ship and add the ship to the dunkerqueporthistoric.csv
- If the ship is already in the bdunkerqueporthistoric.csv, print: "Ship name: already here", and check the date and time (ETA).
- If the ETA is the same as dunkerqueporthistoric.csv, displays: "Same ETA as before, no updates needed".
- If there is a change in the ETA, print: "Has been a change in ETA in this ship". Then it makes an update in dunkerqueporthistoric.csv and save the new information. Afterwards print "Ship updated". 
After doing this for every ship, it prints "Table updated. This is the new table", and the updated table. Following proceeds to print "Saving table in dunkerqueporthistoric.csv" and writing the data to dunkerqueporthistoric.csv.
If there is an error and couldn't save the file, prints: "Couldn’t save dunkerqueporthistoric.csv"
Afterwards, it deletes the csv file generated in order to don't misuse disk data. If there is an error prints: "Couldn’t delete dunkerqueportport.csv, check manually before running script again"
