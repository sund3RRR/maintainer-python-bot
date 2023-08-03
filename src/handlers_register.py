from aiogram import Dispatcher

from handlers.start import start, home
from handlers.add_repo import add_repo, on_repo_enter, AddRepoState
from handlers.remove_repo import remove_repo, on_repo_number_enter, RemoveRepoState
from handlers.list_repo import list_repo

async def register_all_handlers(dp :Dispatcher):
    dp.register_message_handler(
        callback=start,
        commands= [ "start" ]
    )
    dp.register_message_handler(
        callback=home,
        commands= [ "home" ]
    )

    dp.register_message_handler(
        add_repo,
        lambda message: message.text == "✳️Add repo"
    )
    dp.register_message_handler(
        callback=on_repo_enter,
        state=AddRepoState.add_repo
    )
    dp.register_message_handler(
        remove_repo,
        lambda message: message.text == "❌Remove repo"
    )
    dp.register_message_handler(
        callback=on_repo_number_enter,
        state=RemoveRepoState.remove_repo
    )
    dp.register_message_handler(
        list_repo,
        lambda message: message.text == "📋List repos"
    )