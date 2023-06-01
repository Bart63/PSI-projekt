import pygame
import datetime
import time


class MapVisualizer:

    def __init__(self, window_size=(600, 400), car_velocity=1):
        self.screen = None
        self.greenLight = True
        self.window_size = window_size
        self.CAPTION = 'Traffic Visualisation'
        self.c = {"WHITE": (255, 255, 255), "GREEN": (0, 255, 0),
                  "RED": (255, 0, 0), "YELLOW": (255, 234, 0),
                  "BLUE": (0, 0, 255), "GREY": (105, 105, 105),
                  "BLACK": (0, 0, 0)}
        self.car_velocity = car_velocity

    def draw_canvas(self):
        self.screen = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption(self.CAPTION)
        self.screen.fill(self.c["WHITE"])
        pygame.display.flip()

    def draw_car(self, movement):
        pygame.draw.rect(self.screen, self.c['BLUE'], (0 + movement, 150, 100, 50))
        pygame.draw.circle(self.screen, self.c['BLACK'], (20 + movement, 200), 15)
        pygame.draw.circle(self.screen, self.c['BLACK'], (80 + movement, 200), 15)

    def draw_road(self):
        pygame.draw.rect(self.screen, self.c['GREY'], (0, 215, 600, 15))
        pygame.draw.line(self.screen, self.c['WHITE'], (0, 222.5), (600, 222.5))

    def draw_lights(self, x_pos, y_pos, light_duration=12):
        pygame.draw.rect(self.screen, self.c['BLACK'], (400, 170, 10, 60))
        curr_time = datetime.datetime.now().time().second
        if curr_time % light_duration * 2 < light_duration:
            pygame.draw.circle(self.screen, self.c['GREEN'], (x_pos, y_pos), 15)
            self.greenLight = True
        elif curr_time % light_duration * 2 == light_duration:
            pygame.draw.circle(self.screen, self.c['YELLOW'], (x_pos, y_pos), 15)
        elif curr_time % light_duration * 2 > light_duration:
            pygame.draw.circle(self.screen, self.c['RED'], (x_pos, y_pos), 15)
            self.greenLight = False

    def display_sample_map(self):
        self.draw_canvas()
        running = True
        movement = 0
        evaluate_position = 360
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill(self.c['WHITE'])
            self.draw_car(movement)
            self.draw_road()
            self.draw_lights(x_pos=405, y_pos=170)
            pygame.display.flip()
            pygame.display.update()
            if evaluate_position == 80 + movement and self.greenLight == False:
                pass #stops the car
            else:
                movement += self.car_velocity
            if movement > self.window_size[0]:
                movement = -80 #move in a loop
            time.sleep(0.01) #preventing from going too fast
