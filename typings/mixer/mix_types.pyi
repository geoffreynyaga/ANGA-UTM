"""
This type stub file was generated by pyright.
"""

""" Mixer types. """
class BigInteger:
    """ Type for big integers. """
    ...


class EmailString:
    """ Type for emails. """
    ...


class HostnameString:
    """ Type for hostnames. """
    ...


class IP4String:
    """ Type for IPv4 addresses. """
    ...


class IP6String:
    """ Type for IPv6 addresses. """
    ...


class IPString:
    """ Type for IPv4 and IPv6 addresses. """
    ...


class NullOrBoolean:
    """ Type for None or boolean values. """
    ...


class PositiveDecimal:
    """ Type for positive decimals. """
    ...


class PositiveInteger:
    """ Type for positive integers. """
    ...


class PositiveSmallInteger:
    """ Type for positive small integers. """
    ...


class SmallInteger:
    """ Type for small integers. """
    ...


class Text:
    """ Type for texts. """
    ...


class URL:
    """ Type for URLs. """
    ...


class UUID:
    """ Type for UUIDs. """
    ...


class Mix(object):
    """ Virtual link on the mixed object.

    ::

        mixer = Mixer()

        # here `mixer.MIX` points on a generated `User` instance
        user = mixer.blend(User, username=mixer.MIX.first_name)

        # here `mixer.MIX` points on a generated `Message.author` instance
        message = mixer.blend(Message, author__name=mixer.MIX.login)

        # Mixer mix can get a function
        message = mixer.blend(Message, title=mixer.MIX.author(
            lambda author: 'Author: %s' % author.name
        ))

    """
    def __init__(self, value=..., parent=...) -> None:
        ...
    
    def __getattr__(self, value):
        ...
    
    def __call__(self, func):
        ...
    
    def __and__(self, values):
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self):
        ...
    


class ServiceValue(object):
    """ Abstract class for mixer values. """
    def __init__(self, scheme=..., *choices, **params) -> None:
        ...
    
    @classmethod
    def __call__(cls, *args, **kwargs):
        ...
    
    def gen_value(self, type_mixer, name, field):
        """ Abstract method for value generation. """
        ...
    


class Field(ServiceValue):
    """ Set field values.

    By default the mixer generates random or fake a field values by types
    of them. But you can set some values by manual.

    ::

        # Generate a User model
        mixer.blend(User)

        # Generate with some values
        mixer.blend(User, name='John Connor')

    .. note:: Value may be a callable or instance of generator.

    ::

        # Value may be callable
        client = mixer.blend(Client, username=lambda:'callable_value')
        assert client.username == 'callable_value'

        # Value may be a generator
        clients = mixer.cycle(4).blend(
            Client, username=(name for name in ('Piter', 'John')))


    .. seealso:: :class:`mixer.main.Fake`, :class:`mixer.main.Random`,
                 :class:`mixer.main.Select`,
                 :meth:`mixer.main.Mixer.sequence`

    """
    def __init__(self, scheme, name, **params) -> None:
        ...
    
    def __deepcopy__(self, memo):
        ...
    
    def gen_value(self, type_mixer, name, field):
        """ Call :meth:`TypeMixer.gen_field`.

        :return value: A generated value

        """
        ...
    


class Fake(ServiceValue):
    """ Force a `fake` value.

    If you initialized a :class:`~mixer.main.Mixer` with `fake=False` you can
    force a `fake` value for field with this attribute (mixer.FAKE).

    ::

         mixer = Mixer(fake=False)
         user = mixer.blend(User)
         print user.name  # Some like: Fdjw4das

         user = mixer.blend(User, name=mixer.FAKE)
         print user.name  # Some like: Bob Marley

    You can setup a field type for generation of fake value: ::

         user = mixer.blend(User, score=mixer.FAKE(str))
         print user.score  # Some like: Bob Marley

    .. note:: This is also usefull on ORM model generation for filling a fields
              with default values (or null).

    ::

        from mixer.backend.django import mixer

        user = mixer.blend('auth.User', first_name=mixer.FAKE)
        print user.first_name  # Some like: John

    """
    def gen_value(self, type_mixer, name, fake):
        """ Call :meth:`TypeMixer.gen_fake`.

        :return value: A generated value

        """
        ...
    


class Random(ServiceValue):
    """ Force a `random` value.

    If you initialized a :class:`~mixer.main.Mixer` by default mixer try to
    fill fields with `fake` data. You can user `mixer.RANDOM` for prevent this
    behaviour for a custom fields.

    ::

         mixer = Mixer()
         user = mixer.blend(User)
         print user.name  # Some like: Bob Marley

         user = mixer.blend(User, name=mixer.RANDOM)
         print user.name  # Some like: Fdjw4das

    You can setup a field type for generation of fake value: ::

         user = mixer.blend(User, score=mixer.RANDOM(str))
         print user.score  # Some like: Fdjw4das

    Or you can get random value from choices: ::

        user = mixer.blend(User, name=mixer.RANDOM('john', 'mike'))
         print user.name  # mike or john

    .. note:: This is also useful on ORM model generation for randomize fields
              with default values (or null).

    ::

        from mixer.backend.django import mixer

        mixer.blend('auth.User', first_name=mixer.RANDOM)
        print user.first_name  # Some like: Fdjw4das

    """
    def __init__(self, scheme=..., *choices, **params) -> None:
        ...
    
    def gen_value(self, type_mixer, name, random):
        """ Call :meth:`TypeMixer.gen_random`.

        :return value: A generated value

        """
        ...
    


class Select(Random):
    """ Select values from database.

    When you generate some ORM models you can set value for related fields
    from database (select by random).

    Example for Django (select user from exists): ::

        from mixer.backend.django import mixer

        mixer.generate(Role, user=mixer.SELECT)


    You can setup a Django or SQLAlchemy filters with `mixer.SELECT`: ::

        from mixer.backend.django import mixer

        mixer.generate(Role, user=mixer.SELECT(
            username='test'
        ))

    """
    def gen_value(self, type_mixer, name, field):
        """ Call :meth:`TypeMixer.gen_random`.

        :return value: A generated value

        """
        ...
    


class _Deffered(object):
    """ A type which will be generated later. """
    def __init__(self, value, scheme=...) -> None:
        ...
    


