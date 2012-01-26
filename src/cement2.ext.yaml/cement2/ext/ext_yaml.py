"""
This module provides any dynamically loadable code for the YAML 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_yaml.
    
"""

from cement2.core import handler, hook
from cement2.lib.ext_yaml import YamlOutputHandler

handler.register(YamlOutputHandler)

@hook.register()
def cement_post_setup_hook(app):
    """
    Adds the '--yaml' argument to the argument object.
    
    """
    app.args.add_argument('--yaml', dest='output_handler', 
        action='store_const', help='toggle yaml output handler', const='yaml')