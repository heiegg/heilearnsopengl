# a very colourful triangle.
# colour interpolation

import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import *

win_w=800
win_h=600
timeStep=1/120

window = pyglet.window.Window(win_w,win_h)
batch = pyglet.graphics.Batch()
    
vertex_source = """#version 330 core
in vec3 aPos;
in vec4 aColor;

out vec4 ourColor;

void main()
{
    gl_Position = vec4(aPos, 1.0f);
    ourColor = aColor;
}
"""

fragment_source = """#version 330 core

in vec4 ourColor;
out vec4 fragColor;

void main()
{
    fragColor = ourColor;
}
"""

vertex_shader = Shader(vertex_source, 'vertex')
fragment_shader = Shader(fragment_source, 'fragment')
program = ShaderProgram(vertex_shader, fragment_shader)

vlist = program.vertex_list(3,GL_TRIANGLES,batch=batch)
vlist.aPos[:]=( -0.5,-0.5,0.0,
                0.5,-0.5,0.0,
                0.0,0.5,0.0 )
# each vertex has a colour.
# the colour of points in the triangle is determined via interpolation.
vlist.aColor[:]=( 1.0, 0.0, 0.0,1.0, 
                  0.0, 1.0, 0.0,1.0,
                  0.0, 0.0, 1.0,1.0, )


@window.event    
def on_draw():
    window.clear()
    batch.draw()
    
pyglet.app.run()

