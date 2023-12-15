from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

from src.config import start_cmd_message

start_agreement_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Погоджуюсь', callback_data='initial_agreement')
]])

cancel_reg_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Так', callback_data='cancel_reg:1'),
    InlineKeyboardButton(text='Ні', callback_data='cancel_reg:0')
]])