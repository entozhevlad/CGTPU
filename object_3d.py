import pygame as pg
from matrix_functions import *

class Object3D: #Класс для взимодействия с главной программой
    def __init__(self,render):
        self.render = render
        self.vertexes = np.array([(0,0,0,1),(0,1,0,1),(1,1,0,1),(1,0,0,1),
                                  (0,0,1,1),(0,1,1,1),(1,1,1,1),(1,0,1,1)]) # массив вершин, однородные координаты

        self.faces = np.array([(0,1,2,3),(4,5,6,7),(0,4,5,1),(2,3,7,6),(1,2,6,5),(0,3,7,4)]) # массив граней куба
    def draw(self):
        self.screen_projection()

    def screen_projection(self):
        vertexes =  self.vertexes @ self.render.camera.camera_matrix() # перенос вершин объекта в пространство камеры
        vertexes =  vertexes @ self.render.projection.projection_matrix # перенос вершины в пространство отсечения
        vertexes /= vertexes[:,-1].reshape(-1,1) # нормализуем координаты вершин
        vertexes[(vertexes > 1) | (vertexes < -1)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2] # координаты для x,y,z

        for face in self.faces: # проход по всем граням объекта для отображения нужной грани
            polygon = vertexes[face]
            if not np.any((polygon == self.render.H_WIDTH) | (polygon ==  self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), polygon, 3)

        for vertex in vertexes: # отрисовка вершин объекта
            if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
                pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 6)



    def translate(self, pos): # методы по перемещению объекта в пространстве
        self.vertexes = self.vertexes @ translate(pos)

    def scale(self, scale_to):
        self.vertexes =  self.vertexes @ scale(scale_to)

    def rotate_x(self,angle):
        self.vertexes = self.vertexes @ rotate_x(angle)

    def rotate_y(self,angle):
        self.vertexes = self.vertexes @ rotate_y(angle)

    def rotate_z(self,angle):
        self.vertexes = self.vertexes @ rotate_z(angle)

