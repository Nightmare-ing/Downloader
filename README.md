# Python Download Script

This is a simple python script for downloading resources which are protected with login information.
When running this script, a browser window pops up, then you just login as in normal browser. The script will store the cookies and then use them to download files listed in `links.csv`.

## Install Rrequirements

I run with python3.13, don't know whether it's OK for other versions of python. To run the code, create a virtual environment under the current directory, then install the requirements

```shell
python3.13 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run the Script

Run with the command as following, replace `<login url>` with your desired URL.

```shell
(.venv)$ python3 download.py <login url>
```
