from .import models
from .api import API
from .utils import dispatchmethod


class Client(object):
    """ The Client class is the primary access point for the Testrail API

    The intended way to use this class is:

    .. code-block:: python

        import traw
        testrail = traw.Client(username='username',
                               user_api_key='api_key',
                               url='url')

    Authentication credentials will be pulled in the following order:
     - TRAW Client instantiation
       - traw.Client(username='<username>', user_api_key='<api_key>', url='<url>')
       - (optional) You may substitute `password` for `user_api_key`
     - Environmental variables
       - TRAW_USERNAME=<username>
       - TRAW_USER_API_KEY=<api_key>
       - TRAW_URL=<url>
       - (optional) You may substitude `TRAW_PASSWORD` for `TRAW_USER_API_KEY`
     - A configuration file in the user's home directory (~/.traw_config)
       - [TRAW]
         username = <username>
         user_api_key = <user_api_key>
         url = <url>
       - (optional) You may substitute `password = <password>` for `user_api_key`

    If both a user api key and a user password are provided, the api key will be used
    """
    def __init__(self, **credentials):
        """ Initialize the TRAW instance """
        self._api = API(**credentials)

    # POST generics
    @dispatchmethod
    def add(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def close(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def delete(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    @dispatchmethod
    def update(self, obj):
        # Not directly implemented. TypeError is raised if called directly
        pass  # pragma: no cover

    # Project related methods
    @dispatchmethod
    def project(self):
        """ Return a new Project instance """
        return models.Project(self)

    @project.register(int)
    def _project_by_id(self, project_id):
        """ Returns project with ``project_id`` """
        return models.Project(self, self._api.project_by_id(project_id))

    def projects(self, active_only=False, completed_only=False):
        """ Returns the generator of available projects

        Leaving both active_only and completed_only will return all projects

        :param active_only: Only include currently active projects in list
        :param completed_only: Only include completed projects in list

        :yields: Project Objects
        """
        if active_only is True and completed_only is True:
            raise TypeError('Either `active_only` or `completed_only` can be '
                            'set, but not both')

        elif active_only is True or completed_only is True:
            is_completed = 1 if completed_only else 0
        else:
            is_completed = None

        for project in self._api.projects(is_completed):
            yield models.Project(self, project)

    # User related methods
    @dispatchmethod
    def user(self):
        """ Return a new User instance """
        return models.User(self)

    @user.register(str)
    def user_by_email(self, email):
        """ Returns user associated with ``email`` """
        if '@' not in email:
            raise ValueError('"email" must be a string that includes an "@" sym')

        return models.User(self, self._api.user_by_email(email))

    @user.register(int)
    def user_by_id(self, user_id):
        """ Returns user with ``user_id`` """
        return models.User(self, self._api.user_by_id(user_id))

    def users(self):
        """ Returns the generator of available Users

        :yields: User Objects
        """
        for user in self._api.users():
            yield models.User(self, user)
