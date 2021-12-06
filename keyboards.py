import os

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from dotenv import load_dotenv


load_dotenv()

zones_kb = ReplyKeyboardMarkup(resize_keyboard=True)
zones = os.environ.get("ZONES").split(";")
for zone in zones:
    zones_kb.add(KeyboardButton('/z ' + zone))

position_kb = ReplyKeyboardMarkup(resize_keyboard=True)
positions = os.environ.get("POSITIONS").split(";")
for position in positions:
    position_kb.add(KeyboardButton('/p ' + position))

blank_kb = ReplyKeyboardRemove()
