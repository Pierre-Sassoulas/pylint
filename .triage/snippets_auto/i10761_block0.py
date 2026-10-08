from pyglet.gl import glEnable, GL_CULL_FACE

def problem_code():
    glEnable(GL_CULL_FACE)
    print("This line is unreachable apparently!")
