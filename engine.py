from dataclasses import dataclass
from typing import List
import math

#essential data structures

@dataclass
class Vector:
    x: float
    y: float
    z: float

    def mag(self):
        return (self.x ** 2 + self.y ** 2 + self.z **2) ** .5

    #Operator overloading for vector stuff
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __repr__(self):
        return f"Vector({self.x}, {self.y}, {self.z})"
    
    def __mul__(self, other):
        if isinstance(other, (int, float)):
            prod_x = self.x * other
            prod_y = self.y * other
            prod_z = self.z * other
            return Vector(prod_x, prod_y, prod_z)
    

@dataclass
class Triangle:
    points: List[Vector]

@dataclass
class Mesh:
    triangles: List[Triangle]

    def copy(self):
        return Mesh(triangles=[Triangle(points=[Vector(point.x, point.y, point.z) for point in tri.points]) for tri in self.triangles])


@dataclass
class Mat4x4:
    m: List[List[float]]

    def __init__(self, matrix: List[List[float]] = None):
        if matrix is None:
            self.m = [[0.0 for _ in range(4)] for _ in range(4)]
        else:
            self.m = matrix


def offsetMesh(mesh: Mesh, offsetX: float, offsetY: float, offsetZ: float) -> Mesh:
    newMesh = mesh.copy()
    for tri in newMesh.triangles:
        for point in tri.points:
            point.x += offsetX  
            point.y += offsetY
            point.z += offsetZ  
    return newMesh


def scaleMesh(mesh: Mesh, scale: float) -> Mesh:
    newMesh = mesh.copy()
    for tri in newMesh.triangles:
        for point in tri.points:
            point.x *= scale
            point.y *= scale
            point.z *= scale
    return newMesh


def scaleMesh2(mesh: Mesh, scaleX: float, scaleY: float) -> Mesh:
    newMesh = mesh.copy()
    for tri in newMesh.triangles:
        for point in tri.points:
            point.x *= scaleX
            point.y *= scaleY
    return newMesh           

def cubeMesh() -> Mesh:
    # Define the triangles of the cube using the vertices directly
    triangles = [
        # SOUTH
        Triangle(points=[
            Vector(0.0, 0.0, 0.0),
            Vector(0.0, 1.0, 0.0),
            Vector(1.0, 1.0, 0.0)
        ]),
        Triangle(points=[
            Vector(0.0, 0.0, 0.0),
            Vector(1.0, 1.0, 0.0),
            Vector(1.0, 0.0, 0.0)
        ]),

        # EAST
        Triangle(points=[
            Vector(1.0, 0.0, 0.0),
            Vector(1.0, 1.0, 0.0),
            Vector(1.0, 1.0, 1.0)
        ]),
        Triangle(points=[
            Vector(1.0, 0.0, 0.0),
            Vector(1.0, 1.0, 1.0),
            Vector(1.0, 0.0, 1.0)
        ]),

        # NORTH
        Triangle(points=[
            Vector(1.0, 0.0, 1.0),
            Vector(1.0, 1.0, 1.0),
            Vector(0.0, 1.0, 1.0)
        ]),
        Triangle(points=[
            Vector(1.0, 0.0, 1.0),
            Vector(0.0, 1.0, 1.0),
            Vector(0.0, 0.0, 1.0)
        ]),

        # WEST
        Triangle(points=[
            Vector(0.0, 0.0, 1.0),
            Vector(0.0, 1.0, 1.0),
            Vector(0.0, 1.0, 0.0)
        ]),
        Triangle(points=[
            Vector(0.0, 0.0, 1.0),
            Vector(0.0, 1.0, 0.0),
            Vector(0.0, 0.0, 0.0)
        ]),

        # TOP
        Triangle(points=[
            Vector(0.0, 1.0, 0.0),
            Vector(0.0, 1.0, 1.0),
            Vector(1.0, 1.0, 1.0)
        ]),
        Triangle(points=[
            Vector(0.0, 1.0, 0.0),
            Vector(1.0, 1.0, 1.0),
            Vector(1.0, 1.0, 0.0)
        ]),

        # BOTTOM
        Triangle(points=[
            Vector(1.0, 0.0, 1.0),
            Vector(0.0, 0.0, 1.0),
            Vector(0.0, 0.0, 0.0)
        ]),
        Triangle(points=[
            Vector(1.0, 0.0, 1.0),
            Vector(0.0, 0.0, 0.0),
            Vector(1.0, 0.0, 0.0)
        ]),
    ]
    return Mesh(triangles=triangles)

def matrixByVector(vec: Vector, mat: Mat4x4) -> Vector:
    # Convert Vector to 4D
    x = vec.x
    y = vec.y
    z = vec.z
    w = 1.0  # Homogeneous coordinate
    # Perform the matrix multiplication
    new_x = (mat.m[0][0] * x + mat.m[0][1] * y + mat.m[0][2] * z + mat.m[0][3] * w)
    new_y = (mat.m[1][0] * x + mat.m[1][1] * y + mat.m[1][2] * z + mat.m[1][3] * w)
    new_z = (mat.m[2][0] * x + mat.m[2][1] * y + mat.m[2][2] * z + mat.m[2][3] * w)
    new_w = (mat.m[3][0] * x + mat.m[3][1] * y + mat.m[3][2] * z + mat.m[3][3] * w)

    # Convert back to 3D by normalizing if w is not 0
    if new_w != 0:
        new_x /= new_w
        new_y /= new_w
        new_z /= new_w

    return Vector(new_x, new_y, new_z)

