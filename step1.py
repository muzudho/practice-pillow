"""画像を新規作成して保存
直線上に資格を配置
"""

from PIL import Image, ImageDraw

black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
white = (255, 255, 255)

im = Image.new('RGB', (500, 500), white)
draw = ImageDraw.Draw(im)

# 四角を縦に16個並べる
# 幅0、高さ0 で、 1x1 の矩形になる。ブラシの太さ1が関係する？
w = 4
h = 0

x = 10
y = 9
for i in range(0, 16):
    xx = x
    draw.rectangle((xx, y, xx+w, y+h), fill=red, outline=None)
    xx += w+2
    draw.rectangle((xx, y, xx+w, y+h), fill=green, outline=None)
    xx += w+2
    draw.rectangle((xx, y, xx+w, y+h), fill=blue, outline=None)

    # 2px は開けないと、くっついている。 +1 だと隣なので
    y += h+2

y -= h+3
xx = x
draw.text((xx, y), "F", red)
xx += w+2
draw.text((xx, y), "F", green)
xx += w+2
draw.text((xx, y), "F", blue)

im.save('shared/pillow_imagedraw.png', quality=95)
