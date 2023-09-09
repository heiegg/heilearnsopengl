import pyglet
from pyglet.math import *
from pyglet.window import key, mouse

from math import *
from myPygletUtil import scalarMult

camera={
    "pos" : Vec3(0,0,3),
    "front" : Vec3(0,0,-1), #direction camera is facing
    "up" : Vec3(0,1,0), # a general up direction, not really the camera_up
    "yaw" : radians(-90.0),
    "pitch" : 0.0,
    "fov" : 45.0, # degrees
    "walkSpeed": 8
}


def camera_on_mouse_motion(x,y,dx,dy):
    """change direction of looking"""
    global camera
    
    sensitivity = 0.003
    dx *= sensitivity 
    dy *= sensitivity 

    camera["yaw"] += dx
    camera["pitch"] += dy

    if camera["pitch"] > radians(89.0):
        camera["pitch"] =radians( 89.0)
    elif camera["pitch"] < radians(-89.0):
        camera["pitch"] = radians(-89.0)
    
    camera["front"]=Vec3(cos(camera["pitch"]) * cos(camera["yaw"]), sin(camera["pitch"]), cos(camera["pitch"]) * sin(camera["yaw"]))



def camera_on_mouse_scroll(x, y, scroll_x, scroll_y):
    """zoom control"""
    global camera

    sensitivity =2
    scroll_y*=sensitivity
    camera["fov"] += scroll_y

    if camera["fov"] < 1.0:
        camera["fov"]=1.0
    if camera["fov"] > 60.0:
        camera["fov"]=60.0


    

def camera_update(dt,window_aspect_ratio, key_states):
    """handles keyboard pan. window_aspect_ratio is win_w/win_h. computes and returns view and projection matrices."""
    global camera
    
    if key_states[key.W]:
        camera["pos"] +=  scalarMult(camera["walkSpeed"] * dt, camera["front"].normalize())
    elif key_states[key.S]:
        camera["pos"] -=  scalarMult(camera["walkSpeed"] * dt, camera["front"].normalize())
    elif key_states[key.A]:
        camera["pos"] -= scalarMult(camera["walkSpeed"] * dt, camera["front"].cross(camera["up"]).normalize())
    elif key_states[key.D]:
        camera["pos"] += scalarMult(camera["walkSpeed"] * dt, camera["front"].cross(camera["up"]).normalize())

        

    view = Mat4().look_at(camera["pos"], camera["pos"]+camera["front"],camera["up"])
    projection = Mat4.perspective_projection(window_aspect_ratio, 0.1, 100.0, fov=camera["fov"]) # fov is in degrees. Note: different from convention of glm.

    return {"view":view,"projection":projection}


    
# example of usage.
# define a function that calls camera_update to get the matrices.

# window.push_handlers(on_mouse_scroll=camera_on_mouse_scroll,
#                      on_mouse_motion=camera_on_mouse_motion,
# )

# def update(dt):
#     mats=camera_update(dt,win_w/win_h,key_states)
#     shader_program["projection"]=mats["projection"]
#     shader_program["view"]=mats["view"]
#     model=Mat4()
#     shader_program["model"]=model
    
# pyglet.clock.schedule_interval(update, timeStep)