def rotMaty(fTheta):
    matRotY = Mat4x4()
    
    cos_theta = math.cos(fTheta)
    sin_theta = math.sin(fTheta)
    
    #Set the rotation matrix values for Y-axis rotation
    matRotY.m[0][0] = cos_theta
    matRotY.m[0][2] = -sin_theta
    matRotY.m[1][1] = 1
    matRotY.m[2][0] = sin_theta
    matRotY.m[2][2] = cos_theta
    matRotY.m[3][3] = 1
    
    return matRotY

def rotMatz(fTheta):
    matRotZ = Mat4x4()

    cos_theta = math.cos(fTheta)
    sin_theta = math.sin(fTheta)
    
    # Set the rotation matrix values
    matRotZ.m[0][0] = cos_theta
    matRotZ.m[0][1] = sin_theta
    matRotZ.m[1][0] = -sin_theta
    matRotZ.m[1][1] = cos_theta
    matRotZ.m[2][2] = 1
    matRotZ.m[3][3] = 1
    
    return matRotZ

def rotMatx(fTheta):
    matRotX = Mat4x4()  # Initialize a new rotation matrix
    cos_theta = math.cos(fTheta)
    sin_theta = math.sin(fTheta)
    
    matRotX.m[0][0] = 1
    matRotX.m[1][1] = cos_theta
    matRotX.m[1][2] = sin_theta
    matRotX.m[2][1] = -sin_theta
    matRotX.m[2][2] = cos_theta
    matRotX.m[3][3] = 1
    
    return matRotX

def rotate(iMesh, rotMatFunc, angle):
    mesh = iMesh.copy()
    rotMat = rotMatFunc(angle)
    for tri in mesh.triangles:
        for i in range(len(tri.points)):
            tri.points[i] = matrixByVector(tri.points[i], rotMat)
    return mesh

def projection(iMesh: Mesh, camAngle, aspect, maxDepth, minDepth):
    mesh = iMesh.copy()
    a = aspect
    f = f = 1 / math.tan(camAngle / 2)
    q = maxDepth/(maxDepth - minDepth)
    projMat = Mat4x4([
        [a * f, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, q, 1],
        [0, 0, -1*minDepth * q, 0]
    ])
    for tri in mesh.triangles:
        for i in range(len(tri.points)):
            tri.points[i] = matrixByVector(tri.points[i], projMat)  # Update the original point
    return mesh

def cross(v1: Vector, v2: Vector) -> Vector:
    cross_x = v1.y * v2.z - v1.z * v2.y
    cross_y = v1.z * v2.x - v1.x * v2.z
    cross_z = v1.x * v2.y - v1.y * v2.x
    
    return Vector(cross_x, cross_y, cross_z)

def dot_product(v1: Vector, v2: Vector) -> float:
    return v1.x * v2.x + v1.y * v2.y + v1.z * v2.z

def normalize(v: Vector) -> Vector:
    length = math.sqrt(v.x ** 2 + v.y ** 2 + v.z ** 2)
    if length == 0:
        return Vector(0, 0, 0)
    return Vector(v.x / length, v.y / length, v.z / length)

#i barely understand this
def filterNormals(mesh: Mesh, playerPos):
    newTri = []
    for tri in mesh.triangles:
        #Get vectors for the edges of the triangle
        line1 = tri.points[1] - tri.points[0]
        line2 = tri.points[2] - tri.points[0]
    
        #Cross product of the lines to get normal
        normal = cross(line1, line2)
    
        #Normalize the result (so you dont have to later)
        normal = normalize(normal)

        vec2cam = normalize(playerPos - tri.points[0])

        #the normal faces away from the camera get filtered out
        if dot_product(normal, vec2cam) > 0:
            newTri.append(tri)

    mesh.triangles = newTri


def parse_obj(file_path) -> Mesh:
    vertices: List[Vector] = []
    faces: List[List[int]] = []

    with open(file_path, 'r') as file:
        for line in file:
            section = line.split()
            if section and section[0] == 'v':
                # Convert to float to ensure components are not stored as strings
                vertex = Vector(float(section[1]), float(section[2]), float(section[3]))
                vertices.append(vertex)
            elif section and section[0] == 'f':
                face = [int(sec.split('/')[0]) - 1 for sec in section[1:]]
                faces.append(face)

    triangles: List[Triangle] = []
    for face in faces:
        points = [vertices[i] for i in face]  # Get the actual Vector objects
        triangle = Triangle(points=points)
        triangles.append(triangle)

    return Mesh(triangles=triangles)

