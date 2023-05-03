# Example file showing a basic pygame "game loop"
import pygame
from SnakeClass import SnakeClass, SnakeDirect
from Food import Food
import random
import math
from Button import Button
from enum import Enum
from Opening import Opening

class GameEvent(Enum):
    MY_CLOCK = 1000
    SNAKE_MOVE = 2000
    FOOD_EFFECT = 3000
    OPENING = 4000


class TheGame():
    def __init__(self) -> None:
        # pygame setup
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('贪吃蛇')
        self.stage_width = 1280
        self.stage_height = 720
        self.screen = pygame.display.set_mode(
            (self.stage_width, self.stage_height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.snake = SnakeClass([100, 100])
        self.lose = False
        self.score = 0
        self.food: Food = None

        # 加载背景音乐
        self.bg_music = pygame.mixer.Sound('./res/bg.mp3')
        self.bg_music.play(-1)

        self.score_font = pygame.font.Font('./res/digifaw.ttf', 30)
        self.gameover_font = pygame.font.Font(None, 50)

        self.SCORE_MARGIN_RIGHT = 20
        self.SCORE_MARGIN_TOP = 10

        self.my_clock = 0
        self.opening = Opening([0,0], pygame.font.Font(None, 80) ,self.stage_width, self.stage_height)
        self.is_opening = True
        pygame.time.set_timer(GameEvent.OPENING.value, 10)
        self.restart_btn: Button = None
        
        self.you_lose_bg_surf = pygame.transform.scale(pygame.image.load('./res/you_lose/bg.png'), [self.stage_width, self.stage_height])
        self.you_lose_header_surf = pygame.transform.scale(pygame.image.load('./res/you_lose/header.png'), [500,200])
        self.you_lose_table_surf = pygame.transform.scale(pygame.image.load('./res/you_lose/table.png'), [self.stage_width *0.8, self.stage_height*0.6])
    def generate_food(self):
        # 如果食物与小蛇重叠，重新生成
        success = False
        while not success:
            # 初始化食物位置
            food_x = random.randint(0, math.floor(
                self.stage_width/self.snake.body_size)-1)*self.snake.body_size
            food_y = random.randint(0, math.floor(
                self.stage_height/self.snake.body_size)-1)*self.snake.body_size

            for block in self.snake.body:
                if block[0] == food_x and block[1] == food_y:
                    continue

            success = True

        print(f'x:{food_x}, y:{food_y}')
        return Food([food_x, food_y])

    def is_lost(self) -> bool:
        # 判断失败
        if self.snake.body[0][0] < 0 or (self.snake.body[0][0] + self.snake.body_size) > self.stage_width or self.snake.body[0][1] < 0 or (self.snake.body[0][1] + self.snake.body_size) > self.stage_height:
            return True

        for i in range(1, len(self.snake.body)):
            if self.snake.body[0][0] == self.snake.body[i][0] and self.snake.body[0][1] == self.snake.body[i][1]:
                return True
        return False

    def draw_score(self):
        score_str = str(self.score).rjust(4, '0')
        score_surf = self.score_font.render(
            (f'score: {score_str}'), 1, (255, 255, 255))
        self.screen.blit(score_surf, [
                         self.stage_width - score_surf.get_width()-self.SCORE_MARGIN_RIGHT, self.SCORE_MARGIN_TOP])

        my_clock_str = str(self.my_clock)
        my_clock_surf = self.score_font.render(
            f'time: {my_clock_str}', True, (255, 255, 255))
        self.screen.blit(my_clock_surf, [10, 10])

    def draw_lost_scenario(self):
        self.screen.blit(self.you_lose_bg_surf, [(self.stage_width - self.you_lose_bg_surf.get_width()) / 2,
                        (self.stage_height - self.you_lose_bg_surf.get_height()) / 2])
        self.screen.blit(self.you_lose_table_surf, [(self.stage_width - self.you_lose_table_surf.get_width()) / 2,
                        (self.stage_height - self.you_lose_table_surf.get_height()) / 2 -50])
        self.screen.blit(self.you_lose_header_surf, [(self.stage_width - self.you_lose_header_surf.get_width()) / 2,
                        (self.stage_height - self.you_lose_header_surf.get_height()) / 2 -50])

        # gameover_surf = self.gameover_font.render(('GAME OVER'), 1, (0, 0, 0))

        # gameover_pos = [(self.stage_width - gameover_surf.get_width()) / 2,
        #                 (self.stage_height - gameover_surf.get_height()) / 2]
        # self.screen.blit(gameover_surf, gameover_pos)

        score_surf = self.gameover_font.render(
            (f'score: {self.score}'), 1, (0, 0, 0))
        score_pos = [(self.stage_width - score_surf.get_width()) / 2,
                     (self.stage_height - score_surf.get_height()) / 2 + 50]
        self.screen.blit(score_surf, score_pos)

        self.restart_btn = Button(pygame.image.load('./res/restart.png'),
                                  [(self.stage_width - 100) / 2,
                                   self.stage_height - 170],
                                  100, 100)
        self.restart_btn.draw(self.screen)
        pygame.display.flip()

    def draw_background(self):
        # bg_surf = pygame.image.load('./res/bg.jpg')
        # screen.blit(bg_surf, [0, 0], [0, 0, stage_width, stage_height])
        self.screen.fill([104, 131, 139])

    def draw_food(self):
        """没有食物的时候，添加一个食物
        """
        self.food.draw(self.screen)

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                self.keyboard_event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mouse_event_handler(event)
            if event.type == GameEvent.MY_CLOCK.value:
                print('GameEvent.MY_CLOCK')
                self.my_clock += 1
            if event.type == GameEvent.SNAKE_MOVE.value:
                print('GameEvent.SNAKE_MOVE')
                self.snake.move()
            if event.type == GameEvent.FOOD_EFFECT.value:
                print('GameEvent.FOOD_EFFECT')
                self.food_effect_animation()
            if event.type == GameEvent.OPENING.value:
                print('GameEvent.OPENING')
                self.opening_animation()

    def opening_animation(self):
        self.opening.crop_y += 2
        if self.opening.crop_y > 600:
            pygame.time.set_timer(GameEvent.OPENING.value, 0)
            self.opening.display_button = True

    def food_effect_animation(self):
        if self.food is None or not self.food.alive:
            return
        if self.food.size < 1:
            self.food.size += 0.05
        else:
            self.food.size -= 0.05
        
    def keyboard_event_handler(self, event: pygame.event.Event):
        if event.key == pygame.K_UP and self.snake.direct != SnakeDirect.DOWN:
            self.snake.direct = SnakeDirect.UP
        elif event.key == pygame.K_DOWN and self.snake.direct != SnakeDirect.UP:
            self.snake.direct = SnakeDirect.DOWN
        elif event.key == pygame.K_RIGHT and self.snake.direct != SnakeDirect.LEFT:
            self.snake.direct = SnakeDirect.RIGHT
        elif event.key == pygame.K_LEFT and self.snake.direct != SnakeDirect.RIGHT:
            self.snake.direct = SnakeDirect.LEFT

    def mouse_event_handler(self, event: pygame.event.Event):
        if self.is_opening:
            self.opening.crop_y = 602
        if self.restart_btn and self.restart_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
            self.restart_game()
        if self.opening.play_btn and self.opening.play_btn.get_rect().collidepoint(pygame.mouse.get_pos()):
            self.start_game()

    def start_game(self):
        if not self.is_opening:
            return
        print('start game')
        self.is_opening = False
        pygame.time.set_timer(GameEvent.MY_CLOCK.value, 1000)
        pygame.time.set_timer(GameEvent.SNAKE_MOVE.value, 140)
        pygame.time.set_timer(GameEvent.FOOD_EFFECT.value, 300)

    def restart_game(self):
        if not self.lose:
            return
        print('restart')
        # 删除小蛇
        self.snake.remove()
        # 删除食物
        self.food.remove()
        # 生成小蛇
        self.snake = SnakeClass([100, 100])
        # 生成食物
        self.food = self.generate_food()
        # 重置得分
        self.score = 0
        # 重置失败状态
        self.lose = False
        # 重置定时器
        self.my_clock = 0
        pygame.time.set_timer(GameEvent.MY_CLOCK.value, 1000)
        pygame.time.set_timer(GameEvent.SNAKE_MOVE.value, 140)
        pygame.time.set_timer(GameEvent.FOOD_EFFECT.value, 300)

    def run(self):
        self.food = self.generate_food()
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.event_handler()
            self.clock.tick(30)  # limits FPS to 30
            
            if self.is_opening:
                self.opening.draw(self.screen)
                pygame.display.flip()
                continue
            
            # 画出背景
            self.draw_background()

            # RENDER YOUR GAME HERE
            if self.lose:
                self.draw_lost_scenario()
                continue

            # 吃到食物？
            if self.snake.body[0][0] == self.food.location[0] and self.snake.body[0][1] == self.food.location[1]:
                self.snake.eat()
                self.food.remove()
                self.food = self.generate_food()
                self.score += 1

            self.snake.draw(self.screen)
            self.draw_food()
            self.draw_score()
            self.lose = self.is_lost()
            if self.lose:
                pygame.time.set_timer(GameEvent.MY_CLOCK.value, 0)
                pygame.time.set_timer(GameEvent.SNAKE_MOVE.value, 0)
                pygame.time.set_timer(GameEvent.FOOD_EFFECT.value, 0)
                continue
            # flip() the display to put your work on screen
            pygame.display.flip()

        pygame.quit()


def main():
    game = TheGame()
    game.run()


if __name__ == '__main__':
    main()
