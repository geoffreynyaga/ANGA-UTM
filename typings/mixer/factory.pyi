"""
This type stub file was generated by pyright.
"""

from . import _compat as _

""" Mixer factories. """
class GenFactoryMeta(type):
    """ Precache generators. """
    def __new__(mcs, name, bases, params):
        ...
    


class GenFactory(_.with_metaclass(GenFactoryMeta)):
    """ Make generators for types. """
    generators = ...
    fakers = ...
    types = ...
    @classmethod
    def cls_to_simple(cls, fcls):
        """ Translate class to one of simple base types.

        :return type: A simple type for generation

        """
        ...
    
    @staticmethod
    def name_to_simple(fname):
        """ Translate name to one of simple base names.

        :return str:

        """
        ...
    
    @classmethod
    def get_fabric(cls, fcls, fname=..., fake=...):
        """ Make a objects fabric  based on class and name.

        :return function:

        """
        ...
    


