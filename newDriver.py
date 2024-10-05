import pygame
import engine
import graphics
import math
import time
import camera

pygame.init()

#define player variables
fov = math.pi/2
playerAngle = 0
playerPos = engine.Vector(0,0,0)

#game vars/data
maxDepth = 1000
minDepth = .1
angle = 0
angle2 = 0
font = pygame.font.Font(None, 36)

#models
cube = engine.cubeMesh()
tea = engine.parse_obj('teapot.obj')
print(tea)
print(cube)


#define aspect ratio and scale
aspectRatio = [16,9]
aspect = aspectRatio[0]/aspectRatio[1]
windowScaler = 60
baseLineThickness = 1

#define window height
windowHeight = aspectRatio[0] * windowScaler
windowWidth = aspectRatio[1] * windowScaler

#define the center points
centerY = windowWidth/2
centerX = windowHeight/2

#making the window
screen = pygame.display.set_mode((windowHeight, windowWidth))
isRunning = True

#arbitrary background and startup information
pygame.display.set_caption("3D engine")
screen.fill((0, 0, 0)) 
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

#control timing
start_time = time.time()
end_time = 0

#create camera
cam = camera.Camera(playerPos, engine.Vector(0,0,0), windowHeight, windowWidth)

while isRunning:

    #calculate the change in time since last pass
    end_time = time.time()
    tick = end_time - start_time
    start_time = end_time
    fps = 0

    if tick > 0:
        fps = 1/tick
    
    #reset the screen
    screen.fill((0,0,0))

    #add fps label
    text = font.render(f'FPS: {fps:.1f}', True, (255, 255, 255))
    screen.blit(text, (0, 0))

    #check for window close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False

    #handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 0.5 * tick
    if keys[pygame.K_RIGHT]:
        angle += 0.5 * tick
    if keys[pygame.K_DOWN]:
        angle2 -= 0.5 * tick
    if keys[pygame.K_UP]:
        angle2 += 0.5 * tick
    if keys[pygame.K_w]:
        playerPos.z += 0.5 * tick
    if keys[pygame.K_s]:
        playerPos.z -= 0.5 * tick
    if keys[pygame.K_a]:
        playerPos.x -= 0.5 * tick
    if keys[pygame.K_d]:
        playerPos.x += 0.5 * tick
    if keys[pygame.K_SPACE]:
        playerPos.y += 0.5 * tick
    if keys[pygame.K_LSHIFT]:
        playerPos.y -= 0.5 * tick

    #--test code--
    #copy unit cube
    
    #currCube = cube.copy()
    #currCube = cam.renderMesh(currCube)

    offs = [angle, angle2, 0]

    currTea= tea.copy()
    #currTea = cam.renderMesh(currTea)
    currTea = cam.renderSpinningMesh(currTea, offs)

    #draw using the graphics engine
    graphics.drawMesh(screen, currTea, (255,0,0), baseLineThickness)

    # Update the display: flip the buffers
    pygame.display.flip()   
    
    
#properly shutdown
pygame.quit()