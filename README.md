# okzoomer
okzoomer is a python script to help manage and back up zoom cloud recordings to local storage.

All settings are stored in the .env file here is how it is structured:


**API_KEY='' # This will be where you put your Zoom API key\
API_SEC='' # This will be whee you put your Zooom Secret\
DOWNLOAD_DIRECTORY='' # Directory where you want recordings to be downloaded to\
EMAIL_FILE='' # This is the file you will need to put your end users email address so the script can look up their recordings.\
EMAIL_SUFFIX='' # This is needed because the script will strip the suffix from each user to create a directory based on their user name\**

This script creates a few files when first started, it will create a "lastran.txt" file to keep track of when the last time the script is ran. This is important to query Zoom's api to get the most current recordings and not re-download recordings that have already been saved. The info.log file is of course, a log file. You can check this file to check on the status of the script and if there was any errors while downloading.

