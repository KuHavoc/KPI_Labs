import asyncio
from typing import List, Callable, Any, Optional

async def async_filter(array: List[Any], callback: Callable[[Any], bool], debounce_delay: Optional[float] = None) -> List[Any]:
    async def _apply_callback(element):
        start_time = asyncio.get_event_loop().time()
        result = await callback(element)
        end_time = asyncio.get_event_loop().time()
        if debounce_delay and end_time - start_time < debounce_delay:
            await asyncio.sleep(debounce_delay - (end_time - start_time))
        if result:
          return element
    
    tasks = [asyncio.create_task(_apply_callback(element)) for element in array]
    results = await asyncio.gather(*tasks)
    
    return [result for result in results if result is not None]

async def is_even(number: int) -> bool:
    await asyncio.sleep(0.1)
    return number % 2 == 0

async def main():
    numbers = list(range(10))
    even_numbers = await async_filter(numbers, is_even)
    print(f"Original numbers: {numbers}")
    print(f"Even numbers: {even_numbers}")

if __name__ == "__main__":
    asyncio.run(main())
