from flask import Blueprint

bp = Blueprint('main', __name__)

from MudMasterUI.main import routes
from MudMasterUI.main import routes_calibration
from MudMasterUI.main import routes_measure