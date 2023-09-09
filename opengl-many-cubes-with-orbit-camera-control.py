# ten cubes with camera control.
# hardcoded:
# left button or middle button drag to orbit
# 2-dim scroll wheel to pan
# Cmd+scroll or right button drag to zoom

import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import *
from pyglet.window import key, mouse

from math import *

from RenderGroup import *
from myPygletUtil import *
from myPygletOrbitCamera import *

win_w=800
win_h=600
window_aspect_ratio = win_w/win_h
timeStep=1/120


window = pyglet.window.Window(win_w,win_h)
# window.set_exclusive_mouse(True) #if I set this, then middle mouse drag would not work for magic mouse. see myPygletOrbitCamera for more details
# window.set_mouse_visible(False)
batch = pyglet.graphics.Batch()
key_states=key.KeyStateHandler()
window.push_handlers(key_states)
    
vertex_source = """#version 330 core
in vec3 aPos;
in vec2 tex_coords;
out vec2 texture_coords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;


void main()
{
    gl_Position =  projection * view * model * vec4(aPos, 1.0f);
    texture_coords = tex_coords;
}
"""

fragment_source = """#version 330 core

in vec2 texture_coords;

out vec4 fragColor;

uniform sampler2D texture0;
uniform sampler2D texture1;

void main()
{
    fragColor = mix(texture(texture0, texture_coords),
        texture(texture1, texture_coords), 0.2f);
}
"""
    
vertex_shader = Shader(vertex_source, 'vertex')
fragment_shader = Shader(fragment_source, 'fragment')
shader_program = ShaderProgram(vertex_shader, fragment_shader)

glEnable(GL_DEPTH_TEST)

# texture
tex0 = pyglet.resource.texture('container.jpg')
tex1 = pyglet.resource.texture('awesomeface.png')

tex={"texture0": tex0,
     "texture1": tex1}
# keys must correspond to the texture variable names in the fragment shader

group = RenderGroup(tex, shader_program)

vlist_cube = shader_program.vertex_list(36,GL_TRIANGLES,
                                 batch=batch,
             group=group,
             aPos=('f', (-0.5, -0.5, -0.5,
                          0.5, -0.5, -0.5,
                          0.5,  0.5, -0.5,
                          0.5,  0.5, -0.5,
                         -0.5,  0.5, -0.5,
                         -0.5, -0.5, -0.5,
                                          
                         -0.5, -0.5,  0.5,
                          0.5, -0.5,  0.5,
                          0.5,  0.5,  0.5,
                          0.5,  0.5,  0.5,
                         -0.5,  0.5,  0.5,
                         -0.5, -0.5,  0.5,
                                          
                         -0.5,  0.5,  0.5,
                         -0.5,  0.5, -0.5,
                         -0.5, -0.5, -0.5,
                         -0.5, -0.5, -0.5,
                         -0.5, -0.5,  0.5,
                         -0.5,  0.5,  0.5,
                                          
                          0.5,  0.5,  0.5,
                          0.5,  0.5, -0.5,
                          0.5, -0.5, -0.5,
                          0.5, -0.5, -0.5,
                          0.5, -0.5,  0.5,
                          0.5,  0.5,  0.5,
                                          
                         -0.5, -0.5, -0.5,
                          0.5, -0.5, -0.5,
                          0.5, -0.5,  0.5,
                          0.5, -0.5,  0.5,
                         -0.5, -0.5,  0.5,
                         -0.5, -0.5, -0.5,
                                          
                         -0.5,  0.5, -0.5,
                          0.5,  0.5, -0.5,
                          0.5,  0.5,  0.5,
                          0.5,  0.5,  0.5,
                         -0.5,  0.5,  0.5,
                         -0.5,  0.5, -0.5,
                         )),
             tex_coords=('f', (0.0, 0.0,
                               1.0, 0.0,
                               1.0, 1.0,
                               1.0, 1.0,
                               0.0, 1.0,
                               0.0, 0.0,                                                                         
                               0.0, 0.0,
                               1.0, 0.0,
                               1.0, 1.0,
                               1.0, 1.0,
                               0.0, 1.0,
                               0.0, 0.0,
                                        
                               1.0, 0.0,
                               1.0, 1.0,
                               0.0, 1.0,
                               0.0, 1.0,
                               0.0, 0.0,
                               1.0, 0.0,
                                        
                               1.0, 0.0,
                               1.0, 1.0,
                               0.0, 1.0,
                               0.0, 1.0,
                               0.0, 0.0,
                               1.0, 0.0,
                                        
                               0.0, 1.0,
                               1.0, 1.0,
                               1.0, 0.0,
                               1.0, 0.0,
                               0.0, 0.0,
                               0.0, 1.0,
                                        
                               0.0, 1.0,
                               1.0, 1.0,
                               1.0, 0.0,
                               1.0, 0.0,
                               0.0, 0.0,
                               0.0, 1.0,
                               )))


# tex_coords goes
# 3 2
# 0 1
# should just try listing vertices according to this order.

cubePositions = [
    Vec3( 0.0,  0.0,  0.0),
    # Vec3( 0.2,  0.0,  0.1), 
    Vec3( 2.0,  5.0, -15.0), 
    Vec3(-1.5, -2.2, -2.5),  
    Vec3(-3.8, -2.0, -12.3),  
    Vec3( 2.4, -0.4, -3.5),  
    Vec3(-1.7,  3.0, -7.5),  
    Vec3( 1.3, -2.0, -2.5),  
    Vec3( 1.5,  2.0, -2.5), 
    Vec3( 1.5,  0.2, -1.5), 
    Vec3(-1.3,  1.0, -1.5)  
]

window.push_handlers(on_mouse_scroll=camera_on_mouse_scroll,
                     on_mouse_drag=camera_on_mouse_drag,
                     on_mouse_press=camera_on_mouse_press,
                     on_key_press=camera_on_key_press,
                     on_key_release=camera_on_key_release
)

def update(dt):
    mats=camera_update(dt,window_aspect_ratio,key_states)
    shader_program["projection"]=mats["projection"]
    shader_program["view"]=mats["view"]
    
pyglet.clock.schedule_interval(update, timeStep)

    
@window.event    
def on_draw():
    window.clear()
    for i, pos in enumerate(cubePositions):
        model = Mat4().translate(pos).rotate(radians(20.0*i), Vec3(1.0,0.3,0.5).normalize())
        shader_program["model"]=model
        batch.draw()

    
pyglet.app.run()

