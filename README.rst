
hoppy
==============

.. _Hoptoad: http://hoptoadapp.com/
.. _Python: http://python.org/
.. _restkit: http://benoitc.github.com/restkit/

hoppy is a Python library for accessing the Hoptoad_ API.


Requirements
------------

hoppy requires:

* Python_ 2.6
* restkit_ >= 2.1.1
* A Hoptoad_ account


Development Requirements
------------

.. _nosetests: http://somethingaboutorange.com/mrl/projects/nose/0.11.2/
.. _mockito-python: http://code.google.com/p/mockito-python/

The hoppy test suite requires:

* nosetests_ >= 0.11.2
* mockito-python_ >= 0.6.10


Installation
------------

hoppy is available on PyPi, and the recommended method of installation is pip::
    
    pip install hoppy


Usage
-----

Use hoppy to notify Hoptoad of an app deploy::

    import hoppy.api
    hoppy.api.api_key = '<project API key>'
    hoppy.api.Deploy().deploy('PRODUCTION', scm_revision='1a6a445',
            scm_repository='http://github.com/peplin/hoppy')

Use hoppy to retreive a specific error::

    import hoppy.api
    hoppy.api.account = '<your account name>'
    hoppy.api.auth_token = '<your personal API auth token>'
    print hoppy.api.Error().find(2035230)
