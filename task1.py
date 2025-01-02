import asyncio
from typing import List, Callable, Any

async def async_filter(array: List[Any], callback: Callable[[Any], bool]) -> List[Any]:
    async def _apply_callback(element):
        if await callback(element):
          return element
    
    tasks = [asyncio.create_task(_apply_callback(element)) for element in array]
    results = await asyncio.gather(*tasks)
    
    return [result for result in results if result is not None]
