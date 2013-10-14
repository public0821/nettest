import gettext
import os

locale_path = os.path.realpath(os.path.dirname(__file__)) + '/locale'
gettext.install('nettest', locale_path)