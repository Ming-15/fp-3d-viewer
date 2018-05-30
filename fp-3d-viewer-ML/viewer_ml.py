#_*_ coding: utf-8 _*_
'''
@author ML
this program allows you to travel in a 3D floor-plan model
you can move use key w(a,s,d)
change view with key arrow up(down, right, left)
you can raise up your vision using key h and down with key j
to move your vision quickly using key v while key c on the contrary
'''
from math import pi, sin, cos
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from floorplan import Floorplan
import numpy as np
import copy


class Viewer(ShowBase):
    def __init__(self):

        ShowBase.__init__(self)

        base.setBackgroundColor(0, 0, 0)
        self.angle = 0.0
        lens = PerspectiveLens()
        lens.setFov(60)
        lens.setNear(0.01)
        lens.setFar(100000)
        base.cam.node().setLens(lens)
        floorplan = Floorplan('test/floorplan')
        floorplan.read()
        self.scene = floorplan.generateEggModel()
        self.scene.reparentTo(self.render)
        self.scene.setScale(50, 50, 50)
        self.scene.setTwoSided(True)

        # data for zml
        self.date_zml = {'ca_pos':[33, 35, 8] ,'target':[0,0,8] , 'topDownH': 0}

        self.cameraPos = self.date_zml['ca_pos']
        self.target = self.date_zml['target']
        self.H = self.date_zml['topDownH']
        self.movementStep = 0.01
        self.rotationStep = 0.02

        # self.accept('space', self.openDoor)
        # self.accept('enter', self.startChangingView)

        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")
    def spinCameraTask(self, task):
        movementStep = self.movementStep
        if base.mouseWatcherNode.is_button_down('h'):

            self.cameraPos[2] += 1
            self.target[2] += 1
            print self.cameraPos[2]
            pass
        if base.mouseWatcherNode.is_button_down('j'):

            self.cameraPos[2] -= 1
            self.target[2] -= 1
            print self.cameraPos[2]
            pass
        if base.mouseWatcherNode.is_button_down('v'):

            self.movementStep += 0.01
            print movementStep
            pass
        if base.mouseWatcherNode.is_button_down('c'):
            self.movementStep -= 0.01
            print movementStep
            pass
        if base.mouseWatcherNode.is_button_down('w'):
            for c in range(2):
                step = movementStep * (self.target[c] - self.cameraPos[c])
                self.cameraPos[c] += step
                self.target[c] += step
                continue
            pass
        if base.mouseWatcherNode.is_button_down('s'):
            for c in range(2):
                step = movementStep * (self.target[c] - self.cameraPos[c])
                self.cameraPos[c] -= step
                self.target[c] -= step
                continue
            pass
        if base.mouseWatcherNode.is_button_down('a'):
            step = movementStep * (self.target[0] - self.cameraPos[0])
            self.cameraPos[1] += step
            self.target[1] += step
            step = movementStep * (self.target[1] - self.cameraPos[1])
            self.cameraPos[0] -= step
            self.target[0] -= step
            pass
        if base.mouseWatcherNode.is_button_down('d'):
            step = movementStep * (self.target[0] - self.cameraPos[0])
            self.cameraPos[1] -= step
            self.target[1] -= step
            step = movementStep * (self.target[1] - self.cameraPos[1])
            self.cameraPos[0] += step
            self.target[0] += step
            pass
        rotationStep = self.rotationStep
        if base.mouseWatcherNode.is_button_down('arrow_left'):
            angle = np.angle(complex(self.target[0] - self.cameraPos[0], self.target[1] - self.cameraPos[1]))
            angle += rotationStep
            self.target[0] = self.cameraPos[0] + np.cos(angle)
            self.target[1] = self.cameraPos[1] + np.sin(angle)
            pass
        if base.mouseWatcherNode.is_button_down('arrow_right'):
            angle = np.angle(complex(self.target[0] - self.cameraPos[0], self.target[1] - self.cameraPos[1]))
            angle -= rotationStep
            self.target[0] = self.cameraPos[0] + np.cos(angle)
            self.target[1] = self.cameraPos[1] + np.sin(angle)
            pass

        if base.mouseWatcherNode.is_button_down('arrow_up'):
            angle = np.arcsin(self.target[2] - self.cameraPos[2])
            angle += rotationStep
            self.target[2] = self.cameraPos[2] + np.sin(angle)
            pass
        if base.mouseWatcherNode.is_button_down('arrow_down'):
            angle = np.arcsin(self.target[2] - self.cameraPos[2])
            angle -= rotationStep
            self.target[2] = self.cameraPos[2] + np.sin(angle)
            pass

        self.camera.setPos(self.cameraPos[0], self.cameraPos[1], self.cameraPos[2])

        self.camera.lookAt(self.target[0], self.target[1], self.target[2])


        return Task.cont


app = Viewer()
app.run()
