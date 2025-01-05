from tkinter import Tk
import asyncio

class Atk(Tk):
    def __init__(self, interval:int=10, *args):
        super().__init__(*args)
        
        # asyncio loop in tkinter
        self.__loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)
        
        # set asyncio loop's interval
        if type(interval) is not int:
            raise TypeError(f"bad argument {interval!r}: interval must be int, not {type(interval).__name__}")
        elif interval == 0:
            raise TypeError(f"Atk() arg 1 must not be zero")
        self.__interval = interval
        # do asyncio loop only once
        def _do_async_loop():
            self.__loop.call_soon(self.loop.stop)
            self.__loop.run_forever()
            self.after(self.__interval, _do_async_loop)
        self.after(self.__interval, _do_async_loop)
    
    def destroy(self):
        self.__loop.stop()
        super().destroy()