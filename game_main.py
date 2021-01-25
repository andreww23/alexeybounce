import pygame
import random
import os

pygame.init()
size = width, height = 1000, 1000
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
run = False
new_lvl_run = False

level_counter = 0

balance = 0
ball_count = 7
helmet = False

start_counter = 20

snd_dir = os.path.join('C:\PyCharm_git\songs', 'song.wav')
main_sound = pygame.mixer.Sound(snd_dir)

snd_dir = os.path.join('C:\PyCharm_git\songs', 'sirena.wav')
scnd_sound = pygame.mixer.Sound(snd_dir)
scnd_sound.set_volume(1.5)

vox_sound = pygame.mixer.Sound(os.path.join('C:\PyCharm_git\songs', 'vox.wav'))

menu_sound = pygame.mixer.Sound(os.path.join('C:\PyCharm_git\songs', 'sound.mp3'))


def load_image(name, colorkey=None):
    fullname = os.path.join('C:\PyCharm_git\images', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Картинка не найдена')
        raise SystemExit(message)
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def start_screen():
    global run
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image('menu.png'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = True
                return
        pygame.display.flip()
        clock.tick(50)


def lose_screen():
    global run, counter, hero, coins, helmet, balance
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image('lose.png'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and balance >= 300:
                    balance -= 300
                    helmet = True
                    hero.kill()
                    hero = Hero(all_sprites)
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_again()
                return
        pygame.display.flip()
        clock.tick(50)


def win_screen():
    global balance, helmet, hero
    main_sound.set_volume(0.0)
    pygame.mouse.set_visible(True)
    fon = pygame.transform.scale(load_image('victory.png'), (width, height))
    screen.blit(fon, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b and balance >= 300:
                    balance -= 300
                    helmet = True
                    hero.kill()
                    hero = Hero(all_sprites)

            if event.type == pygame.MOUSEBUTTONDOWN:
                next_level()
                return
        pygame.display.flip()
        clock.tick(50)


def play_again():
    global counter, hero, level_counter
    if level_counter == 0:
        counter = 20
    else:
        counter = 25
    hero.colide = False
    main()


def next_level():
    global counter, hero, ball_count, start_counter, level_counter
    level_counter += 1
    counter = 25
    start_counter = 25
    ball_count = 12
    hero.colide = False
    main_sound.set_volume(1.0)
    for _ in range(3):
        Ball(random.randint(10, 15))
    main()


class Hero(pygame.sprite.Sprite):
    size = (20, 20)

    def __init__(self, group):
        super().__init__(group)
        self.add(hero_gr)
        if not helmet:
            self.image_boom = load_image('alex.png', (255, 255, 255))
        else:
            self.image_boom = load_image('alex_in_helmet.png', (255, 255, 255))
        self.image = self.image_boom
        self.rect = self.image.get_rect()
        self.colide = False

    def update(self):
        if pygame.sprite.spritecollideany(self, balls) is not None \
                and counter != start_counter and counter != start_counter - 1 and counter != start_counter - 2 \
                and helmet \
                and counter != start_counter - 10 and counter != start_counter - 11 and counter != start_counter - 12:
            vox_sound.play()
            self.colide = True

        if pygame.sprite.spritecollideany(self, balls) is not None \
                and counter != start_counter and counter != start_counter - 1 and counter != start_counter - 2:
            vox_sound.play()
            self.colide = True


class Ball(pygame.sprite.Sprite):
    image_putin = load_image('putiin.png', (255, 255, 255))

    def __init__(self, radius):
        super().__init__(all_sprites)
        self.add(balls)
        self.radius = radius
        self.image = Ball.image_putin
        self.rect = self.image.get_rect()
        self.vx = random.randint(-3, 3)
        self.vy = random.randrange(-3, 3)
        self.rect.topleft = ((random.randint(100, width - self.rect.width),
                              random.randint(100, width - self.rect.height)))

    def update(self):
        self.rect = self.rect.move(self.vx, self.vy)
        if pygame.sprite.spritecollideany(self, horizontal_borders):
            self.vy = -self.vy
        if pygame.sprite.spritecollideany(self, vertical_borders):
            self.vx = -self.vx
        for sprite in balls:
            if sprite is self:
                continue
            if self.rect.colliderect(sprite.rect):
                self.vx = +self.vx


class Coins(pygame.sprite.Sprite):
    image_coin = load_image('dollar.png', (255, 255, 255))

    def __init__(self):
        super().__init__(all_sprites)
        self.add(coins)
        self.is_collected = False
        self.image = Coins.image_coin
        self.rect = self.image.get_rect()
        self.rect.topleft = ((random.randint(0, width - self.rect.width),
                              random.randint(0, width - self.rect.height)))

    def update(self):
        global balance
        self.is_collected = False
        if pygame.sprite.spritecollideany(self, hero_gr) is not None:
            balance += 100
            self.is_collected = True
            self.kill()
        if counter % 5 == 1:
            self.kill()


all_sprites = pygame.sprite.Group()
balls = pygame.sprite.Group()
coins = pygame.sprite.Group()
hero_gr = pygame.sprite.Group()
hero = None

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:  # вертикальная стенка
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:  # горизонтальная стенка
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


Border(0, 0, width, 0)
Border(0, height, width, height)
Border(0, 0, 0, height)
Border(width, 0, width, height)

for i in range(7):
    Ball(random.randint(10, 15))

counter, text = 20, '20'.rjust(3)
pygame.time.set_timer(pygame.USEREVENT, 1000)
font = pygame.font.SysFont('Comfortaa', 40)
font_big = pygame.font.SysFont('Comfortaa', 80)

menu_sound.play()
start_screen()
menu_sound.set_volume(0.0)
main_sound.play()
coin_counter = 0


def main():
    global counter, hero, run, text, scnd_sound, start_counter
    pygame.mouse.set_visible(False)
    for event in pygame.event.get():
        if event.type == pygame.USEREVENT:
            if counter > 0 and counter % 5 == 0:
                counter -= 1
                Coins()
            elif counter > 0:
                counter -= 1
            if counter > 3:
                text = 'Осталось продержаться: ' + str(counter).rjust(3)
            elif counter == 3:
                text = 'Осталось продержаться: Три!'
                scnd_sound.play()
                main_sound.set_volume(0.4)
            elif counter == 2:
                text = 'Осталось продержаться: Два!'
                main_sound.set_volume(0.4)
            elif counter == 1:
                text = 'Осталось продержаться: Один!'
                main_sound.set_volume(0.4)
            else:
                text = 'Поздравляем! Отлично!'

        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEMOTION:
            if hero is None:
                hero = Hero(all_sprites)
            else:
                hero.rect.topleft = event.pos
    if hero:
        if helmet and (counter == start_counter or counter == start_counter - 1 or counter == start_counter - 2):
            screen.blit(font.render(f'Щит действует {counter - (start_counter - 3)} секунд', True,
                                    (0, random.randint(150, 255), 0)), (350, 470))
            clock.tick(10)
        elif helmet and start_counter == 25 and (counter == start_counter - 10 or counter == start_counter - 11
                                      or counter == start_counter - 12):
            screen.blit(font.render(f'Щит действует {counter - (start_counter - 13)} секунд', True,
                                    (0, random.randint(150, 255), 0)), (350, 470))
            clock.tick(10)
        elif counter == start_counter or counter == start_counter - 1 or counter == start_counter - 2:
            screen.blit(font.render(f'Щит действует {counter - (start_counter - 3)} секунд', True,
                                    (0, random.randint(150, 255), 0)), (350, 470))
            clock.tick(10)
        if counter == 0 and not hero.colide:
            win_screen()
        elif not hero.colide:
            all_sprites.draw(screen)
            all_sprites.update()
            screen.blit(font.render(text, True, (0, 0, 0)), (320, 10))
            screen.blit(font.render(f'{str(balance)}$', True, (0, 255, 0)), (750, 10))
        else:
            lose_screen()

        pygame.display.flip()
        clock.tick(60)
        screen.fill((255, 255, 255))


while run:
    main()

pygame.quit()
