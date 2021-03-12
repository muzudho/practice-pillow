from PIL import Image, ImageDraw
import math

black = (0, 0, 0)
red = (0xff, 0x33, 0x66)
green = (0x66, 0xff, 0x33)
blue = (0x33, 0x66, 0xff)
light_gray = (0xee, 0xee, 0xee)
white = (255, 255, 255)

im = Image.new('RGB', (450, 450), white)
draw = ImageDraw.Draw(im)


def main():

    # 0時の方向から時計回り
    theta_list = [90, 75, 60, 45, 30, 15, 0, 345,
                  330, 315, 300, 285, 270, 255, 240, 225, 210, 195, 180, 165, 150, 135, 120, 105]
    # 0時を赤
    color_list = [(0xff, 0x66, 0x99), (0xff, 0x77, 0x77),
                  (0xff, 0x99, 0x66), (0xff, 0xaa, 0x55),
                  (0xff, 0xcc, 0x33), (0xff, 0xdd, 0x33),
                  (0xbb, 0xee, 0x33), (0xaa, 0xff, 0x44),
                  (0x99, 0xff, 0x66), (0x88, 0xff, 0x88),
                  (0x66, 0xff, 0x99), (0x33, 0xff, 0xbb),
                  (0x33, 0xee, 0xcc), (0x33, 0xdd, 0xdd),
                  (0x33, 0xcc, 0xff), (0x55, 0xaa, 0xff),
                  (0x66, 0x99, 0xff), (0x66, 0x66, 0xff),
                  (0x99, 0x66, 0xff), (0xbb, 0x44, 0xff),
                  (0xcc, 0x33, 0xff), (0xee, 0x33, 0xff),
                  (0xff, 0x33, 0xcc), (0xff, 0x44, 0xbb)]

    # 環状 ゲージ 描画
    gauge_center_coords = center_coords_on_ring(225, 225, 190, theta_list)
    paint_gauge_ring(gauge_center_coords, color_list)

    # 環状 色セル 描画
    color_cell_center_coords = center_coords_on_ring(225, 225, 120, theta_list)
    size = len(color_cell_center_coords)
    for i in range(0, size):
        x, y = color_cell_center_coords[i]

        circle_w = 16

        fill_color = color_list[i]
        draw.ellipse((x-circle_w/2, y-circle_w/2, x +
                      circle_w, y+circle_w), fill=fill_color)

    # ゲージ座標
    size = len(gauge_center_coords)
    for i in range(0, size):
        p = gauge_center_coords[i]
        x, y = coord_on_gauge(p)

        # ゲージ3+隙間1 の 4 なんでゲージは左にずれているから中心を調整する
        x -= 1

        point_w = 4

        horizontal_interval = 13

        # 赤ゲージ
        draw.ellipse((x-point_w/2-horizontal_interval, y-point_w/2, x+point_w-horizontal_interval, y+point_w), fill=red,
                     outline=(155, 155, 155))

        # 緑ゲージ
        draw.ellipse((x-point_w/2, y-point_w/2, x+point_w, y+point_w), fill=green,
                     outline=(155, 155, 155))

        # 青ゲージ
        draw.ellipse((x-point_w/2+horizontal_interval, y-point_w/2, x+point_w+horizontal_interval, y+point_w), fill=blue,
                     outline=(155, 155, 155))

    im.save('shared/pillow_imagedraw.png', quality=95)


def center_coords_on_ring(left, top, range, theta_list):
    coolds = []
    for theta in theta_list:
        x = range*math.cos(math.radians(theta))+left
        # yは上下反転
        y = -range*math.sin(math.radians(theta))+top
        coolds.append((x, y))
    return coolds


def paint_gauge_ring(gauge_center_coords, color_list):
    """ 環状 ゲージ 描画
    """
    size = len(gauge_center_coords)
    for i in range(0, size):
        p = gauge_center_coords[i]
        color = color_list[i]
        paint_gauge(p[0], p[1], color[0], color[1], color[2])


def coord_on_gauge(p):
    """RPGゲージの頂点という変なところの座標を求めます
    """
    return p[0], p[1]


def paint_gauge(src_center_x, src_center_y, r, g, b):
    # 四角を縦に16個並べる
    # 幅0、高さ0 で、 1x1 の矩形になる。ブラシの太さ1が関係する？
    w = 10
    h = 0

    # フォントのだいたいの高さ
    font_height = 8

    # ゲージの矩形面積をだいたい計算
    gauge_w = 3*(w+2)-2
    gauge_h = 16*(h+2)+font_height-2

    # 中心座標を 左上起点座標に変更
    src_x = src_center_x - gauge_w/2
    src_y = src_center_y - gauge_h/2

    # ゲージの面積をだいたい視覚化
    # draw.rectangle((src_x, src_y, gauge_w+src_x,
    #                gauge_h+src_y), outline=black)

    # 赤ゲージ
    paint_one_color_gauge(src_x, src_y, w, h, r, red)

    # 青ゲージ
    paint_one_color_gauge(src_x+w+2, src_y, w, h, g, green)

    # 緑ゲージ
    paint_one_color_gauge(src_x+2*(w+2), src_y, w, h, b, blue)

    y = gauge_h+src_y-font_height
    x = src_x
    draw.text((x, y), f"{r:02x}", red)
    x += w+2
    draw.text((x, y), f"{g:02x}", green)
    x += w+2
    draw.text((x, y), f"{b:02x}", blue)


def paint_one_color_gauge(src_left, src_top, w, h, value, fill_color):
    """一色ゲージ
    Parameters
    ----------
    value : int
        0...255
    """

    half_byte = byte_to_half_byte(value)

    y = src_top
    for i in range(0, 16):
        x = src_left

        if half_byte < (16-i):
            fc = light_gray
        else:
            fc = fill_color

        draw.rectangle((x, y, x+w, y+h), fill=fc, outline=None)

        # 2px は開けないと、くっついている。 +1 だと隣なので
        y += h+2
    pass


def byte_to_half_byte(value):
    """0～255を、0～15に縮めます
    """
    return int(value/16)


main()
