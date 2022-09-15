import logging
from asyncio.events import get_event_loop

from wxasync import WxAsyncApp

from tg_subscriber.gui import MainWindow

logging.basicConfig(
    filename="std.log",
    format='%(asctime)s %(message)s',
    filemode='w'
    )
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

if __name__ == '__main__':
    app = WxAsyncApp(0)
    window = MainWindow()
    window.Show()
    loop = get_event_loop()
    loop.run_until_complete(app.MainLoop())
