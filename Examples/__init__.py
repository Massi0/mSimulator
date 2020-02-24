

from Modules import *


import importlib

to_import = ["CollisionAvoidance_PathFollowing","Unicycle"]


thismodule = sys.modules[__name__]

for module in to_import:
#    set_trace()
    mod = importlib.import_module(".{}".format(module),"Examples")
    setattr(thismodule,module,getattr(mod,module))