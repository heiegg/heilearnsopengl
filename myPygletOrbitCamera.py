from pyglet.math import *
from pyglet.window import key, mouse
from math import *
from myPygletUtil import scalarMult, rotate_vec3

modifier_down=False
mouse_loc=None

camera={
    "pos" : Vec3(0,0,10),
    "front" : Vec3(0,0,-1), #direction camera is facing
    "up" : Vec3(0,1,0), #  camera up direction
    "right": Vec3(1,0,0), # camera right direction
    "fov" : 45.0, # degrees
}

def camera_on_mouse_press(x, y, button, modifiers):
    global mouse_loc
    mouse_loc=(x,y)

def camera_on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    """orbit around origin (left or middle button drag) and zoom (right button drag)"""
    global camera, mouse_loc

    # somehow middle mouse via Multitouch with magic mouse always produces 0 for dx, dy :(
    # in addition, if I set exclusive mouse, mouse location would be locked and below would not work.
    if buttons & mouse.LEFT or buttons & mouse.MIDDLE:
        #orbit

        if buttons & mouse.MIDDLE:
            # manually work out dx, dy
            dx=x-mouse_loc[0]
            dy=y-mouse_loc[1]
            mouse_loc=(x,y)
        
        camera_orbit(dx,dy)
            

    elif  buttons & mouse.RIGHT:
        camera_zoom(dy)

def camera_on_mouse_scroll(x, y, scroll_x, scroll_y):
    """pan/zoom control"""
    global camera, modifier_down

    if not modifier_down:
        #pan
        camera_pan(scroll_x,scroll_y)

    elif modifier_down:
        #zoom
        camera_zoom(scroll_y)
        
def camera_orbit(dx,dy):
    sensitivity=0.03
    dx *= sensitivity
    dy *= sensitivity

    mouse_move_vec = scalarMult(dx, camera["right"]) + scalarMult(dy, camera["up"])

    rot_axis = mouse_move_vec.cross(camera["pos"]).normalize()
    for k in camera:
        if k == "pos" or k=="front" or k=="up" or k=="right":
            camera[k] = rotate_vec3(camera[k], -mouse_move_vec.mag, rot_axis)


def camera_zoom(dy):
    sensitivity =2
    dy *= sensitivity
    camera["fov"] += dy

    if camera["fov"] < 1:
        camera["fov"]=1
    if camera["fov"] > 75.0:
        camera["fov"]=75.0


            
def camera_pan(dx,dy):
    sensitivity =0.1
    dx*=sensitivity
    dy*=sensitivity

    mouse_pan_vec=scalarMult(dx, camera["right"]) + scalarMult(dy, camera["up"])

    camera["pos"] -=  mouse_pan_vec

def camera_on_key_press(symbol, modifiers):
    global modifier_down
    if symbol & key.LCOMMAND:
        modifier_down = True

def camera_on_key_release(symbol, modifiers):
    global modifier_down
    if symbol & key.LCOMMAND:
        modifier_down = False

def camera_update(dt,window_aspect_ratio, key_states):
    """window_aspect_ratio is win_w/win_h. computes and returns view and projection matrices. key_states not used now."""
    global camera
    view = Mat4().look_at(camera["pos"], camera["pos"]+camera["front"],camera["up"])
    projection = Mat4.perspective_projection(window_aspect_ratio, 0.1, 100.0, fov=camera["fov"]) # fov is in degrees. Note: different from convention of glm.

    return {"view":view,"projection":projection}


# sample usage
# window.push_handlers(on_mouse_scroll=camera_on_mouse_scroll,
#                      on_mouse_drag=camera_on_mouse_drag,
#                      on_mouse_press=camera_on_mouse_press,
#                      on_key_press=camera_on_key_press,
#                      on_key_release=camera_on_key_release
# )
# def update(dt):
#     mats=camera_update(dt,window_aspect_ratio,key_states)
#     shader_program["projection"]=mats["projection"]
#     shader_program["view"]=mats["view"]
#     model=Mat4()
#     shader_program["model"]=model
    
# pyglet.clock.schedule_interval(update, timeStep)
