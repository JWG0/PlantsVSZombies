import pygame
import random
#配置图片地址
IMAGE_PATH = 'imgs/'

#设置页面宽高
scrrr_width = 800#一小块地是80*80
scrrr_height = 560

#创建控制游戏结束的状态
GAMEOVER = False

#图片加载报错处理
LOG = '文件:{}中的方法:{}出错'.format(__file__, __name__)

#创建地图类
class Map():
    #存储两张不同颜色的图片名称
    map_names_list = [IMAGE_PATH + 'map1.jpg', IMAGE_PATH + 'map2.jpg']#静态变量
    #初始化地图
    def __init__(self, x, y, img_index):
        self.image = pygame.image.load(Map.map_names_list[img_index])
        self.position = (x, y)
        #是否能够种植
        self.can_grow = True
        if x>=800 or y>=540:
            if y>=540:
                self.image = pygame.image.load(IMAGE_PATH + 'map4.jpg')
            else:
                self.image = pygame.image.load(IMAGE_PATH + 'map3.jpg')
            self.can_grow=False##超出限定范围不能种植
    #加载地图
    def load_map(self):
        MainGame.window.blit(self.image, self.position)

#植物类
class Plant(pygame.sprite.Sprite):
    def __init__(self):
        super(Plant, self).__init__()#这是对继承自父类的属性进行初始化。
        # 而且是用父类的初始化方法来初始化继承的属性。
        self.live = True#活着的

    def load_image(self):#这个函数没啥用
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            #hasattr() 函数用于判断对象是否包含对应的属性。
            MainGame.window.blit(self.image, self.rect)
        else:
            print(LOG)

