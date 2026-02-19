import pygame
import random
pygame.init()

    

screenW, screenH=1350, 810
color=(255, 255, 255)
clock=pygame.time.Clock()
screen=pygame.display.set_mode((screenW, screenH))
pygame.display.set_caption("minesweeper")

bgIMG=pygame.image.load("assets/bg.png").convert()
titleIMG=pygame.image.load("assets/title.png").convert_alpha()
iconIMG=pygame.image.load("assets/icon.png").convert_alpha()
pygame.display.set_icon(iconIMG)
game_mode="unselected"
explode=False
gameover=False
first_click=True
mine_count=0
easybtnIMG=pygame.image.load("assets/difficulty-1.png").convert_alpha()
medibtnIMG=pygame.image.load("assets/difficulty-2.png").convert_alpha()
hardbtnIMG=pygame.image.load("assets/difficulty-3.png").convert_alpha()

btn_hitbox1=pygame.Rect(30, 370, 400, 300) #按鈕點擊範圍
btn_hitbox2=pygame.Rect(470, 370, 400, 300)
btn_hitbox3=pygame.Rect(910, 370, 400, 300)

flash=pygame.Surface((screenW, screenH))
flash.fill((255, 255, 255))

win_flash=pygame.Surface((screenW, screenH))
win_flash.fill((255, 255, 0))

unclickedSqIMG=pygame.image.load("assets/b-unclicked.png").convert()

clicked0IMG=pygame.image.load("assets/clicked0.png").convert()
clicked1IMG=pygame.image.load("assets/clicked1.png").convert()
clicked2IMG=pygame.image.load("assets/clicked2.png").convert()
clicked3IMG=pygame.image.load("assets/clicked3.png").convert()
clicked4IMG=pygame.image.load("assets/clicked4.png").convert()
clicked5IMG=pygame.image.load("assets/clicked5.png").convert()
clicked6IMG=pygame.image.load("assets/clicked6.png").convert()
clicked7IMG=pygame.image.load("assets/clicked7.png").convert()
clicked8IMG=pygame.image.load("assets/clicked8.png").convert()
explodedIMG=pygame.image.load("assets/clicked_mine.png").convert()
flaggedIMG=pygame.image.load("assets/b_flagged.png").convert()
wrongIMG=pygame.image.load("assets/b_wrong.png").convert()
mineIMG=pygame.image.load("assets/minesq.png").convert()


loseIMG=pygame.image.load("assets/lose.png").convert_alpha()
winIMG=pygame.image.load("assets/win.png").convert_alpha()
hintIMG=pygame.image.load("assets/hint.png").convert_alpha()
hint_scale=0.4
loseW, loseH=loseIMG.get_size()
winW, winH=winIMG.get_size()
hintW, hintH=hintIMG.get_size()
hintIMG=pygame.transform.scale(hintIMG, (hintW*hint_scale, hintH*hint_scale))
remainingIMG=pygame.image.load("assets/mine.png").convert_alpha()
remainingW, remainingH=remainingIMG.get_size()
remaining_scale=0.2
remainingIMG=pygame.transform.scale(remainingIMG, (remainingW*remaining_scale, remainingH*remaining_scale))
button_snd=pygame.mixer.Sound("assets/button.mp3")
dig_snd=pygame.mixer.Sound("assets/dig.mp3")
lose_snd=pygame.mixer.Sound("assets/lose.mp3")
win_snd=pygame.mixer.Sound("assets/win.mp3")
flag_snd=pygame.mixer.Sound("assets/flag.mp3")
unflag_snd=pygame.mixer.Sound("assets/unflag.mp3")
# button_snd.set_volume(0.4)
# dig_snd.set_volume(0.4)
# lose_snd.set_volume(0.4)
# win_snd.set_volume(0.4)
# flag_snd.set_volume(0.4)
# unflag_snd.set_volume(0.4)
gameover_timer=0
squares=[]
remaining=0
dt=0
game_timer=0

