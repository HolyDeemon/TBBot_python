import asyncio
import logging
import re
import json

import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from inlineMenus.PrinterInline import ikb_printer_menu
from  aiogram.types import CallbackQuery
from Keyboards import keyboard_name_phone, keyboard_phone, ikb_skip, ikb_change
from data.PrinterNames import PrinterNames
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="6898158089:AAHNLqSFDF8XkWSAl1D0qNhrqbck2lWAjrE")
# Диспетчер
dp = Dispatcher()

printernames = [
    "Helidorus",
    "Helidorus",
    "Helidorus",
    "Helidorus",
]

class OrderRequest:
    name =""
    email =""
    tel =""
    printername =""
    description =""

    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

state = ""
order = OrderRequest()

# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global state
    state = ""
    await message.answer("Выберите принтер:", reply_markup=ikb_printer_menu)

@dp.message()
async def handle_help(message: types.Message):
    global state
    global order
    if(state == "Name"):
        if(message.contact != None):
            order.tel = message.contact.phone_number
            order.name = message.contact.first_name + " " + message.contact.last_name
            state = "Email"
            await message.answer('Введите Email')
            return
        order.name = message.text
        state = "Tel"
        await message.answer('Введите номер телефона. Вы можете автоматически ввесит все контакты из Telegram, используя кнопку в меню', reply_markup=keyboard_phone)
    elif(state == "Tel"):
        if(message.contact != None):
            order.tel = message.contact.phone_number
            state = "Email"
            await message.answer('Введите Email')
            return
        if(checkPhone(message.text)):
            order.tel = message.text
            state = "Email"
            await message.answer('Введите Email')
        else:
            await message.answer('Пожалуйста, введите номер телефона', reply_markup=keyboard_phone)
    elif(state =="Email"):
        if(checkEmail(message.text)):
            order.email = message.text
            state = "Description"
            await message.answer('Можете ввести комментарий', reply_markup=ikb_skip)
    elif(state == "Description"):
        order.description = message.text
        state = "EndOrder"
        await message.answer(str(ReturnEndForm()), reply_markup=ikb_change)

    elif(state == "ChName"):
        if(message.contact != None):
            order.tel = message.contact.phone_number
            order.name = message.contact.first_name + " " + message.contact.last_name
            state = "EndOrder"
            await message.answer(ReturnEndForm(), reply_markup=ikb_change)
            return
        await message.answer(ReturnEndForm(), reply_markup=ikb_change)

    elif(state == "ChTel"):
        if(message.contact != None):
            order.tel = message.contact.phone_number
            state = "EndOrder"
            await message.answer(ReturnEndForm(), reply_markup=ikb_change)
            return
        if(checkPhone(message.text)):
            order.tel = message.text
            state = "EndOrder"
            await message.answer(ReturnEndForm(), reply_markup=ikb_change)
        else:
            await message.answer('Пожалуйста, введите номер телефона', reply_markup=keyboard_phone)

    elif(state == "ChEmail"):
        if(checkEmail(message.text)):
            order.email = message.text
            state = "EndOrder"
            await message.answer(ReturnEndForm(), reply_markup=ikb_change)
        else:
            await message.answer(ReturnEndForm(), reply_markup=ikb_change)

    elif(state == "ChDescription"):
        order.description = message.text
        state = "EndOrder"
        await message.answer(ReturnEndForm(), reply_markup=ikb_change)
    else:
        await message.answer(state)


@dp.callback_query()
async def callback(call: CallbackQuery):
    global state
    global order
    if(PrinterNames.__contains__(call.data)):
        await call.answer("Вы выбрали принтер " + call.data)
        state = "Name"
        order.printername = call.data
        await call.message.answer("Напишите имя. Чтобы автоматически ввести все контакты из Telegram выберите сообветсвующую функцию в меню", reply_markup=keyboard_name_phone)
    if(call.data == "description_skip" or call.data == "EndOrder"):
        order.description = ""
        state = "EndOrder"
        await call.message.answer(ReturnEndForm(), reply_markup=ikb_change)

    if (call.data == "ChName"):
        state = callback.data
        await call.message.answer("Напишите ваше имя", reply_markup=keyboard_name_phone)

    if (call.data == "ChTel"):
        state = callback.data
        await call.message.answer("Напишите ваш телефон", reply_markup=keyboard_phone)

    if (call.data == "ChEmail"):
        state = callback.data
        await call.message.answer("Напишите ваш Email")

    if (call.data == "ChDescription"):
        state = callback.data
        await call.message.answer("Напишите ваш комментарий", reply_markup=ikb_skip)

    if(call.data == "SendOrder"):
        state = ""
        SendOrder()
        order = OrderRequest()
        await call.message.answer("Заказ отправлен для дальнейшего рассмотрения! Напишите /start, если хотите оформить еще один заказ")



# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

def checkPhone(text):
    text = str(text)
    plusFirst = text[0] == '+'
    if (plusFirst):
        CountAcess = len(text) <= 12
    else:
        CountAcess = len(text) <= 11

    try:
        int(text)
        parsing = True
    except ValueError:
        parsing = False
    return CountAcess & (plusFirst or parsing)

def ReturnEndForm():
    global order
    return "Заказ оформлен на принтер "+ order.printername + "! Коментарий к заказу: "+ order.description + " \nВаши данные:\n    Имя: " + order.name + "\n   Телефон: " + order.tel + "\n    Email: " + order.email


def checkEmail(text):
    text = str(text)
    pattern = re.compile(r"(\w*)@(\w*).(\w*)")
    return pattern.match(text)

def SendOrder():
    global order
    url = "https://neopixel3d.ru/api/orders"
    data = order.toJSON()
    response = requests.post(url, data)
    print(response)


if __name__ == "__main__":
    asyncio.run(main())