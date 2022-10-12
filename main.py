import asyncio
import logging
from typing import NoReturn

from telegram import __version__ as TG_VER
from telegram.constants import ParseMode

from service import TotalAPI
from settings import Config

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Bot
from telegram.error import NetworkError

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

#THIS IS QUICK DEV
STATIONS_ID = ['NF078142', 'NF082271', 'NF059950', 'NF070629']

async def main() -> NoReturn:
    old_station = None
    """Run the bot."""
    # Here we use the `async with` syntax to properly initialize and shutdown resources.
    async with Bot(Config.TELEGRAM_API_KEY) as bot:
        logger.info("waiting for station notification")
        list_station = {}
        while True:
            for stationid in STATIONS_ID:
                msg = ""
                try:
                    station = TotalAPI(stationid)
                except:
                    continue
                if stationid in list_station:
                    msg = station.compare_before(list_station[stationid])
                else:
                    list_station[stationid] = station

                if msg != "":
                    try:
                        await bot.send_message(chat_id=-1001800131931, text=msg, parse_mode=ParseMode.MARKDOWN)
                        await bot.send_location(chat_id=-1001800131931, longitude=station.get_location()[0],
                                                latitude=station.get_location()[1])
                    except NetworkError:
                        await asyncio.sleep(1)
                await asyncio.sleep(10)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:  # Ignore exception when Ctrl-C is pressed
        pass