from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.PrinterNames import PrinterNames

buttons_row1 = []

buttons_row2 = []

for i in range(0, len(PrinterNames), 2):
    buttons_row1.append(InlineKeyboardButton(text=PrinterNames[i], callback_data=PrinterNames[i]))
for i in range(1, len(PrinterNames), 2):
    buttons_row2.append(InlineKeyboardButton(text=PrinterNames[i], callback_data=PrinterNames[i]))

ikb_printer_menu = InlineKeyboardMarkup(row_width=2, inline_keyboard=[buttons_row1, buttons_row2])