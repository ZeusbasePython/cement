"""
Cement core interface module.

"""

from cement2.core import exc

class Interface(object):
    def __init__(self):
        """
        An interface definition class.  All Interfaces should subclass from
        here.  Note that this is not an implementation and should never be
        used directly.
        """
        raise exc.CementInterfaceError("Interfaces can not be used directly.")
            
class Attribute(object):
    def __init__(self, description):
        """
        An interface attribute definition.
        
        Required Arguments:
        
            description
                The description of the attribute.
                
        """
        self.description = description
    
    def __repr__(self):
        return "<interface.Attribute - '%s'>" % self.description
        
def validate(interface, obj, members, **kw):
    """
    A wrapper to validate interfaces.
    
    Required Arguments:
    
        interface
            The interface class to validate against
            
        obj
            The object to validate.
            
        members
            The object members that must exist.
            
    Optional Arguments:
    
        Meta
            A list of members to validate in the handler classes Meta class.
            Defaults to ['interface', 'label'].
            
    """
    invalid = []
    Meta = kw.get('Meta', ['interface', 'label'])

    if hasattr(obj, 'Meta') and interface != obj.Meta.interface:
        raise exc.CementInterfaceError("%s does not implement '%s'." % \
                                      (obj, interface))
        
    for member in members:
        if not hasattr(obj, member):
            invalid.append(member)
    
    if not hasattr(obj, 'Meta'):
        invalid.append("Meta")
    else:
        for member in Meta:
            if not hasattr(obj.Meta, member):
                invalid.append("Meta.%s" % member)
            
    if invalid:
        raise exc.CementInterfaceError("Invalid or missing: %s in %s" % \
                                      (invalid, obj))