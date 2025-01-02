import asyncio
import time
from typing import List, Callable, Any, Optional, TypeVar, ParamSpec

P = ParamSpec("P")
T = TypeVar("T")

def debounce(delay: Optional[float] = None) -> Callable[[Callable[P, T]], Callable[P, T]]:
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            start_time = asyncio.get_event_loop().time()
            result = await func(*args, **kwargs)
            end_time = asyncio.get_event_loop().time()
            if delay and end_time - start_time < delay:
                await asyncio.sleep(delay - (end_time - start_time))
            return result
        return wrapper
    return decorator

async def async_filter(array: List[Any], callback: Callable[[Any], bool], debounce_delay: Optional[float] = None) -> List[Any]:
    @debounce(debounce_delay)
    async def _apply_callback(element):
        if await callback(element):
          return element
    
    tasks = [asyncio.create_task(_apply_callback(element)) for element in array]
    results = await asyncio.gather(*tasks)
    
    return [result for result in results if result is not None]

async def async_map(array: List[Any], callback: Callable[[Any], Any], debounce_delay: Optional[float] = None) -> List[Any]:
    @debounce(debounce_delay)
    async def _apply_callback(element):
      return await callback(element)
    
    tasks = [asyncio.create_task(_apply_callback(element)) for element in array]
    results = await asyncio.gather(*tasks)
    
    return results

@debounce(0.1)
async def is_even_slow(number: int) -> bool:
    await asyncio.sleep(0.05)
    return number % 2 == 0

async def is_even_fast(number: int) -> bool:
    return number % 2 == 0

@debounce(0.1)
async def multiply_by_two_slow(number: int) -> int:
    await asyncio.sleep(0.05)
    return number * 2

async def multiply_by_two_fast(number: int) -> int:
    return number * 2

async def main():
    numbers = list(range(10))
    
    print("--- async_filter without Debounce ---")
    start_time = time.time()
    even_numbers = await async_filter(numbers, is_even_slow)
    end_time = time.time()
    print(f"Even numbers: {even_numbers}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")

    print("\n--- async_filter with Debounce ---")
    start_time = time.time()
    even_numbers_with_debounce = await async_filter(numbers, is_even_slow, debounce_delay=0.1)
    end_time = time.time()
    print(f"Even numbers (with debounce): {even_numbers_with_debounce}")
    print(f"Time taken (with debounce): {end_time - start_time:.4f} seconds")
    
    print("\n--- async_filter With Debounce and Fast Callback ---")
    start_time = time.time()
    even_numbers_fast_with_debounce = await async_filter(numbers, is_even_fast, debounce_delay=0.1)
    end_time = time.time()
    print(f"Even numbers (with fast debounce): {even_numbers_fast_with_debounce}")
    print(f"Time taken (with fast debounce): {end_time - start_time:.4f} seconds")
    
    
    print("\n--- async_map without Debounce ---")
    start_time = time.time()
    mapped_numbers = await async_map(numbers, multiply_by_two_slow)
    end_time = time.time()
    print(f"Mapped numbers: {mapped_numbers}")
    print(f"Time taken: {end_time - start_time:.4f} seconds")
    
    print("\n--- async_map with Debounce ---")
    start_time = time.time()
    mapped_numbers_with_debounce = await async_map(numbers, multiply_by_two_slow, debounce_delay=0.1)
    end_time = time.time()
    print(f"Mapped numbers (with debounce): {mapped_numbers_with_debounce}")
    print(f"Time taken (with debounce): {end_time - start_time:.4f} seconds")
    
    print("\n--- async_map With Debounce and Fast Callback ---")
    start_time = time.time()
    mapped_numbers_fast_with_debounce = await async_map(numbers, multiply_by_two_fast, debounce_delay=0.1)
    end_time = time.time()
    print(f"Mapped numbers (with fast debounce): {mapped_numbers_fast_with_debounce}")
    print(f"Time taken (with fast debounce): {end_time - start_time:.4f} seconds")


if __name__ == "__main__":
    asyncio.run(main())