font=pygame.font.SysFont(None,40)
class Square:
    def __init__(self, img, row, col, mode):
        self.img=img
        self.w, self.h=img.get_size()
        self.row, self.col=row, col
        self.clicked=False
        self.flagged=False
        self.mines=0
        self.values=[clicked0IMG, clicked1IMG, clicked2IMG, clicked3IMG, clicked4IMG, clicked5IMG,
                     clicked6IMG, clicked7IMG, clicked8IMG, explodedIMG]
        self.mine=mineIMG
        self.flagSq=flaggedIMG
        self.exploded=False
        self.wrong=wrongIMG
        self.change(mode)
    def change(self, mode):
        match mode:
            case "easy": #if mode=="easy"
                self.scale=0.3
                gridx, gridy=7, 7
            case "medium": #match/case is available for Python 3.10+
                self.scale=0.15
                gridx, gridy=16, 16
            case "hard": 
                self.scale=0.15
                gridx, gridy=30, 16
            case _: return #if mode=="unselected"
        self.img=pygame.transform.scale(self.img, (self.w*self.scale, self.h*self.scale))
        boardW, boardH=self.w*gridx*self.scale, self.h*gridy*self.scale
        self.x0, self.y0=screenW/2-boardW/2, screenH/2-boardH/2
        self.x=self.x0+self.col*self.img.get_width()
        self.y=self.y0+self.row*self.img.get_height()
        self.values=[pygame.transform.scale(val, (self.w*self.scale, self.h*self.scale)) for val in self.values]
        self.hitbox=pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
        self.mine=pygame.transform.scale(self.mine, (self.w*self.scale, self.h*self.scale))
        self.flagSq=pygame.transform.scale(self.flagSq, (self.w*self.scale, self.h*self.scale))
        self.wrong=pygame.transform.scale(self.wrong, (self.w*self.scale, self.h*self.scale))
    def draw(self, gamesurface, gameover=False):
        if explode:
            if self.exploded: gamesurface.blit(self.values[-1], (self.x, self.y))
            elif self.flagged and self.mines!=-1: gamesurface.blit(self.wrong, (self.x, self.y))
            elif self.mines==-1:
                if self.flagged: gamesurface.blit(self.flagSq, (self.x, self.y))
                else: gamesurface.blit(self.mine, (self.x, self.y))
            elif self.clicked: gamesurface.blit(self.values[self.mines], (self.x, self.y))
            else: gamesurface.blit(self.img, (self.x, self.y))
        elif gameover:
            if self.mines==-1: gamesurface.blit(self.flagSq, (self.x, self.y))
            else: gamesurface.blit(self.values[self.mines], (self.x, self.y))
        else:
            if self.flagged: gamesurface.blit(self.flagSq, (self.x, self.y))
            elif not self.clicked: gamesurface.blit(self.img, (self.x, self.y))
            else: gamesurface.blit(self.values[self.mines], (self.x, self.y))


def place_mines(board, mine_count, clckdR, clckdC):
    rows=len(board)
    cols=len(board[0])
    placed=0
    while placed<mine_count:
        r, c= random.randrange(rows), random.randrange(cols)
        if r==clckdR and c==clckdC: continue
        if board[r][c].mines!=-1:
            board[r][c].mines=-1
            placed+=1
def mark(board):
    r, c=len(board), len(board[0])
    for y in range(r):
        for x in range(c):
            if board[y][x].mines==-1: continue
            else:
                board[y][x].mines=0
                for dy in range(-1, 2):
                    if 0<=y+dy<r:
                        for dx in range(-1, 2):
                            if 0<=x+dx<c:
                                if board[y+dy][x+dx].mines==-1: board[y][x].mines+=1
def flood_fill(board, clckdr, clckdc):
    r, c=len(board), len(board[0])
    stack=[(clckdr, clckdc)]
    while stack:
        y, x=stack.pop()
        square=board[y][x]
        if square.clicked or square.mines==-1: continue
        square.clicked=True
        dig_snd.play()
        if square.mines==0:
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if 0<=y+dy<r and 0<=x+dx<c:
                        if not board[y+dy][x+dx].clicked: stack.append((y+dy, x+dx))
    return board
def chord_open(board, clckdR, clckdC):
    if not board[clckdR][clckdC].clicked: return
    flag_count=0
    for dy in range(-1, 2):
        if 0<=clckdR+dy<len(board):
            for dx in range(-1, 2):
                if 0<=clckdC+dx<len(board[0]):
                    if board[clckdR+dy][clckdC+dx].flagged: flag_count+=1
    if flag_count==board[clckdR][clckdC].mines:
        for dy in range(-1, 2):
            if 0<=clckdR+dy<len(board):
                for dx in range(-1, 2):
                    if 0<=clckdC+dx<len(board[0]):
                        target=board[clckdR+dy][clckdC+dx]
                        if not target.clicked and not target.flagged:
                            if target.mines==-1:
                                target.exploded=True
                                return "explode"
                            else:
                                flood_fill(board, clckdR+dy, clckdC+dx)
def generate_board(mode):
    match mode:
        case "easy": 
            gridX, gridY=7, 7
        case "medium": 
            gridX, gridY=16, 16
        case "hard": 
            gridX, gridY=30, 16
        case "unselected": 
            mine_count=0
            return []
    squares=[]
    for rs in range(gridY):
        row_list=[Square(unclickedSqIMG, rs, cs, mode) for cs in range(gridX)]
        squares.append(row_list)
    return squares

