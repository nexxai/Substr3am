# Substr3am

Substr3am is a python tool inspired by [subbrute](https://github.com/TheRook/subbrute) and [Sublist3r](https://github.com/aboul3la/Sublist3r) designed to generate a list of potential subdomains using the [certstream](https://github.com/CaliDog/certstream-python) service. It helps penetration testers and bug hunters collect and gather subdomains for their lists by connecting to the certstream firehose, watching for real subdomains, and adding them to a list for use with the above tools.

## Installation

```
git clone https://github.com/nexxai/Substr3am.git
```

## Recommended Python Version:

Substr3am currently supports **Python 3**.  Stop using **Python 2**.  I suck at Python and even I know that.

* The recommened version for Python 3 is **3.7.x**

## Dependencies:

Substr3am depends on the `certstream`, `argparse`, `tldextract`, and `sqlalchemy` python modules.

These dependencies can be installed using the requirements file:

- Installation on Windows:
```
c:\python\python.exe -m pip install -r requirements.txt
```
- Installation on Linux
```
sudo pip3 install -r requirements.txt
```

## Usage

Short Form    | Long Form     | Description
------------- | ------------- |-------------
-d            | --dump        | Dump the list of collected subdomains to names.txt

### Examples

* To export your collected subdomains from the sqlite DB to a file called 'names.txt

```python Substr3am.py -d```

## License

Substr3am is licensed under the GNU GPL license. take a look at the [LICENSE](https://github.com/nexxai/Substr3am/blob/master/LICENSE) for more information.


## Credits

* [aboul3la](https://github.com/aboul3la) - Substr3am's code was inspired by his wonderful tool **Sublist3r**
* [CaliDog](https://github.com/CaliDog) - For providing the awesome **certstream** service

## Version
**Current version is 1.0**