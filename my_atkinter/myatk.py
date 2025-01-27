import tkinter as tk
import asyncio
from typing import Coroutine

class Atk(tk.Tk):
    def __init__(self, interval:int=10, threadsafe=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # asyncio loop in tkinter
        self.__loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.__loop)
        
        # asyncio Queue and Queue.join()'s Task
        self.__queue = asyncio.Queue()
        self.__qTask:asyncio.Task|None = None
        
        # set asyncio loop's interval
        if type(interval) is not int:
            raise TypeError(f"bad argument {interval!r}: interval must be int, not {type(interval).__name__}")
        elif interval == 0:
            raise TypeError(f"Atk() arg 1 must not be zero")
        self.__interval = interval
        
        # do asyncio loop only once
        def _do_async_loop(threadsafe):
            if threadsafe:
                self.__loop.call_soon_threadsafe(self.__loop.stop)
            else:
                self.__loop.call_soon(self.__loop.stop)
            self.__loop.run_forever()
            self.after(self.__interval, _do_async_loop, threadsafe)
        self.after(self.__interval, _do_async_loop, threadsafe)
    
    # add task that do coroutine to loop
    def add_task(self, coro:Coroutine) -> asyncio.Task:
        return self.__loop.create_task(coro)
    
    # make task that do all coroutines and add task to loop
    def add_tasks(self, *coros:list[Coroutine]) -> asyncio.Task:
        return self.__loop.create_task(self._do_coros(coros))
        
    # func that use in add_tasks()
    async def _do_coros(self, coros:list[Coroutine]) -> Coroutine:
        await asyncio.gather(*coros)
    
    # add callback to task
    def after_task(self, task:asyncio.Task, callback) -> None:
        task.add_done_callback(callback)
    
    # add task to queue then process queue item if queue's Task is None or done
    def add_queue(self, coro:Coroutine) -> None:
        self.__queue.put_nowait(coro)
        if self.__qTask is None or self.__qTask.done():
            self.__qTask = self.add_task(self.__queue.join())
    
    # get atk's event loop
    def get_event_loop(self) -> asyncio.AbstractEventLoop:
        return self.__loop
    
    # set atk's event loop
    def set_event_loop(self, loop:asyncio.AbstractEventLoop) -> None:
        self.__loop.close()
        self.__loop = loop
    
    # stop async loop when window close
    def destroy(self) -> None:
        self.__loop.stop()
        super().destroy()

if __name__ == "__main__":
    COUNTER = 5
    root = Atk()
    root.title = "MyAtkTest"
    
    labelvars = [tk.IntVar(root) for _ in range(COUNTER)]
    labels = [tk.Label(root, textvariable=labelvars[i], width=3) for i in range(COUNTER)]
    
    async def countup(n) -> None:
        for i in range(6):
            labelvars[n].set(i)
            await asyncio.sleep(1)
    buttons = [tk.Button(root, text=str(i), command=lambda i=i:root.create_task(countup(i)), width=2) for i in range(COUNTER)]
    
    for i in range(COUNTER):
        labels[i].grid(column=i, row=0)
        buttons[i].grid(column=i, row=1)
    
    root.mainloop()