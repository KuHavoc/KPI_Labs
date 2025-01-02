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

async def long_operation(task_id: int) -> str:
    delay = random.randint(1, 5)
    print(f"Task {task_id}: Starting (delay {delay}s)...")
    await asyncio.sleep(delay)
    result = f"Task {task_id}: Completed after {delay} seconds"
    print(result)
    return result

async def process_task(task_id: int):
    try:
        result = await long_operation(task_id)
        return f"Processed: {result}"
    except Exception as e:
        return f"Error: {e}"

async def main():
    results_promise = await asyncio.gather(*[long_operation_promise(i).then(lambda result: f"Processed: {result}").await_result() for i in range(1,4)])
    results_async_await = await asyncio.gather(
        process_task(4),
        process_task(5),
        process_task(6),
    )
    print("All tasks completed using Promises.")
    for result in results_promise:
      print(result)
    print("All tasks completed using Async Await.")
    for result in results_async_await:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
