from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

import requests

import config

key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

data = requests.get(key)
data = data.json()
BTC2 = float(data['price'])
global BTC
BTC1 = round(BTC2, 2)

def price1():
    key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

    data = requests.get(key)
    data = data.json()
    BTC1 = float(data['price'])
    BTC2 = round(BTC1, 2)
    global BTC
    BTC = round(((BTC2 / 100 * proccent) + BTC2), 2)





TOKEN_API = config.botik
support = config.contact_support
admin_id = config.admin_id
btc_wallet = config.btc_wallet
usdt_wallet = config.usdt_wallet
proccent = config.proccent

img_url = 'https://i.imgur.com/RYDr3D3.png'
img_url1 = 'https://i.imgur.com/JvifEq6.png'
first_crypto_minimum = round(400 / BTC2, 8)
usdt_reserve = '56.546,4'
usdt_res = float('56546.4')

storage = MemoryStorage()
bot = Bot(TOKEN_API)
dp = Dispatcher(bot=bot,
                storage=storage)

class UserState(StatesGroup):
    name = State()
    address = State()
    gmail = State()

class UsdtState(StatesGroup):
    one = State()
    two = State()
    three = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    ikb = InlineKeyboardMarkup(row_width = 2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await message.answer(f'Hello! \n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)


@dp.callback_query_handler(lambda c: c.data =='BTC')
async def btc(callback_query: types.CallbackQuery):
    price1()

    await callback_query.message.answer('How many BTC (BEP20) do you want to exchange?\n\n'
                                                 ''
                                                 f'<i>Reminder:</i> <b>minimum exchange amount is {first_crypto_minimum} BTC (BEP20)</b>\n'
                                                 '-------------------------\n'
                                                 'Exchange rate:\n'
                                                 f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                 'The reserve is:\n'
                                                 f'{usdt_reserve} USDT (TRC20)<a href="{img_url}">.</a>', parse_mode=ParseMode.HTML)
    await UserState.name.set()

    await bot.answer_callback_query(callback_query.id)

    @dp.message_handler(state=UserState.name)
    async def check_number(message: types.Message, state: FSMContext):
        global usname
        usname = message.from_user.username
        if message.text.find(',') != -1:
            await message.answer('Please enter the value without ","\n'
                                 'Use "."\n'
                                 f'<b>Example:</b> 450.39', parse_mode='html')
            return await callback_query.message.answer('How many BTC (BEP20) do you want to exchange?\n\n'
                                                       ''
                                                       f'<i>Reminder:</i> <b>minimum exchange amount is {first_crypto_minimum} BTC (BEP20)</b>\n'
                                                       '-------------------------\n'
                                                       'Exchange rate:\n'
                                                       f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                       'The reserve is:\n'
                                                       f'{usdt_reserve} USDT (TRC20)<a href="{img_url}">.</a>',
                                                       parse_mode=ParseMode.HTML)

        elif float(message.text) < first_crypto_minimum:
            await message.answer("Minimum exchange amount is 2,3 BTC (BEP20)")
            return await callback_query.message.answer('How many BTC (BEP20) do you want to exchange?\n\n'
                                                 ''
                                                 f'<i>Reminder:</i> <b>minimum exchange amount is {first_crypto_minimum} BTC (BEP20)</b>\n'
                                                 '-------------------------\n'
                                                 'Exchange rate:\n'
                                                 f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                 'The reserve is:\n'
                                                 f'{usdt_reserve} USDT (TRC20)<a href="{img_url}">.</a>', parse_mode=ParseMode.HTML)


        elif float(message.text) > 5.63:
            await message.answer('Maximum exchange amount is 5,64 BTC (BEP20)')
            return await callback_query.message.answer('How many BTC (BEP20) do you want to exchange?\n\n'
                                                 ''
                                                 f'<i>Reminder:</i> <b>minimum exchange amount is {first_crypto_minimum} BTC (BEP20)</b>\n'
                                                 '-------------------------\n'
                                                 'Exchange rate:\n'
                                                 f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                 'The reserve is:\n'
                                                 f'{usdt_reserve} USDT (TRC20)<a href="{img_url}">.</a>', parse_mode=ParseMode.HTML)


        else:
            global amount
            amount = float(message.text)
            kb = InlineKeyboardMarkup(row_width=1)

            item1 = InlineKeyboardButton(text='Yes', callback_data='yes')
            item2 = InlineKeyboardButton(text='Menu', callback_data='menu')

            kb.add(item1, item2)

            await message.answer(f"You are giving away: {amount} BTC (BEP20)?", reply_markup=kb)

            await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'yes')
async def yes(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'You are giving away: {amount} BTC (BEP20)\n\n'
                                                         f"You'll get: {round(amount * BTC, 2)} USDT (TRC20)")
    await callback_query.message.answer(f'<b>Enter your USDT (TRC20) wallet:</b>', parse_mode='html')

    await UserState.address.set()

    await bot.answer_callback_query(callback_query.id)

    @dp.message_handler(commands=['start'], state=UserState.address)
    async def start_addres(message: types.Message, state: FSMContext):
        ikb = InlineKeyboardMarkup(row_width=2)

        item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
        item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
        item3 = InlineKeyboardButton(text='Support', url=support)

        ikb.add(item1, item2, item3)

        await message.answer(f'Hello! \n\n'
                             f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                             f'<b>To continue working, select the currency pair:</b>',
                             parse_mode=ParseMode.HTML, reply_markup=ikb)

        await state.finish()

        await bot.answer_callback_query(callback_query.id)

    @dp.message_handler(state=UserState.address)
    async def process_age_invalid(message: types.Message):
        global wal
        wal = message.text

        if len(message.text) == 34:
            await message.answer(f"Enter your email address to create an application:")

            await UserState.gmail.set()

        else:
            await callback_query.message.answer(f'error!')

            return await callback_query.message.answer(f'<b>Enter your USDT (TRC20) wallet:</b>', parse_mode='html')





@dp.callback_query_handler(text="menu")
async def start_menu(call: types.CallbackQuery):
    ikb = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await call.message.answer(f'Hello!\n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)


@dp.message_handler(state=UserState.gmail)
async def order_user(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)

    item1 = InlineKeyboardButton(text='I paid', callback_data='paidyt')
    item2 = InlineKeyboardButton(text='Menu', callback_data='menu')

    kb.add(item1, item2)

    await message.answer('Wallet where you receive:\n\n'
                         f'{wal}\n\n'
                         f'Amount of transfer: {amount} BTC (BEP20)\n\n'
                         f"You'll get: {round(amount * BTC, 2)} USDT (TRC20)\n\n"
                         "Open the client from where you will transfer BTC (BEP20), and enter the following information:\n\n"
                         "‼️<b>BTC (BEP20)</b>‼\n\n"
                         "-------------------------------------------------------------------", parse_mode='html')
    await message.answer(f'{btc_wallet}')

    await message.answer('-------------------------------------------------------------------\n\n'
                         '‼️Your ticket has been created, pay the amount of BTC (BEP20) specified in the application to the wallet specified above, after payment, click the "I paid" button.‼️', reply_markup=kb)

@dp.callback_query_handler(text="paidyt", state=UserState.gmail)
async def order_user1(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1)

    item1 = InlineKeyboardButton(text='Menu', callback_data='menu')

    kb.add(item1)

    await call.message.answer(f'<b>✅ Your order has been accepted!</b>', parse_mode='html')

    await call.message.answer(f'Order created!\n\n'
                              f''
                              f'You exchanged: {amount} BTC (BEP20) on the {round(amount * BTC, 2)} USDT (TRC20)\n\n'
                              f''
                              f'Order status:\n'
                              f'<b>Waiting for the receipt of funds</b>', reply_markup=kb, parse_mode='html')

    await bot.send_message(chat_id=admin_id, text=f'Новый обмен!\n\n'
                                                    f''
                                                    f'<b>От:</b> @{usname}\n'
                                                    f'<b>Кошелек (USDT): {wal}</b>\n'
                                                    f'<b>Сумма BTC:</b> {amount}\n'
                                                    f'<b>Сумма USDT:</b> {round(amount * BTC, 2)}\n'
                                                    f'<b>Статус:</b> Оплачено', parse_mode='html')



@dp.callback_query_handler(text="menu", state=UserState.gmail)
async def start_gmail(call: types.CallbackQuery, state: FSMContext):
    ikb = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await call.message.answer(f'Hello!\n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)

    await state.finish()


@dp.message_handler(commands=['start'], state=UserState.name)
async def start_name(message: types.Message, state: FSMContext):
    ikb = InlineKeyboardMarkup(row_width = 2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await message.answer(f'Hello! \n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)

    await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'USDT')
async def usdt(callback_query: types.CallbackQuery):
    price1()

    await callback_query.message.answer('How many USDT (TRC20) do you want to exchange?\n\n'
                                                 ''
                                                 f'<i>Reminder:</i> <b>minimum exchange amount is 400 USDT (TRC20)</b>\n'
                                                 '-------------------------\n'
                                                 'Exchange rate:\n'
                                                 f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                 'The reserve is:\n'
                                                 f'{usdt_reserve} USDT (TRC20)<a href="{img_url1}">.</a>', parse_mode=ParseMode.HTML)
    await UsdtState.one.set()

    await bot.answer_callback_query(callback_query.id)

    @dp.message_handler(commands=['start'], state=UsdtState.one)
    async def start_addres2(message: types.Message, state: FSMContext):
            ikb = InlineKeyboardMarkup(row_width=2)

            item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
            item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
            item3 = InlineKeyboardButton(text='Support', url=support)

            ikb.add(item1, item2, item3)

            await message.answer(f'Hello! \n\n'
                                 f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                 f'<b>To continue working, select the currency pair:</b>',
                                 parse_mode=ParseMode.HTML, reply_markup=ikb)

            await state.finish()


    @dp.message_handler(state=UsdtState.one)
    async def check_number2(message: types.Message, state: FSMContext):
        if float(message.text) < 400:
            await message.answer("Minimum exchange amount is 400 USDT (TRC20)")
            return await callback_query.message.answer('How many USDT (TRC20) do you want to exchange?\n\n'
                                                 ''
                                                 f'<i>Reminder:</i> <b>minimum exchange amount is 400 USDT (TRC20)</b>\n'
                                                 '-------------------------\n'
                                                 'Exchange rate:\n'
                                                 f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                 'The reserve is:\n'
                                                 f'{usdt_reserve} USDT (TRC20)<a href="{img_url1}">.</a>', parse_mode=ParseMode.HTML)


        elif float(message.text) > float(usdt_res):
            await message.answer(f'Maximum exchange amount is {usdt_reserve} USDT (TRC20)')
            return await callback_query.message.answer('How many USDT (TRC20) do you want to exchange?\n\n'
                                                       ''
                                                       f'<i>Reminder:</i> <b>minimum exchange amount is 400 USDT (TRC20)</b>\n'
                                                       '-------------------------\n'
                                                       'Exchange rate:\n'
                                                       f'1 BTC (BEP20) = {BTC} USDT (TRC20)\n'
                                                       'The reserve is:\n'
                                                       f'{usdt_reserve} USDT (TRC20)<a href="{img_url1}">.</a>',
                                                       parse_mode=ParseMode.HTML)


        else:
            global amount2
            amount2 = float(message.text)
            kb = InlineKeyboardMarkup(row_width=1)

            item1 = InlineKeyboardButton(text='Yes', callback_data='yes2')
            item2 = InlineKeyboardButton(text='Menu', callback_data='menu2')

            kb.add(item1, item2)

            await message.answer(f"You are giving away: {amount2} USDT (TRC20)?", reply_markup=kb)

            await state.finish()







@dp.callback_query_handler(lambda c: c.data == 'yes2', )
async def yes2(callback_query: types.CallbackQuery):
    await callback_query.message.answer(f'You are giving away: {amount2} USDT (TRC20)\n\n'
                                                         f"You'll get: {round(amount2 / BTC, 8)} BTC (BEP20)")
    await callback_query.message.answer(f'<b>Enter your BTC (BEP20) wallet:</b>', parse_mode='html')

    await UsdtState.two.set()

    @dp.message_handler(commands=['start'], state=UsdtState.two)
    async def start_addres21(message: types.Message, state: FSMContext):
        ikb = InlineKeyboardMarkup(row_width=2)

        item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
        item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
        item3 = InlineKeyboardButton(text='Support', url=support)

        ikb.add(item1, item2, item3)

        await message.answer(f'Hello! \n\n'
                             f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                             f'<b>To continue working, select the currency pair:</b>',
                             parse_mode=ParseMode.HTML, reply_markup=ikb)

        await state.finish()

        await bot.answer_callback_query(callback_query.id)

    @dp.message_handler(state=UsdtState.two)
    async def process_age_invalid2(message: types.Message):
        global wal2
        wal2 = message.text

        if len(message.text) == 42:
            await message.answer(f"Enter your email address to create an application:")

            await UsdtState.three.set()

        else:
            await callback_query.message.answer(f'error!')

            return await callback_query.message.answer(f'<b>Enter your BTC (BEP20) wallet:</b>', parse_mode='html')



@dp.callback_query_handler(text="menu2")
async def start_menu2(call: types.CallbackQuery):
    ikb = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await call.message.answer(f'Hello!\n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)

@dp.message_handler(state=UsdtState.three)
async def order_user2(message: types.Message):
    kb = InlineKeyboardMarkup(row_width=1)

    item1 = InlineKeyboardButton(text='I paid', callback_data='paidyt2')
    item2 = InlineKeyboardButton(text='Menu', callback_data='menu2')

    kb.add(item1, item2)

    await message.answer('Wallet where you receive:\n\n'
                         f'{wal2}\n\n'
                         f'Amount of transfer: {amount2} USDT (TRC20)\n\n'
                         f"You'll get: {round(amount2 / BTC, 8)} BTC (BEP20)\n\n"
                         "Open the client from where you will transfer USDT (TRC20), and enter the following information:\n\n"
                         "‼️<b>USDT (TRC20)</b>‼\n\n"
                         "-------------------------------------------------------------------", parse_mode='html')
    await message.answer(f'{btc_wallet}')

    await message.answer('-------------------------------------------------------------------\n\n'
                         '‼️Your ticket has been created, pay the amount of USDT (TRC20) specified in the application to the wallet specified above, after payment, click the "I paid" button.‼️', reply_markup=kb)

@dp.callback_query_handler(text="paidyt2", state=UsdtState.three)
async def order_user12(call: types.CallbackQuery, state: FSMContext):
    kb = InlineKeyboardMarkup(row_width=1)

    item1 = InlineKeyboardButton(text='Menu', callback_data='menu2')

    kb.add(item1)

    await call.message.answer(f'<b>✅ Your order has been accepted!</b>', parse_mode='html')

    await call.message.answer(f'Order created!\n\n'
                              f''
                              f'You exchanged: {amount2} USDT (TRC20) on the {round(amount2 / BTC, 8)} BTC (BEP20)\n\n'
                              f''
                              f'Order status:\n'
                              f'<b>Waiting for the receipt of funds</b>', reply_markup=kb, parse_mode='html')

    await bot.send_message(chat_id=admin_id, text=f'Новый обмен!\n\n'
                                                    f''
                                                    f'<b>От:</b> @{usname}\n'
                                                    f'<b>Кошелек (BTC): {wal2}</b>\n'
                                                    f'<b>Сумма USDT:</b> {amount2}\n'
                                                    f'<b>Сумма BTC:</b> {round(amount2 / BTC, 8)}\n'
                                                    f'<b>Статус:</b> Оплачено', parse_mode='html')


@dp.callback_query_handler(text="menu2", state=UsdtState.three)
async def start_gmail2(call: types.CallbackQuery, state: FSMContext):
    ikb = InlineKeyboardMarkup(row_width=2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await call.message.answer(f'Hello! \n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)

    await state.finish()


@dp.message_handler(commands=['start'], state=UsdtState.three)
async def start_name2(message: types.Message, state: FSMContext):
    ikb = InlineKeyboardMarkup(row_width = 2)

    item1 = InlineKeyboardButton(text='BTC/USDT TRC20', callback_data='BTC')
    item2 = InlineKeyboardButton(text='USDT/BTC BEP20', callback_data='USDT')
    item3 = InlineKeyboardButton(text='Support', url=support)

    ikb.add(item1, item2, item3)

    await message.answer(f'Hello! \n\n'
                                      f'This bot allows you to make an exchange between BTC (BEP20) and USDT (TRC20) coins.\n\n'
                                      f'<b>To continue working, select the currency pair:</b>',
                                        parse_mode=ParseMode.HTML, reply_markup=ikb)

    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp)