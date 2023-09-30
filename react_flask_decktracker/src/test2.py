import asyncio
import genshin
import json
from flask import *

app = Flask(__name__)


def test():
    return jsonify({5: 'test'})