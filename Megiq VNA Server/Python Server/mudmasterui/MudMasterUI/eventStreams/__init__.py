from flask import Blueprint

bp = Blueprint('eventStreams', __name__)

from MudMasterUI.eventStreams import routes