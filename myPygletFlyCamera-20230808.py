import pyglet
from pyglet.math import *
from pyglet.window import key, mouse

from math import *
from myPygletUtil import *
# TODO: finish factoring out the fly camera. Well don't do it before I know how I would like to use this.
cameraPos = Vec3(0,0,3)
cameraFront = Vec3(0,0,-1)
cameraUp = Vec3(0,1,0)

yaw = radians(-90.0)
pitch = 0.0
fov = 45.0 # degrees

timeStep=1/120

key_states=key.KeyStateHandler()
window.push_handlers(key_states)

shader_program = None

def make_fly_camera(window, program, fov, parameters):
    window.set_exclusive_mouse(True)
    window.set_mouse_visible(False)
    window.push_handlers(on_mouse_motion, on_mouse_scroll)


def on_mouse_motion(x,y,dx,dy):
    global yaw, pitch, cameraFront
    
    sensitivity = 0.003
    dx *= sensitivity 
    dy *= sensitivity 

    yaw += dx
    pitch += dy

    if pitch > radians(89.0):
        pitch =radians( 89.0)
    elif pitch < radians(-89.0):
        pitch = radians(-89.0)
    
    cameraFront=Vec3(cos(pitch) * cos(yaw), sin(pitch), cos(pitch) * sin(yaw))


def on_mouse_scroll(x, y, scroll_x, scroll_y):    
    global fov

    sensitivity =2
    scroll_y*=sensitivity
    fov += scroll_y

    if fov < 1.0:
        fov=1.0
    if fov > 60.0:
        fov=60.0

def update_camera(dt):
    global cameraPos, cameraFront, cameraUp, fov
    
    cameraWalkSpeed = 8 

    if key_states[key.W]:
        cameraPos +=  scalarMult(cameraWalkSpeed * dt, cameraFront.normalize())
    elif key_states[key.S]:
        cameraPos -=  scalarMult(cameraWalkSpeed * dt, cameraFront.normalize())
    elif key_states[key.A]:
        cameraPos -= scalarMult(cameraWalkSpeed * dt, cameraFront.cross(cameraUp).normalize())
    elif key_states[key.D]:
        cameraPos += scalarMult(cameraWalkSpeed * dt, cameraFront.cross(cameraUp).normalize())

    view = Mat4().look_at(cameraPos, cameraPos+cameraFront,cameraUp)

    shader_program["view"]=view

    projection = Mat4.perspective_projection(win_w/win_h, 0.1, 100.0, fov=fov) # fov is in degrees. Note: different from convention of glm.
    shader_program["projection"]=projection

pyglet.clock.schedule_interval(update_camera, timeStep)
