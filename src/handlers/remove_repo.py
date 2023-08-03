import sys
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from .list_repo import create_repo_list, list_repo
from .start import home

import sys
sys.path.append("..")
from db import get_db_conn_and_cursor


class RemoveRepoState(StatesGroup):
    repos = []
    remove_repo = State()


async def remove_repo(message :types.Message):
    repos_list_str, repos = create_repo_list(message.from_user.id)
    await list_repo(message, repos_list_str)
    await RemoveRepoState.remove_repo.set()
    RemoveRepoState.repos = repos

    await message.answer("Enter a number of repo you want to remove",
        reply_markup=types.ReplyKeyboardRemove())

async def on_repo_number_enter(message :types.Message, state :FSMContext):
    try:
        repo_number = int(message.text)
        if repo_number == 0:
            raise
        repo = RemoveRepoState.repos[repo_number - 1]

        conn, cursor = get_db_conn_and_cursor()
        cursor.execute("""
            DELETE FROM repos
            WHERE id = ?""",
            (
                repo[0],
            )
        )
        conn.commit()

        await message.answer("Repo removed successfully!")
        await home(message, state)
    except:
        await message.answer("Repo id is incorrect, please try again")
