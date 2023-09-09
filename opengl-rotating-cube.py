# shows a cube that is spinning.
# uses many coordinate transforms
# local coords --model--> world coords --view--> coords adapted to camera/view --projection-->
# this space can essentially be thought of as 2d ----> linearly mapped to the screen? window? space

import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import *
from math import *
import time

from RenderGroup import *


win_w=800
win_h=600
timeStep=1/120
initTime=time.time()

window = pyglet.window.Window(win_w,win_h)
batch = pyglet.graphics.Batch()
    
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
program = ShaderProgram(vertex_shader, fragment_shader)

glEnable(GL_DEPTH_TEST)

# texture
tex0 = pyglet.resource.texture('container.jpg')
tex1 = pyglet.resource.texture('awesomeface.png')

tex={"texture0": tex0,
     "texture1": tex1}

group = RenderGroup(tex, program)

vlist_cube = program.vertex_list(36,GL_TRIANGLES,
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


@window.event    
def on_draw():
    window.clear()
    batch.draw()

    

def update(dt):
    t = (time.time() - initTime)

    # transformation matrices
    
    model = Mat4().rotate(t ,Vec3(0.5,1.0,0).normalize()) # important: normalise
    # it seems that rotation with respect to an axis follows the right-hand rule
    view = Mat4().translate((0,0,-3))
    projection = Mat4.perspective_projection(win_w/win_h, 0.1, 100.0, fov=45) # fov is in degrees. Note: different from convention of glm.
    program["model"]=model
    program["view"]=view
    program["projection"]=projection

pyglet.clock.schedule_interval(update, timeStep)
    
pyglet.app.run()

