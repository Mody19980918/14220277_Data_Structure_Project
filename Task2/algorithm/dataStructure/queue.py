from collections import deque
from typing import List

class Queue:
    """
    ============================================================================
    Queue  - FIFO (First In First Out) 
    ============================================================================
    
    Queue Operations:
    - enqueue (enqueue): Add an element to the rear of the queue        -> O(1)
    - dequeue (dequeue): Remove an element from the front of the queue  -> O(1)
    - peek (peek): View the front element of the queue                  -> O(1)
    - is_empty (is_empty): Check if the queue is empty                  -> O(1)
    
    Visualization of Queue:
    
    Initial: Queue = [start_vertex]
           front                                rear
             ↓                                     ↓
           [ 0 ]  <- start_vertex is enqueued
    
    Step 1: Visit 0, neighbors 1, 2 are enqueued
           front                                rear
             ↓                                     ↓
           [ 1, 2 ]  <- 0 is dequeued, 1, 2 are enqueued
    
    Step 2: Visit 1, neighbor 3 is enqueued
           front                                rear
             ↓                                    ↓
           [ 2, 3 ]  <- 1 is dequeued, 3 is enqueued
    
    Step 3: Visit 2, neighbor 4 is enqueued
           front                                rear
             ↓                                    ↓
           [ 3, 4 ]  <- 2 is dequeued, 4 is enqueued
    
    Key Feature: The node that entered first (closer distance) is processed first, implementing "layer by layer expansion"
    ============================================================================
    """
    
    def __init__(self):
        self._data: deque = deque()
    
    def enqueue(self, item: int) -> None:
        """Enqueue - Add an element to the rear of the queue O(1)"""
        self._data.append(item)
    
    def dequeue(self) -> int:
        """Dequeue - Remove an element from the front of the queue O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data.popleft()
    
    def peek(self) -> int:
        """Peek - View the front element of the queue O(1)"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[0]
    
    def is_empty(self) -> bool:
        """Check if the queue is empty O(1)"""
        return len(self._data) == 0
    
    def __len__(self) -> int:
        return len(self._data)
    
    def to_list(self) -> List[int]:
        """Convert to list (for display)"""
        return list(self._data)