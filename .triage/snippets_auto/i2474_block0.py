[chaen@notANamespace]$ cat useModule.py 
from module.myClass import MyClass
MyClass()
[chaen@notANamespace]$ cat module/__init__.py 
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__ + '.impl')
[chaen@notANamespace]$ cat module/impl/myClass.py 
class MyClass(object):
  def __init__(self):
    print "Hello PyLint"
