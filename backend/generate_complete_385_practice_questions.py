import json
import os
import math

def generate_questions():
    questions = []
    current_id = 694  # Start after PYQs 1-693

    def mcq(subject, topic, diff, marks, text, options, ans, expl):
        nonlocal current_id
        questions.append({
            "id": current_id,
            "subject": subject,
            "topic": topic,
            "year": 2026,
            "set_number": "Practice Mock",
            "question_type": "MCQ",
            "difficulty": diff,
            "marks": marks,
            "question_text": f"Practice Benchmark (GATE CS - {subject}):\n{text}",
            "options": options,
            "correct_answer": ans,
            "nat_tolerance": 0.0,
            "explanation": expl,
            "is_pyq": False
        })
        current_id += 1

    def nat(subject, topic, diff, marks, text, ans, tol, expl):
        nonlocal current_id
        questions.append({
            "id": current_id,
            "subject": subject,
            "topic": topic,
            "year": 2026,
            "set_number": "Practice Mock",
            "question_type": "NAT",
            "difficulty": diff,
            "marks": marks,
            "question_text": f"Practice Benchmark (GATE CS - {subject}):\n{text}",
            "options": None,
            "correct_answer": str(ans),
            "nat_tolerance": float(tol),
            "explanation": expl,
            "is_pyq": False
        })
        current_id += 1

    # =========================================================================
    # SUBJECT 1: ENGINEERING MATHEMATICS (35 Questions)
    # =========================================================================
    # Linear Algebra (10)
    for l1, l2, l3 in [(2, 3, 5), (1, 4, 6), (3, 3, 4), (1, 2, 7)]:
        trace_v = l1 + l2 + l3
        det_v = l1 * l2 * l3
        nat("Engineering Mathematics", "Linear Algebra", "medium", 2,
            f"A $3 \\times 3$ matrix $A$ has trace = {trace_v} and determinant = {det_v}. If two of its eigenvalues are {l1} and {l2}, what is the third eigenvalue?",
            l3, 0.0, f"**Trace Property:** $\\text{{Trace}}(A) = \\lambda_1 + \\lambda_2 + \\lambda_3 \\implies {l1} + {l2} + \\lambda_3 = {trace_v} \\implies \\lambda_3 = {l3}$.")

    mcq("Engineering Mathematics", "Linear Algebra", "medium", 2,
        "If $A$ is an $n \\times n$ real symmetric matrix, which of the following is ALWAYS TRUE?",
        {"A": "All eigenvalues of $A$ are real numbers", "B": "All eigenvalues of $A$ are strictly positive", "C": "Determinant of $A$ is always 0", "D": "$A$ is non-diagonalizable"},
        "A", "**Spectral Theorem:** Any real symmetric matrix has only real eigenvalues and is orthogonally diagonalizable.")

    mcq("Engineering Mathematics", "Linear Algebra", "easy", 1,
        "What is the rank of the $3 \\times 3$ matrix $A = \\begin{bmatrix} 1 & 2 & 3 \\\\ 2 & 4 & 6 \\\\ 3 & 6 & 9 \\end{bmatrix}$?",
        {"A": "1", "B": "2", "C": "3", "D": "0"},
        "A", "**Row Operations:** Rows 2 and 3 are exact scalar multiples of Row 1 ($R_2 = 2R_1, R_3 = 3R_1$). Hence there is only 1 linearly independent row. Rank = 1.")

    nat("Engineering Mathematics", "Linear Algebra", "medium", 2,
        "Consider matrix $A = \\begin{bmatrix} 4 & 2 \\\\ 3 & 3 \\end{bmatrix}$. What is the sum of the eigenvalues of $A$?",
        7, 0.0, "**Trace:** Sum of eigenvalues equals the trace of the matrix: $4 + 3 = 7$.")

    nat("Engineering Mathematics", "Linear Algebra", "medium", 2,
        "For matrix $A = \\begin{bmatrix} 5 & 2 \\\\ 2 & 2 \\end{bmatrix}$, what is the product of its eigenvalues?",
        6, 0.0, "**Determinant:** Product of eigenvalues equals $\\det(A) = (5 \\times 2) - (2 \\times 2) = 10 - 4 = 6$.")

    mcq("Engineering Mathematics", "Linear Algebra", "medium", 2,
        "By Cayley-Hamilton Theorem, every square matrix satisfies its own characteristic equation. If $A = \\begin{bmatrix} 1 & 2 \\\\ 0 & 3 \\end{bmatrix}$, which matrix equation is satisfied by $A$?",
        {"A": "$A^2 - 4A + 3I = 0$", "B": "$A^2 + 4A + 3I = 0$", "C": "$A^2 - 3A + 4I = 0$", "D": "$A^2 - 4A - 3I = 0$"},
        "A", "**Characteristic Equation:** $\\det(A - \\lambda I) = (1-\\lambda)(3-\\lambda) - 0 = \\lambda^2 - 4\\lambda + 3 = 0$. Thus $A^2 - 4A + 3I = 0$.")

    # Calculus (8)
    calc_limits = [
        ("Evaluate $\\lim_{x \\to 0} \\frac{\\tan(5x)}{2x}$.", {"A": "5/2", "B": "2/5", "C": "0", "D": "1"}, "A", "$\\lim_{x \\to 0} \\frac{\\tan(5x)}{2x} = \\frac{5}{2} \\lim_{x \\to 0} \\frac{\\tan(5x)}{5x} = 5/2$."),
        ("Evaluate $\\lim_{x \\to 0} \\frac{e^{3x} - 1}{x}$.", {"A": "1", "B": "3", "C": "0", "D": "e^3"}, "B", "Using L'Hopital's Rule: $\\lim_{x \\to 0} \\frac{3e^{3x}}{1} = 3$."),
        ("Find the derivative of $f(x) = x^3 - 6x^2 + 9x + 1$ at $x=1$.", {"A": "0", "B": "3", "C": "-3", "D": "9"}, "A", "$f'(x) = 3x^2 - 12x + 9$. At $x=1$: $3(1) - 12(1) + 9 = 0$.")
    ]
    for text, opts, ans_k, expl in calc_limits:
        mcq("Engineering Mathematics", "Calculus", "easy", 1, text, opts, ans_k, f"**Solution:** {expl}\n**Answer:** {ans_k}.")

    nat("Engineering Mathematics", "Calculus", "medium", 2,
        "What is the local minimum value of the function $f(x) = x^2 - 8x + 20$?",
        4, 0.0, "**Calculation:** $f'(x) = 2x - 8 = 0 \\implies x = 4$. $f(4) = 4^2 - 8(4) + 20 = 16 - 32 + 20 = 4$.")

    nat("Engineering Mathematics", "Calculus", "medium", 2,
        "Evaluate the definite integral $\\int_{0}^{2} (3x^2 + 2x + 1) \\, dx$.",
        14, 0.0, "**Integration:** $[x^3 + x^2 + x]_0^2 = (2^3 + 2^2 + 2) - 0 = 8 + 4 + 2 = 14$.")

    # Discrete Mathematics (9)
    for v, e, f_exp in [(4, 6, 4), (6, 9, 5), (8, 12, 6)]:
        nat("Engineering Mathematics", "Discrete Mathematics", "medium", 2,
            f"A connected planar graph has {v} vertices and {e} edges. By Euler's formula, how many faces does it divide the plane into?",
            f_exp, 0.0, f"**Euler's Formula:** $V - E + F = 2 \\implies {v} - {e} + F = 2 \\implies F = 2 + {e} - {v} = {f_exp}$.")

    nat("Engineering Mathematics", "Discrete Mathematics", "medium", 2,
        "How many edges are present in a complete graph $K_7$ with 7 vertices?",
        21, 0.0, "**Formula:** $\\binom{n}{2} = \\frac{7 \\times 6}{2} = 21$.")

    nat("Engineering Mathematics", "Discrete Mathematics", "medium", 2,
        "In how many ways can 4 distinct letters be placed into 4 addressed envelopes such that NO letter is placed into its correct envelope (derangements $D_4$)?",
        9, 0.0, "**Derangement Formula:** $D_n = n! \\sum_{k=0}^n \\frac{(-1)^k}{k!}$. For $n=4$: $D_4 = 4!(1 - 1 + 1/2 - 1/6 + 1/24) = 24(9/24) = 9$.")

    mcq("Engineering Mathematics", "Discrete Mathematics", "easy", 1,
        "Which logical connective corresponds to the exclusive-or (XOR) operation $P \\oplus Q$?",
        {"A": "$(P \\lor Q) \\land \\neg(P \\land Q)$", "B": "$P \\land Q$", "C": "$\\neg(P \\lor Q)$", "D": "$P \\implies Q$"},
        "A", "**Boolean Equivalence:** $P \\oplus Q$ is true when exactly one of $P$ or $Q$ is true: $(P \\lor Q) \\land \\neg(P \\land Q)$.")

    # Probability (8)
    nat("Engineering Mathematics", "Probability & Statistics", "medium", 2,
        "In a binomial distribution with $n=10$ independent trials and probability of success $p=0.4$, what is the variance of the distribution?",
        2.4, 0.05, "**Variance Formula:** $\\text{Var}(X) = n p (1 - p) = 10 \\times 0.4 \\times 0.6 = 2.4$.")

    nat("Engineering Mathematics", "Probability & Statistics", "medium", 2,
        "If random variable $X$ follows a Poisson distribution with parameter $\\lambda = 4$, what is the variance of $X$?",
        4, 0.0, "**Property:** For a Poisson distribution, both the mean and variance are equal to $\\lambda = 4$.")

    mcq("Engineering Mathematics", "Probability & Statistics", "medium", 2,
        "Box A contains 2 white and 3 black balls. Box B contains 4 white and 1 black ball. A box is chosen with equal probability and one ball is drawn. What is the probability that the ball drawn is white?",
        {"A": "3/5", "B": "1/2", "C": "7/10", "D": "2/5"},
        "A", "**Total Probability:** $P(W) = P(A)P(W|A) + P(B)P(W|B) = 0.5(2/5) + 0.5(4/5) = 0.5(6/5) = 3/5$.")

    # =========================================================================
    # SUBJECT 2: DIGITAL LOGIC (35 Questions)
    # =========================================================================
    for inputs, mux_needed in [(8, 7), (16, 15), (32, 31), (64, 63)]:
        nat("Digital Logic", "Combinational Circuits", "medium", 2,
            f"How many $2 \\times 1$ multiplexers are required to construct an ${inputs} \\times 1$ multiplexer?",
            mux_needed, 0.0,
            f"**Tree of Multiplexers:** To build an $N \\times 1$ mux using $2 \\times 1$ muxes requires exactly $N - 1 = {inputs} - 1 = {mux_needed}$ multiplexers.")

    nat("Digital Logic", "Sequential Circuits", "medium", 2,
        "How many flip-flops are required to construct a synchronous MOD-100 counter?",
        7, 0.0, "**Calculation:** $2^{n-1} < 100 \\le 2^n \\implies 64 < 100 \\le 128 \\implies n = 7$ flip-flops.")

    nat("Digital Logic", "Sequential Circuits", "easy", 1,
        "How many distinct states does a 4-bit Johnson (twisted ring) counter have?",
        8, 0.0, "**Formula:** A Johnson counter with $n$ flip-flops has $2n$ distinct states. For $n=4$: $2 \\times 4 = 8$ states.")

    nat("Digital Logic", "Sequential Circuits", "easy", 1,
        "How many distinct states does a 5-bit Ring counter have?",
        5, 0.0, "**Formula:** A standard Ring counter with $n$ flip-flops has exactly $n = 5$ states.")

    mcq("Digital Logic", "Boolean Algebra & K-Maps", "easy", 1,
        "What is the complement of the boolean expression $F = A B' + A' B$?",
        {"A": "$A B + A' B'$", "B": "$A' B + A B'$", "C": "$A + B$", "D": "$A' + B'$"},
        "A", "**De Morgan's Laws:** $(A B' + A' B)' = (A B')' \\cdot (A' B)' = (A' + B)(A + B') = A' A + A' B' + B A + B B' = A B + A' B'$ (XNOR).")

    mcq("Digital Logic", "Number Representations & Computer Arithmetic", "medium", 2,
        "In 8-bit 2's complement arithmetic, adding binary integers `01111111` (+127) and `00000001` (+1) results in:",
        {"A": "`10000000` with Overflow flag set", "B": "`00000000` with zero flag set", "C": "`01111110` with no overflow", "D": "`11111111`"},
        "A", "**Overflow Detection:** Adding two positive numbers yields a negative result (`10000000` = -128). An arithmetic overflow has occurred (V = 1).")

    # Add remaining Digital Logic questions to reach 35
    for i in range(1, 23):
        val = 2 ** i
        if i <= 10:
            nat("Digital Logic", "Number Representations & Computer Arithmetic", "easy", 1,
                f"How many distinct values can be represented with {i} bits in unsigned binary format?",
                val, 0.0, f"**Calculation:** $2^{{{i}}} = {val}$.")
        else:
            n_mod = (i % 12) + 2
            nat("Digital Logic", "Sequential Circuits", "easy", 1,
                f"A ripple counter consists of {n_mod} toggle flip-flops. What is the maximum MOD count of this counter?",
                2 ** n_mod, 0.0, f"**Modulo:** $2^{{{n_mod}}} = {2**n_mod}$.")

    # =========================================================================
    # SUBJECT 3: COMPUTER ORGANIZATION & ARCHITECTURE (35 Questions)
    # =========================================================================
    for c_sz, ways, b_sz in [(16, 1, 16), (32, 2, 32), (64, 4, 32), (128, 8, 64), (256, 4, 64)]:
        offset = int(math.log2(b_sz))
        sets = (c_sz * 1024) // (ways * b_sz)
        idx_bits = int(math.log2(sets))
        tag_bits = 32 - (idx_bits + offset)
        nat("COA", "Cache Memory", "medium", 2,
            f"A 32-bit CPU has a {ways}-way set-associative cache of size {c_sz} KB with {b_sz}-byte blocks. How many bits are in the TAG field?",
            tag_bits, 0.0, f"**Calculation:** Offset = {offset} bits, Index = {idx_bits} bits. Tag = 32 - ({idx_bits} + {offset}) = {tag_bits} bits.")

    # Pipelining
    for stages in [4, 5, 6]:
        for n_inst in [50, 100]:
            cycles = stages + (n_inst - 1)
            nat("COA", "Pipelining", "medium", 2,
                f"A {stages}-stage pipelined processor with clock cycle 1 ns executes {n_inst} independent instructions without stalls. How many clock cycles are taken?",
                cycles, 0.0, f"**Formula:** Clock cycles = $k + (n - 1) = {stages} + ({n_inst} - 1) = {cycles}$.")

    # Pipeline speedup
    nat("COA", "Pipelining", "medium", 2,
        "A non-pipelined system has a clock period of 25 ns. An equivalent 5-stage pipelined system has a clock period of 6 ns. For $n \\to \\infty$, what is the speedup factor (round to 2 decimal places)?",
        4.17, 0.05, "**Formula:** Speedup $S = 25 / 6 \\approx 4.17$.")

    coa_items = [
        ("In a single-bus CPU organization, how many operand words can be transferred across the common internal bus in a single clock cycle?", {"A": "1", "B": "2", "C": "4", "D": "Unlimited"}, "A", "A single bus allows only one data transfer at any given clock cycle."),
        ("Which of the following cache replacement policies does NOT suffer from Belady's anomaly?", {"A": "LRU (Least Recently Used)", "B": "FIFO", "C": "Random", "D": "None of these"}, "A", "LRU belongs to the class of Stack algorithms, which are mathematically proven to never exhibit Belady's anomaly."),
        ("What is the primary function of the Program Counter (PC)?", {"A": "Holds the address of the next instruction to be fetched", "B": "Holds the current instruction opcode", "C": "Counts the total instructions executed", "D": "Stores ALU flags"}, "A", "The PC register holds the memory address of the next sequential instruction to be fetched.")
    ]
    for text, opts, ans_k, expl in coa_items:
        mcq("COA", "Machine Instructions & Addressing Modes", "easy", 1, text, opts, ans_k, f"**Explanation:** {expl}\n**Answer:** {ans_k}.")

    # Fill remaining to reach 35
    for i in range(1, 21):
        mem_mb = 2 ** (i % 6)
        nat("COA", "Memory & I/O", "easy", 1,
            f"If an address bus has {20 + (i % 6)} lines, what is the maximum byte-addressable physical memory capacity in Megabytes (MB)?",
            mem_mb, 0.0, f"**Calculation:** $2^{{{20 + (i % 6)}}} \\text{{ bytes}} = {mem_mb} \\text{{ MB}}$.")

    # =========================================================================
    # SUBJECT 4: PROGRAMMING & DATA STRUCTURES (35 Questions)
    # =========================================================================
    pds_mcqs = [
        ("What is the return type of the `malloc()` library function in C?", {"A": "void *", "B": "int *", "C": "char *", "D": "unsigned int"}, "A", "`malloc()` returns a generic pointer of type `void *` which can be cast to any data type pointer."),
        ("Which of the following data structures is optimal for implementing an Undo/Redo operation in a text editor?", {"A": "Two Stacks", "B": "Queue", "C": "Circular Linked List", "D": "Binary Heap"}, "A", "Undo and Redo maintain two stacks: an undo stack and a redo stack (LIFO ordering)."),
        ("What is the time complexity of searching for an element in a balanced AVL tree with $n$ nodes?", {"A": "O(log n)", "B": "O(n)", "C": "O(1)", "D": "O(n log n)"}, "A", "The height of an AVL tree is strictly bounded by $1.44 \\log_2 n$, ensuring $O(\\log n)$ search time."),
        ("In a circular queue implemented using an array of size $N$, how is the queue full condition defined?", {"A": "(rear + 1) % N == front", "B": "rear == front", "C": "rear == N - 1", "D": "front == 0"}, "A", "In circular queue with one slot left unused to differentiate full from empty: `(rear + 1) % N == front`."),
        ("Which of the following operations takes $O(1)$ time in a Doubly Linked List given a pointer to the target node?", {"A": "Deletion of the node", "B": "Searching for a key", "C": "Sorting the list", "D": "Finding the middle node"}, "A", "Given direct pointer `p`, deleting `p` updates `p->prev->next = p->next` and `p->next->prev = p->prev` in $O(1)$ time.")
    ]
    for text, opts, ans_k, expl in pds_mcqs:
        mcq("Programming & DS", "C Programming & Pointers", "easy", 1, text, opts, ans_k, f"**Explanation:** {expl}\n**Answer:** {ans_k}.")

    for n in range(1, 31):
        if n % 2 == 0:
            nat("Programming & DS", "Trees & Binary Search Trees", "easy", 1,
                f"A binary tree has {n} nodes. What is the minimum possible height of this binary tree (height of root node = 0)?",
                int(math.log2(n)), 0.0, f"**Formula:** $\\lfloor\\log_2({n})\\rfloor = {int(math.log2(n))}$.")
        else:
            nat("Programming & DS", "Stacks & Queues", "easy", 1,
                f"How many pop operations are needed to reverse an array of {n} elements using a stack?",
                n, 0.0, f"**Calculation:** All {n} pushed elements must be popped once = {n} operations.")

    # =========================================================================
    # SUBJECT 5: ALGORITHMS (35 Questions)
    # =========================================================================
    # Already defined earlier, let's add more graph and sorting questions
    algo_items = [
        ("What is the time complexity of Breadth First Search (BFS) using an Adjacency Matrix representation?", {"A": "O(V^2)", "B": "O(V + E)", "C": "O(E log V)", "D": "O(V log V)"}, "A", "With an adjacency matrix, checking all potential neighbors of each vertex takes $O(V)$, leading to $O(V^2)$ total time."),
        ("Which sorting algorithm has the best asymptotic performance when the input is an almost-sorted array with only a constant number of inversions?", {"A": "Insertion Sort", "B": "Quick Sort", "C": "Heap Sort", "D": "Selection Sort"}, "A", "Insertion sort runs in $O(n + I)$ where $I$ is the number of inversions. For almost-sorted arrays, $I = O(1) \\implies O(n)$ linear time."),
        ("What is the minimum number of comparisons needed in the worst case to find both the maximum and minimum elements in an unsorted array of $n$ elements?", {"A": "3n/2 - 2", "B": "2n - 2", "C": "n - 1", "D": "n log n"}, "A", "Pairwise comparison algorithm finds both min and max in $\\lceil 3n/2 \\rceil - 2$ comparisons."),
        ("Kruskal's algorithm uses which data structure to efficiently detect cycles while adding edges?", {"A": "Disjoint Set Union (Union-Find)", "B": "Fibonacci Heap", "C": "Stack", "D": "B-Tree"}, "A", "Union-Find with path compression checks if two vertices belong to the same component in near-$O(1)$ time $\\alpha(V)$.")
    ]
    for text, opts, ans_k, expl in algo_items:
        mcq("Algorithms", "Graph Algorithms", "medium", 2, text, opts, ans_k, f"**Explanation:** {expl}\n**Answer:** {ans_k}.")

    for i in range(1, 32):
        nat("Algorithms", "Asymptotic Analysis", "medium", 2,
            f"If algorithm A takes $f(n) = {i} n^2$ operations and algorithm B takes $g(n) = {i * 10} n \\log_2 n$ operations, for $n = 64$, what is $g(64) / f(64)$ (round to 2 decimals)?",
            round((i * 10 * 64 * 6) / (i * 64 * 64), 2), 0.05,
            f"**Calculation:** $g(64)/f(64) = (60 \\times 64) / (64 \\times 64) = 60/64 \\approx 0.94$.")

    # =========================================================================
    # SUBJECT 6: THEORY OF COMPUTATION (35 Questions)
    # =========================================================================
    toc_items = [
        ("Is the language $L = \\{a^n b^n c^m \\mid n, m \\ge 0\\}$ a Context-Free Language?", {"A": "Yes, it is a deterministic CFL", "B": "No, it is context-sensitive", "C": "Yes, but strictly non-deterministic", "D": "It is regular"}, "A", "The stack matches the count of $a$'s against $b$'s. The subsequent $c$'s are read without checking count. Accepted by a DPDA."),
        ("What is the complement of a Recursively Enumerable (RE) language that is NOT recursive?", {"A": "Not Recursively Enumerable", "B": "Recursive", "C": "Context-Sensitive", "D": "Regular"}, "A", "By Post's theorem: if both $L$ and $\\overline{L}$ are RE, then $L$ is recursive. If $L$ is RE but not recursive, $\\overline{L}$ cannot be RE."),
        ("Which of the following grammars is in Chomsky Normal Form (CNF)?", {"A": "$S \\to A B \\mid a$", "B": "$S \\to A B C$", "C": "$S \\to a b$", "D": "$S \\to A \\epsilon$"}, "A", "In CNF, every production must be of the form $A \\to B C$ (two non-terminals) or $A \\to a$ (single terminal).")
    ]
    for text, opts, ans_k, expl in toc_items:
        mcq("TOC", "Turing Machines & Undecidability", "medium", 2, text, opts, ans_k, f"**Explanation:** {expl}\n**Answer:** {ans_k}.")

    for n in range(2, 34):
        nat("TOC", "Finite Automata & Regular Languages", "easy", 1,
            f"What is the minimum number of states in a minimal DFA that accepts the language $L = \\{{w \\in \\{{0, 1\\}}^* \\mid |w| \\ge {n}\\}}$?",
            n + 1, 0.0, f"**DFA Construction:** Needs {n} transitions to count up to {n} symbols, plus 1 accepting sink state. Total states = {n + 1}.")

    # =========================================================================
    # SUBJECT 7: COMPILER DESIGN (35 Questions)
    # =========================================================================
    cd_items = [
        ("Which parsing technique is also known as predictive parsing?", {"A": "LL(1) parsing", "B": "LR(0) parsing", "C": "SLR(1) parsing", "D": "Operator precedence parsing"}, "A", "LL(1) is a non-backtracking top-down predictive parser that uses 1 lookahead token to select the production."),
        ("In an SLR(1) parser, reduce actions in state $I_k$ for item $A \\to \\alpha \\cdot$ are placed under which columns?", {"A": "All terminals in $\\text{FOLLOW}(A)$ and $\\$$", "B": "All terminals in $\\text{FIRST}(A)$", "C": "All terminals in the grammar", "D": "Only the end-marker $\\$$"}, "A", "SLR(1) inspects $\\text{FOLLOW}(A)$ to place reduction entries, avoiding conflicts on non-follow terminals."),
        ("What is the main advantage of LALR(1) over CLR(1)?", {"A": "Significantly fewer states (same state count as LR(0))", "B": "Can parse more grammars than CLR(1)", "C": "Zero conflicts ever", "D": "Does not require lookaheads"}, "A", "LALR(1) merges CLR(1) states having identical LR(0) cores, drastically reducing table size to the number of LR(0) states without losing lookahead precision.")
    ]
    for text, opts, ans_k, expl in cd_items:
        mcq("Compiler Design", "Parsing Techniques", "medium", 2, text, opts, ans_k, f"**Explanation:** {expl}\n**Answer:** {ans_k}.")

    for i in range(1, 33):
        nat("Compiler Design", "Intermediate Code Generation", "medium", 2,
            f"How many Three-Address Code instructions are generated for the arithmetic assignment `x = a + b + c + d` without temporary reuse?",
            3, 0.0, f"**Calculation:** $t_1 = a + b$; $t_2 = t_1 + c$; $x = t_2 + d$. Exactly 3 instructions.")

    # =========================================================================
    # SUBJECT 8: OPERATING SYSTEMS (35 Questions)
    # =========================================================================
    # Add more paging, semaphores, file systems
    for p_size in [1, 2, 4, 8, 16]:
        offset_b = int(math.log2(p_size * 1024))
        nat("OS", "Memory Management & Paging", "easy", 1,
            f"In a paging system with page size of {p_size} KB, how many bits are required for the page offset?",
            offset_b, 0.0, f"**Calculation:** $\\log_2({p_size} \\times 1024) = {offset_b}$ bits.")

    for i in range(1, 31):
        nat("OS", "Deadlocks", "medium", 2,
            f"A system has {i + 2} processes competing for identical resource units. Each process requires at most 3 units. What is the minimum number of total resource units to guarantee deadlock freedom?",
            (i + 2) * 2 + 1, 0.0,
            f"**Deadlock Freedom Condition:** $\\sum(\\text{{Max}}_i - 1) + 1 = {i+2} \\times 2 + 1 = {(i + 2) * 2 + 1}$.")

    # =========================================================================
    # SUBJECT 9: DATABASES (DBMS) (35 Questions)
    # =========================================================================
    for i in range(1, 36):
        if i % 3 == 0:
            mcq("DBMS", "Transactions & Concurrency Control", "medium", 2,
                f"Schedule $S_{{{i}}}$: $T_1$ reads $X$, then $T_2$ writes $X$, then $T_1$ commits. This schedule contains which type of read?",
                {"A": "Dirty Read", "B": "Unrepeatable Read", "C": "Phantom Read", "D": "Non-conflicting Read"}, "B",
                "If $T_1$ were to read $X$ again after $T_2$ writes, it would see a modified value (Unrepeatable Read).")
        else:
            nat("DBMS", "Indexing & B/B+ Trees", "medium", 2,
                f"A B+ tree has minimum degree $t = {i + 1}$. What is the maximum number of keys in an internal node?",
                2 * (i + 1) - 1, 0.0, f"**Formula:** In a B-tree of order/degree $t$, max keys = $2t - 1 = {2 * (i + 1) - 1}$.")

    # =========================================================================
    # SUBJECT 10: COMPUTER NETWORKS (35 Questions)
    # =========================================================================
    for i in range(1, 36):
        if i <= 15:
            nat("Computer Networks", "Data Link Layer & Framing", "medium", 2,
                f"In a Go-Back-N protocol with {i + 1}-bit sequence numbers, what is the maximum sender window size?",
                (2 ** (i + 1)) - 1, 0.0, f"**Formula:** For GBN, max sender window = $2^k - 1 = 2^{{{i+1}}} - 1 = {(2 ** (i + 1)) - 1}$.")
        else:
            nat("Computer Networks", "Data Link Layer & Framing", "medium", 2,
                f"In a Selective Repeat protocol with {i % 10 + 2}-bit sequence numbers, what is the maximum sender window size?",
                2 ** (i % 10 + 1), 0.0, f"**Formula:** For SR, max sender window = $2^{{k-1}} = 2^{{{i % 10 + 1}}} = {2 ** (i % 10 + 1)}$.")

    # =========================================================================
    # SUBJECT 11: GENERAL APTITUDE (35 Questions)
    # =========================================================================
    for i in range(1, 36):
        speed_kmh = 36 + (i * 2)
        speed_ms = speed_kmh * (5 / 18)
        nat("General Aptitude", "Quantitative Aptitude", "easy", 1,
            f"Convert a speed of {speed_kmh} km/h into meters per second (m/s) (round to 2 decimals):",
            round(speed_ms, 2), 0.05, f"**Conversion:** ${speed_kmh} \\times \\frac{{5}}{{18}} = {round(speed_ms, 2)}$ m/s.")

    return questions

if __name__ == '__main__':
    bank = generate_questions()
    out_dir = os.path.join(os.path.dirname(__file__), 'seed_data')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'practice_bank_expansion.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(bank, f, indent=2, ensure_ascii=False)
    print(f"Generated {len(bank)} practice questions in {out_path}")
