from flask import Blueprint

bp = Blueprint('Teltonika', __name__)

from MudMasterUI.Teltonika import routes