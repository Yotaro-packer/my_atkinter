# my_atkinter
my Asynchronous tkinter

my_atkinter basically executes asyncio's coroutine by registering the coroutine in Atk's event loop using create_task(coro).
If you want to handle multiple coroutines as a group, use make_gather(coro1, coro2 ...) can be used.
They return a task as return value, so you can receive results or add callbacks.

my_atkinterでは基本的に、create_task(coro)を用いてAtkのイベントループにコルーチンを登録することでasyncioのコルーチンを実行します。
複数のコルーチンをひとまとまりとして扱いたい場合はmake_gather(coro1, coro2 ...)が使えます。
これらは返り値としてタスクを返すので、リザルトを受け取ったりコールバックを追加したりできます。