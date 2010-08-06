from xml.dom.minidom import parseString
from restkit import Resource

account = None
auth_token = None
api_key = None

class HoptoadError(Exception): pass


class HoptoadResource(Resource):
    def __init__(self, use_ssl=False):
        self.auth_token = auth_token
        self.account = account
        self.host = self.base_uri(use_ssl)
        super(HoptoadResource, self).__init__(self.host, follow_redirect=True)
        self.check_configuration()

    def base_uri(self, use_ssl=False):
        base = 'http://%s.hoptoadapp.com' % self.account
        base = base.replace('http://', 'https://') if use_ssl else base
        return base

    def check_configuration(self):
        if not self.auth_token:
            raise HoptoadError('API Token cannot be blank')
        if not self.account:
            raise HoptoadError('Account cannot be blank')

    def request(self, *args, **kwargs):
        response = super(HoptoadResource, self).request(
                auth_token=self.auth_token, *args, **kwargs)
        return parseString(response.body_string())


class Error(HoptoadResource):
    def find(self, error_id):
        return self.get(self._error_path(error_id))

    @staticmethod
    def _error_path(error_id):
        return 'errors/%d.xml' % error_id


class Notice(HoptoadResource):
    def find(self, notice_id, error_id):
        return self.get(self._notice_path(notice_id, error_id))
    
    @staticmethod
    def _notice_path(notice_id, error_id):
        return 'errors/%(error_id)d/notices/%(notice_id)d.xml' % locals()


class Deploy(Resource):
    def __init__(self, use_ssl=False):
        self.api_key = api_key
        self.host = self.base_uri(use_ssl)
        super(Deploy, self).__init__(self.host, follow_redirect=True)
        self.check_configuration()

    def check_configuration(self):
        if not self.api_key:
            raise HoptoadError('API Key cannot be blank')

    def request(self, *args, **kwargs):
        response = super(Deploy, self).request(
                api_key=self.api_key, *args, **kwargs)
        return response.body_string()

    def base_uri(self, use_ssl=False):
        base = 'http://hoptoadapp.com/deploys.txt'
        base = base.replace('http://', 'https://') if use_ssl else base
        return base

    def deploy(self, env, **kwargs):
        """ Optional parameters accepted by Hoptoad are:
        scm_revision
        scm_repository
        local_username
        """

        params = {}
        params['deploy[rails_env]'] = env
        for key, value in kwargs:
            params['deploy[%s]' % key] = value

        return self.post(**params)
