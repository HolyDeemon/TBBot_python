from aiogram import types
from  aiogram.types import KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_name_phone = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Отправить имя пользователя и телефон", request_contact=True)]])
keyboard_phone = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[KeyboardButton(text="Отправить телефон", request_contact=True)]])

ikb_skip = InlineKeyboardMarkup(row_width=1, inline_keyboard=[[InlineKeyboardButton(text="Пропустить комментарий", callback_data="description_skip")]])

ikb_change = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [InlineKeyboardButton(text="Имя", callback_data="ChName")],
    [InlineKeyboardButton(text="Телефон", callback_data="ChTel"), InlineKeyboardButton(text="Email", callback_data="ChEmail")],
    [InlineKeyboardButton(text="Комментарий", callback_data="ChDescription")],
    [InlineKeyboardButton(text="Завершить заказ", callback_data="SendOrder")]
])

ikb_back = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [InlineKeyboardButton(text="Вернуться к оформлению", callback_data="EndOrder")]
])
