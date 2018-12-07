from flask import Flask
import sys
sys.path.append('./src')
from generator.bot import Bot

app = Flask(__name__)

bot = Bot()
