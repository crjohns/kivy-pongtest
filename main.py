from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint
from kivy.config import Config
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

class PongPaddle(Widget):

    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.vel

            # prevent getting stuck
            if vx < 0 and self.x > self.get_parent_window().width/2:
                return
            elif vx > 0 and self.x < self.get_parent_window().width/2:
                return
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.vel = vel.x, vel.y + offset

class PongGame(Widget):

    ball = ObjectProperty(None)

    def update(self, delta):
        self.ball.move()

        # player bounce
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # wall bounce
        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.vel_y *= -1

        # point score
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        rotate = randint(0,90)-45
        if randint(0,2) == 0:
            rotate = rotate+180
        self.ball.vel = Vector(vel).rotate(rotate)

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y

class PongBall(Widget):
    vel_x = NumericProperty(0)
    vel_y = NumericProperty(0)

    vel = ReferenceListProperty(vel_x, vel_y)

    def move(self):
        self.pos = Vector(*self.vel) + self.pos

class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game



PongApp().run()
