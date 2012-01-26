"""
This module provides any dynamically loadable code for the ConfigParser 
Framework Extension such as hook and handler registration.  Additional 
classes and functions exist in cement2.lib.ext_configparser.
    
"""

from cement2.core import handler
from cement2.lib.ext_configparser import ConfigParserConfigHandler

handler.register(ConfigParserConfigHandler)