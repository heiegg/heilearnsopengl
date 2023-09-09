import pyglet
from pyglet.gl import *
from pyglet.graphics.shader import Shader, ShaderProgram
from pyglet.graphics import Group

# copied from pyglet's examples with added annotation
#####################################################
# Define a custom `Group` to encapsulate OpenGL state
#####################################################
class RenderGroup(Group):
    """A Group that enables and binds Textures and ShaderProgram.

    RenderGroups are equal if their Textures and ShaderProgram
    are equal.
    """
    def __init__(self, textures, program, order=0, parent=None):
        """Create a RenderGroup.

        :Parameters:
            `texture` : a dictionary of textures `~pyglet.image.Texture`
                Textures to bind. 
            `program` : `~pyglet.graphics.shader.ShaderProgram`
                ShaderProgram to use.
            `order` : int
                Change the order to render above or below other Groups.
            `parent` : `~pyglet.graphics.Group`
                Parent group.
        """
        # textures example {"texture0": tex0, "texture1": tex1} where tex0, tex1 are texture objects.
        # make sure the keys have the same name as the uniforms in the fragment shader.
        self.textures = textures
        self.program = program
        texture = list(self.textures.values())[0]
        self.target = texture.target
        super().__init__(order, parent)

    def set_state(self):
        self.program.use()

        # this seems to depend on the implementation of dictionary, that it is ordered by
        # the order when it is constructed. It is OK:
        # https://docs.python.org/3/library/stdtypes.html#typesmapping
        # "Changed in version 3.7: Dictionary order is guaranteed to be insertion order."
        
        for idx, name in enumerate(self.textures):
            # set a uniform, which is a texture index, in the fragment shader
            # it seems it is important to set this first, before activating the texture
            self.program[name] = idx

        for i, texture in enumerate(self.textures.values()):
            glActiveTexture(GL_TEXTURE0 + i)
            # it is guarantee  that GL_TEXTURE1 = GL_TEXTURE0 +1 etc.
            glBindTexture(self.target, texture.id)
            
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)


    def unset_state(self):
        glDisable(GL_BLEND)
        self.program.stop()
        glActiveTexture(GL_TEXTURE0)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.texture}-{self.texture.id})'

    def __eq__(self, other):
        return (other.__class__ is self.__class__ and
                self.program is other.program and
                self.textures == other.textures)

    def __hash__(self):
        return hash((id(self.parent),
                     id(self.textures)))
