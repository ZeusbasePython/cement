"""
Cement core handler module.

"""

import re
from cement2.core import exc, backend

Log = backend.minimal_logger(__name__)

def get(handler_type, handler_label, *args):
    """
    Get a handler object.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
        
        handler_label
            The label of the handler (i.e. 'json')
            
    Optional Arguments:
    
        fallback
            A fallback value to return if handler_label doesn't exist.
            
    Usage:
    
        from cement2.core import handler
        output = handler.get('output', 'json')
        output.render(dict(foo='bar'))

    """
    if handler_type not in backend.handlers:
        raise exc.CementRuntimeError("handler type '%s' does not exist!" % \
                                     handler_type)

    if handler_label in backend.handlers[handler_type]:
        return backend.handlers[handler_type][handler_label]
    elif len(args) > 0:
        return args[0]
    else:
        raise exc.CementRuntimeError("handlers['%s']['%s'] does not exist!" % \
                                    (handler_type, handler_label))
    
def list(handler_type):
    """
    Return a list of handlers for a given type.
    
    Required Arguments:
    
        handler_type
            The type of handler (i.e. 'output')
    
    """
    res = []
    for label in backend.handlers[handler_type]:
        if label == '__interface__':
            continue
        res.append(backend.handlers[handler_type][label])
    return res
        
def defined(handler_type):
    """
    Test whether a handler type is defined.
    
    Required Arguments:
    
        handler_type
            The name or 'type' of the handler (I.e. 'logging').
    
    Returns: bool
    
    """
    if handler_type in backend.handlers:
        return True
    else:
        return False
        
def define(interface):
    """
    Define a handler based on the provided interface.  Defines a handler type
    based on <interface>.IMeta.label.
    
    Required arguments:

        interface
            The handler interface class that defines the interface to be 
            implemented.
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import handler

        handler.define(IDatabaseHandler)
    
    """
    
    ### FIX ME: Remove before Cement2 stable release
    if hasattr(interface, 'imeta'):
        interface.IMeta = interface.imeta
        print("CementDeprecationWarning -> Interface.imeta is deprecated.  Use 'IMeta' instead.")
        
        
    if not hasattr(interface, 'IMeta'):
        raise exc.CementInterfaceError("Invalid %s, " % interface + \
                                       "missing 'IMeta' class.")  
    if not hasattr(interface.IMeta, 'label'):
        raise exc.CementInterfaceError("Invalid %s, " % interface + \
                                       "missing 'IMeta.label' class.")  
                                       
    Log.debug("defining handler type '%s' (%s)" % \
        (interface.IMeta.label, interface.__name__))
                                                                              
    if interface.IMeta.label in backend.handlers:
        raise exc.CementRuntimeError("Handler type '%s' already defined!" % \
                                     interface.IMeta.label)
    backend.handlers[interface.IMeta.label] = {'__interface__' : interface}
    
def register(obj):
    """
    Register a handler object to a handler.  If the same object is already
    registered then no exception is raised, however if a different object
    attempts to be registered to the same name a CementRuntimeError is 
    raised.
    
    Required Options:
    
        obj
            The handler object to register
    
    Usage:
    
    .. code-block:: python
    
        from cement2.core import handler
        
        class MyDatabaseHandler(object):
            class Meta:
                interface = IDatabase
                label = 'mysql'
            
            def connect(self):
            ...
            
        handler.register(MyDatabaseHandler)
    
    """
    
    ### FIX ME: Remove before Cement2 stable release
    if hasattr(obj, 'meta'):
        obj.Meta = obj.meta
        print("CementDeprecationWarning -> Handler.meta is deprecated.  Use 'Meta' instead.")
        
    # This is redundant with the validator, but if we don't check for them
    # then we'll get an uncontrolled exception.
    if not hasattr(obj, 'Meta'):
        raise exc.CementInterfaceError("Invalid handler %s, " % obj + \
                                       "missing 'Meta' class.")  
    if not hasattr(obj.Meta, 'label'):
        raise exc.CementInterfaceError("Invalid handler %s, " % obj + \
                                       "missing 'Meta.label'.")
    if not hasattr(obj.Meta, 'interface'):
        raise exc.CementInterfaceError("Invalid handler %s, " % obj + \
                                       "missing 'Meta.interface'.")

    # translate dashes to underscores
    obj.Meta.label = re.sub('-', '_', obj.Meta.label)
    
    handler_type = obj.Meta.interface.IMeta.label
    Log.debug("registering handler '%s' into handlers['%s']['%s']" % \
             (obj, handler_type, obj.Meta.label))
             
    if handler_type not in backend.handlers:
        raise exc.CementRuntimeError("Handler type '%s' doesn't exist." % \
                                     handler_type)                     
    if obj.Meta.label in backend.handlers[handler_type] and \
        backend.handlers[handler_type][obj.Meta.label] != obj:
        raise exc.CementRuntimeError("handlers['%s']['%s'] already exists" % \
                                (handler_type, obj.Meta.label))

    interface = backend.handlers[handler_type]['__interface__']
    if hasattr(interface.IMeta, 'validator'):
        interface.IMeta().validator(obj)
    else:
        Log.debug("Interface '%s' does not have a validator() function!" % \
                 interface)
        
    backend.handlers[handler_type][obj.Meta.label] = obj
   
def enabled(handler_type, handler_label):
    """
    Check if a handler is enabled.
    
    Required Arguments:
    
        handler_type
            The type of handler
            
        handler_label
            The label of the handler
          
    Returns: Boolean
    
    """
    if handler_type in backend.handlers and \
       handler_label in backend.handlers[handler_type]:
        return True

    return False