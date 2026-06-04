"""
SVGのベジェ曲線をPillowで再現し、favicon-32x32.png と apple-touch-icon.png を生成する。
"""
from PIL import Image, ImageDraw

OLIVE = (107, 127, 94)
LIGHT = (168, 188, 154)
CREAM = (250, 250, 248)


def cubic_bezier(p0, p1, p2, p3, n=24):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt**2*t*p1[0] + 3*mt*t**2*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt**2*t*p1[1] + 3*mt*t**2*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def make_outer(sc, ox, oy):
    """外側の炎シルエット（32×32座標系を sc 倍して (ox,oy) 平行移動）"""
    def t(p): return (p[0]*sc + ox, p[1]*sc + oy)
    segs = [
        cubic_bezier(t((16,2)),  t((19,6)),  t((24,11)), t((23,18))),
        cubic_bezier(t((23,18)), t((22,23)), t((19,28)), t((16,29))),
        cubic_bezier(t((16,29)), t((13,28)), t((10,23)), t((9,18))),
        cubic_bezier(t((9,18)),  t((8,11)),  t((10,8)),  t((12,7))),
        cubic_bezier(t((12,7)),  t((11,10)), t((12,13)), t((14,12)), 18),
        cubic_bezier(t((14,12)), t((14,8)),  t((15,4)),  t((16,2)),  18),
    ]
    pts = []
    for seg in segs:
        pts.extend(seg[:-1])
    return [(round(x), round(y)) for x, y in pts]


def make_inner(sc, ox, oy):
    """内側ハイライト"""
    def t(p): return (p[0]*sc + ox, p[1]*sc + oy)
    segs = [
        cubic_bezier(t((16,14)), t((17,17)), t((18,20)), t((17,23)), 16),
        cubic_bezier(t((17,23)), t((17,25)), t((16,26)), t((16,26)), 10),
        cubic_bezier(t((16,26)), t((15,25)), t((15,25)), t((15,23)), 10),
        cubic_bezier(t((15,23)), t((14,20)), t((15,17)), t((16,14)), 16),
    ]
    pts = []
    for seg in segs:
        pts.extend(seg[:-1])
    return [(round(x), round(y)) for x, y in pts]


def gen_32():
    img = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.polygon(make_outer(1, 0, 0), fill=(*OLIVE, 255))
    overlay = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    di = ImageDraw.Draw(overlay)
    di.polygon(make_inner(1, 0, 0), fill=(*LIGHT, 140))
    img = Image.alpha_composite(img, overlay)
    img.save('favicon-32x32.png')
    print('  OK  favicon-32x32.png')


def gen_180():
    SIZE = 180
    sc   = 5.0
    ox   = SIZE / 2 - 16 * sc       # 炎の x 中心を画像中心に揃える
    oy   = (SIZE - 27 * sc) / 2     # 炎の高さ（27単位）を上下中央に揃える

    img = Image.new('RGBA', (SIZE, SIZE), (*CREAM, 255))
    d = ImageDraw.Draw(img)
    d.polygon(make_outer(sc, ox, oy), fill=(*OLIVE, 255))
    overlay = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    di = ImageDraw.Draw(overlay)
    di.polygon(make_inner(sc, ox, oy), fill=(*LIGHT, 140))
    img = Image.alpha_composite(img, overlay)
    img.convert('RGB').save('apple-touch-icon.png')
    print('  OK  apple-touch-icon.png')


if __name__ == '__main__':
    print('生成中...')
    gen_32()
    gen_180()
    print('完了')
