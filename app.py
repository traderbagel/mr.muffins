import os
from flask import Flask, request, abort, send_file
import json
import requests
import muffins

muffins.logger.init()
app = muffins.create_app()
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)