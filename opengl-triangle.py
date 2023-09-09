# produces a green triangle whose and the shade of green changes with respect to time

import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import *
import time
import math

win_w=800
win_h=600
timeStep=1/120
initTime=time.time()

# making a window is easy. Can I use it with other libraries, like matplotlib?
# I think the answer is yes. https://matplotlib.org/stable/users/explain/backends.html

window = pyglet.window.Window(win_w,win_h)
batch = pyglet.graphics.Batch()
    
vertex_source = """#version 330 core
in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0);
}
"""
# note: name must match. I use aPos here, later my vlist will have the attribute aPos

fragment_source = """#version 330 core

out vec4 fragColor;

uniform vec4 ourColor;

void main()
{
    fragColor = ourColor;
}
"""

vertex_shader = Shader(vertex_source, 'vertex')
fragment_shader = Shader(fragment_source, 'fragment')
shader_program = ShaderProgram(vertex_shader, fragment_shader)

vlist = shader_program.vertex_list(3,GL_TRIANGLES,batch=batch)
vlist.aPos[:]=( -0.5,-0.5,0.0,
                0.5,-0.5,0.0,
                0.0,0.5,0.0 )


@window.event    
def on_draw():
    window.clear()
    batch.draw()


def updateColor(dt):
    # I don't know how else to get the time since app is running.
    timeElapsed = time.time() - initTime
    greenValue = math.sin(timeElapsed) / 2.0 + 0.5
    shader_program['ourColor']=Vec4(0.0, greenValue, 0.0, 1.0)
    
pyglet.clock.schedule_interval(updateColor, timeStep)
pyglet.app.run()

