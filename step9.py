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

    draw_image(theta_list, color_list, 'shared/pillow_imagedraw.png')


def draw_image(theta_list, color_list, file_name):
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

    # ３本ゲージ各天辺座標計算
    three_gauges_top_coords = []
    size = len(gauge_center_coords)
    for i in range(0, size):
        p = gauge_center_coords[i]
        color = color_list[i]

        # 黄緑の中心から見て、赤と青の中心が離れているピクセル数
        horizontal_interval = 12

        # 赤ゲージ
        rx, ry = coord_on_gauge(p, color[0])
        # ゲージ3+隙間1 の 4 なんでゲージは左にずれているので、その１ピクセル分調整（本来はゲージ全体を1ピクセル右にずらすのも合わせるべき）
        rx = rx - 1 - horizontal_interval

        # 緑ゲージ
        gx, gy = coord_on_gauge(p, color[1])
        gx = gx - 1

        # 青ゲージ
        bx, by = coord_on_gauge(p, color[2])
        bx = bx - 1 + horizontal_interval

        three_gauges_top_coords.append(((rx, ry), (gx, gy), (bx, by)))

    # 赤緑青個別ゲージ座標
    for top_coords in three_gauges_top_coords:

        # １ドットの点を打つと、次の４パターンにぶれる。1ピクセル単位の精度に期待しないこと
        #
        # パターン１  パターン２ パターン３  パターン４
        #  x         xx        xxx        xx
        # x x        xx        xxx        xx
        #  x                              xx
        point_w = 4

        # 赤ゲージ
        x, y = top_coords[0]
        # ゲージ3+隙間1 の 4 なんでゲージは左にずれているので、その１ピクセル分調整（本来はゲージ全体を1ピクセル右にずらすのも合わせるべき）
        x -= 1
        draw.ellipse((x-point_w/2, y-point_w/2, x+point_w, y+point_w), fill=red,
                     outline=(155, 155, 155))

        # 緑ゲージ
        x, y = top_coords[1]
        x -= 1
        draw.ellipse((x-point_w/2, y-point_w/2, x+point_w, y+point_w), fill=green,
                     outline=(155, 155, 155))

        # 青ゲージ
        x, y = top_coords[2]
        x -= 1
        draw.ellipse((x-point_w/2, y-point_w/2, x+point_w, y+point_w), fill=blue,
                     outline=(155, 155, 155))

    # 赤レーザー
    draw_beams(three_gauges_top_coords, 0, red)

    # 緑レーザー
    draw_beams(three_gauges_top_coords, 1, green)

    # 青レーザー
    draw_beams(three_gauges_top_coords, 2, blue)

    # im.save(file_name, quality=95)
    im.save(file_name)


def draw_beams(three_gauges_top_coords, rgb_index, color):
    half_size = int(len(three_gauges_top_coords)/2)
    for i in range(0, half_size):
        top_coords1 = three_gauges_top_coords[i]
        top_coords2 = three_gauges_top_coords[i+half_size]
        # 赤ゲージ１
        src_x, src_y = top_coords1[rgb_index]
        # 赤ゲージ２
        dst_x, dst_y = top_coords2[rgb_index]

        draw.line((src_x, src_y, dst_x, dst_y), fill=color, width=2)
    pass


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


def coord_on_gauge(p, value):
    """RPGゲージの頂点という変なところの座標を求めます
    """
    half_byte = byte_to_half_byte(value)
    # 目視で ３本ゲージ面積の矩形の中心から 11 ピクセル下が 一番下のバー
    return p[0], p[1]+11-2*half_byte


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
