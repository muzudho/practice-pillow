from PIL import Image, ImageDraw
import math

# black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
white = (255, 255, 255)

im = Image.new('RGB', (430, 430), white)
draw = ImageDraw.Draw(im)


def main():

    theta_list = [90, 75, 60, 45, 30, 15, 0, 345,
                  330, 315, 300, 285, 270, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105]
    paint_gauge_ring(195, 195, 190, theta_list)


def paint_gauge_ring(left, top, range, theta_list):
    for theta in theta_list:
        x = range*math.cos(math.radians(theta))
        y = range*math.sin(math.radians(theta))
        paint_gauge(x+left, y+top, 0x00, 0x09, 0xff)


def paint_gauge(x, y, r, g, b):
    # 四角を縦に16個並べる
    # 幅0、高さ0 で、 1x1 の矩形になる。ブラシの太さ1が関係する？
    w = 10
    h = 0

    for _ in range(0, 16):
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
    draw.text((xx, y), f"{r:02x}", red)
    xx += w+2
    draw.text((xx, y), f"{g:02x}", green)
    xx += w+2
    draw.text((xx, y), f"{b:02x}", blue)

    im.save('shared/pillow_imagedraw.png', quality=95)
    pass


main()
