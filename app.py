from flask import Flask;from flask_ipban import IpBan;from flask_limiter import Limiter;from flask_limiter.util import get_remote_address
from blueprint.main import main
from socket import gethostname
from os import getcwd, path
from yaml import safe_load
import logging, secrets

def loadConfig():
    PATH = (getcwd()+'/config.yaml')
    if path.isfile(PATH):
        with open(PATH,'r+') as config:
            return safe_load(config)
    else:
        print('[err] config.yaml not found!')
        return None
def GenerateRandomToken(length=30):
     return secrets.token_urlsafe(length)


config = loadConfig()
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['HOST_NAME'] = config['HOST_NAME']
app.config['SESSION_COOKIE_DOMAIN'] = False
app.secret_key = GenerateRandomToken()
app.register_blueprint(main)


logging.basicConfig(filename='logs.log',
                    level=logging.DEBUG,
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


ip_ban = IpBan(ban_seconds=(config['IpBan']))
ip_ban.init_app(app)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=config['default_limits']
)

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(debug=True)