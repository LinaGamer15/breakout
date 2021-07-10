from turtle import Turtle, Screen
import random

ws = Screen()
ws.bgcolor('black')
ws.setup(900, 500)


def create_bricks(color, list_bricks, row):
    for i in range(15):
        brick = Turtle()
        brick.shape('square')
        brick.shapesize(0.2, 2.1, 0)
        brick.color(color)
        brick.penup()
        brick.goto(-326 + (i * 46.5), 190 - (row * 10))
        list_bricks.append(brick)


class Player(Turtle):
    def __init__(self):
        super().__init__()
        self.color('cyan')
        self.shape('square')
        self.shapesize(0.5, 5, 0)
        self.penup()
        self.goto(0, -130)

    def move_player(self, side):
        if side == 'left' and self.xcor() >= -250:
            self.backward(50)
        elif side == 'right' and self.xcor() <= 250:
            self.forward(50)


class Border(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.hideturtle()

    def create_border(self):
        self.penup()
        self.forward(350)
        self.left(90)
        self.forward(200)
        self.pendown()
        for i in range(4):
            self.left(90)
            if i == 1 or i == 3:
                self.forward(350)
            else:
                self.forward(700)


class WriterScore(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.hideturtle()
        self.penup()

    def draw_score(self):
        global score
        ws.tracer(0)
        self.goto(-350, 200)
        self.pendown()
        self.write(f'Score: {score}', font=('Arial', 20, 'normal'))
        self.penup()
        ws.tracer(1)


class WriterBallScore(Turtle):
    def __init__(self):
        super().__init__()
        self.color('white')
        self.hideturtle()
        self.penup()

    def draw_ball(self):
        global ball_score
        ws.tracer(0)
        self.goto(255, 200)
        self.pendown()
        self.write(f'Ball: {3 - ball_score}/3', font=('Arial', 20, 'normal'))
        self.penup()
        ws.tracer(1)


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.color('gray')
        self.shape('circle')
        self.shapesize(0.5)
        self.speed(1)
        self.penup()
        self.goto(0, -110)

        self.bricks = []

        self.colors = ['red', 'red', 'orange', 'orange', 'yellow', 'yellow', 'green', 'green', 'blue', 'blue']

    def add_bricks(self):
        for i in range(len(self.colors)):
            create_bricks(self.colors[i], self.bricks, i)

    def move_ball(self, player_1):
        ws.tracer(1)
        global game, ball_score, score
        if self.xcor() == 0 and self.ycor() == -110:
            y = self.bricks[-1].ycor()
            self.goto(random.randint(-175, 175), y)
        elif (self.xcor() <= -350 and -175 <= self.ycor() <= 175) or (self.xcor() >= 350 and -175 <= self.ycor() <= 175)\
                or (-350 <= self.xcor() <= 350 and self.ycor() >= 200):
            ball_score += 1
            wr_ball.clear()
            wr_ball.draw_ball()
            ws.tracer(0)
            self.goto(player_1.xcor(), -130)
        for i in range(len(self.bricks)):
            if self.bricks[i].color()[0] == 'black' and self.bricks[i].ycor() - self.ycor() <= 10 and \
                    0 <= abs(self.xcor() - self.bricks[i].xcor()) <= 30:
                if self.xcor() > 0:
                    ws.tracer(0)
                    self.goto(self.xcor() + 5, self.ycor() + 5)
                    ws.tracer(1)
                elif self.xcor() < 0:
                    ws.tracer(0)
                    self.goto(self.xcor() - 5, self.ycor() + 5)
                    ws.tracer(1)
                break
            elif self.bricks[i].ycor() - self.ycor() <= 0 and 0 <= abs(self.xcor() - self.bricks[i].xcor()) <= 30 and \
                    self.bricks[i].color()[0] != 'black':
                if self.bricks[i].color()[0] == 'red':
                    score += 50
                elif self.bricks[i].color()[0] == 'orange':
                    score += 40
                elif self.bricks[i].color()[0] == 'yellow':
                    score += 30
                elif self.bricks[i].color()[0] == 'green':
                    score += 20
                elif self.bricks[i].color()[0] == 'blue':
                    score += 10
                wr_score.clear()
                wr_score.draw_score()
                self.bricks[i].hideturtle()
                self.bricks[i].color('black')
                self.goto(random.randint(-175, 175), -130)
        if 0 <= abs(self.xcor() - player_1.xcor()) <= 50 and self.ycor() == player_1.ycor():
            y = self.bricks[-1].ycor()
            self.goto(random.randint(-175, 175), y)
        elif abs(self.xcor() - player_1.xcor()) > 50 and self.ycor() == player_1.ycor():
            ball_score += 1
            wr_ball.clear()
            wr_ball.draw_ball()
            ws.tracer(0)
            self.goto(player_1.xcor(), -130)
        ws.update()


ws.tracer(0)
player = Player()
border = Border()
border.create_border()
ball = Ball()
ball.add_bricks()
wr_score = WriterScore()
wr_ball = WriterBallScore()
ws.update()

ws.listen()
ws.onkey(lambda: player.move_player('right'), 'Right')
ws.onkey(lambda: player.move_player('left'), 'Left')

game = True
ball_score = 0
score = 0

wr_score.draw_score()
wr_ball.draw_ball()

while game:
    ball.move_ball(player)
    if ball_score == 3:
        game = False
ws.exitonclick()
