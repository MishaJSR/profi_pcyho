import asyncio
import time

import emoji
from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto, InputFile, FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_query_user import get_users_for_excel_parents, get_users_for_excel_teacher, \
    get_users_for_excel_all
from keyboards.admin.reply_admin import spam_actions_kb, excel_actions, excel_actions_kb

import pandas as pd
import os

admin_excel_loader_router = Router()


@admin_excel_loader_router.message(F.text == 'Выгрузка данных')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    print(os.getcwd())
    await message.answer("Выберите какие данные выгружать", reply_markup=excel_actions_kb(excel_actions))

@admin_excel_loader_router.message(F.text == 'Выгрузка данных родителей')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_parents(session)

        name = os.getcwd() + "\parent.xlsx"
        df = pd.DataFrame(res)
        df.rename(columns={'user_id': 'ID пользователя', 'username': 'Имя',
                                'phone_number': 'Телефон', 'user_class': 'Принадлежность',
                                'is_subscribe': 'Пройдена ли авторизация', 'parent_id': 'ID родителя',
                                'user_become_children': 'Родитель прошел полный курс'}, inplace=True)
        df.replace(True, 'Да', inplace=True)
        df.replace(False, 'Нет', inplace=True)
        df.to_excel(name)
        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
    except Exception as e:
        await message.answer("Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))

@admin_excel_loader_router.message(F.text == 'Выгрузка данных педагогов')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_teacher(session)
        name = os.getcwd() + "\prepod.xlsx"
        df = pd.DataFrame(res)
        df.rename(columns={'user_id': 'ID пользователя', 'username': 'Имя',
                                'phone_number': 'Телефон', 'user_class': 'Принадлежность',
                                'is_subscribe': 'Пройдена ли авторизация', 'parent_id': 'ID родителя',
                                'user_become_children': 'Родитель прошел полный курс'}, inplace=True)
        df.replace(True, 'Да', inplace=True)
        df.replace(False, 'Нет', inplace=True)
        df.to_excel(name)
        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
    except Exception as e:
        await message.answer("Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))


@admin_excel_loader_router.message(F.text == 'Общая выгрузка')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_all(session)
        df = pd.DataFrame(res)
        name = os.getcwd() + "\common.xlsx"
        df.rename(columns={'user_id': 'ID пользователя', 'username': 'Имя',
                                'phone_number': 'Телефон', 'user_class': 'Принадлежность',
                                'is_subscribe': 'Пройдена ли авторизация', 'parent_id': 'ID родителя',
                                'user_become_children': 'Родитель прошел полный курс'}, inplace=True)
        df.replace(True, 'Да', inplace=True)
        df.replace(False, 'Нет', inplace=True)
        df.to_excel(name)

        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
    except Exception as e:
        await message.answer("Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))