from typing import List
class Stack:
    """
    ============================================================================
    Stack - LIFO (Last In First Out) 
    ============================================================================
    
    Stack Operations:
    - push (push): Add an element to the top of the stack    -> O(1)
    - pop (pop): Remove an element from the top of the stack -> O(1)
    - peek (peek): View the top element of the stack         -> O(1)
    - is_empty (is_empty): Check if the stack is empty       -> O(1)
    
    Visualization of Stack:
    
    Initial:  Stack = [start_vertex]
           top
            ↓
           [ 0 ]  <- start_vertex is pushed
    
    Step 1: Visit 0, neighbors 1, 2 are pushed
           top
            ↓
           [ 2 ]  <- pushed last
           [ 1 ]  <- pushed first
           [ 0 ]  <- visited, popped
    
    Step 2: Visit 2（top！），neighbor 4 is pushed
           top
            ↓
           [ 4 ]  <- pushed last
           [ 1 ]  <- still waiting
    
    Step 3: Visit 4，no new neighbors, backtrack to 1
           top
            ↓
           [ 1 ]  <- now processing
    
    Key Feature: The node that entered last is processed first, implementing "depth first, first walk to the end"
    ============================================================================
    """
    
    def __init__(self):
        self._data: List[int] = []
    
    def push(self, item: int) -> None:
        """Push - Add an element to the top of the stack O(1)"""
        self._data.append(item)
    
    def pop(self) -> int:
        """Pop - Remove an element from the top of the stack O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data.pop()
    
    def peek(self) -> int:
        """Peek - View the top element of the stack O(1)"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._data[-1]
    
    def is_empty(self) -> bool:
        """Check if the stack is empty O(1)"""
        return len(self._data) == 0
    
    def __len__(self) -> int:
        return len(self._data)
    
    def to_list(self) -> List[int]:
        """Convert to list (for display, top is at the end)"""
        return self._data.copy()