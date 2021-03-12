from PIL import Image, ImageDraw
import math

# black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
white = (255, 255, 255)

im = Image.new('RGB', (500, 500), white)
draw = ImageDraw.Draw(im)


def main():

    top = 160
    left = 160
    range = 160
    theta_list = [90, 75, 60, 45, 30, 15, 0, 345,
                  330, 315, 300, 285, 270, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105]
    for theta in theta_list:
        x = range*math.sin(math.radians(theta))
        y = range*math.cos(math.radians(theta))
        paint_gauge(x+top, y+left)

    """
    paint_gauge(10, 9)
    paint_gauge(30, 9)
    paint_gauge(50, 9)
    paint_gauge(70, 9)
    paint_gauge(90, 9)
    paint_gauge(110, 9)
    paint_gauge(130, 9)
    paint_gauge(150, 9)
    paint_gauge(170, 9)
    paint_gauge(190, 9)
    paint_gauge(210, 9)
    paint_gauge(230, 9)
    """


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
