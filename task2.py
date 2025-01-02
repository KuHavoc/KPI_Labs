import asyncio
import random
from typing import Callable

class Promise:
    def __init__(self, future: asyncio.Future):
        self._future = future

    def then(self, on_fulfilled: Callable):
        async def run_then():
            result = await self._future
            if on_fulfilled:
                return on_fulfilled(result)
            else:
              return result

        return Promise(asyncio.ensure_future(run_then()))

    def catch(self, on_rejected: Callable):
        async def run_catch():
            try:
              await self._future
            except Exception as e:
              return on_rejected(e)

        return Promise(asyncio.ensure_future(run_catch()))

    async def await_result(self):
        return await self._future

def long_operation_promise(task_id: int) -> Promise:
    future = asyncio.ensure_future(long_operation(task_id))
    return Promise(future)

async def main():
    promise1 = long_operation_promise(1).then(lambda result: f"Processed: {result}")
    promise2 = long_operation_promise(2).then(lambda result: result.upper())
    promise3 = long_operation_promise(3).catch(lambda error: f"Error: {error}")

    results = await asyncio.gather(*[promise1.await_result(),
                                     promise2.await_result(),
                                     promise3.await_result()])
    print("All tasks completed.")
    for result in results:
      print(result)

if __name__ == "__main__":
    asyncio.run(main())
