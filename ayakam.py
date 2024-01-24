import pyxel
import random
import time

# メモ
#   ・座標の取り方は、左上が原点。（例えば、x=0, y=0なら左上の角。yが大きくなるほど下に下がる。xが大きくなるほど右に行く。アイテムなども同じ。）


#上から落とすアイテムのクラス
class Item: 
    def __init__(self):
        self.x = pyxel.width // 2  # アイテムの最初横位置
        self.y = 10  # アイテムの最初の高さ
        self.speed = 3  # アイテムの落ちる速度
        self.is_falling = False  # アイテムが落ちてるのか否かフラグ（最初は落ちてないのでfalse）
        self.radius = 5  # ボールの直径
        self.color = 8  # ボールの色
        pyxel.load("usagi.pyxres")
        self.num = 0

    def update(self):
        if self.is_falling:
            # アイテムが落下中の場合、y座標を増加させる
            self.y += self.speed
        else:
            # アイテムを上部に固定する
            self.y = 10
            # マウスのx座標に追随させる
            self.x = pyxel.mouse_x
            
    def draw(self):

        # pyxel.circ(self.x, self.y, self.radius, self.color)
        # numの番号でアイテムの種類が変わる
        if self.num == 0:
            pyxel.blt(self.x, self.y, 0, 0,  3, 13, 9, 0)  #消しゴム　ピクセルで表示されてた座標の位置
            self.width = 10
        elif self.num == 1:
            pyxel.blt(self.x, self.y, 0, 0, 21, 20, 5, 0)  #ペン
            self.width = 10
        elif self.num == 2:
            pyxel.blt(self.x, self.y, 0, 0, 35, 50, 16, 0)  #定規
            self.width = 10
        elif self.num == 3:
            pyxel.blt(self.x, self.y, 0, 0, 51, 20, 16, 0)  # にんじん
            self.width = 10
        
        # pyxel.rect(self.x, self.y, 10, 5, 11)



#下にあるバー（筆箱？）のクラス
class Bar: 
    def __init__(self):
        self.width = 45
        self.height = 5
        self.x = random.randint(0, pyxel.width - self.width)  # バーの初期位置をランダムに設定
        self.y = pyxel.height - 30  # バーを画面下部に配置
        self.speed = 2

    def update(self):
        # バーの移動および反転処理（筆箱）
        self.x += self.speed
        
        # バーが画面端に到達した場合、位置を修正して移動の向きを反転。と同時に、バーの速度をランダムに変化させる。
        if self.x <= 0: #左端に来た場合
            self.x = 0
            self.speed = random.uniform(1, 5)
        elif self.x + self.width >= pyxel.width: #右端に来た場合
            self.x = pyxel.width - self.width
            self.speed = -random.uniform(1, 5)

    def draw(self):
        # バーを描画
        # pyxel.rect(self.x, self.y, self.width, self.height, 11)
        pyxel.blt(self.x, self.y, 0, 1, 80, 60, 30, 0)
        

#ゲーム全体の動きのクラス
class Game: 
    def __init__(self): #ゲームの初期設定についての関数
        # Pyxelの初期化（初期設定）
        pyxel.init(200, 150, fps=60) #初期は160,120,60
        pyxel.mouse(True)
        

        # ゲームオブジェクトの初期化（それぞれの値をセット）
        self.item = Item() #同じものだよと定義教えてる
        self.bar = Bar()
        self.score = 0
        self.life = 5  # ライフの数

        # ゲームループの開始
        pyxel.run(self.update, self.draw)

    def restart(self): #ゲームを再スタートするための関数
        # ゲームオブジェクトの再初期化
        self.item = Item()
        self.bar = Bar()
        self.score = 0
        self.life = 5 # ライフ数

    def update(self):
        # ボールとバーの更新
        self.item.update()
        self.bar.update()

        # アイテムとペンケースの当たり判定
        if ( #もし、
            self.item.is_falling # ボールが落下中(.is_falling = True)で
            and self.bar.y <= self.item.y + self.item.radius <= self.bar.y + self.bar.height # かつ、「アイテム（の左上）のy座標 + ボールの直径」が、バー（の左上）のy座標よりも大きく、「バーの（の左上）y座標 + バーの縦幅」よりも小さかった場合で、
            and self.bar.x - self.item.radius <= self.item.x <= self.bar.x + self.bar.width # かつ、アイテムの（の左上）のx座標が、「バーの（の左上）のx座標 - ボールの直径」よりも大きく、「バーの（の左上）のx座標 + バーの横幅」よりも小さかった場合、
        ):  # (その時、ボールはバーに当たっていることになるので、）
            
            # ボールがバーに当たったら、スコアを加算して落下をリセット
            self.score += 10
            self.item.is_falling = False # （落下を止めたいので、）アイテムの落下状態をリセット

            time.sleep(0.5)
            self.item.num = random.randrange(4)

            
        # ボールが（バーに当たらずに）画面下部に到達したら、ライフを減らして落下をリセット
        if self.item.y > pyxel.height:
            self.item.is_falling = False
            self.life -= 1

        # クリックorスペースキーでボールを落下させる
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE) :
            self.item.is_falling = True

    def draw(self):
        # 画面をクリア
        pyxel.cls(0)

        # ボールとバーを描画
        self.item.draw()
        self.bar.draw()

        # スコアとライフを表示
        pyxel.text(10, 20, f"Score: {self.score}", 7) # スコアを表示

        pyxel.text(10, 10, "Life:", 8) 
        for i in range(0, self.life):
            pyxel.blt(30 + i * 12, 8, 0, 3, 69, 10, 10, 0)  # 残りライフの数だけ、ハートの絵を表示

        # pyxel.rectb(self.bar.x, self.item.y + self.item.radius, self.bar.x + self.bar.width, self.bar.y - self.bar.height, 10)


        # ゲームオーバーの時
        if self.life <= 0: # ライフが0になったら
            # 画面をクリア
            pyxel.cls(0)
            # ゲームオーバーのメッセージを表示
            pyxel.text(30, 50, f" GAME OVER!!! \n \n Press 'R' to restart", 8)

            if pyxel.btnp(pyxel.KEY_R): #Rキーが押されたら、ゲームを再スタート
                self.restart()


# ゲームを実行
Game()
