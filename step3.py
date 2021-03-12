from PIL import Image, ImageDraw
import math

# black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
white = (255, 255, 255)

im = Image.new('RGB', (400, 400), white)
draw = ImageDraw.Draw(im)


def main():

    theta_list = [90, 75, 60, 45, 30, 15, 0, 345,
                  330, 315, 300, 285, 270, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105]
    paint_gauge_ring(190, 180, 160, theta_list)


def paint_gauge_ring(left, top, range, theta_list):
    for theta in theta_list:
        x = range*math.cos(math.radians(theta))
        y = range*math.sin(math.radians(theta))
        paint_gauge(x+left, y+top)


def paint_gauge(x, y):
    # 四角を縦に16個並べる
    # 幅0、高さ0 で、 1x1 の矩形になる。ブラシの太さ1が関係する？
    w = 4
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
    draw.text((xx, y), "F", red)
    xx += w+2
    draw.text((xx, y), "F", green)
    xx += w+2
    draw.text((xx, y), "F", blue)

    im.save('shared/pillow_imagedraw.png', quality=95)
    pass


main()
