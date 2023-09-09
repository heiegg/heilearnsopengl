import pyglet
from pyglet.gl import *
from pyglet.graphics import Group
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.math import *
from math import * 

from RenderGroup import *

win_w=800
win_h=600
timeStep=1/120

window = pyglet.window.Window(win_w,win_h)
batch = pyglet.graphics.Batch()
    
vertex_source = """#version 330 core
in vec3 aPos;
in vec3 tex_coords;
out vec3 texture_coords;

void main()
{
    gl_Position =  vec4(aPos, 1.0f);
    texture_coords = tex_coords;
}
"""

fragment_source = """#version 330 core

in vec3 texture_coords;

out vec4 fragColor;

uniform sampler2D texture0;
uniform sampler2D texture1;

void main()
{
    fragColor = mix(texture(texture0, texture_coords.xy),
        texture(texture1, texture_coords.xy), 0.2f);
}
"""
# regarding uniform sampler2D ourTexture.
# we do not need to assign to it, if we use only one texture.
# we can use multiple textures. there is a limit to the number of textures.

vertex_shader = Shader(vertex_source, 'vertex')
fragment_shader = Shader(fragment_source, 'fragment')
program = ShaderProgram(vertex_shader, fragment_shader)

# texture
tex0 = pyglet.resource.texture('container.jpg')
tex1 = pyglet.resource.texture('awesomeface.png')
# print(f"{tex0.tex_coords}") # get (0, 0, 0,   1, 0, 0,   1, 1, 0,   0, 1, 0)
# What good is there to have texture coordinates vectors of length 3?
# right now, I don't see.
# with pyglet there is no need to flip the image upside down.

tex={"texture0": tex0,
     "texture1": tex1}

group = RenderGroup(tex, program)

vlist_rectangle = program.vertex_list_indexed(4,GL_TRIANGLES,
                                              indices=[0,1,3,1,2,3],
                                              batch=batch,
                                              group=group,
                                              aPos=('f', (-0.5,-0.5,0.0,
                                                          0.5,-0.5,0.0,
                                                          0.5,0.5,0.0,
                                                          -0.5,0.5,0.0)),
                                              tex_coords=('f', tex0.tex_coords))
# tex_coords goes
# 3 2
# 0 1
# so listing vertices according to this order.
# if you want to make one triangle one texture and the other some other texture
# probably you just have to list the vertices twice and assign the correct texture coords.
# then just use vertex_list instead of vertex_list_indexed.

@window.event    
def on_draw():
    window.clear()
    batch.draw()

    
pyglet.app.run()

