import asyncio
import random

async def long_operation(task_id: int) -> str:
    delay = random.randint(1, 5)
    print(f"Task {task_id}: Starting (delay {delay}s)...")
    await asyncio.sleep(delay)
    result = f"Task {task_id}: Completed after {delay} seconds"
    print(result)
    return result

async def main():
    tasks = [long_operation(i) for i in range(1, 4)]
    results = await asyncio.gather(*tasks)
    print("All tasks completed.")
    for result in results:
      print(result)

if __name__ == "__main__":
    asyncio.run(main())
