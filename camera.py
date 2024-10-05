import engine
import graphics
import math

class Camera:
    def __init__(self):
        self.cameraPos = engine.Vector(0,0,0) #camera in world space
        self.cameraDir = engine.Vector(0,0,0) #camera direction vector
        self.cameraFOV = math.pi/2
        self.maxDepth = 1000 
        self.minDepth = .1
        self.aspectRatio = 16/9
        self.windowHeight = 1600
        self.windowWidth = 900
    
    def __init__(self, cPos, cDir):
        self.cameraPos = cPos
        self.cameraDir = cDir
        self.cameraFOV = math.pi/2
        self.maxDepth = 1000 
        self.minDepth = .1
        self.aspectRatio = 16/9
        self.windowHeight = 1600
        self.windowWidth = 900

    def __init__(self, cPos, cDir, h, w):
        self.cameraPos = cPos
        self.cameraDir = cDir
        self.cameraFOV = math.pi/2
        self.maxDepth = 1000 
        self.minDepth = .1
        self.windowHeight = h
        self.windowWidth = w
        self.aspectRatio = h/w
        
    
    def setDepth(self, min, max):
        self.maxDepth = max
        self.minDepth = min
    
    def setFOV(self, fov):
        self.cameraFOV = fov

    def setOutputPlane(self, h, w):
        self.windowHeight = h
        self.windowWidth = w
        self.aspectRatio = h/w
    
    def renderMesh(self, Mesh):
        mesh = Mesh.copy()
        # Rotate the mesh around the z and x axes
        mesh = engine.rotate(mesh, engine.rotMatz, 1)
        mesh = engine.rotate(mesh, engine.rotMatx, 1)
        mesh = engine.rotate(mesh, engine.rotMaty, 1)

        mesh = engine.offsetMesh(mesh, 0, 0, 30)

        # Project the 3D mesh down to 2D based on camera parameters
        projectedMesh = engine.projection(mesh, self.cameraFOV, self.aspectRatio, self.maxDepth, self.minDepth)

        projectedMesh = engine.offsetMesh(projectedMesh, 1.5, 0.5, 0)

        # Filter the mesh by normals, using camera position for perspective
        engine.filterNormals(projectedMesh, self.cameraPos)

        #scale the mesh to fit the screen size
        projectedMesh = engine.scaleMesh2(projectedMesh, 0.5 * self.windowWidth, 0.5 * self.windowHeight)

        return projectedMesh
    

    def renderSpinningMesh(self, Mesh, angle: list):
        mesh = Mesh.copy()
        # Rotate the mesh around the z and x axes
        mesh = engine.rotate(mesh, engine.rotMatz, angle[2])
        mesh = engine.rotate(mesh, engine.rotMatx, angle[0])
        mesh = engine.rotate(mesh, engine.rotMaty, angle[1])

        #Offset the mesh in the z-direction for depth
        mesh = engine.offsetMesh(mesh, 0, 0, 30)

        #project the 3D mesh down to 2D based on camera parameters
        projectedMesh = engine.projection(mesh, self.cameraFOV, self.aspectRatio, self.maxDepth, self.minDepth)

        #Offset the projected mesh
        projectedMesh = engine.offsetMesh(projectedMesh, 3, 1.2, 0)

        # Filter the mesh by normals, using camera position for perspective
        engine.filterNormals(projectedMesh, self.cameraPos)

        #Scale the mesh to fit the screen size
        projectedMesh = engine.scaleMesh2(projectedMesh, 0.3 * self.windowWidth, 0.3 * self.windowHeight)

        return projectedMesh