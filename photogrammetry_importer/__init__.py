'''
Copyright (C) 2018 Sebastian Bullinger


Created by Sebastian Bullinger

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {
    "name": "Photogrammetry Import Export Addon",
    "description": "Allows to import and export photogrammetry results (cameras, points and meshes).",
    "author": "Sebastian Bullinger",
    "version": (2, 0, 0),
    "blender": (2, 80, 0),
    "location": "File / Import and File/Export",
    "warning": "",
    "wiki_url": "https://blender-addon-photogrammetry-importer.readthedocs.io/en/latest/installation.html",
    "tracker_url": "https://github.com/SBCV/Blender-Addon-Photogrammetry-Importer/issues",
    "category": "Import-Export" }

import bpy

# load and reload submodules
##################################

import importlib
from .utils import developer_utils
importlib.reload(developer_utils)
modules = developer_utils.setup_addon_modules(__path__, __name__, "bpy" in locals())

# The root dir is Blenders addon folder.
# Therefore, we need the "photogrammetry_importer" specifier for this addon
from photogrammetry_importer.blender_logging import log_report

from photogrammetry_importer.preferences.addon_preferences import PhotogrammetryImporterPreferences

from photogrammetry_importer.registration import register_importers
from photogrammetry_importer.registration import unregister_importers
from photogrammetry_importer.registration import register_exporters
from photogrammetry_importer.registration import unregister_exporters

from photogrammetry_importer.panel.opengl_panel import OpenGLPanel
from photogrammetry_importer.opengl.visualization_utils import redraw_points
bpy.app.handlers.load_post.append(redraw_points)

# =========================================================================
# === Uncomment for fast debugging ===
# from bpy.app.handlers import persistent
# @persistent
# def load_handler(dummy):
#     from photogrammetry_importer.file_handler.ply_file_handler import PLYFileHandler
#     from photogrammetry_importer.utils.visualization_utils import draw_points
#     points = PLYFileHandler.parse_ply_file('path/to/file.ply')

#     class LogOp():
#         def report(sef, arg1, arg2):
#             print(arg1, arg2)

#     log_op = LogOp()
#     draw_points(log_op, points)
# =========================================================================
# 

def register():
    bpy.utils.register_class(PhotogrammetryImporterPreferences)

    import_export_prefs = bpy.context.preferences.addons[__name__].preferences
    register_importers(import_export_prefs)
    register_exporters(import_export_prefs)

    bpy.utils.register_class(OpenGLPanel)

    # === Uncomment for fast debugging ===
    # bpy.app.handlers.load_post.append(load_handler)

    print("Registered {} with {} modules".format(bl_info["name"], len(modules)))

def unregister():
    bpy.utils.unregister_class(PhotogrammetryImporterPreferences)

    unregister_importers()
    unregister_exporters()

    bpy.utils.unregister_class(OpenGLPanel)

    print("Unregistered {}".format(bl_info["name"]))


if __name__ == '__main__':
    print('main called')
    
