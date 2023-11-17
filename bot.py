import asyncio
import logging
from asyncio import Lock
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.storage import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token="6953418785:AAFqReT_TmoSRZtPJyQkDE1080n0K-t12SU")
dp = Dispatcher(bot=bot, storage=MemoryStorage())

lock = Lock()

engine = create_engine('sqlite:///data.db')
Base = declarative_base()


class User(Base):
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    client_name = Column(String)
    product = Column(String)

    def __init__(self, a, b):
        self.client_name = a
        self.product = b


Session = sessionmaker(bind=engine)
session = Session()


class States(StatesGroup):
    name = State()
    product = State()


class DataSales:
    dt_user = {}


user_but = ReplyKeyboardMarkup(resize_keyboard=True)
user_but.add(KeyboardButton(text='шапка'), KeyboardButton(text='куртка'), KeyboardButton(text='штаны'))

user_inl1 = InlineKeyboardMarkup()
user_inl1.add(InlineKeyboardButton(text='купить', callback_data='шапка'))
user_inl2 = InlineKeyboardMarkup()
user_inl2.add(InlineKeyboardButton(text='купить', callback_data='куртка'))
user_inl3 = InlineKeyboardMarkup()
user_inl3.add(InlineKeyboardButton(text='купить', callback_data='штаны'))


@dp.message_handler(text='/start')
async def cmd_start(message: types.Message):
    await message.answer(text='ассортимент магазина', reply_markup=user_but)


@dp.message_handler()
async def inl_but(message: types.Message):
    if message.text == 'шапка':
        await message.reply(text='для заказа нажмите на кнопку', reply_markup=user_inl1)
        await States.product.set()
    if message.text == 'куртка':
        await message.reply(text='для заказа нажмите на кнопку', reply_markup=user_inl2)
        await States.product.set()
    if message.text == 'штаны':
        await message.reply(text='для заказа нажмите на кнопку', reply_markup=user_inl3)
        await States.product.set()


@dp.callback_query_handler(state=[States.product, States.name])
async def inl_query(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == 'шапка':
        await callback.message.reply(f'заказ: {callback.data} - подтвержден')
        async with lock:
            DataSales.dt_user['client_name'] = callback.from_user.first_name
            DataSales.dt_user['product'] = callback.data
        await state.finish()
        session.add(User(DataSales.dt_user['client_name'], DataSales.dt_user['product']))
        session.commit()
    if callback.data == 'куртка':
        await callback.message.reply(f'заказ: {callback.data} - подтвержден')
        async with lock:
            DataSales.dt_user['client_name'] = callback.from_user.first_name
            DataSales.dt_user['product'] = callback.data
        await state.finish()
        session.add(User(DataSales.dt_user['client_name'], DataSales.dt_user['product']))
        session.commit()
    if callback.data == 'штаны':
        await callback.message.reply(f'заказ: {callback.data} - подтвержден')
        async with lock:
            DataSales.dt_user['client_name'] = callback.from_user.first_name
            DataSales.dt_user['product'] = callback.data
        await state.finish()
        session.add(User(DataSales.dt_user['client_name'], DataSales.dt_user['product']))
        session.commit()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    asyncio.run(main())
