from pyglet.math import *

def scalarMult(scalar, vector):
    vec_fun=None
    if len(vector) == 3:
        vec_fun=Vec3
    elif len(vector) == 2:
        vec_fun=Vec2
    elif len(vector) == 4:
        vec_fun=Vec4

    return vec_fun(*(scalar*x for x in vector))

def rotate_vec3(vec, angle, axis):
    """rotate a Vec3 by angle in radian with respect to the given axis (Vec3)"""
    homog_vec=Vec4(vec.x, vec.y, vec.z, 1)
    rot=Mat4().rotate(-angle, axis.normalize()) # now I am confused about the direction
    result = rot @ homog_vec
    return Vec3(result.x/result.w, result.y/result.w, result.z/result.w)
