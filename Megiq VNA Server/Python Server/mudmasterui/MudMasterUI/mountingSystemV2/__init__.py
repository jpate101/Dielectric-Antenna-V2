from flask import Blueprint

bp = Blueprint('mountingSystemV2', __name__)

from MudMasterUI.mountingSystemV2 import routes