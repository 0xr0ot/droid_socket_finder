# Droid Socket Finder
A Python script for mapping local sockets to their corresponding processes.  I believe the original script was published on Wooyun around 2015.

## Setup

* Create a ```bin``` directory underneath the root folder and drop in ```adb```
* Use PIP to install the required packages

## Usage
```python 
python run.py
```
## Example Output
```
[2016-12-02 09:34:15.594185] Running search ...
------------------------------------------------------------------------------------------------------------------------------------------------------
[0] com.google.android.youtube		tcp6       0      0 ::ffff:127.0.0.1:38052 :::*                   LISTEN
```
