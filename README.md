# Python utility for printing lables on Brother P-Touch P750W

Since I haven't found any reasonable way to use broher p-touch software on linux with Brother P-Touch P750W printer, with help of [this](http://www.odorik.cz/w/ptouch) ruby code I've written a python utility for printing labels.

## Dependencies
- python 3+
- [pillow](https://pypi.org/project/Pillow/) - for text to image conversion
- [treepoem](https://pypi.org/project/treepoem/) - for generating datamatricies

## Usage

```python labelprint.py text_to_print path_to_printer [custom_datamatrix_data]```

- For me the printer is located at /dev/usb/lp0 and belongs to the lp group.
- Without the last parameter, datamatrix contain text_to_print data

## Example
<img style="border: 1px solid black;" src="example.png">
