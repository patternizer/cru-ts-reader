# cru-ts-reader

Python CRU TS reader code:

* Python reader for CRU TS .dtb files and analogous format data files.

## Contents

* `read_cruts_dtb.py` - python reader

The first step is to clone the latest cru-ts-reader code and step into the check out directory: 

    $ git clone https://github.com/patternizer/cru-ts-reader.git
    $ cd cru-ts-reader

Set the filename_txt variable in read_cruts_dtb.py with the name and path for your .dtb file.

### Usage

The code was tested locally in a Python 3.8.5 virtual environment.

    $ python read_cruts_dtb.py

This should generate a .CSV file from a pandas dataframe having the same filename as your chosen .dtb file.

## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)