#向日葵类
class Sunflower(Plant):
    def __init__(self, x, y):
        super(Sunflower, self).__init__()
        self.image = pygame.image.load('imgs/sunflower.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 1000
        # 5 时间计数器
        self.time_count = 0
    #新增功能：生成阳光
    def produce_money(self):
        self.time_count += 1
        if self.time_count == 25:
            MainGame.money += 50
            self.time_count = 0
    #向日葵加入到窗口中
    def display_sunflower(self):#画图
        MainGame.window.blit(self.image, self.rect)

#豌豆射手类
class PeaShooter(Plant):
    def __init__(self, x, y):
        super(PeaShooter, self).__init__()
        # self.image 为一个 surface
        self.image = pygame.image.load('imgs/peashooter.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 50
        self.hp = 200
        # 6 发射计数器
        self.shot_count = 0
    #增加射击方法
    def shot(self):
        # 6 记录是否应该射击
        should_fire = False
        for zombie in MainGame.zombie_list:
            if zombie.rect.y == self.rect.y and zombie.rect.x < 800 and zombie.rect.x > self.rect.x:
                should_fire = True
        # 6 如果活着
        if self.live and should_fire:
            self.shot_count += 1
            # 6 计数器到25发射一次
            if self.shot_count == 25:
                # 6 基于当前豌豆射手的位置，创建子弹
                peabullet = PeaBullet(self)
                # 6 将子弹存储到子弹列表中
                MainGame.peabullet_list.append(peabullet)
                self.shot_count = 0#计数器置零
    def display_peashooter(self):#画图,把豌豆射手画上去
        MainGame.window.blit(self.image, self.rect)

#坚果类
class Nut_class(Plant):
    def __init__(self, x, y):
        super(Nut_class, self).__init__()
        self.image = pygame.image.load('imgs/nut.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.price = 100
        self.hp = 5000
    #坚果加入到窗口中
    def display_nut(self):#画图
        MainGame.window.blit(self.image, self.rect)

#豌豆子弹类
class PeaBullet(pygame.sprite.Sprite):
    def __init__(self, peashooter):
        self.live = True
        self.image = pygame.image.load('imgs/peabullet.png')
        #print(self.image.get_rect())(0,0,80,80)
        self.damage = 50
        self.speed = 10
        self.rect = self.image.get_rect()
        self.rect.x = peashooter.rect.x + 60
        self.rect.y = peashooter.rect.y +7

    def move_bullet(self):
        # 7 在屏幕范围内，实现往右移动
        if self.rect.x < scrrr_width:
            self.rect.x += self.speed
            self.rect.y +=0
        else:
            self.live = False

    # 7 新增，子弹与僵尸的碰撞
    def hit_zombie(self):
        for zombie in MainGame.zombie_list:
            if pygame.sprite.collide_rect(self, zombie):
                # 打中僵尸之后，修改子弹的状态，
                self.live = False
                # 僵尸掉血
                zombie.hp -= self.damage
                if zombie.hp <= 0:
                    zombie.live = False
                    self.nextLevel()
    # 7闯关方法

    def nextLevel(self):
        MainGame.score += 20
        MainGame.remnant_score -= 20
        for i in range(1, 100):
            if MainGame.score <= 200 * i and MainGame.remnant_score <= 0:
                MainGame.remnant_score = 100 * i#残余分数
                MainGame.shaoguan += 1
                MainGame.produce_zombie += 50

    def display_peabullet(self):
        MainGame.window.blit(self.image, self.rect)

#僵尸类
class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Zombie, self).__init__()
        self.image = pygame.image.load('imgs/zombie.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = 1000
        self.damage = 10
        self.speed = 0.4
        self.live = True
        self.stop = False

    # 9 僵尸的移动
    def move_zombie(self):
        if self.live and not self.stop:
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                # 8 调用游戏结束方法
                MainGame().gameOver()

    # 9 判断僵尸是否碰撞到植物，如果碰撞，调用攻击植物的方法
    def hit_plant(self):
        for plant in MainGame.plants_list:
            if pygame.sprite.collide_rect(self, plant):
                # 8  僵尸移动状态的修改
                self.stop = True
                self.eat_plant(plant)
    # 9 僵尸攻击植物

    def eat_plant(self, plant):
        # 9 植物生命值减少
        plant.hp -= self.damage
        # 9 植物死亡后的状态修改，以及地图状态的修改
        if plant.hp <= 0:
            a = plant.rect.y // 80 - 1  # //表示整数除法
            b = plant.rect.x // 80
            map = MainGame.map_list[a][b]
            map.can_grow = True#可以种植
            plant.live = False
            # 8 修改僵尸的移动状态
            self.stop = False

    # 9 将僵尸加载到地图中
    def display_zombie(self):
        MainGame.window.blit(self.image, self.rect)

#主程序
class MainGame():
    # 2 创建关数，得分，剩余分数，钱数
    shaoguan = 1
    score = 0
    remnant_score = 100
    money = 500#初始钱币
    # 3 存储所有地图坐标点
    map_points_list = []
    # 3 存储所有的地图块
    map_list = []
    # 4 存储所有植物的列表
    plants_list = []
    # 7 存储所有豌豆子弹的列表
    peabullet_list = []
    # 9 新增存储所有僵尸的列表
    zombie_list = []
    count_zombie = 0
    produce_zombie = 100
    #判断
    #mouse_is_pressed=False
    zhong_zhi_plant=0#0啥也不中，1向日葵，2豌豆射手，3是坚果，4是土豆雷，10铲子

    # 1 加载游戏窗口
    def init_window(self):
        # 1 调用显示模块的初始化
        pygame.display.init()#用pygame.init()也可以
        pygame.display.set_caption('植物大战僵尸')  # 设置窗口标题
        # 1 创建窗口#静态变量
        MainGame.window = pygame.display.set_mode([scrrr_width+160, scrrr_height+80])

    # 2 文本绘制
    def draw_text(self, content, size=20, color=(255,0,255)):#默认字体20#默认紫色
        pygame.font.init()#初始化，如果之前用了pygame.init()，那这里就不用初始化字体了
        font = pygame.font.SysFont('kaiti', size)
        text = font.render(content, True, color)
        return text

    # 2 加载帮助提示
    def load_help_text(self):
        text1 = self.draw_text('点击最下面的购物栏，即可选中即将要种植的植物，将鼠标移动到指定位置，再按左键，即可种植植物', 20, (255, 0, 0))
        MainGame.window.blit(text1, (0, 0))

    # 3 初始化坐标点一个二维数组，y行x列
    def init_plant_points(self):
        for y in range(1, 8):
            points = []
            for x in range(12):#(0,1,,,,,,11)
                point = (x, y)#第x列，第y行
                points.append(point)
            MainGame.map_points_list.append(points)#points存储一行的数据
            #print("MainGame.map_points_list", MainGame.map_points_list)

    # 3 初始化地图
    def init_map(self):
        for points in MainGame.map_points_list:#points存储一行的数据
            temp_map_list = list()#空列表
            for point in points:
                if (point[0] + point[1]) % 2 == 0:
                    map = Map(point[0] * 80, point[1] * 80, 0)
                else:
                    map = Map(point[0] * 80, point[1] * 80, 1)
                # 将地图块加入到窗口中
                temp_map_list.append(map)
                #print("temp_map_list", temp_map_list)
            MainGame.map_list.append(temp_map_list)
        #print("MainGame.map_list", MainGame.map_list)

    # 3 将地图加载到窗口中
    def load_map(self):
        for temp_map_list in MainGame.map_list:
            for map in temp_map_list:
                map.load_map()#Map中的一个函数,将地图加载到窗口中


    # 6 豌豆射手发射处理，向日葵产生阳光
    def load_plants(self):
        for plant in MainGame.plants_list:
            # 6 优化加载植物的处理逻辑
            if plant.live:
                if isinstance(plant, Sunflower):#如果plant是Sunflower类型
                    plant.display_sunflower()#将向日葵画上去
                    plant.produce_money()#产生金币
                elif isinstance(plant, PeaShooter):
                    plant.display_peashooter()
                    plant.shot()
                elif isinstance(plant,Nut_class):
                    plant.display_nut()
            else:
                MainGame.plants_list.remove(plant)#从植物列表中删除这个植物

    # 7 加载所有子弹的方法
    def load_peabullets(self):
        for b in MainGame.peabullet_list:
            if b.live:
                b.display_peabullet()
                b.move_bullet()
                # v1.9 调用子弹是否打中僵尸的方法
                b.hit_zombie()
            else:
                MainGame.peabullet_list.remove(b)

    # 8事件处理
    def deal_events(self):
        # 8 遍历事件列表，判断
        for e in pygame.event.get():
            #mouse_location = pygame.mouse.get_pos()#可以实时获得鼠标位置
            mouse_location = pygame.mouse.get_pos()

            if e.type == pygame.QUIT:
                self.gameOver()
            elif e.type == pygame.MOUSEBUTTONDOWN:# print('按下鼠标按键')
                # print(e.pos)#print(e.button)#左键1  按下滚轮2 右键 3 上转滚轮为4 下转滚轮为5
                x = e.pos[0] // 80
                y = e.pos[1] // 80
                map = MainGame.map_list[y - 1][x]#第一行没有种植植物,第y-1行，第x列
                print(map.position)
                # 8 增加创建时候的地图装填判断以及金钱判断
                mouse_location = pygame.mouse.get_pos()
                if e.button == 1  and mouse_location[1]>=560:
                    #选择植物或铲子
                    if mouse_location[0] < 80:
                        MainGame.zhong_zhi_plant = 1
                    elif mouse_location[0] < 160 and mouse_location[0] > 80:
                        MainGame.zhong_zhi_plant = 2
                    elif mouse_location[0] < 240 and mouse_location[0] > 160:
                        MainGame.zhong_zhi_plant = 3
                    elif mouse_location[0] < 800 and mouse_location[0] > 720:
                        MainGame.zhong_zhi_plant = 10
                elif e.button == 1 and MainGame.zhong_zhi_plant==1:
                    if map.can_grow and MainGame.money >= 50:
                        sunflower = Sunflower(map.position[0], map.position[1])
                        MainGame.plants_list.append(sunflower)
                        print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 50
                elif e.button == 1 and MainGame.zhong_zhi_plant==2:
                    if map.can_grow and MainGame.money >= 150:
                        peashooter = PeaShooter(
                            map.position[0], map.position[1])#产生豌豆精灵
                        MainGame.plants_list.append(peashooter)
                        print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 150
                elif e.button == 1 and MainGame.zhong_zhi_plant==3:
                    if map.can_grow and MainGame.money >= 100:
                        nut_object = Nut_class(
                            map.position[0], map.position[1])#产生豌豆精灵
                        MainGame.plants_list.append(nut_object)
                        print('当前植物列表长度:{}'.format(len(MainGame.plants_list)))
                        map.can_grow = False
                        MainGame.money -= 100
                elif e.button == 1 and MainGame.zhong_zhi_plant==10:#铲子
                    for chanplant in MainGame.plants_list:
                        if chanplant.rect.x//80==x and chanplant.rect.y//80==y:
                            MainGame.plants_list.remove(chanplant)
                            MainGame.map_list[y-1][x].can_grow=True

    # 9 新增初始化僵尸的方法
    def init_zombies(self):
        for i in range(1, 7):#僵尸的初始y坐标
            dis = random.randint(1, 5) * 200
            zombie = Zombie(800 + dis, i * 80)
            MainGame.zombie_list.append(zombie)#加到僵尸列表中

    # 9将所有僵尸加载到地图中
    def load_zombies(self):
        for zombie in MainGame.zombie_list:
            if zombie.live:
                zombie.display_zombie()
                zombie.move_zombie()
                # v2.0 调用是否碰撞到植物的方法
                zombie.hit_plant()
            else:
                MainGame.zombie_list.remove(zombie)
    # 1 开始游戏

    def start_game(self):
        # 1 初始化窗口
        self.init_window()
        # 3 初始化坐标和地图
        self.init_plant_points()
        self.init_map()
        # 9 调用初始化僵尸的方法
        self.init_zombies()
        # 1 只要游戏没结束，就一直循环
        sunflower = Sunflower(-80, -80)##不显示在地图上
        MainGame.plants_list.append(sunflower)##赠送一颗向日葵
        while not GAMEOVER:
            # 1 渲染白色背景
            MainGame.window.fill((255, 255, 255))
            # 2 渲染的文字和坐标位置
            self.load_help_text()#加载提示信息
            MainGame.window.blit(self.draw_text('当前钱数$: {}'.format(MainGame.money), 26, (255, 0, 0)), (500, 40))
            MainGame.window.blit(self.draw_text('当前关数{}，得分{},距离下关还差{}分'.format(MainGame.shaoguan,MainGame.score,MainGame.remnant_score),26,(255,0,0)),(5,40))
            # 3 需要反复加载地图
            self.load_map()
            # 6 调用加载植物的方法
            self.load_plants()
            # 7  调用加载所有子弹的方法
            self.load_peabullets()
            # 8 调用事件处理的方法
            self.deal_events()
            # 9 调用展示僵尸的方法
            self.load_zombies()

            #展示购物栏#1号-太阳花
            image_sunflower= pygame.image.load("imgs/sunflower.png")
            image_sunflower_rect=image_sunflower.get_rect()
            image_sunflower_rect.left=0
            image_sunflower_rect.top=560#(0,80)(560,640)
            MainGame.window.blit(image_sunflower, image_sunflower_rect)
            ####添加文字（价格）
            ziti_color=(255,0,0)
            MainGame.window.blit(self.draw_text('50', 20, ziti_color), (50, 560+60))
            #2号豌豆射手
            image_peashooter = pygame.image.load("imgs/peashooter.png")
            image_peashooter_rect = image_peashooter.get_rect()
            image_peashooter_rect.left = 80
            image_peashooter_rect.top = 560
            MainGame.window.blit(image_peashooter, image_peashooter_rect)
            MainGame.window.blit(self.draw_text('150', 20, ziti_color), (50+80, 560 + 60))
            # 3号坚果
            image_nut = pygame.image.load("imgs/nut.png")
            image_nut_rect = image_nut.get_rect()
            image_nut_rect.left = 160
            image_nut_rect.top = 560
            MainGame.window.blit(image_nut, image_nut_rect)
            MainGame.window.blit(self.draw_text('150', 20, ziti_color), (50 + 160, 560 + 60))
            # 4号土豆雷
            # image_mine = pygame.image.load("imgs/mine.png")
            # image_mine_rect = image_mine.get_rect()
            # image_mine_rect.left = 240
            # image_mine_rect.top = 560
            # MainGame.window.blit(image_mine, image_mine_rect)
            # MainGame.window.blit(self.draw_text('150', 20, ziti_color), (50 + 240, 560 + 60))
            #5号

            #10号铲子
            image_chanzi = pygame.image.load("imgs/chanzi.png")
            image_chanzi_rect = image_chanzi.get_rect()
            image_chanzi_rect.left = 720
            image_chanzi_rect.top = 560
            MainGame.window.blit(image_chanzi, image_chanzi_rect)

            if MainGame.zhong_zhi_plant!=0:
                ###画箭头
                image_jiantou = pygame.image.load("imgs/jiantou.png")
                image_jiantou_rect = image_jiantou.get_rect()
                image_jiantou_rect.left = MainGame.zhong_zhi_plant * 80-80
                image_jiantou_rect.top = 560  # (0,80)(560,640)
                MainGame.window.blit(image_jiantou, image_jiantou_rect)

            # 画线pygame.draw.line( screen, mycolcor, start, end, width )
            for line in range(2, 8):
                pygame.draw.line(MainGame.window, (0, 0, 0), (800, line * 80 - 2), (960, line * 80 - 2), 2)
            for line in range(1, 12):
                pygame.draw.line(MainGame.window, (0, 255, 0), (80 * line, 560), (80 * line, 640), 2)

            pygame.display.update()

            # 10计数器增长，每数到100，调用初始化僵尸的方法
            MainGame.count_zombie += 1
            if MainGame.count_zombie >= MainGame.produce_zombie:
                self.init_zombies()
                MainGame.count_zombie = 0
            pygame.time.wait(10)#暂停程序一段时间0.01s
            pygame.display.update()

    def gameOver(self):
        MainGame.window.blit(self.draw_text('游戏结束', 80, (255, 0, 0)), (300, 200))
        pygame.display.update()##刷新一下窗口
        print('游戏结束')
        pygame.time.wait(3000)
        global GAMEOVER
        GAMEOVER = True


if __name__ == '__main__':
    game = MainGame()
    game.start_game()
    #print("*&"*90)