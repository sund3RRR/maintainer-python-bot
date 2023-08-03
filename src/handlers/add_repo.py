import sys
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from github.GithubException import UnknownObjectException
from github.Repository import Repository

from .start import home

import sys
sys.path.append("..")
from fetcher.github_fetcher import g
from db import get_db_conn_and_cursor

class AddRepoState(StatesGroup):
    add_repo = State()


def check_repo_has_releases(repo :Repository):
    try:
        last_release = repo.get_latest_release()
        return True, last_release.tag_name
    except UnknownObjectException as ex:
        last_tag_name = repo.get_tags()[0].name
        return False, last_tag_name


def check_url_is_valid(url :str):
    url = url.removeprefix("https://")
    url = url.removeprefix("http://")
    url = url.removeprefix("github.com/")

    repo_str = url.removesuffix(".git")

    try:
        repo = g.get_repo(repo_str)
    except UnknownObjectException as ex:
        return False, "Bad url, it is not github public repository, please try again", ""
    
    try:
        last_tag = repo.get_tags()[0]
        return True, "", repo
    except IndexError as ex:
        return False, "There is no tags in this repo", ""


async def add_repo(message :types.Message):
    await AddRepoState.add_repo.set()

    await message.answer("Enter url to github repository", 
        reply_markup=types.ReplyKeyboardRemove())


async def on_repo_enter(message: types.Message, state: FSMContext):
    is_url_valid, message_str, repo = check_url_is_valid(str(message.text))

    if is_url_valid:
        is_repo_has_releases, last_tag_name = check_repo_has_releases(repo)
        conn, cursor = get_db_conn_and_cursor()

        cursor.execute("SELECT MAX(id) from repos")
        last_id = cursor.fetchone()[0]
        if last_id is None:
            last_id = 0
        repo_id = last_id + 1

        owner, repo_name = repo.owner.login, repo.name
        cursor.execute("""
            INSERT INTO repos (id, user, owner, repo, last_tag_name, is_release)
            VALUES(?, ?, ?, ?, ?, ?)""",
            (
                repo_id,
                message.from_user.id,
                owner,
                repo_name,
                last_tag_name,
                int(is_repo_has_releases)
            )
        )
        conn.commit()

        await message.answer(f"Successfully added repo `{repo.owner.login}/{repo.name}`!", parse_mode="markdown")
        await home(message, state)
    else:
        await message.answer(message_str)