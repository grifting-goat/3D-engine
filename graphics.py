import pygame
import engine

def drawLine(screen, line, otherLine, color, thickness):
    pygame.draw.line(screen,color , [otherLine.x, otherLine.y],[line.x, line.y], thickness)

def drawTri(screen, tri, color, thickness):
    drawLine(screen, tri.points[1], tri.points[0], color, thickness)
    drawLine(screen, tri.points[2], tri.points[1], color, thickness)
    drawLine(screen, tri.points[2], tri.points[0], color, thickness)

def drawMesh(screen, mesh: engine.Mesh, color, thickness):
    for tri in mesh.triangles:
        drawTri(screen, tri, color, thickness)




