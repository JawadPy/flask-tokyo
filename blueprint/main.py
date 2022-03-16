from flask import Blueprint, render_template
from yaml import safe_load
from os import getcwd, path
from markupsafe import escape

def loadConfig():
    PATH = (getcwd() +'/config.yaml')
    if path.isfile(PATH):
        with open(PATH,'r+') as config:
            return safe_load(config)
    else:
        print('[err] config.yaml not found!')
        return None

config = loadConfig()
main = Blueprint('main', __name__)

@main.route('/')
def main_():
    return render_template('index.html', data=config)
