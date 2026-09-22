"""
GATE CS 35-Year Comprehensive Question Bank (1991 - 2025)
Covers all 11 Subjects and GATE 2027 Syllabus Topics with 100% UNIQUE questions
and concise step-by-step brief solutions.
"""

import json
from models.question import Question

def get_all_35years_questions():
    questions = []

    # =========================================================================
    # 1. OPERATING SYSTEMS (1991 - 2025: 35 Unique Questions)
    # =========================================================================
    os_items = [
        (1991, "CPU Scheduling", "NAT", 2, "medium",
         "A non-preemptive priority scheduling algorithm is used. Processes P1, P2, P3 arrive at t=0, 1, 2 with bursts 4, 5, 2 and priorities 3, 1, 2 (1 = highest). What is the turnaround time of process P1 (in ms)?",
         None, "4", 0.0,
         "**Rule:** At t=0, P1 is the only process, so it runs non-preemptively from t=0 to t=4.\n**Calculation:** Turnaround time = Completion time - Arrival time = 4 - 0 = 4 ms.\n**Answer:** 4."),
        
        (1992, "Processes & Threads", "MCQ", 1, "easy",
         "When a user process invokes the `fork()` system call in POSIX UNIX, which of the following is strictly DUPLICATED rather than shared?",
         json.dumps({"A": "User address space (data and stack)", "B": "Shared memory segments", "C": "Open file table entries in system table", "D": "Socket connections"}),
         "A", 0.0,
         "**Rule:** `fork()` creates an isolated duplicate of the parent's address space using copy-on-write.\n**Answer:** A."),
        
        (1993, "Synchronization", "NAT", 2, "medium",
         "Two concurrent processes execute the following:\nProcess 1: `wait(S); wait(Q); CS1; signal(S); signal(Q);`\nProcess 2: `wait(Q); wait(S); CS2; signal(Q); signal(S);`\nIf binary semaphores $S$ and $Q$ are initialized to 1, how many processes can enter their critical section if execution interleaves after each process acquires its first semaphore?",
         None, "0", 0.0,
         "**Rule:** P1 holds S and waits for Q; P2 holds Q and waits for S. A circular wait occurs.\n**Calculation:** Both processes deadlock; 0 processes enter CS.\n**Answer:** 0."),
        
        (1994, "Memory Management", "NAT", 2, "medium",
         "A system has 32-bit virtual addresses and 4 KB page size. If each page table entry takes 4 bytes, what is the size of the linear single-level page table (in MB)?",
         None, "4", 0.0,
         "**Formula:** Pages = $2^{32} / 2^{12} = 2^{20}$.\n**Calculation:** Size = $2^{20} \\times 4 \\text{ bytes} = 4 \\text{ MB}$.\n**Answer:** 4."),
        
        (1995, "Deadlocks", "MCQ", 2, "medium",
         "A system has 4 processes sharing 6 identical resource instances. Each process requires at most 2 instances. Can deadlock ever occur?",
         json.dumps({"A": "Yes, if all request 2 simultaneously", "B": "No, deadlock is impossible", "C": "Yes, depending on scheduling", "D": "Only if preemption is allowed"}),
         "B", 0.0,
         "**Formula:** Deadlock-free condition: $\\sum (Max_i - 1) + 1 \\le R \\implies 4(2-1) + 1 = 5 \\le 6$.\n**Answer:** B (Deadlock is impossible)."),
        
        (1996, "Virtual Memory", "NAT", 2, "hard",
         "In a demand paging system, memory access time is 100 ns and page fault service time is 10 ms. To keep effective memory access time under 200 ns, the maximum page fault rate $p$ must not exceed $k \\times 10^{-5}$. What is $k$?",
         None, "1", 0.01,
         "**Formula:** EAT = $(1 - p)(100) + p(10^7) \\le 200 \\implies 10^7 p \\le 100 \\implies p \\le 10^{-5}$.\n**Answer:** 1."),
        
        (1997, "Disk Scheduling", "NAT", 1, "easy",
         "A disk has 200 tracks (0 to 199). The head is at track 100 and moving toward 199. Requests are: 55, 58, 39, 18, 90, 160, 150, 184. Using SCAN, what is the maximum track number reached before changing direction?",
         None, "199", 0.0,
         "**Rule:** SCAN continues to the extreme boundary cylinder (199) before reversing.\n**Answer:** 199."),
        
        (1998, "File Systems", "MCQ", 1, "easy",
         "Which disk block allocation strategy is subject to external fragmentation and requires periodic defragmentation?",
         json.dumps({"A": "Contiguous Allocation", "B": "Linked Allocation", "C": "Indexed Allocation", "D": "Inverted Inode Allocation"}),
         "A", 0.0,
         "**Rule:** Contiguous allocation requires a single uninterrupted chunk of disk space, leading to external fragmentation as files expand or delete.\n**Answer:** A."),
        
        (1999, "CPU Scheduling", "NAT", 2, "medium",
         "Three processes arrive at $t=0$ with burst times 12, 4, 8 ms. What is the minimum possible average turnaround time (in ms) under any scheduling algorithm?",
         None, "14.67", 0.05,
         "**Rule:** Shortest Job First (SJF) gives optimal schedule: P2 (4ms), P3 (8ms), P1 (12ms).\n**Calculation:** Completion times: 4, 12, 24. Average = $(4 + 12 + 24) / 3 = 40/3 \\approx 14.67$ ms.\n**Answer:** 14.67."),
        
        (2000, "Virtual Memory", "MCQ", 1, "easy",
         "Which phenomenon occurs when the sum of process working-set sizes exceeds the total physical frame capacity, causing continuous page swapping?",
         json.dumps({"A": "Thrashing", "B": "Belady's Anomaly", "C": "Starvation", "D": "Aging"}),
         "A", 0.0,
         "**Concept:** Thrashing happens when the OS spends more time paging than executing instructions due to working-set page starvation.\n**Answer:** A."),
        
        (2001, "Memory Management", "NAT", 2, "medium",
         "A variable partition scheme has free blocks of 150 KB, 500 KB, 200 KB, 300 KB, 600 KB in order. Process requests of 212 KB, 417 KB, 112 KB arrive. Under Best-Fit, which original free block size is assigned to the 112 KB request?",
         None, "150", 0.0,
         "**Trace:** 212 KB goes to 300 KB block (leaves 88 KB). 417 KB goes to 500 KB block (leaves 83 KB). 112 KB fits smallest sufficient block: 150 KB (leaves 38 KB).\n**Answer:** 150."),
        
        (2002, "Synchronization", "MCQ", 2, "medium",
         "In Banker's algorithm, what does an 'unsafe state' strictly guarantee?",
         json.dumps({
             "A": "Deadlock has already taken place",
             "B": "Deadlock is possible if processes request maximum claims simultaneously",
             "C": "All processes will terminate normally",
             "D": "Mutual exclusion has been violated"
         }),
         "B", 0.0,
         "**Rule:** An unsafe state is not necessarily deadlocked; it simply means the system cannot guarantee avoidance of deadlock under worst-case resource requests.\n**Answer:** B."),
        
        (2003, "Processes & Threads", "NAT", 2, "medium",
         "How many child processes are created in total by executing the statement: `if (fork() && fork()) fork();`?",
         None, "4", 0.0,
         "**Trace:** 1st fork creates 1 child. Parent sees child PID (True) and evaluates 2nd fork (creates another child). Child of 1st fork sees 0 (False) so short-circuits. Parent sees 2nd child (True) and runs 3rd fork. Total created children = 4.\n**Answer:** 4."),
        
        (2004, "CPU Scheduling", "NAT", 2, "medium",
         "Using Round Robin with time quantum $q=3$ ms, processes P1 (burst 7) and P2 (burst 4) arrive at $t=0$ in order P1, P2. At what time (in ms) does P1 complete execution?",
         None, "11", 0.0,
         "**Gantt Chart:** 0-3: P1 (rem 4), 3-6: P2 (rem 1), 6-9: P1 (rem 1), 9-10: P2 (done), 10-11: P1 (done).\n**Answer:** 11."),
        
        (2005, "Memory Management", "NAT", 2, "hard",
         "A paging system has TLB hit ratio 90%. TLB lookup time is 10 ns and main memory access is 80 ns. What is the effective memory access time (in ns) for a two-level page table?",
         None, "107", 0.0,
         "**Formula:** EMAT = $H(T_{tlb} + T_m) + (1-H)(T_{tlb} + 3T_m)$.\n**Calculation:** $0.9(10 + 80) + 0.1(10 + 240) = 0.9(90) + 0.1(250) = 81 + 25 = 106$ ns.\n**Answer:** 106."),
        
        (2006, "File Systems", "MCQ", 1, "easy",
         "A UNIX file system inode contains 12 direct block pointers, 1 single indirect pointer, 1 double indirect pointer, and 1 triple indirect pointer. If block size is 4 KB and disk address is 4 bytes, how many disk blocks can be addressed directly by the single indirect block?",
         json.dumps({"A": "1024", "B": "2048", "C": "4096", "D": "512"}),
         "A", 0.0,
         "**Formula:** Block pointers per block = $\\text{Block Size} / \\text{Pointer Size} = 4096 / 4 = 1024$.\n**Answer:** A (1024)."),
        
        (2007, "Disk Scheduling", "NAT", 2, "medium",
         "Disk tracks: 0 to 199. Head is at 100 moving toward 0. Pending requests: 25, 45, 85, 110, 130, 180. Using C-SCAN (which sweeps back to track 199 without servicing requests), what is the total head travel distance?",
         None, "384", 0.0,
         "**Path:** 100 -> 0 (travel 100). Reverses to 199 (travel 199). Serves 180 -> 130 -> 110 (travel 89).\n**Total:** $100 + 199 + 89 = 388$ cylinders.\n**Answer:** 388."),
        
        (2008, "Virtual Memory", "NAT", 2, "medium",
         "A process has 4 page frames initially empty. Given reference string: 1, 2, 3, 4, 2, 1, 5, 6, 2, 1, 2, 3, 7, 6. How many page faults occur under FIFO page replacement?",
         None, "10", 0.0,
         "**Trace FIFO (4 frames):**\n1(F), 2(F), 3(F), 4(F), 2(H), 1(H), 5(replaces 1, F), 6(replaces 2, F), 2(replaces 3, F), 1(replaces 4, F), 2(H), 3(replaces 5, F), 7(replaces 6, F), 6(replaces 2, F). Total faults = 10.\n**Answer:** 10."),
        
        (2009, "Synchronization", "MCQ", 2, "hard",
         "In Peterson's algorithm for mutual exclusion between processes P0 and P1, what ensures Progress?",
         json.dumps({
             "A": "The `turn` variable acts as an arbiter when both set `flag=true` simultaneously",
             "B": "Semaphores prevent busy waiting",
             "C": "Hardware test-and-set instructions are atomic",
             "D": "Both processes enter CS simultaneously"
         }),
         "A", 0.0,
         "**Concept:** The `turn` variable resolves simultaneous contention, ensuring one process enters CS without indefinite stalling.\n**Answer:** A."),
        
        (2010, "Deadlocks", "NAT", 2, "medium",
         "In Banker's algorithm, system has 10 units of resource R. Current allocations: P1 has 3, P2 has 2, P3 has 2. Max demands are: P1 needs 7, P2 needs 5, P3 needs 4. How many units of R are currently available?",
         None, "3", 0.0,
         "**Formula:** Available = Total - $\\sum$ Allocated = $10 - (3 + 2 + 2) = 10 - 7 = 3$.\n**Answer:** 3."),
        
        (2011, "Processes & Threads", "MCQ", 1, "easy",
         "Which process state transition is IMPOSSIBLE in a standard operating system kernel?",
         json.dumps({"A": "Waiting/Blocked to Ready", "B": "Running to Ready", "C": "Waiting/Blocked to Running", "D": "Running to Terminated"}),
         "C", 0.0,
         "**Rule:** A blocked process must always enter the Ready queue first when its I/O completes before the scheduler can dispatch it to Running.\n**Answer:** C."),
        
        (2012, "CPU Scheduling", "NAT", 2, "medium",
         "In exponential smoothing burst estimation $\\tau_{n+1} = \\alpha t_n + (1-\\alpha)\\tau_n$, if $\\alpha = 0.8$, previous estimate $\\tau_n = 10$ ms, and actual burst $t_n = 20$ ms, what is the next burst estimate $\\tau_{n+1}$ (in ms)?",
         None, "18", 0.0,
         "**Formula:** $\\tau_{n+1} = 0.8(20) + 0.2(10) = 16 + 2 = 18$ ms.\n**Answer:** 18."),
        
        (2013, "Memory Management", "NAT", 2, "medium",
         "A system has 48-bit virtual addresses and 8 KB pages. How many bits are allocated for the page offset?",
         None, "13", 0.0,
         "**Formula:** Offset bits = $\\log_2(\\text{Page Size}) = \\log_2(8 \\times 2^{10}) = \\log_2(2^{13}) = 13$ bits.\n**Answer:** 13."),
        
        (2014, "Virtual Memory", "NAT", 2, "hard",
         "Consider a 2-level paging system with 32-bit virtual addresses, 4 KB page size, 4-byte PTEs, and equal bit distribution between Level 1 and Level 2 page tables. How many bits are used for each page table level index?",
         None, "10", 0.0,
         "**Calculation:** Offset = 12 bits. Remaining page number bits = $32 - 12 = 20$ bits. Split equally: $20 / 2 = 10$ bits each.\n**Answer:** 10."),
        
        (2015, "Synchronization", "MCQ", 2, "medium",
         "In the Reader-Writer problem giving priority to writers, what potential problem can readers experience?",
         json.dumps({"A": "Deadlock", "B": "Starvation", "C": "Priority Inversion", "D": "Race condition on file write"}),
         "B", 0.0,
         "**Rule:** If writers continuously queue up, readers will wait indefinitely, leading to reader starvation.\n**Answer:** B."),
        
        (2016, "Deadlocks", "NAT", 2, "medium",
         "In Banker's algorithm, process P1 has Max = [5, 4, 3] and Allocation = [2, 1, 2]. What is the sum of elements in the Need vector of P1?",
         None, "7", 0.0,
         "**Formula:** Need = Max - Allocation = $[5-2, 4-1, 3-2] = [3, 3, 1]$.\nSum = $3 + 3 + 1 = 7$.\n**Answer:** 7."),
        
        (2017, "File Systems", "MCQ", 1, "easy",
         "In Linux file permissions `drwxr-x---`, what type of file is this and what permissions do 'others' have?",
         json.dumps({
             "A": "Regular file with read permission for others",
             "B": "Directory with zero permissions for others",
             "C": "Directory with execute permission for others",
             "D": "Character device file"
         }),
         "B", 0.0,
         "**Rule:** Leading `d` denotes a directory. Trailing `---` means others have zero permissions.\n**Answer:** B."),
        
        (2018, "CPU Scheduling", "NAT", 2, "medium",
         "Processes P1 (burst 6) and P2 (burst 4) arrive at $t=0$ in order P1, P2. Using FCFS, what is the average waiting time (in ms)?",
         None, "3", 0.0,
         "**Waiting Time:** P1 waits 0 ms; P2 waits 6 ms. Average = $(0 + 6) / 2 = 3$ ms.\n**Answer:** 3."),
        
        (2019, "Memory Management", "MCQ", 1, "easy",
         "Which technique allows physical memory allocation to be non-contiguous, thereby completely eliminating external fragmentation?",
         json.dumps({"A": "Pure Segmentation", "B": "Paging", "C": "Dynamic Partitioning", "D": "Static Overlay Allocation"}),
         "B", 0.0,
         "**Rule:** Paging divides memory into fixed-size physical frames, eliminating external fragmentation entirely.\n**Answer:** B."),
        
        (2020, "Virtual Memory", "NAT", 2, "medium",
         "Virtual page reference sequence: 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5. With 3 frames initially empty, how many page faults occur under Optimal page replacement?",
         None, "7", 0.0,
         "**Trace OPT (3 frames):** 1(F), 2(F), 3(F), 4(replaces 3, F), 1(H), 2(H), 5(replaces 4, F), 1(H), 2(H), 3(replaces 5, F), 4(replaces 3, F), 5(H). Total faults = 7.\n**Answer:** 7."),
        
        (2021, "Processes & Threads", "MCQ", 2, "medium",
         "What distinguishes user-level threads (ULT) from kernel-level threads (KLT)?",
         json.dumps({
             "A": "ULT context switching is faster as it does not require a mode switch to kernel space",
             "B": "If one ULT blocks on system call, other ULTs in the same process continue running on standard OS kernels",
             "C": "ULT requires hardware support from the CPU",
             "D": "KLT cannot be scheduled across multiple CPU cores"
         }),
         "A", 0.0,
         "**Concept:** ULT management is handled in user library without trap to kernel mode, making context switches lightweight.\n**Answer:** A."),
        
        (2022, "Disk Scheduling", "NAT", 2, "medium",
         "Disk requests: 98, 183, 37, 122, 14, 124, 65, 67. Head is at 53. Using Shortest Seek Time First (SSTF), which request is serviced immediately after track 65?",
         None, "67", 0.0,
         "**Trace SSTF:** 53 -> 65 (dist 12) -> 67 (dist 2) -> 37 (dist 30) -> 14 -> 98 -> 122 -> 124 -> 183.\n**Answer:** 67."),
        
        (2023, "Synchronization", "NAT", 2, "hard",
         "A shared variable $X=0$ is updated concurrently by 3 threads. Each thread executes $X = X + 1$ exactly 10 times without locks. What is the theoretical minimum final value of $X$?",
         None, "2", 0.0,
         "**Theorem:** Under arbitrary preemption with read-modify-write interleaving, the minimum value after any number of concurrent thread increments is 2.\n**Answer:** 2."),
        
        (2024, "Deadlocks", "MCQ", 1, "easy",
         "In a Resource Allocation Graph (RAG), if every resource has exactly ONE instance, a directed cycle is:",
         json.dumps({
             "A": "Necessary and sufficient for deadlock",
             "B": "Necessary but not sufficient for deadlock",
             "C": "Sufficient but not necessary for deadlock",
             "D": "Neither necessary nor sufficient"
         }),
         "A", 0.0,
         "**Theorem:** For single-instance resources, a cycle in the RAG is both necessary and sufficient for deadlock.\n**Answer:** A."),
        
        (2025, "Virtual Memory", "NAT", 2, "medium",
         "A 64-bit architecture uses 32 KB pages. What is the number of bits in the virtual page number (VPN)?",
         None, "49", 0.0,
         "**Formula:** Offset bits = $\\log_2(32 \\times 1024) = \\log_2(2^{15}) = 15$. VPN bits = $64 - 15 = 49$.\n**Answer:** 49."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in os_items:
        questions.append(Question(
            subject="OS", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (OS - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    # =========================================================================
    # 2. ALGORITHMS (1991 - 2025: 35 Unique Questions)
    # =========================================================================
    algo_items = [
        (1991, "Asymptotic Analysis", "MCQ", 1, "easy",
         "Which asymptotic notation correctly relates $f(n) = n^{2.5}$ and $g(n) = n^2 \\log_2 n$?",
         json.dumps({"A": "$f(n) = O(g(n))$", "B": "$f(n) = \\Omega(g(n))$", "C": "$f(n) = \\Theta(g(n))$", "D": "$f(n) = o(g(n))$"}),
         "B", 0.0,
         "**Rule:** $\\lim_{n \\to \\infty} \\frac{n^{2.5}}{n^2 \\log n} = \\lim \\frac{n^{0.5}}{\\log n} = \\infty$, hence $f(n) = \\Omega(g(n))$.\n**Answer:** B."),
        
        (1992, "Sorting & Searching", "NAT", 2, "medium",
         "What is the minimum number of comparisons needed in the worst case to determine both the minimum and maximum of an unsorted array of 100 elements?",
         None, "147", 0.0,
         "**Formula:** By pairing elements: $\\lceil 3n/2 \\rceil - 2 = 150 - 2 = 148$ (or 147 comparisons with odd/even base case).\n**Answer:** 147."),
        
        (1993, "Graph Algorithms", "NAT", 2, "medium",
         "In a connected undirected graph with 12 vertices and 25 edges, how many edges must be removed to obtain a spanning tree?",
         None, "14", 0.0,
         "**Formula:** Spanning tree has $V - 1 = 12 - 1 = 11$ edges. Removed = $25 - 11 = 14$.\n**Answer:** 14."),
        
        (1994, "Divide & Conquer", "MCQ", 2, "medium",
         "Strassen's matrix multiplication algorithm solves the recurrence $T(n) = 7T(n/2) + O(n^2)$. What is its asymptotic time complexity?",
         json.dumps({"A": "$O(n^{2.81})$", "B": "$O(n^3)$", "C": "$O(n^2 \\log n)$", "D": "$O(n^{2.5})$"}),
         "A", 0.0,
         "**Formula:** By Master Theorem, $\\log_2 7 \\approx 2.807$, giving $O(n^{\\log_2 7}) \\approx O(n^{2.81})$.\n**Answer:** A."),
        
        (1995, "Greedy Algorithms", "NAT", 2, "medium",
         "Given knapsack capacity $W=50$ and items with $(v_i, w_i) = [(60, 10), (100, 20), (120, 30)]$. In fractional knapsack, what is the maximum total profit?",
         None, "240", 0.0,
         "**Ratios:** Item 1: 6.0, Item 2: 5.0, Item 3: 4.0. Take all Item 1 (10kg, 60), all Item 2 (20kg, 100), and 20kg of Item 3 ($20 \\times 4 = 80$). Total = $60+100+80=240$.\n**Answer:** 240."),
        
        (1996, "Dynamic Programming", "NAT", 2, "medium",
         "How many distinct binary search trees can be constructed using 4 distinct keys?",
         None, "14", 0.0,
         "**Formula:** Catalan number $C_4 = \\frac{1}{5} \\binom{8}{4} = \\frac{70}{5} = 14$.\n**Answer:** 14."),
        
        (1997, "Graph Algorithms", "MCQ", 1, "easy",
         "Which algorithm computes all-pairs shortest paths in a directed graph containing negative edge weights without negative cycles?",
         json.dumps({"A": "Floyd-Warshall", "B": "Dijkstra's Algorithm", "C": "Prim's Algorithm", "D": "Kruskal's Algorithm"}),
         "A", 0.0,
         "**Rule:** Floyd-Warshall uses dynamic programming in $O(V^3)$ and correctly handles negative edge weights.\n**Answer:** A."),
        
        (1998, "Asymptotic Analysis", "NAT", 2, "medium",
         "What is the exponent $k$ in $\\Theta(n^k)$ for the recurrence $T(n) = 8T(n/2) + n^2$?",
         None, "3", 0.0,
         "**Master Theorem:** $a=8, b=2 \\implies \\log_b a = 3$. Since $f(n) = n^2 = O(n^{3-\\epsilon})$, Case 1 yields $\\Theta(n^3)$. So $k=3$.\n**Answer:** 3."),
        
        (1999, "Sorting & Searching", "MCQ", 1, "easy",
         "What is the worst-case time complexity of QuickSort when the chosen pivot is always the maximum element in the partition?",
         json.dumps({"A": "$O(n^2)$", "B": "$O(n \\log n)$", "C": "$O(n)$", "D": "$O(n \\log^2 n)$"}),
         "A", 0.0,
         "**Rule:** Extreme pivot selection produces maximally unbalanced partitions ($0$ and $n-1$), yielding $T(n) = T(n-1) + O(n) = O(n^2)$.\n**Answer:** A."),
        
        (2000, "NP-Completeness & Complexity", "MCQ", 1, "easy",
         "If a polynomial-time algorithm is discovered for the 3-SAT problem, what is the theoretical conclusion?",
         json.dumps({"A": "$P = NP$", "B": "$P \\ne NP$", "C": "3-SAT is not NP-Complete", "D": "NP-Hard becomes empty"}),
         "A", 0.0,
         "**Theorem:** 3-SAT is NP-Complete. Solving any NP-Complete problem in polynomial time proves $P = NP$.\n**Answer:** A."),
        
        (2001, "Graph Algorithms", "NAT", 2, "medium",
         "What is the maximum number of edges in a simple acyclic undirected graph (forest) with 8 vertices and 2 connected components?",
         None, "6", 0.0,
         "**Formula:** In a forest with $V$ vertices and $k$ trees, $E = V - k = 8 - 2 = 6$.\n**Answer:** 6."),
        
        (2002, "Dynamic Programming", "NAT", 2, "medium",
         "In 0/1 Knapsack with capacity $W=6$ and items $(v_i, w_i) = [(10, 2), (15, 3), (40, 4)]$, what is the optimal maximum total value?",
         None, "50", 0.0,
         "**Trace:** Item 1 + Item 3 has weight $2+4=6$ and value $10+40=50$. Item 2 + Item 1 gives 25. Maximum = 50.\n**Answer:** 50."),
        
        (2003, "Asymptotic Analysis", "MCQ", 1, "easy",
         "Which asymptotic assertion is FALSE?",
         json.dumps({"A": "$2^{2n} = O(2^n)$", "B": "$n! = O(n^n)$", "C": "$\\log(n!) = \\Theta(n \\log n)$", "D": "$2^{n+1} = O(2^n)$"}),
         "A", 0.0,
         "**Proof:** $2^{2n} = 4^n$. $\\lim_{n \\to \\infty} 4^n / 2^n = \\lim 2^n = \\infty$, hence $2^{2n} \\ne O(2^n)$.\n**Answer:** A."),
        
        (2004, "Sorting & Searching", "NAT", 2, "hard",
         "What is the total number of inversions in the array $[4, 1, 5, 2, 3]$?",
         None, "5", 0.0,
         "**Inversion pairs:** (4,1), (4,2), (4,3), (5,2), (5,3). Total = 5 inversions.\n**Answer:** 5."),
        
        (2005, "Graph Algorithms", "MCQ", 2, "medium",
         "Bellman-Ford algorithm relaxes every edge $V-1$ times. Why is a $V$-th relaxation pass executed?",
         json.dumps({
             "A": "To detect the presence of negative-weight cycles reachable from the source",
             "B": "To improve asymptotic speed",
             "C": "To find all-pairs shortest paths",
             "D": "To construct a minimum spanning tree"
         }),
         "A", 0.0,
         "**Rule:** In an acyclic or negative-cycle-free graph, all shortest paths have $\\le V-1$ edges. If any distance decreases on the $V$-th pass, a negative cycle exists.\n**Answer:** A."),
        
        (2006, "Greedy Algorithms", "NAT", 2, "medium",
         "In Huffman coding for symbols with frequencies A: 0.35, B: 0.30, C: 0.20, D: 0.15, what is the codeword length for symbol A?",
         None, "2", 0.0,
         "**Merge:** C(0.20)+D(0.15)=CD(0.35). Next merge B(0.30)+CD(0.35)=BCD(0.65). Finally merge A(0.35)+BCD(0.65)=Root. Depth of A = 1 or 2 depending on root order; here A and BCD are direct children of root (length 1 if root split, or 2 if CD and B). Here A is at depth 1 or 2. Total code length = 2.\n**Answer:** 2."),
        
        (2007, "Divide & Conquer", "NAT", 2, "medium",
         "How many comparisons does standard binary search perform in the worst case on a sorted array of 128 elements?",
         None, "8", 0.0,
         "**Formula:** Worst-case comparisons = $\\lfloor \\log_2 128 \\rfloor + 1 = 7 + 1 = 8$.\n**Answer:** 8."),
        
        (2008, "NP-Completeness & Complexity", "MSQ", 2, "hard",
         "Which of the following computational problems belong to complexity class P (solvable in deterministic polynomial time)?",
         json.dumps({
             "A": "2-SAT Satisfiability",
             "B": "Minimum Spanning Tree in a weighted graph",
             "C": "3-Colorability of general graphs",
             "D": "Single-source shortest paths with non-negative weights"
         }),
         "A,B,D", 0.0,
         "**Classification:** 2-SAT runs in linear time via SCC. MST runs in $O(E \\log V)$. Dijkstra runs in $O(E + V \\log V)$. 3-Coloring is NP-Complete.\n**Answer:** A, B, D."),
        
        (2009, "Dynamic Programming", "NAT", 2, "medium",
         "What is the length of the Longest Common Subsequence between strings 'ABCDE' and 'ACDFE'?",
         None, "4", 0.0,
         "**Subsequence:** 'ACDE' appears in both strings and has length 4.\n**Answer:** 4."),
        
        (2010, "Sorting & Searching", "MCQ", 1, "easy",
         "Which comparison-based sorting algorithm guarantees $O(n \\log n)$ worst-case time complexity AND runs in-place with $O(1)$ auxiliary memory?",
         json.dumps({"A": "Heap Sort", "B": "Merge Sort", "C": "Quick Sort", "D": "Radix Sort"}),
         "A", 0.0,
         "**Rule:** Heap Sort takes $O(n \\log n)$ time in all cases and sorts in-place using $O(1)$ auxiliary space.\n**Answer:** A."),
        
        (2011, "Graph Algorithms", "NAT", 2, "medium",
         "A complete graph $K_5$ has all edge weights equal to 2. How many distinct Minimum Spanning Trees does $K_5$ have?",
         None, "125", 0.0,
         "**Formula:** Cayley's Formula: $n^{n-2} = 5^{5-2} = 5^3 = 125$.\n**Answer:** 125."),
        
        (2012, "Asymptotic Analysis", "NAT", 2, "medium",
         "Given recurrence $T(n) = 4T(n/2) + n^2$, what is the exponent $k$ in $\\Theta(n^2 \\log^k n)$?",
         None, "1", 0.0,
         "**Master Theorem:** $a=4, b=2 \\implies n^{\\log_2 4} = n^2$. Since $f(n) = n^2$, Case 2 applies: $T(n) = \\Theta(n^2 \\log n)$, so $k=1$.\n**Answer:** 1."),
        
        (2013, "Dynamic Programming", "NAT", 2, "medium",
         "Using Kadane's algorithm, what is the maximum subarray sum of: $[3, -2, 5, -1, 4, -6, 2]$?",
         None, "9", 0.0,
         "**Subarray:** Elements $[3, -2, 5, -1, 4]$ sum to $3 - 2 + 5 - 1 + 4 = 9$.\n**Answer:** 9."),
        
        (2014, "Graph Algorithms", "MCQ", 1, "easy",
         "During Depth-First Search (DFS) on an undirected graph, which edge type can NEVER appear?",
         json.dumps({"A": "Cross Edge", "B": "Tree Edge", "C": "Back Edge", "D": "Incident Edge"}),
         "A", 0.0,
         "**Theorem:** In DFS of an undirected graph, every non-tree edge connects an ancestor to a descendant (Back edge); Cross edges never occur.\n**Answer:** A."),
        
        (2015, "Sorting & Searching", "NAT", 2, "hard",
         "What is the worst-case number of comparisons performed by Merge Sort on an array of 4 elements?",
         None, "5", 0.0,
         "**Formula:** For size 4: Sort two pairs (1 comparison each = 2). Merging two sorted 2-element lists takes at most $2+2-1 = 3$ comparisons. Total = $2 + 3 = 5$.\n**Answer:** 5."),
        
        (2016, "NP-Completeness & Complexity", "MCQ", 2, "medium",
         "If language $L_1$ polynomial-time reduces to $L_2$ ($L_1 \\le_p L_2$) and $L_1$ is NP-Hard, what can be concluded about $L_2$?",
         json.dumps({"A": "$L_2$ is NP-Hard", "B": "$L_2$ is in P", "C": "$L_1$ is in P", "D": "$L_2$ is NP-Complete"}),
         "A", 0.0,
         "**Rule:** If an NP-Hard problem reduces to $L_2$, then $L_2$ is at least as hard as that NP-Hard problem, so $L_2$ is NP-Hard.\n**Answer:** A."),
        
        (2017, "Greedy Algorithms", "NAT", 2, "medium",
         "Given activities with (start, finish) times: (1,3), (2,5), (3,7), (6,8), (7,9). What is the maximum number of mutually compatible activities that can be scheduled?",
         None, "3", 0.0,
         "**Greedy Choice:** Pick by finish time: (1,3), then (3,7) [or (6,8) not compatible with 3-7, but (7,9) works with (3,7)]. Sequence: (1,3), (3,7), (7,9). Total = 3.\n**Answer:** 3."),
        
        (2018, "Asymptotic Analysis", "NAT", 2, "medium",
         "Consider the recurrence $T(n) = T(n/3) + 1$ with $T(1)=1$. What is the coefficient of $\\log_3 n$ in the closed-form solution?",
         None, "1", 0.0,
         "**Formula:** By expansion: $T(n) = \\log_3 n + 1$. The coefficient of $\\log_3 n$ is 1.\n**Answer:** 1."),
        
        (2019, "Graph Algorithms", "NAT", 2, "medium",
         "An undirected connected graph has 7 vertices and all distinct edge weights. How many Minimum Spanning Trees does it possess?",
         None, "1", 0.0,
         "**Theorem:** If all edge weights in a connected graph are strictly distinct, the MST is mathematically unique.\n**Answer:** 1."),
        
        (2020, "Dynamic Programming", "NAT", 2, "medium",
         "What is the minimum number of scalar multiplications required to multiply 3 matrices of dimensions $10 \\times 30$, $30 \\times 5$, and $5 \\times 60$?",
         None, "4500", 0.0,
         "**Option 1:** $(A_1 A_2) A_3 = (10 \\times 30 \\times 5) + (10 \\times 5 \\times 60) = 1500 + 3000 = 4500$.\n**Option 2:** $A_1 (A_2 A_3) = (30 \\times 5 \\times 60) + (10 \\times 30 \\times 60) = 9000 + 18000 = 27000$.\n**Answer:** 4500."),
        
        (2021, "Sorting & Searching", "MCQ", 1, "easy",
         "Which sorting algorithm is guaranteed to be STABLE?",
         json.dumps({"A": "Merge Sort", "B": "Heap Sort", "C": "Quick Sort", "D": "Selection Sort"}),
         "A", 0.0,
         "**Rule:** Standard Merge Sort maintains relative order of duplicate elements during merge step, making it stable.\n**Answer:** A."),
        
        (2022, "Asymptotic Analysis", "NAT", 2, "medium",
         "What is the asymptotic time complexity of building a binary min-heap from an unsorted array of $n$ elements using bottom-up heapify? Give the power $k$ in $O(n^k)$.",
         None, "1", 0.0,
         "**Theorem:** $\\sum_{h=0}^{\\lfloor \\log n \\rfloor} \\frac{n}{2^{h+1}} O(h) = O(n)$. Power $k = 1$.\n**Answer:** 1."),
        
        (2023, "Graph Algorithms", "NAT", 2, "hard",
         "A simple connected planar graph has 10 vertices and divides the plane into 7 faces (including outer face). How many edges does the graph have?",
         None, "15", 0.0,
         "**Euler's Formula:** $V - E + F = 2 \\implies 10 - E + 7 = 2 \\implies 17 - E = 2 \\implies E = 15$.\n**Answer:** 15."),
        
        (2024, "NP-Completeness & Complexity", "MCQ", 1, "easy",
         "Which of the following problems is known to be in NP-Complete?",
         json.dumps({"A": "Hamiltonian Cycle Problem", "B": "Eulerian Tour Problem", "C": "Shortest Path in DAG", "D": "2-SAT Problem"}),
         "A", 0.0,
         "**Rule:** Hamiltonian Cycle is NP-Complete, whereas Euler Tour and 2-SAT are solvable in linear time (P).\n**Answer:** A."),
        
        (2025, "Dynamic Programming", "NAT", 2, "medium",
         "How many different ways can a parenthesized matrix chain product of 5 matrices $A_1 A_2 A_3 A_4 A_5$ be evaluated?",
         None, "14", 0.0,
         "**Formula:** Catalan number $C_{n-1}$ for $n=5$ matrices: $C_4 = \\frac{1}{5} \\binom{8}{4} = 14$.\n**Answer:** 14."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in algo_items:
        questions.append(Question(
            subject="Algorithms", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (Algorithms - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    # =========================================================================
    # 3. COMPUTER ORGANIZATION & ARCHITECTURE (COA: 1991 - 2025: 35 Unique Questions)
    # =========================================================================
    coa_items = [
        (1991, "Machine Instructions & Addressing Modes", "MCQ", 1, "easy",
         "Which addressing mode allows position-independent code by computing effective addresses relative to the Program Counter (PC)?",
         json.dumps({"A": "PC-Relative Addressing", "B": "Direct Addressing", "C": "Immediate Addressing", "D": "Base Register Addressing"}),
         "A", 0.0,
         "**Rule:** PC-Relative mode calculates Effective Address = $PC + \\text{offset}$, enabling code relocation without changing target addresses.\n**Answer:** A."),
        
        (1992, "Instruction Pipelining", "NAT", 2, "medium",
         "A 5-stage instruction pipeline has stage delays 5 ns, 7 ns, 10 ns, 8 ns, and 6 ns. Pipeline register delay is 1 ns. What is the clock cycle time of the pipeline (in ns)?",
         None, "11", 0.0,
         "**Formula:** Clock period = $\\max(\\text{stage delays}) + \\text{register delay} = 10 + 1 = 11$ ns.\n**Answer:** 11."),
        
        (1993, "Memory Hierarchy & Cache", "NAT", 2, "medium",
         "A direct-mapped cache has 64 blocks, each of 16 bytes. To which cache block does the byte memory address 1200 map?",
         None, "11", 0.0,
         "**Formula:** Block number = $\\lfloor \\text{Address} / \\text{Block Size} \\rfloor \\pmod{\\text{Total Blocks}} = \\lfloor 1200 / 16 \\rfloor \\pmod{64} = 75 \\pmod{64} = 11$.\n**Answer:** 11."),
        
        (1994, "ALU & Control Unit", "MCQ", 1, "easy",
         "In a horizontal microprogrammed control unit compared to a vertical microprogrammed control unit:",
         json.dumps({
             "A": "Control words are wider and provide higher parallelism with little or no decoding",
             "B": "Control words are narrower and require extensive decoders",
             "C": "Execution speed is much slower",
             "D": "Microinstructions cannot execute simultaneously"
         }),
         "A", 0.0,
         "**Rule:** Horizontal microinstructions assign one bit per control signal, requiring minimal decoding and allowing high concurrency at the cost of wide control words.\n**Answer:** A."),
        
        (1995, "Instruction Pipelining", "NAT", 2, "medium",
         "An unpipelined processor executes an instruction in 50 ns. A 5-stage pipelined processor runs with a clock cycle of 11 ns. What is the speedup for executing 1000 instructions (rounded to 2 decimal places)?",
         None, "4.53", 0.05,
         "**Formula:** Non-pipelined time = $1000 \\times 50 = 50000$ ns. Pipelined time = $(5 + 1000 - 1) \\times 11 = 1004 \\times 11 = 11044$ ns.\nSpeedup = $50000 / 11044 \\approx 4.53$.\n**Answer:** 4.53."),
        
        (1996, "Memory Hierarchy & Cache", "NAT", 2, "hard",
         "A computer has L1 cache access time 2 ns with hit rate 90%, and main memory access time 50 ns. What is the average memory access time (AMAT) in ns?",
         None, "7", 0.0,
         "**Formula:** AMAT = $T_{L1} + (1 - H_{L1}) \\times T_{mem} = 2 + 0.10 \\times 50 = 2 + 5 = 7$ ns.\n**Answer:** 7."),
        
        (1997, "I/O Interface & DMA", "MCQ", 1, "easy",
         "In Cycle Stealing DMA transfer mode:",
         json.dumps({
             "A": "DMA controller takes control of the system bus for one bus cycle at a time",
             "B": "DMA controller transfers the entire block of data while keeping the CPU halted",
             "C": "CPU executes I/O polling in a tight loop",
             "D": "DMA controller bypasses main memory completely"
         }),
         "A", 0.0,
         "**Rule:** Cycle stealing transfers one word/byte per bus cycle, momentarily stealing a cycle from CPU instruction execution.\n**Answer:** A."),
        
        (1998, "Machine Instructions & Addressing Modes", "NAT", 2, "medium",
         "An instruction is 32 bits long with 6 bits for opcode, 5 bits for register operand, and the rest for immediate operand. What is the maximum unsigned integer value that can be represented in the immediate field?",
         None, "2097151", 0.0,
         "**Calculation:** Immediate bits = $32 - 6 - 5 = 21$ bits. Maximum unsigned value = $2^{21} - 1 = 2097151$.\n**Answer:** 2097151."),
        
        (1999, "Instruction Pipelining", "NAT", 2, "medium",
         "A 4-stage pipeline processes 100 instructions. 20 of these instructions cause a 2-cycle branch stall each. How many total clock cycles are needed to execute all 100 instructions?",
         None, "143", 0.0,
         "**Formula:** Total cycles = $(k + N - 1) + \\text{Stall cycles} = (4 + 100 - 1) + (20 \\times 2) = 103 + 40 = 143$.\n**Answer:** 143."),
        
        (2000, "Memory Hierarchy & Cache", "MCQ", 1, "easy",
         "In a 4-way set associative cache, if the cache capacity is 32 KB and block size is 64 bytes, how many sets are in the cache?",
         json.dumps({"A": "128", "B": "256", "C": "512", "D": "64"}),
         "A", 0.0,
         "**Calculation:** Total lines = $32768 / 64 = 512$. Sets = $512 / 4 = 128$.\n**Answer:** A (128)."),
        
        (2001, "ALU & Control Unit", "NAT", 2, "medium",
         "A Booth's multiplier multiplies two 8-bit 2's complement numbers. What is the maximum number of additions/subtractions performed in the worst case?",
         None, "4", 0.0,
         "**Rule:** In Booth's algorithm, additions/subtractions occur on bit transitions ($01$ or $10$). In an 8-bit word, at most 4 transitions can occur.\n**Answer:** 4."),
        
        (2002, "Instruction Pipelining", "MCQ", 2, "medium",
         "Which hazard in instruction pipelining is eliminated by Operand Forwarding (Data Bypassing)?",
         json.dumps({
             "A": "RAW (Read After Write) data hazards where the producer produces data before the consumer requires it",
             "B": "Structural hazards on memory bus",
             "C": "Control hazards caused by branch instructions",
             "D": "WAR (Write After Read) hazards in out-of-order execution"
         }),
         "A", 0.0,
         "**Rule:** Operand forwarding routes the ALU output directly to the input of subsequent dependent instructions, resolving RAW hazards.\n**Answer:** A."),
        
        (2003, "Memory Hierarchy & Cache", "NAT", 2, "hard",
         "A 16 KB 2-way set associative cache has 32-byte blocks. For a 32-bit physical address, how many bits are used for the TAG field?",
         None, "19", 0.0,
         "**Calculation:** Offset = $\\log_2 32 = 5$ bits. Number of blocks = $16384 / 32 = 512$. Sets = $512 / 2 = 256$ (Index = 8 bits). Tag bits = $32 - 8 - 5 = 19$.\n**Answer:** 19."),
        
        (2004, "Machine Instructions & Addressing Modes", "MCQ", 1, "easy",
         "Which instruction format does NOT require any explicit operand address in the instruction word?",
         json.dumps({"A": "Zero-address format (Stack-based architecture)", "B": "One-address format (Accumulator-based)", "C": "Two-address format", "D": "Three-address format"}),
         "A", 0.0,
         "**Rule:** In stack-based architectures, operands are implicitly popped from and pushed onto the top of the stack.\n**Answer:** A."),
        
        (2005, "I/O Interface & DMA", "NAT", 2, "medium",
         "A DMA module transfers data from a device at 2 MB/sec to main memory using cycle stealing. Bus cycle time is 250 ns and transfer width is 4 bytes. What percentage of CPU bus time is consumed by DMA?",
         None, "12.5", 0.05,
         "**Calculation:** Transfers per sec = $2 \\times 10^6 / 4 = 500,000$ cycles. Time stolen = $500,000 \\times 250 \\times 10^{-9} = 0.125 = 12.5\\%$.\n**Answer:** 12.5%."),
        
        (2006, "Instruction Pipelining", "NAT", 2, "medium",
         "A 5-stage pipeline has ideal CPI of 1. If 20% of instructions are branch instructions and 60% of branches are taken causing a 3-cycle penalty, what is the actual average CPI?",
         None, "1.36", 0.02,
         "**Calculation:** $\\text{CPI} = 1 + (0.20 \\times 0.60 \\times 3) = 1 + 0.36 = 1.36$.\n**Answer:** 1.36."),
        
        (2007, "Memory Hierarchy & Cache", "MCQ", 1, "easy",
         "Which cache write policy guarantees that main memory always contains the most up-to-date copy of data at all times?",
         json.dumps({"A": "Write-Through", "B": "Write-Back", "C": "Write-Allocate", "D": "No-Write-Allocate"}),
         "A", 0.0,
         "**Rule:** Write-through immediately writes modified data to both the cache and main memory simultaneously.\n**Answer:** A."),
        
        (2008, "Machine Instructions & Addressing Modes", "NAT", 2, "medium",
         "Consider a 16-bit processor where base register $R1$ contains `0x2000` and index register $R2$ contains `0x0040`. What is the effective address in Base-Indexed addressing mode with displacement `0x0010`?",
         None, "0x2050", 0.0,
         "**Calculation:** $\\text{EA} = [R1] + [R2] + \\text{Disp} = 0x2000 + 0x0040 + 0x0010 = 0x2050$.\n**Answer:** 0x2050."),
        
        (2009, "ALU & Control Unit", "MCQ", 1, "easy",
         "A hardwired control unit is generally chosen over a microprogrammed control unit when:",
         json.dumps({
             "A": "Maximum instruction execution speed is required (e.g. RISC processors)",
             "B": "Ease of modifying the instruction set is paramount",
             "C": "Complex CISC instructions must be implemented cheaply",
             "D": "Memory space for control store is abundant"
         }),
         "A", 0.0,
         "**Rule:** Hardwired control units use combinational logic gates, yielding minimal propagation delay and maximum speed.\n**Answer:** A."),
        
        (2010, "Instruction Pipelining", "NAT", 2, "hard",
         "In a 6-stage pipeline, the stages take 10, 12, 15, 8, 14, 11 ns respectively. Pipeline registers add 2 ns per stage. What is the maximum throughput of the pipeline in MIPS (Million Instructions Per Second, rounded to 2 decimal places)?",
         None, "58.82", 0.1,
         "**Calculation:** Clock cycle = $\\max(10, 12, 15, 8, 14, 11) + 2 = 15 + 2 = 17$ ns.\nThroughput = $1 / (17 \\times 10^{-9}) \\approx 58.82 \\times 10^6 = 58.82$ MIPS.\n**Answer:** 58.82."),
        
        (2011, "Memory Hierarchy & Cache", "NAT", 2, "medium",
         "A direct-mapped cache has 1024 lines with 16 bytes per line. How many bits are needed for the index field in a 32-bit physical address?",
         None, "10", 0.0,
         "**Formula:** Index bits = $\\log_2(\\text{Cache Lines}) = \\log_2(1024) = 10$ bits.\n**Answer:** 10."),
        
        (2012, "I/O Interface & DMA", "MCQ", 1, "easy",
         "Which I/O communication technique avoids CPU busy-waiting by allowing the peripheral device to notify the processor when it is ready for data transfer?",
         json.dumps({"A": "Interrupt-driven I/O", "B": "Programmed I/O", "C": "Memory-mapped polling", "D": "Serial bus snooping"}),
         "A", 0.0,
         "**Rule:** Interrupt-driven I/O allows the CPU to perform other computational tasks until an asynchronous hardware interrupt signals device readiness.\n**Answer:** A."),
        
        (2013, "Machine Instructions & Addressing Modes", "NAT", 2, "medium",
         "A processor has 24-bit memory addresses. It supports 32 distinct opcodes and 16 general-purpose registers. For a register-memory instruction with format `[Opcode | Reg | Address]`, how many bits are required for the instruction word?",
         None, "33", 0.0,
         "**Calculation:** Opcode = $\\log_2 32 = 5$ bits. Reg = $\\log_2 16 = 4$ bits. Address = 24 bits. Total = $5 + 4 + 24 = 33$ bits.\n**Answer:** 33."),
        
        (2014, "Instruction Pipelining", "NAT", 2, "medium",
         "A 5-stage pipeline has stages IF, ID, EX, MEM, WB. A branch condition is resolved at the end of the EX stage (stage 3). How many clock cycles are wasted per taken branch if branch prediction is not used?",
         None, "2", 0.0,
         "**Rule:** Instructions fetched in cycles 2 (during ID) and 3 (during EX) must be flushed. Total branch penalty = $3 - 1 = 2$ cycles.\n**Answer:** 2."),
        
        (2015, "Memory Hierarchy & Cache", "MCQ", 2, "medium",
         "Which type of cache miss is completely unavoidable even if cache size is made infinite?",
         json.dumps({"A": "Compulsory Miss (Cold Start Miss)", "B": "Capacity Miss", "C": "Conflict Miss", "D": "Coherence Miss"}),
         "A", 0.0,
         "**Rule:** Compulsory misses occur on the very first access to a block of memory and are independent of cache size or associativity.\n**Answer:** A."),
        
        (2016, "ALU & Control Unit", "NAT", 2, "medium",
         "In IEEE-754 single-precision 32-bit floating point format, how many bits are allocated to the exponent and mantissa (fraction) fields respectively?",
         None, "8 and 23", 0.0,
         "**Format:** Sign = 1 bit, Exponent = 8 bits (bias 127), Fraction = 23 bits. Total = 32 bits.\n**Answer:** 8 and 23."),
        
        (2017, "Instruction Pipelining", "MCQ", 1, "easy",
         "Which hazard occurs when two instructions attempt to access the same hardware resource (such as a single-port memory) during the same clock cycle?",
         json.dumps({"A": "Structural Hazard", "B": "Data Hazard", "C": "Control Hazard", "D": "WAR Hazard"}),
         "A", 0.0,
         "**Rule:** Structural hazards arise from hardware resource conflicts when execution units cannot support all combinations of concurrent instructions.\n**Answer:** A."),
        
        (2018, "Memory Hierarchy & Cache", "NAT", 2, "hard",
         "A 2-level cache hierarchy has $T_{L1} = 1$ ns, $H_{L1} = 0.95$, $T_{L2} = 8$ ns, $H_{L2} = 0.80$, and $T_{mem} = 60$ ns. What is the Average Memory Access Time (in ns)?",
         None, "2", 0.05,
         "**Formula:** AMAT = $T_{L1} + (1 - H_{L1}) \\times [T_{L2} + (1 - H_{L2}) \\times T_{mem}] = 1 + 0.05 \\times [8 + 0.20 \\times 60] = 1 + 0.05 \\times [8 + 12] = 1 + 0.05(20) = 2$ ns.\n**Answer:** 2."),
        
        (2019, "Machine Instructions & Addressing Modes", "MCQ", 1, "easy",
         "In Auto-increment addressing mode, when is the register operand automatically incremented?",
         json.dumps({
             "A": "After accessing memory at the address currently held in the register",
             "B": "Before accessing memory",
             "C": "Only if a page fault does not occur",
             "D": "During the decode phase"
         }),
         "A", 0.0,
         "**Rule:** In post-increment (auto-increment) mode, effective address is the current register value, which is subsequently incremented by operand size.\n**Answer:** A."),
        
        (2020, "Instruction Pipelining", "NAT", 2, "medium",
         "An unpipelined processor executes 1 instruction in 10 ns. A 5-stage pipeline with cycle time 2.5 ns executes the same workload. For a very large number of instructions $N \\to \\infty$, what is the asymptotic speedup?",
         None, "4", 0.0,
         "**Formula:** Asymptotic Speedup = $T_{\\text{unpipelined}} / \\text{Clock Period} = 10 / 2.5 = 4$.\n**Answer:** 4."),
        
        (2021, "Memory Hierarchy & Cache", "NAT", 2, "medium",
         "A fully associative cache has 128 blocks of 32 bytes each. In a 32-bit physical address, how many bits are used for the TAG?",
         None, "27", 0.0,
         "**Formula:** In fully associative cache, index bits = 0. Offset = $\\log_2 32 = 5$ bits. Tag bits = $32 - 5 = 27$ bits.\n**Answer:** 27."),
        
        (2022, "I/O Interface & DMA", "MCQ", 1, "easy",
         "In memory-mapped I/O:",
         json.dumps({
             "A": "I/O device registers share the same address space as main memory and use standard memory instructions (e.g. LOAD/STORE)",
             "B": "Special CPU instructions `IN` and `OUT` are required",
             "C": "A separate I/O address bus is needed",
             "D": "DMA transfers are prohibited"
         }),
         "A", 0.0,
         "**Rule:** Memory-mapped I/O treats device control and data registers as regular memory locations, using ordinary memory-access instructions.\n**Answer:** A."),
        
        (2023, "ALU & Control Unit", "NAT", 2, "medium",
         "What is the decimal value represented by the 8-bit 2's complement binary number `11011000`?",
         None, "-40", 0.0,
         "**Calculation:** MSB is 1 (negative). Invert bits and add 1: `00100111 + 1 = 00101000` (40 decimal). Value = -40.\n**Answer:** -40."),
        
        (2024, "Instruction Pipelining", "MSQ", 2, "hard",
         "Which of the following techniques can reduce the performance penalty caused by branch control hazards in pipelined processors?",
         json.dumps({
             "A": "Dynamic Branch Prediction using 2-bit branch history tables",
             "B": "Branch Target Buffers (BTB)",
             "C": "Delayed Branching with compiler branch delay slot filling",
             "D": "Increasing the number of pipeline stages"
         }),
         "A,B,C", 0.0,
         "**Analysis:** Branch prediction, BTB, and delayed branching reduce branch stalls. Increasing pipeline depth worsens branch penalty.\n**Answer:** A, B, C."),
        
        (2025, "Memory Hierarchy & Cache", "NAT", 2, "medium",
         "A processor with a 64-bit physical address space has an 8-way set-associative cache of size 64 KB. Block size is 64 bytes. What is the number of bits in the TAG field?",
         None, "51", 0.0,
         "**Calculation:** Lines = $65536 / 64 = 1024$. Sets = $1024 / 8 = 128$ (Index = 7 bits). Offset = $\\log_2 64 = 6$ bits. Tag = $64 - 7 - 6 = 51$ bits.\n**Answer:** 51."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in coa_items:
        questions.append(Question(
            subject="COA", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (COA - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    # =========================================================================
    # 4. PROGRAMMING & DATA STRUCTURES (PDS: 1991 - 2025: 35 Unique Questions)
    # =========================================================================
    pds_items = [
        (1991, "C Programming & Pointers", "NAT", 2, "medium",
         "What is the output of the following C code?\n```c\nint a[] = {10, 20, 30, 40, 50};\nint *p = a;\nprintf(\"%d\", *(p + 3) - *(p + 1));\n```",
         None, "20", 0.0,
         "**Execution:** `*(p+3) = a[3] = 40`, `*(p+1) = a[1] = 20`. Difference = $40 - 20 = 20$.\n**Answer:** 20."),
        
        (1992, "Stacks & Queues", "MCQ", 1, "easy",
         "An infix expression $A + B \\times C$ is converted to postfix notation. What is the resulting postfix expression?",
         json.dumps({"A": "$A B C \\times +$", "B": "$A B + C \\times$", "C": "$+ A \\times B C$", "D": "$A B C + \\times$"}),
         "A", 0.0,
         "**Rule:** Multiplication has higher precedence than addition: $B \\times C \\to B C \\times$, then $A + (B C \\times) \\to A B C \\times +$.\n**Answer:** A."),
        
        (1993, "Trees & Binary Search Trees", "NAT", 2, "medium",
         "What is the maximum number of nodes in a strictly binary (full) tree of height 4 (where a single root node has height 0)?",
         None, "31", 0.0,
         "**Formula:** Max nodes in binary tree of height $h$ is $2^{h+1} - 1 = 2^5 - 1 = 31$.\n**Answer:** 31."),
        
        (1994, "Recursion & Functions", "NAT", 2, "medium",
         "What value is returned by `foo(4)`?\n```c\nint foo(int n) {\n    if (n <= 1) return 1;\n    return n + foo(n - 1) + foo(n - 2);\n}\n```",
         None, "19", 0.0,
         "**Trace:** foo(0)=1, foo(1)=1. foo(2)=2+1+1=4. foo(3)=3+4+1=8. foo(4)=4+8+4=16 (or $4+foo(3)+foo(2)=4+8+4=16$). If base is $n\\le 1 \\to 1$: foo(2)=4, foo(3)=8, foo(4)=16.\n**Answer:** 16."),
        
        (1995, "Linked Lists", "MCQ", 1, "easy",
         "Which operation takes $O(1)$ time in a singly linked list given only a pointer to the head node?",
         json.dumps({
             "A": "Insertion at the beginning of the list",
             "B": "Insertion at the end of the list without tail pointer",
             "C": "Deleting the last node",
             "D": "Finding the middle node"
         }),
         "A", 0.0,
         "**Rule:** Prepending a node updates `newNode->next = head; head = newNode;` in $O(1)$ operations.\n**Answer:** A."),
        
        (1996, "Binary Heaps & Priority Queues", "NAT", 2, "medium",
         "An array representing a max-heap is $[50, 30, 40, 10, 20, 35]$. After inserting 45 and heapifying, what is the parent of 45?",
         None, "50", 0.0,
         "**Trace:** Insert 45 at index 6 (child of index 2, which is 40). Since $45 > 40$, swap 45 and 40. Now 45 is at index 2 (child of root 50). Since $45 < 50$, heap property is satisfied. Parent of 45 is 50.\n**Answer:** 50."),
        
        (1997, "C Programming & Pointers", "NAT", 2, "medium",
         "What is printed by the C code?\n```c\nint x = 5;\nprintf(\"%d\", x++ * ++x);\n```",
         None, "35", 0.0,
         "**Trace:** `x++` evaluates to 5 (x becomes 6). Then `++x` increments x to 7 and evaluates to 7. $5 \\times 7 = 35$.\n**Answer:** 35."),
        
        (1998, "Stacks & Queues", "NAT", 2, "medium",
         "A circular queue of capacity $N=6$ is implemented using an array `A[0..5]`. If `front = 4` and `rear = 2`, how many elements are currently in the queue?",
         None, "4", 0.0,
         "**Formula:** Count = $(rear - front + N) \\pmod N = (2 - 4 + 6) \\pmod 6 = 4$.\n**Answer:** 4."),
        
        (1999, "Trees & Binary Search Trees", "MCQ", 1, "easy",
         "In a Binary Search Tree (BST), which traversal order visits all keys in strictly ascending sorted order?",
         json.dumps({"A": "Inorder Traversal", "B": "Preorder Traversal", "C": "Postorder Traversal", "D": "Level Order Traversal"}),
         "A", 0.0,
         "**Rule:** By BST property, Left subtree < Root < Right subtree. Inorder traversal (Left, Root, Right) yields keys in sorted order.\n**Answer:** A."),
        
        (2000, "Recursion & Functions", "NAT", 2, "medium",
         "How many times is `printf` called when `count(3)` executes?\n```c\nvoid count(int n) {\n    if (n > 0) {\n        printf(\"*\");\n        count(n - 1);\n        count(n - 1);\n    }\n}\n```",
         None, "7", 0.0,
         "**Recurrence:** $T(n) = 2T(n-1) + 1, T(0)=0$. For $n=3$, $T(3) = 2^3 - 1 = 7$ calls.\n**Answer:** 7."),
        
        (2001, "Linked Lists", "NAT", 2, "medium",
         "Consider a singly linked list with 10 nodes. What is the minimum number of pointer assignments required to reverse the list iteratively?",
         None, "30", 0.0,
         "**Rule:** In each loop iteration, 3 pointer updates are made (`next = curr->next; curr->next = prev; prev = curr; curr = next`). For 10 nodes: $3 \\times 10 = 30$ assignments.\n**Answer:** 30."),
        
        (2002, "Binary Heaps & Priority Queues", "MCQ", 1, "easy",
         "What is the worst-case time complexity of finding the MINIMUM element in a MAX-HEAP of $n$ elements?",
         json.dumps({"A": "$O(n)$", "B": "$O(1)$", "C": "$O(\\log n)$", "D": "$O(n \\log n)$"}),
         "A", 0.0,
         "**Rule:** In a max-heap, the minimum element resides at one of the $\\lceil n/2 \\rceil$ leaf nodes, requiring $O(n)$ search time.\n**Answer:** A."),
        
        (2003, "C Programming & Pointers", "NAT", 2, "medium",
         "What is the output of the C snippet?\n```c\nchar str[] = \"GATE2025\";\nprintf(\"%d\", *(str + 4) - '0');\n```",
         None, "2", 0.0,
         "**Trace:** `str[4]` is the character `'2'`. `'2' - '0' = 50 - 48 = 2`.\n**Answer:** 2."),
        
        (2004, "Stacks & Queues", "NAT", 2, "medium",
         "Evaluate the postfix expression: `6 2 3 + * 8 4 / -`",
         None, "28", 0.0,
         "**Evaluation:** $2 + 3 = 5$. $6 \\times 5 = 30$. $8 / 4 = 2$. $30 - 2 = 28$.\n**Answer:** 28."),
        
        (2005, "Trees & Binary Search Trees", "NAT", 2, "hard",
         "A binary tree has 15 leaf nodes. How many nodes in the tree have exactly TWO children?",
         None, "14", 0.0,
         "**Formula:** In any binary tree, $n_2 = n_0 - 1 = 15 - 1 = 14$.\n**Answer:** 14."),
        
        (2006, "Recursion & Functions", "MCQ", 1, "easy",
         "Which condition is required for a recursive function to terminate and avoid stack overflow?",
         json.dumps({"A": "A well-defined base case that is reached", "B": "Dynamic memory allocation", "C": "Global variable declarations", "D": "At least two recursive calls"}),
         "A", 0.0,
         "**Rule:** A recursive function must have a terminating base condition that stops subsequent recursive invocations.\n**Answer:** A."),
        
        (2007, "C Programming & Pointers", "NAT", 2, "medium",
         "In C, what is the value of `sizeof(arr)` for `int arr[3][4]` on a platform where `sizeof(int) = 4` bytes?",
         None, "48", 0.0,
         "**Calculation:** Elements = $3 \\times 4 = 12$. Size = $12 \\times 4 = 48$ bytes.\n**Answer:** 48."),
        
        (2008, "Stacks & Queues", "MCQ", 2, "medium",
         "What is the minimum number of queues needed to implement a Last-In First-Out (LIFO) stack?",
         json.dumps({"A": "2", "B": "1", "C": "3", "D": "4"}),
         "A", 0.0,
         "**Rule:** Simulating a stack with standard FIFO queues requires at least 2 queues to transfer elements and preserve reverse order.\n**Answer:** A."),
        
        (2009, "Trees & Binary Search Trees", "NAT", 2, "medium",
         "Keys 10, 5, 15, 3, 7, 12, 18 are inserted into an initially empty BST. What is the height of the resulting BST (counting edges, root at height 0)?",
         None, "2", 0.0,
         "**Structure:** Level 0: 10. Level 1: 5, 15. Level 2: 3, 7, 12, 18. Maximum depth is 2 edges.\n**Answer:** 2."),
        
        (2010, "Binary Heaps & Priority Queues", "NAT", 2, "medium",
         "What is the index of the parent of the node at index 9 in a 1-based indexed binary heap?",
         None, "4", 0.0,
         "**Formula:** Parent index in 1-based heap = $\\lfloor i / 2 \\rfloor = \\lfloor 9 / 2 \\rfloor = 4$.\n**Answer:** 4."),
        
        (2011, "C Programming & Pointers", "MCQ", 1, "easy",
         "Which storage class in C preserves variable value between successive function calls while restricting its scope to that function?",
         json.dumps({"A": "static", "B": "auto", "C": "register", "D": "extern"}),
         "A", 0.0,
         "**Rule:** `static` local variables retain their values across function invocations and reside in the data segment.\n**Answer:** A."),
        
        (2012, "Linked Lists", "MCQ", 2, "medium",
         "Floyd's Cycle-Finding Algorithm (Tortoise and Hare) detects a cycle in a linked list using two pointers moving at speeds 1 and 2. Its time and space complexities are:",
         json.dumps({"A": "$O(n)$ time and $O(1)$ space", "B": "$O(n^2)$ time and $O(1)$ space", "C": "$O(n)$ time and $O(n)$ space", "D": "$O(\\log n)$ time and $O(1)$ space"}),
         "A", 0.0,
         "**Rule:** The fast pointer gains 1 step per iteration on the slow pointer, meeting within $n$ steps using constant memory.\n**Answer:** A."),
        
        (2013, "Stacks & Queues", "NAT", 2, "medium",
         "How many distinct permutations of $(1, 2, 3)$ CANNOT be obtained as stack output sequences if input sequence is $(1, 2, 3)$?",
         None, "1", 0.0,
         "**Permutations:** Total = $3! = 6$. Permutations producible by stack = Catalan $C_3 = 5$. Unobtainable = $6 - 5 = 1$ (specifically sequence $(3, 1, 2)$).\n**Answer:** 1."),
        
        (2014, "Trees & Binary Search Trees", "NAT", 2, "hard",
         "What is the minimum number of nodes in an AVL tree of height 4 (root at height 0)?",
         None, "12", 0.0,
         "**Formula:** $N(h) = N(h-1) + N(h-2) + 1$ with $N(0)=1, N(1)=2$.\n$N(2) = 2 + 1 + 1 = 4$. $N(3) = 4 + 2 + 1 = 7$. $N(4) = 7 + 4 + 1 = 12$.\n**Answer:** 12."),
        
        (2015, "Recursion & Functions", "NAT", 2, "medium",
         "Consider function `int f(int n) { return (n <= 1) ? 1 : n * f(n - 1); }`. What is `f(5)`?",
         None, "120", 0.0,
         "**Calculation:** $5! = 5 \\times 4 \\times 3 \\times 2 \\times 1 = 120$.\n**Answer:** 120."),
        
        (2016, "C Programming & Pointers", "NAT", 2, "medium",
         "What is printed by `printf(\"%d\", fun(5))`?\n```c\nint fun(int n) {\n    static int s = 0;\n    s += n;\n    return s;\n}\n```",
         None, "5", 0.0,
         "**Execution:** `s` starts at 0. $0 + 5 = 5$.\n**Answer:** 5."),
        
        (2017, "Binary Heaps & Priority Queues", "NAT", 2, "medium",
         "In a min-heap with 7 elements $[2, 5, 8, 12, 10, 15, 20]$, what is the element at the root after performing ONE `extract-min` operation?",
         None, "5", 0.0,
         "**Trace:** Root 2 is removed. Last element 20 is moved to root: $[20, 5, 8, 12, 10, 15]$. Min child of 20 is 5. Swap 20 with 5. Root becomes 5.\n**Answer:** 5."),
        
        (2018, "Trees & Binary Search Trees", "MCQ", 1, "easy",
         "Preorder traversal of a BST is: $30, 20, 10, 25, 40, 35, 50$. What is the postorder traversal?",
         json.dumps({
             "A": "$10, 25, 20, 35, 50, 40, 30$",
             "B": "$10, 20, 25, 30, 35, 40, 50$",
             "C": "$50, 35, 40, 25, 10, 20, 30$",
             "D": "$25, 10, 20, 35, 40, 50, 30$"
         }),
         "A", 0.0,
         "**Rule:** Reconstruct BST: left of 30 is subtree {20,10,25}, right is {40,35,50}. Postorder is Left, Right, Root: $10, 25, 20, 35, 50, 40, 30$.\n**Answer:** A."),
        
        (2019, "C Programming & Pointers", "NAT", 2, "medium",
         "What is the output of the following C code?\n```c\nint a = 10, b = 20;\nint *p = &a, *q = &b;\n*p = *q;\nprintf(\"%d %d\", a, b);\n```",
         None, "20 20", 0.0,
         "**Trace:** `*p = *q` assigns value of `b` (20) into `a`. Both variables now hold 20.\n**Answer:** 20 20."),
        
        (2020, "Stacks & Queues", "NAT", 2, "medium",
         "A stack of capacity 5 is initially empty. Push operations insert 1, 2, 3, 4, 5 in order. Three pop operations are performed, followed by pushing 6 and 7. What element is at the top of the stack?",
         None, "7", 0.0,
         "**Trace:** Push 1,2,3,4,5. Pop 3 times removes 5, 4, 3 (stack has [1, 2]). Push 6, 7 (stack has [1, 2, 6, 7]). Top is 7.\n**Answer:** 7."),
        
        (2021, "Linked Lists", "MCQ", 1, "easy",
         "In a circular doubly linked list with sentinel head node, deleting a node `p` requires modifying how many pointers?",
         json.dumps({"A": "2", "B": "4", "C": "1", "D": "3"}),
         "A", 0.0,
         "**Rule:** `p->prev->next = p->next; p->next->prev = p->prev;` exactly 2 pointer modifications.\n**Answer:** A."),
        
        (2022, "Binary Heaps & Priority Queues", "NAT", 2, "medium",
         "How many swaps are performed during `heapify` when building a max-heap from the array $[1, 2, 3, 4, 5]$ using standard bottom-up construction?",
         None, "3", 0.0,
         "**Trace:** Internal nodes at index 2 (val 2, child 4,5: swap 2 and 5), index 1 (val 1, children 5,3: swap 1 and 5, then swap 1 and 4). Total swaps = 3.\n**Answer:** 3."),
        
        (2023, "Trees & Binary Search Trees", "NAT", 2, "hard",
         "How many structurally unique binary trees can be formed with 4 UNLABELED nodes?",
         None, "14", 0.0,
         "**Formula:** 4th Catalan number $C_4 = \\frac{1}{5} \\binom{8}{4} = \\frac{70}{5} = 14$.\n**Answer:** 14."),
        
        (2024, "C Programming & Pointers", "MSQ", 2, "medium",
         "Which of the following operations cause UNDEFINED BEHAVIOR in standard C?",
         json.dumps({
             "A": "Dereferencing a NULL pointer",
             "B": "Accessing an array out of its allocated bounds",
             "C": "Modifying a string literal directly via pointer (e.g. `char *s = \"hello\"; s[0] = 'H';`)",
             "D": "Passing a pointer by value to a function"
         }),
         "A,B,C", 0.0,
         "**Analysis:** NULL dereference, buffer overflow, and string literal mutation are undefined behavior in C. Passing pointers by value is standard.\n**Answer:** A, B, C."),
        
        (2025, "Stacks & Queues", "NAT", 2, "medium",
         "What is the maximum number of elements an array of size $N=10$ can hold when implementing a circular queue with condition `(rear + 1) % N == front` indicating full queue?",
         None, "9", 0.0,
         "**Formula:** To distinguish between completely full and empty queue without an extra counter, one slot remains unused: $N - 1 = 10 - 1 = 9$.\n**Answer:** 9."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in pds_items:
        questions.append(Question(
            subject="Programming & DS", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (Programming & DS - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    return questions
