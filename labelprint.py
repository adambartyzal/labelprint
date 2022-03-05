import sys
import treepoem
from PIL import Image, ImageDraw, ImageFont

if (len(sys.argv) < 3):
  print(f'Usage: python {sys.argv[0]} text_to_print path_to_printer [custom_datamatrix_data]')
  exit()

text = sys.argv[1]
printer = sys.argv[2]
datamatrix_data = sys.argv[3] if (len(sys.argv) == 4) else text

label_height = 64

datamatrix_width = label_height

text_size = 24
text_border_width = 10

label_length = int(datamatrix_width  + 2 * text_border_width + ((len(text)) * (text_size) * 0.6))

label = Image.new('1', (label_length, label_height), color = 1)

fnt = ImageFont.truetype('./RobotoMono-Regular.ttf', text_size)
d = ImageDraw.Draw(label)
d.text((datamatrix_width + text_border_width, 15), text, font=fnt, color = 1)

label = label.rotate(270, expand=1)

datamatrix = treepoem.generate_barcode(
    barcode_type = 'datamatrix',
    data = datamatrix_data,
).resize((datamatrix_width, datamatrix_width), resample=Image.NEAREST).rotate(270)

label.paste(datamatrix)

image_data = bytearray(label.tobytes())

for i in range(len(image_data)):
  image_data[i] = -image_data[i] + 255 # invert colors

data = b'\x00' * 100
data += b'\x1B\x40' # print start
data += b'\x1B\x69\x4D\x40' # pre-cut
data += b'\x1B\x69\x4B\x08' # end cut
data += b'\x4d\x02' # compression

for line in range(label_length):
  data_start = int(line * (label_height / 8))
  data_end = int(data_start + (label_height / 8) - 1)
  lower_padding = int((16 - label_height / 8) / 2)
  upper_padding = int((16 - label_height / 8) - lower_padding)
  image_part = image_data[data_start:data_end+1] # cut one line of the image
  binary = bin(int(image_part.hex(), 16))[2:].zfill(64) # bytes to binary str
  reversed = int(binary[::-1], 2).to_bytes(len(binary) // 8, byteorder='big') # reverse bit order and convert back to bytes
  data_part = b'\x47\x11\x00\x0F' + b'\x00' * lower_padding + reversed + b'\x00' * upper_padding # line data for printer
  data += data_part
data += b'\x1A' # print end

with open(printer, 'wb') as file:
  file.write(data)
