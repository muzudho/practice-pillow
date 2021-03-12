from PIL import Image, ImageDraw
import math

black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
white = (255, 255, 255)

im = Image.new('RGB', (450, 450), white)
draw = ImageDraw.Draw(im)


def main():

    theta_list = [90, 75, 60, 45, 30, 15, 0, 345,
                  330, 315, 300, 285, 270, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105]
    paint_gauge_ring(225, 225, 190, theta_list)


def paint_gauge_ring(left, top, range, theta_list):
    for theta in theta_list:
        x = range*math.cos(math.radians(theta))
        y = range*math.sin(math.radians(theta))
        paint_gauge(x+left, y+top, 0x00, 0x09, 0xff)


def paint_gauge(src_center_x, src_center_y, r, g, b):
    # 四角を縦に16個並べる
    # 幅0、高さ0 で、 1x1 の矩形になる。ブラシの太さ1が関係する？
    w = 10
    h = 0

    # ゲージの矩形面積をだいたい計算
    gauge_w = 3*(w+2)-2
    gauge_h = 16*(h+2)+6

    # 中心座標を 左上起点座標に変更
    src_x = src_center_x - gauge_w/2
    src_y = src_center_y - gauge_h/2

    # ゲージの面積をだいたい視覚化
    draw.rectangle((src_x, src_y, gauge_w+src_x,
                    gauge_h+src_y), outline=black)

    y = src_y
    for _ in range(0, 16):
        x = src_x
        draw.rectangle((x, y, x+w, y+h), fill=red, outline=None)
        x += w+2
        draw.rectangle((x, y, x+w, y+h), fill=green, outline=None)
        x += w+2
        draw.rectangle((x, y, x+w, y+h), fill=blue, outline=None)

        # 2px は開けないと、くっついている。 +1 だと隣なので
        y += h+2

    y -= h+3
    x = src_x
    draw.text((x, y), f"{r:02x}", red)
    x += w+2
    draw.text((x, y), f"{g:02x}", green)
    x += w+2
    draw.text((x, y), f"{b:02x}", blue)

    im.save('shared/pillow_imagedraw.png', quality=95)
    pass


main()
