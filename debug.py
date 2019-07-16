# This file can be used to execute the pipeline from the blender scripting UI
import os
import bpy
import sys
import importlib

# Make sure the current script directory is in PATH, so we can load other python modules
dir = os.path.dirname(bpy.context.space_data.text.filepath)

if not dir in sys.path:
    sys.path.append(dir)

# Reload all models inside src/, as they are cached inside blender
for module in sys.modules.keys():
    if module.startswith("src"):
        print(module)
        importlib.reload(sys.modules[module])

working_dir = bpy.context.space_data.text.filepath

from src.main.Pipeline import Pipeline

config_path = "config/debug.json"

# Focus the 3D View, this is necessary to make undo work (otherwise undo will focus on the scripting area)
for window in bpy.context.window_manager.windows:
    screen = window.screen

    for area in screen.areas:
        if area.type == 'VIEW_3D':
            override = {'window': window, 'screen': screen, 'area': area}
            bpy.ops.screen.screen_full_area(override)
            break

try:
    pipeline = Pipeline(config_path, argv[1:], working_dir)
    pipeline.run()
finally:
    # Revert back to previous view
    bpy.ops.screen.back_to_previous()