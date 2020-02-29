from flask import Flask
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__, template_folder="templates", static_folder="static")
from urls import routes
routes.add_routes(app)