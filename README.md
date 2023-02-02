
# SourceMapStats


## What is this?
A way to display map relevancy for a given gamemode and game.
![parsecd_JitopkOtxP](https://user-images.githubusercontent.com/29761720/216379923-94c30771-f4c8-45ac-81af-e2708c6b1598.png)



## Usage
* You simply open Statistics_Write.py and start collecting data.
The data will be stored in a output.csv folder by default in the same directory.
* Once you have a Output.csv with some data. You can view it with the Statistics_Read.py file.
This will show you relevant information about the data you've just collected.

## Installation
* Launch the install.bat to get py dependencies
* Launch the Statistics_Write.py to gather in .csv format
* Launch the Statistics_Read.py to view the gathered information.
* Configure the desired map prefix. default is dr_
* Configure the desired game. default is tf

## Configure
You have to open the py files to configure them.
The parameters are at the top of the files so it should be easy to use them.



## Note
Currently the script is configure to scan TF2 servers with a specific map prefix. The Prefix can be changed, but changing the game might require more effort.

