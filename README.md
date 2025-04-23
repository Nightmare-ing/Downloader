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

### Download Files

Run with the command in the verbose form as following, replace `<login url>` with your desired URL, and replace `<links.csv>` with the directory to the file which contain links.

```shell
(.venv)$ python3 download.py --file <links.csv> --url <login url>
```

Or you can run in the non-verbose form

```shell
(.venv)$ python3 download.py -f <links.csv> -u <login url>
```

### Generate Files for Downloading

You can run script `DL_config_gen.py` to generate downloading configs from source file `*.src`, an example for `*.src` file is shown in dir `examples/`. The code to run the script is

```shell
(.venv)$ python3 DL_config_gen.py -f <links.src>
```

All the lines start with `#` and empty lines will be ignored

## Features

- Support downloading with both `yml` file and `csv` file.
  - Format of both file are shown in `examples/links-example.csv` and `examples/links-example.yml`
  - If you download with `yml`, the script will create sub-directories with the value of `group name` in `yml`
  - If you download with `csv`, no sub-directories will be created, all files are under directory `outputs`

## TODO

- Process multiple csv files
  - [ ] Becase csv file can't contain comments, so unable to group links with notation
  - [x] Try to use something like json file, each term contains the name of the link group and the file name of this link group
- Login to multiple required websites
  - [ ] May want to download files from several different websites
  - [ ] Try to store login urls into a csv file
