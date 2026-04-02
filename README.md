# 14220277_Data_Structure_Project
# Library System & Graph Algorithms

This repository contains two tasks for the course project:

- **Task 1**: A GUI-based library management system with admin and user panels.  
- **Task 2**: A data structures and algorithms demo focusing on **Graphs** and **Breadth-First Search (BFS)** with visualisation.

- **Task 1 video link**: https://mailouhkedu-my.sharepoint.com/:v:/g/personal/s1422027_live_hkmu_edu_hk/IQDYmq94wpnfSpJemwtlsy2lAYEpBdAnVd6pKLOhJ8YgJt4?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=x0O6Yh

- **Task 2 video link**:https://mailouhkedu-my.sharepoint.com/:v:/g/personal/s1422027_live_hkmu_edu_hk/IQD_3m80oiXKQrl88lX1fV0RAcj0vT89sN9Hbs-K_X36z2g?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0NvcHkifX0&e=EsJ8K8

- **Task 1 admin account**: username : test_admin, password : 12345678
- **Task 1 user account**: username : 1234, password : 12345678
---

## Task 1 – Library System Application

### Overview

Task 1 is a library system application implemented with a graphical user interface (GUI).  
The system is divided into two main parts: an **Admin Panel** and a **User Panel**.

### Admin Panel Features

- View monthly statistics for:
  - Number of borrowed books.
  - Total outstanding fines.
- Add and remove books and book categories.
- Delete user accounts when necessary.
- Help user to clear the fines

### User Panel Features

- View personal borrowing history and current loans.
- Borrow and return books through the GUI.
- Fine restriction rule:
  - If a user has outstanding fines, they are not allowed to borrow new books.
  - The user must contact an admin to clear the fines before returning books and borrowing again.

### Instruction : 
- Please go to task 1, install the library first:
```
pip install -r requirement
```
- after that, please will this command to open the project
```
python main.py
```
---

### Login Account :
1. Admin : username : test_admin, password : 12345678
2. User : username : 1234, password : 12345678

## Task 2 – Graph Data Structure & BFS Algorithm

### Overview

Task 2 focuses on self‑study of one **data structure** (Graph) and one **algorithm** (Breadth‑First Search).  
Both the data structure and the algorithm are accompanied by a GUI display to visualise the graph and traversals.

### Data Structure: Graph

In this task, the graph is studied and implemented in several forms:

- **Representations**
  - Adjacency matrix.
  - Adjacency list.

- **Types of graphs**
  - Undirected graphs.
  - Directed graphs.

The program also will use the abstract data type (ADT) operations (such as adding vertices/edges).

### Algorithm: Breadth‑First Search (BFS)

For the algorithm part, the focus is on **Breadth‑First Search** on graphs:

- Explanation of the BFS procedure using a **queue** to traverse the graph level by level.
- Time complexity analysis:
  - BFS visits each vertex at most once and inspects each edge at most once.
  - The running time is \(O(V + E)\), where \(V\) is the number of vertices and \(E\) is the number of edges.

BFS also will be compared with **Depth‑First Search (DFS)**:

- DFS explores as deep as possible along each branch using a **stack** (or recursion), while BFS explores breadth‑wise using a queue.
- The report contrasts how the choice of stack vs. queue changes the traversal order and applications of the algorithms.

### Instruction
please go to Task2 folder, please input each command to see the data structure graph and algorithm breadth-first search
```
python graphMain.py
python bfsMain.py
```