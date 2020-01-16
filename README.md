# Census Geocoder API

This package facilitates the use of the [Census Geocoding Services](https://www.census.gov/data/developers/data-sets/Geocoding-services.html) in batch submission format.

## Usage

The script `encode_addresses.py` reads a csv file containing the required fields `address1`, `city`, `state` and `postalcode` and (optionally) a unique field `'addressid`. The `postalcode` should be in numerical ZIP5 or ZIP9 format. 

It writes the encoded addresses in batches of 1,000 to the `encoded` folder. 

You can run the script from the command line:
 ```python
python encode_addresses.py [-h] [-f FILE_NAME]
```
 
 The script looks for the csv file in the `data` folder and, per default expects it to be called `addresses.csv`. You can use the optional argument `-f` to specify an alternative filename. 
 
 
 ## Testing the script
 
 To test the script and view the results, you can run
 ```python
python encode_addresses.py -f test_addresses
```
This will encode 3,220 test addresses provided by https://github.com/EthanRBrown/rrad via the [OpenAddresses](https://openaddresses.io/) project.

## Installation

The dependencies are listed in `requirements.txt`; just run `pip install -r requirements.txt` in a virtual environment using Python 3.6+.


 