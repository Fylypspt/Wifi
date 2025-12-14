import pygame
import math

WIDTH, HEIGHT = 900, 600
rayNum = 360
maxRayL = 500
initPower = 80
minPower = 1.0 
wallPwrLoss = 0.7

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
tx_pos = [WIDTH // 2, HEIGHT // 2]

walls = [
    ((200, 150), (700, 150)),
    ((700, 150), (700, 450)),
    ((700, 450), (200, 450)),
    ((200, 450), (200, 150)),
    ((400, 150), (400, 450))
]

def line_intersection(p1, p2, p3, p4):

    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
    if den == 0:
        return None

    t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
    u = ((x1 - x3)*(y1 - y2) - (y1 - y3)*(x1 - x2)) / den

    if 0 <= t <= 1 and 0 <= u <= 1:
        ix = x1 + t * (x2 - x1)
        iy = y1 + t * (y2 - y1)
        return (ix, iy)

    return None

def distance(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def drawRays(angle_deg):
    angle = math.radians(angle_deg)

    dx = math.cos(angle)
    dy = math.sin(angle)

    ray_start = tuple(tx_pos)
    ray_end = (
        tx_pos[0] + dx * maxRayL,
        tx_pos[1] + dy * maxRayL
    )

    power = initPower
    current_start = ray_start

    for _ in range(5):
        closest_hit = None
        closest_wall = None
        min_dist = float("inf")

        for wall in walls:
            hit = line_intersection(current_start, ray_end, wall[0], wall[1])
            if hit:
                d = distance(current_start, hit)
                if d < min_dist:
                    min_dist = d
                    closest_hit = hit
                    closest_wall = wall

        if closest_hit is None:
            break

        intensity = max(0, min(255, int(power * 2)))
        
        pygame.draw.line(
            screen,
            (intensity, intensity, 0),
            current_start,
            closest_hit,
            1
        )

        power *= wallPwrLoss

        if power < minPower:
            break

        current_start = (
            closest_hit[0] + dx * 0.1,
            closest_hit[1] + dy * 0.1
        )

    if power >= minPower:
        intensity = max(0, min(255, int(power * 2)))
        pygame.draw.line(
            screen,
            (intensity, intensity, 0),
            current_start,
            ray_end,
            1
        )

running = True

ultra = False

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if ultra == False:
                    ultra = True
                    wallPwrLoss = 0.4
                    maxRayL = 250
                    initPower = 130
                else:
                    ultra = False
                    wallPwrLoss = 0.7
                    maxRayL = 500
                    initPower = 60

    if pygame.mouse.get_pressed()[0]:
        tx_pos = list(pygame.mouse.get_pos())
    

    screen.fill((20, 20, 20))

    for w in walls:
        pygame.draw.line(screen, (200, 200, 200), w[0], w[1], 3)

    for angle_deg in range(0, 360, 4):
       drawRays(angle_deg) 

    pygame.draw.circle(screen, (255, 0, 0), tx_pos, 6)

    pygame.display.flip()

pygame.quit()