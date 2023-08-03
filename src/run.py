import logging, os, asyncio, traceback, datetime, sys
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers_register import register_all_handlers
from fetcher.repo_fetcher import fetch_repos


def log_exception(exc_type, exc_value, exc_traceback):
    logging.error("Uncaught exception",
                  exc_info=(exc_type, exc_value, exc_traceback))
    tb = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    dt = datetime.datetime.now().strftime(r"%Y-%m-%d-%H:%M")
    with open(f"log/exception-{dt}.log", "w") as f:
        f.write(tb)


async def main(dp, bot):
    loop.create_task(dp.start_polling())
    await register_all_handlers(dp)
    await fetch_repos(bot)
    

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)

    sys.excepthook = log_exception

    bot = Bot(os.environ["tgToken"])
    dp = Dispatcher(bot, storage=MemoryStorage())

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(dp, bot))