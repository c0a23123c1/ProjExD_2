import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {pg.K_UP: (0, -5),
         pg.K_DOWN: (0, +5),
         pg.K_LEFT: (-5, 0),
         pg.K_RIGHT: (+5, 0),
         }
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    引数:こうかとん または 爆弾のRect
    戻り値:真理値のタプル
    画面外ならFalse  画面内ならTure
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate


def game_over(screen, sub_kk_rct):
    """
    ゲーム失敗時の画面の関数
    """
    go_img = pg.Surface((WIDTH,HEIGHT)) # ゲーム終了時の背景画面作成
    pg.draw.rect(go_img, (0, 0, 0), pg.Rect(0,0,1100, 650))
    go_img.set_alpha(155)
    screen.blit(go_img, [0, 0])

    fonto = pg.font.Font(None, 80)  # 文字の追加
    txt = fonto.render("Game Over", True, (255, 0, 0))
    rect = txt.get_rect(center = (WIDTH // 2, HEIGHT // 2))
    screen.blit(txt, rect)

    sub_kk = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1)  # こうかとんの追加
    screen.blit(sub_kk, sub_kk_rct)
    pg.display.update()


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))  # 爆弾作成
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10),  10)
    bb_img.set_colorkey((0, 0, 0))
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, -5  # 爆弾の速度 
    clock = pg.time.Clock()
    sub_kk_rct = kk_rct
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0])
        if kk_rct.colliderect(bb_rct):  # こうかとんと爆弾が重なっていたら
            game_over(screen, sub_kk_rct)
            time.sleep(5)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]  # 縦座標, 横座標
        #if key_lst[pg.K_UP]:
        #    sum_mv[1] -= 5
        #if key_lst[pg.K_DOWN]:
        #    sum_mv[1] += 5
        #if key_lst[pg.K_LEFT]:
        #    sum_mv[0] -= 5
        #if key_lst[pg.K_RIGHT]:
        #    sum_mv[0] += 5
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]  # 横方向
                sum_mv[1] += tpl[1]  # 縦方向
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):  # 爆弾が画面外に行かないように
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1    
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
