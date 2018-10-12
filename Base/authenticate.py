from .Base import Base
import  os


class two_legged_access(Base):
    def __init__(self):
        super(two_legged_access,self).__init__()
        self.header = {'Content-Type': 'application/x-www-form-urlencoded',}
        self.method = 'post'
        self.data = [
            ('client_id', 'GhE6ZN7eEjIhtid6ELjUAeoqWEbYAnjR'),
            ('client_secret', 'r2dzHcpXmspSwAlR'),
            ('grant_type', 'client_credentials'),
            ('scope', 'data:read data:write viewables:read bucket:create bucket:read')
            # ('scope', 'bucket:create bucket:read')
        ]

        self.url = 'https://developer.api.autodesk.com/authentication/v1/authenticate'
        self.filepath = os.getcwd()
        self.filename = self.filepath + '/Tem/tem.txt'

    def get_access_token(self):
        return  'Bearer '+self.GetItem('access_token')
    def get_token_type(self):
        return  self.GetItem('access_token')

    def get_expires_in(self):
        return self.GetItem('expires_in')

    def save_access_token(self):

        with open(self.filename,'w') as f:
            f.writelines(str(self.get_access_token()))

    def get_access_token_fromfile(self):
        with open(self.filename, 'r') as f:
            accesstoken = f.readline()
        return accesstoken



class authenticate:
    def __init__(self):
        self.two_legged_access=two_legged_access()
    @property
    def get_access_token(self):
        self.two_legged_access.save_access_token()

        return  self.two_legged_access.get_access_token()
    def get_access_token_fromfile(self):

        return  self.two_legged_access.get_access_token_fromfile()

    def Three_legged_access(self):
        pass