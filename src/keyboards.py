from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from config import start_cmd_message

start_agreement_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Погоджуюсь', callback_data='initial_agreement')
]])