def confirm(board):
    r, c=len(board), len(board[0])
    for y in range(r):
        for x in range(c):
            if board[y][x].mines!=-1 and not board[y][x].clicked: return False
    return True

gamesurface=pygame.Surface((screenW, screenH))
running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            if game_mode=="unselected":
                if btn_hitbox1.collidepoint(event.pos):
                    game_mode="easy" #確認是否點到按鈕
                    squares=generate_board(game_mode)
                    button_snd.play()
                    mine_count=10
                    remaining=mine_count
                    
                elif btn_hitbox2.collidepoint(event.pos):
                    game_mode="medium"
                    squares=generate_board(game_mode)
                    button_snd.play()
                    mine_count=40
                    remaining=mine_count
                    
                elif btn_hitbox3.collidepoint(event.pos):
                    game_mode="hard"
                    squares=generate_board(game_mode)
                    button_snd.play()
                    mine_count=99
                    remaining=mine_count
                    
            elif not gameover:
                if event.button==1: #滑鼠左鍵（點開格子）
                    for rs in squares:
                        for cs in rs:
                            if cs.hitbox.collidepoint(event.pos):
                                if cs.clicked:
                                    result=chord_open(squares, cs.row, cs.col)
                                    if result=="explode":
                                        explode=True
                                        gameover=True
                                        gameover_timer=0
                                        lose_snd.play()
                                    break
                                if cs.flagged==True: continue
                                if first_click:
                                    first_click=False
                                    dig_snd.play()
                                    place_mines(squares, mine_count, cs.row, cs.col)
                                    mark(squares)
                                if cs.mines==-1 and not cs.flagged: 
                                    cs.exploded=True
                                    explode, gameover=True, True
                                    gameover_timer=0
                                    lose_snd.play()
                                else: 
                                    flood_fill(squares, cs.row, cs.col)
                                break
                if event.button==3: #滑鼠右鍵（標旗）
                    for rs in squares:
                        for cs in rs:
                            if cs.hitbox.collidepoint(event.pos) and not cs.clicked:
                                if cs.flagged: 
                                    cs.flagged=False
                                    unflag_snd.play()
                                    remaining+=1
                                else: 
                                    cs.flagged=True
                                    flag_snd.play()
                                    remaining-=1
            elif gameover:
                explode=False
                gameover=False
                first_click=True
                game_mode="unselected"
                game_timer=0
        
    if game_mode!="unselected" and not first_click and not gameover: game_timer+=dt
    if game_mode=="unselected":
        gamesurface.blit(bgIMG, (0, 0))
        gamesurface.blit(titleIMG, (456, 150))
        gamesurface.blit(easybtnIMG, (30, 370))
        gamesurface.blit(medibtnIMG, (470, 370))
        gamesurface.blit(hardbtnIMG, (910, 370))
    else:
        gamesurface.blit(bgIMG, (0, 0))
        gamesurface.blit(remainingIMG, (0, 0))
        counter_txt=font.render(f"x{remaining}", True, (0, 0, 0))
        gamesurface.blit(counter_txt, (remainingW*remaining_scale, remainingH*remaining_scale/4))
        timer_txt=font.render(f"Elapsed Time:{int(game_timer//3600)}h {int((game_timer%3600)//60)}m {(game_timer%60):05.2f}s", True, (0, 0, 0))
        timerW, timerH=timer_txt.get_size()
        gamesurface.blit(timer_txt, (screenW/2-timerW/2, 0))
        for row in squares:
            for square in row:
                square.draw(gamesurface, gameover)
        if not gameover and confirm(squares):
            remaining=0
            explode=False
            gameover=True
            gameover_timer=0
            win_snd.play()
            first_click=True
        if gameover:
            if explode: 
                if gameover_timer<=0.2:
                    alpha=255*(1-gameover_timer/0.2)
                    flash.set_alpha(alpha)
                    gamesurface.blit(flash, (0, 0))
                elif gameover_timer>=1:
                    gamesurface.blit(loseIMG, (screenW/2-loseW/2, screenH/2-loseH/2))
                    gamesurface.blit(hintIMG, (screenW/2-hintW*hint_scale/2, screenH/2+loseH/2))
                gameover_timer+=dt
            else: 
                if gameover_timer<=0.2:
                    alpha=255*(1-gameover_timer/0.2)
                    win_flash.set_alpha(alpha)
                    gamesurface.blit(win_flash, (0, 0))
                elif gameover_timer>=0.5:
                    gamesurface.blit(winIMG, (screenW/2-winW/2, screenH/2-winH/2))
                    gamesurface.blit(hintIMG, (screenW/2-hintW*hint_scale/2, screenH/2+winH/2))
                gameover_timer+=dt


        
    screen.blit(gamesurface, (0, 0))
    pygame.display.flip()
    dt=clock.tick(60)/1000
pygame.quit()
