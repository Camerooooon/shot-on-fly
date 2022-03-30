import pygame
import math as math
pygame.init()

window_width = 2000
window_height = 1000
font = pygame.font.Font('freesansbold.ttf', 32)

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Robot Simulation")

robot_x = window_width/2
robot_y = window_height/2
robot_rot = 360
robot_vx = 0
robot_vy = 0
robot_speed_multiplier = 0.5
robot_acceleration = 10
robot_friction = 0.7

balls = []

class Ball:
    pos_x = 0
    pos_y = 0
    velocity_x = 0
    velocity_y = 0
    def __init__(self, pos_x, pos_y, velocity_x, velocity_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y


def aim_at(pos_x, pos_y):
    try:
        if (pos_x - robot_x) < 0:
            return 180 + math.atan((pos_y - robot_y)/(pos_x - robot_x)) / (math.pi/180)
        return math.atan((pos_y - robot_y)/(pos_x - robot_x)) / (math.pi/180)
    except:
        return 0

def smart_aim(pos_x, pos_y):
    robot_heading = aim_at(robot_x + -robot_vx, robot_y + -robot_vy)
    vx = math.cos(robot_rot * (math.pi/180)) * 100
    vy = math.sin(robot_rot * (math.pi/180)) * 100
    #ball_speed = math.fabs(vx) + math.fabs(vy)
    #goal_dist = math.sqrt(math.pow((robot_x - pos_x),2) + math.pow((robot_y - pos_y),2))
    dist_x = math.fabs(robot_x - pos_x)
    dist_y = math.fabs(robot_y - pos_y)
    ball_travel = dist_x/vx
    #ball_travel = (goal_dist/ball_speed) 


    tx = vx*(ball_travel)
    ty = vy*(ball_travel)
    print(ball_travel)
    return tx, ty

run = True
while run:
    pygame.time.delay(50)
    tx = 0
    ty = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        keys = pygame.key.get_pressed()

    
    if keys[pygame.K_a]:
        robot_vx -= robot_acceleration
    if keys[pygame.K_d]:
        robot_vx += robot_acceleration
    if keys[pygame.K_w]:
        robot_vy -= robot_acceleration
    if keys[pygame.K_s]:
        robot_vy += robot_acceleration

    if keys[pygame.K_UP]:
        robot_rot += 5
    if keys[pygame.K_DOWN]:
        robot_rot -= 5
    if keys[pygame.K_SPACE]:
        robot_rot = aim_at(window_width/2, window_height/2)
        tx, ty = smart_aim(window_width/2, window_height/2)
    if keys[pygame.K_e]:
        vx = math.cos(robot_rot * (math.pi/180)) * 100
        vy = math.sin(robot_rot * (math.pi/180)) * 100
        balls.append(Ball(robot_x, robot_y, robot_vx + vx, robot_vy + vy))
        print(math.fabs(vx+robot_vx) + math.fabs(vy+robot_vy))
    if robot_rot > 360:
        robot_rot = robot_rot - 360
    if robot_rot <= 0:
        robot_rot = robot_rot + 360

    robot_x = robot_x + robot_vx * robot_speed_multiplier
    robot_y = robot_y + robot_vy * robot_speed_multiplier

    robot_vx = robot_vx * robot_friction
    robot_vy = robot_vy * robot_friction


    win.fill((0,0,0))

    text = font.render("PosX: " + str(round(robot_x, 1)) + " - PosY: " + str(round(robot_y, 1)) + " - Rotation: " + str(round(robot_rot, 1)) + " - Velocity X (px/frame): " + str(round(robot_vx, 1)) + " - Velocity Y (px/frame): " + str(round(robot_vy, 1)) + " - Speed (px/frame): " + str(round(math.fabs(robot_vx) + math.fabs(robot_vy))), True, (255,255,255))
    textRect = text.get_rect()
    win.blit(text, textRect)

    for ball in balls:
        ball.pos_x = ball.pos_x + ball.velocity_x
        ball.pos_y = ball.pos_y + ball.velocity_y

        pygame.draw.circle(win, (255,0,0), (ball.pos_x, ball.pos_y), radius = 5)

    # Draw robot
    pygame.draw.rect(win, (255,0,0), (robot_x-(25/2), robot_y-(25/2), 25, 25))
    
    # Smart aim redicle
    pygame.draw.rect(win, (255,255,0), (window_width/2 + tx, window_height/2 + ty, 15, 15))

    pygame.draw.line(win, (0, 0, 255), (robot_x, robot_y), (robot_x + (math.cos(robot_rot * (math.pi/180)) * 300), robot_y + (math.sin(robot_rot * (math.pi/180)) * 300)), width=5)

    # Goal velocity relative
    pygame.draw.line(win, (0, 0, 255), (window_width/2, window_height/2), (window_width/2 + (math.cos(robot_rot * (math.pi/180)) * 300), window_height/2 + (math.sin(robot_rot * (math.pi/180)) * 300)), width=5)
    
    pygame.draw.line(win, (255, 255, 255), (window_width/2, window_height/2), (window_width/2 + -robot_vx, window_height/2 + -robot_vy), width=5)
    
    
    pygame.draw.line(win, (0, 255, 255), (robot_x, robot_y), (robot_x + (robot_vx), robot_y + (robot_vy)), width=5)

    # Draw goal
    pygame.draw.circle(win, (0,255,255), (window_width/2, window_height/2), 15)

    pygame.display.update()

pygame.quit()

