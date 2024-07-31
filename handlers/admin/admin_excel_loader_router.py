from aiogram import types, Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from database.orm_user.orm_query_user import get_users_for_excel_parents, get_users_for_excel_teacher, \
    get_users_for_excel_all
from handlers.admin.states import AdminStateSpammer
from keyboards.admin.reply_admin import spam_actions_kb, excel_actions, excel_actions_kb, start_kb

import pandas as pd
import os

admin_excel_loader_router = Router()


class AdminStateExcel(StatesGroup):
    start = State()
    choose_block = State()


@admin_excel_loader_router.message(StateFilter(AdminStateExcel), F.text.casefold() == "назад")
async def back_step_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AdminStateExcel.choose_block:
        await message.answer(text='Выберите действие', reply_markup=spam_actions_kb())
        await state.set_state(AdminStateSpammer.spam_actions)
        return

    if current_state == AdminStateExcel.start:
        await message.answer(text='Выберите действие', reply_markup=start_kb())
        await state.set_state(AdminStateSpammer.start)
        return


@admin_excel_loader_router.message(F.text == 'Выгрузка данных')
async def fill_admin_state(message: types.Message, state: FSMContext):
    await state.set_state(AdminStateExcel.choose_block)
    await message.answer("Выберите какие данные выгружать", reply_markup=excel_actions_kb(excel_actions))


@admin_excel_loader_router.message(StateFilter(AdminStateExcel.choose_block), F.text == 'Выгрузка данных родителей')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_parents(session)
        name = os.getcwd() + "\excel_files\parent.xlsx"
        df = inplace_df(res)
        df.to_excel(name)
        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
        await state.set_state(AdminStateExcel.start)
    except Exception as e:
        await message.answer("Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))


@admin_excel_loader_router.message(StateFilter(AdminStateExcel.choose_block), F.text == 'Выгрузка данных педагогов')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_teacher(session)
        name = os.getcwd() + "\excel_files\prepod.xlsx"
        df = inplace_df(res)
        df.to_excel(name)
        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
        await state.set_state(AdminStateExcel.start)
    except Exception as e:
        await message.answer("Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))


@admin_excel_loader_router.message(StateFilter(AdminStateExcel.choose_block), F.text == 'Общая выгрузка')
async def fill_admin_state(message: types.Message, session: AsyncSession, state: FSMContext):
    try:
        res = await get_users_for_excel_all(session)
        name = os.getcwd() + "\excel_files\common.xlsx"
        df = inplace_df(res)
        df.to_excel(name)
        file = FSInputFile(name)
        await message.answer_document(file)
        await message.answer("Выгрузка завершена", reply_markup=spam_actions_kb(excel_actions))
        await state.set_state(AdminStateExcel.start)
    except Exception as e:
        await message.answer(f"Ошибка выгрузки", reply_markup=spam_actions_kb(excel_actions))


def inplace_df(res) -> pd.DataFrame:
    df = pd.DataFrame(res)
    df.rename(columns={
        'user_id': 'ID пользователя', 'username': 'Имя',
        'phone_number': 'Телефон', 'user_class': 'Принадлежность',
        'is_subscribe': 'Пройдена ли авторизация', 'parent_id': 'ID родителя',
        'user_become_children': 'Прошел полный курс',
        'user_callback': 'Отзыв', 'points': 'E-коины'}, inplace=True)
    df.replace(True, 'Да', inplace=True)
    df.replace(False, 'Нет', inplace=True)
    df.replace("no", 'Негатив', inplace=True)
    df.replace("yes", 'Позитив', inplace=True)
    df.replace("skip", 'Пропустил', inplace=True)
    return df
