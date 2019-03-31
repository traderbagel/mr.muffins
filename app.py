from flask import Flask, request, abort, send_file
import json
import requests
import muffins

muffins.logger.init()
app = muffins.create_app()
