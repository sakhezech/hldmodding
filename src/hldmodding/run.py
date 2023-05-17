from hldmodding.hooks import Hook, Patch
from hldmodding.mini_controllers import MiniController
from hldmodding.predef import on
from hldlib import find_path, default_load


def run():
    path_to_hld = find_path()
    
    # TODO: TURN THIS INTO A SEPARATE VALIDATE FUNC
    hooks = [hook for hook in Hook.__subclasses__() if hook._pending]
    patches = [patch for patch in Patch.__subclasses__() if patch._pending]
    
    for hook in hooks:
        if True:  # TODO: CHECK IF MOD IS ENABLED
            hook._subscribed = hook._pending
    for patch in patches:
        if True:  # TODO: CHECK IF MOD IS ENABLED
            patch._subscribed = patch._pending

    # TODO: UN HARDCODE PATCHES
    # patches
    on.patch.pre.fire(path_to_hld)

    if on.patch.levels._subscribed:
        levels = default_load(path_to_hld)
        on.patch.levels.fire(levels)
        levels.dump_all(path_to_hld)

    on.patch.textures.fire(path_to_hld)

    on.patch.post.fire(path_to_hld)

    input('Patches done. You can start the game')
    # hooks
    used_hooks = [hook for hook in Hook.__subclasses__() if hook._subscribed]
    
    # init watchers
    mini_controllers = [mini for mini in MiniController.__subclasses__()]
    for mini in mini_controllers: mini.init()

    # start cycle 
    # TODO: RATE LIMIT THE LOOP
    while True:
        for mini in mini_controllers: mini.update()
        for hook in used_hooks: hook.dependency()