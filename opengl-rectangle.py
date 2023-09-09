# produces an orange rectangle

import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram

win_w=800
win_h=600

window = pyglet.window.Window(win_w,win_h)
batch = pyglet.graphics.Batch()
    
vertex_source = """#version 330 core
in vec3 aPos;

void main()
{
    gl_Position = vec4(aPos, 1.0f);
}
"""
# note: name must match. I use aPos here, later my vlist will have the attribute aPos

fragment_source = """#version 330 core

out vec4 fragColor;

void main()
{
    fragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}
"""

vertex_shader = Shader(vertex_source, 'vertex')
fragment_shader = Shader(fragment_source, 'fragment')
program = ShaderProgram(vertex_shader, fragment_shader)

# using vertex list indexed
# give 4 vertices and say which ones form a triangle
vlist_rectangle = program.vertex_list_indexed(4,GL_TRIANGLES,
                                              indices=[0,1,3,1,2,3],
                                              batch=batch,
                                              aPos=('f', (0.5,0.5,0.0,
                                                    0.5,-0.5,0.0,
                                                    -0.5,-0.5,0.0,
                                                    -0.5,0.5,0.0)))

@window.event    
def on_draw():
    window.clear()
    batch.draw()

pyglet.app.run()

