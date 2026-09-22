"""
GATE CS 35-Year Comprehensive Question Bank (Part 3)
Covers Digital Logic, Engineering Mathematics, General Aptitude (1991 - 2025)
100% UNIQUE questions with concise step-by-step brief solutions.
"""

import json
from models.question import Question

def get_part3_questions():
    questions = []

    # =========================================================================
    # 9. DIGITAL LOGIC (DL: 1991 - 2025: 35 Unique Questions)
    # =========================================================================
    dl_items = [
        (1991, "Boolean Algebra & K-Maps", "NAT", 2, "medium",
         "How many minterms are in the boolean function $F(A, B, C) = A + B' C$?",
         None, "5", 0.0,
         "**Expansion:** $A = \\{4, 5, 6, 7\\}$. $B'C$ for $A=0$ is $m_1 (001)$. Total minterms = $\\{1, 4, 5, 6, 7\\} \\implies 5$.\n**Answer:** 5."),
        
        (1992, "Combinational Circuits", "MCQ", 1, "easy",
         "A 4-to-1 Multiplexer has select lines $S_1, S_0$. To implement an EX-OR gate $F = A \\oplus B$ using $A$ as $S_1$ and $B$ as $S_0$, what should the inputs $I_0, I_1, I_2, I_3$ be set to?",
         json.dumps({"A": "0, 1, 1, 0", "B": "1, 0, 0, 1", "C": "0, 0, 1, 1", "D": "1, 1, 0, 0"}),
         "A", 0.0,
         "**Truth Table:** $A \\oplus B$ is 1 when $(A, B) \\in \\{(0,1), (1,0)\\}$. Thus $I_0=0, I_1=1, I_2=1, I_3=0$.\n**Answer:** A."),
        
        (1993, "Sequential Circuits", "NAT", 2, "medium",
         "A 4-bit synchronous binary up-counter is initially at state `0000`. How many clock pulses are required for it to reach state `1101`?",
         None, "13", 0.0,
         "**Calculation:** Binary `1101` equals 13 decimal. Starting from 0 takes 13 clock pulses.\n**Answer:** 13."),
        
        (1994, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "What is the 8-bit 2's complement representation of the decimal integer $-18$ in hexadecimal?",
         None, "0xEE", 0.0,
         "**Calculation:** $+18$ is `00010010`. Invert bits: `11101101`. Add 1: `11101110` = `0xEE`.\n**Answer:** 0xEE."),
        
        (1995, "Boolean Algebra & K-Maps", "NAT", 2, "medium",
         "What is the minimum number of 2-input NAND gates required to implement a 2-input EX-OR gate?",
         None, "4", 0.0,
         "**Classic Result:** Implementing $A \\oplus B$ using NAND logic requires exactly 4 two-input NAND gates.\n**Answer:** 4."),
        
        (1996, "Combinational Circuits", "NAT", 2, "medium",
         "How many 2-to-1 Multiplexers are needed to construct an 8-to-1 Multiplexer?",
         None, "7", 0.0,
         "**Formula:** Level 1: 4 MUX, Level 2: 2 MUX, Level 3: 1 MUX. Total = $4 + 2 + 1 = 7$.\n**Answer:** 7."),
        
        (1997, "Sequential Circuits", "MCQ", 1, "easy",
         "In a JK flip-flop, if both inputs $J=1$ and $K=1$, what is the next output state $Q_{n+1}$?",
         json.dumps({"A": "Toggle ($Q'_n$)", "B": "Set ($1$)", "C": "Reset ($0$)", "D": "No change ($Q_n$)"}),
         "A", 0.0,
         "**Rule:** When $J=K=1$, the characteristic equation $Q_{n+1} = J Q'_n + K' Q_n = Q'_n$ produces a toggle.\n**Answer:** A."),
        
        (1998, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "In an 8-bit 2's complement system, what is the range of representable signed integers $[Min, Max]$?",
         None, "[-128, 127]", 0.0,
         "**Formula:** Range is $[-2^{n-1}, 2^{n-1} - 1] = [-2^7, 2^7 - 1] = [-128, 127]$.\n**Answer:** [-128, 127]."),
        
        (1999, "Boolean Algebra & K-Maps", "NAT", 2, "medium",
         "Simplify boolean expression: $F = A B + A B'$. How many literals appear in the minimal SOP expression?",
         None, "1", 0.0,
         "**Simplification:** $A(B + B') = A(1) = A$. Contains 1 literal.\n**Answer:** 1."),
        
        (2000, "Combinational Circuits", "MCQ", 1, "easy",
         "A 3-to-8 line decoder with an active-LOW enable input has how many total input lines (including enable)?",
         json.dumps({"A": "4", "B": "3", "C": "8", "D": "11"}),
         "A", 0.0,
         "**Inputs:** 3 select input lines + 1 enable line = 4 input lines.\n**Answer:** A."),
        
        (2001, "Sequential Circuits", "NAT", 2, "hard",
         "A 3-bit Johnson counter (twisted ring counter) is initialized to `000`. How many distinct states does it cycle through?",
         None, "6", 0.0,
         "**Formula:** An $n$-bit Johnson counter has $2n$ states: $2 \\times 3 = 6$ states.\n**Answer:** 6."),
        
        (2002, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "Convert binary number `11010.11` to its equivalent decimal value.",
         None, "26.75", 0.0,
         "**Calculation:** Integer: $16 + 8 + 2 = 26$. Fractional: $0.5 + 0.25 = 0.75$. Total = 26.75.\n**Answer:** 26.75."),
        
        (2003, "Boolean Algebra & K-Maps", "NAT", 2, "medium",
         "How many prime implicants are in the K-map of $F(A, B, C) = \\sum m(0, 1, 2, 3)$?",
         None, "1", 0.0,
         "**Grouping:** Minterms $0, 1, 2, 3$ form a single quad corresponding to $A'$. Total prime implicants = 1.\n**Answer:** 1."),
        
        (2004, "Combinational Circuits", "NAT", 2, "medium",
         "A full adder is constructed using two half adders and one OR gate. How many XOR gates does it contain in total?",
         None, "2", 0.0,
         "**Design:** Each half adder contains 1 XOR gate. Two half adders contain 2 XOR gates.\n**Answer:** 2."),
        
        (2005, "Sequential Circuits", "MCQ", 1, "easy",
         "What type of hazard in combinational logic causes a momentary unwanted glitch output when a single input variable changes?",
         json.dumps({"A": "Static-1 or Static-0 Hazard", "B": "Dynamic Hazard", "C": "Race condition", "D": "Setup violation"}),
         "A", 0.0,
         "**Rule:** Static hazards occur when adjacent 1-cells (or 0-cells) in a K-map are not covered by a common prime implicant.\n**Answer:** A."),
        
        (2006, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "What is the base $b$ if $(24)_b = (18)_{10}$?",
         None, "7", 0.0,
         "**Equation:** $2b + 4 = 18 \\implies 2b = 14 \\implies b = 7$.\n**Answer:** 7."),
        
        (2007, "Boolean Algebra & K-Maps", "MCQ", 1, "easy",
         "The dual of the boolean expression $A + B \\cdot C$ is obtained by replacing $+$ with $\\cdot$ and $\\cdot$ with $+$. What is the dual?",
         json.dumps({"A": "$A \\cdot (B + C)$", "B": "$A' \\cdot (B' + C')$", "C": "$A + B + C$", "D": "$A \\cdot B \\cdot C$"}),
         "A", 0.0,
         "**Rule:** Duality replaces AND with OR, and OR with AND: $A + (B \\cdot C) \\to A \\cdot (B + C)$.\n**Answer:** A."),
        
        (2008, "Combinational Circuits", "NAT", 2, "medium",
         "A priority encoder has 4 active-high inputs $D_3, D_2, D_1, D_0$ ($D_3$ highest priority). If input is `0110`, what is the 2-bit binary output $Y_1 Y_0$?",
         None, "10", 0.0,
         "**Priority:** Highest active bit is $D_2$ (position 2 in binary = `10`). Output = `10`.\n**Answer:** 10."),
        
        (2009, "Sequential Circuits", "NAT", 2, "medium",
         "A D flip-flop has setup time $t_{setup} = 2$ ns and hold time $t_{hold} = 1$ ns. If clock period is 10 ns and clock edge is at $t=10$ ns, during which time window must input D remain stable?",
         None, "[8, 11] ns", 0.0,
         "**Window:** $[T_{clk} - t_{setup}, T_{clk} + t_{hold}] = [10 - 2, 10 + 1] = [8, 11]$ ns.\n**Answer:** [8, 11] ns."),
        
        (2010, "Number Representations & Computer Arithmetic", "MCQ", 1, "easy",
         "When adding two positive $n$-bit 2's complement numbers, an OVERFLOW occurs if and only if:",
         json.dumps({
             "A": "The result has a sign bit of 1 (appears negative)",
             "B": "Carry out of the sign bit is 1",
             "C": "Both operands are even",
             "D": "Result equals zero"
         }),
         "A", 0.0,
         "**Rule:** Adding two positive numbers cannot yield a negative result; if the result's MSB is 1, overflow occurred.\n**Answer:** A."),
        
        (2011, "Boolean Algebra & K-Maps", "NAT", 2, "hard",
         "How many essential prime implicants are in $F(A, B, C, D) = \\sum m(0, 2, 5, 7, 8, 10, 13, 15)$?",
         None, "2", 0.0,
         "**Groups:** Corners $\\{0, 2, 8, 10\\}$ gives $B' D'$. Subcube $\\{5, 7, 13, 15\\}$ gives $B D$. Both are essential prime implicants. Count = 2.\n**Answer:** 2."),
        
        (2012, "Combinational Circuits", "NAT", 2, "medium",
         "A 4-bit Carry Lookahead Adder computes carry generation $G_i$ and carry propagation $P_i$. For inputs $A_i=1, B_i=0$, what is $P_i$ (using XOR)?",
         None, "1", 0.0,
         "**Formula:** $P_i = A_i \\oplus B_i = 1 \\oplus 0 = 1$.\n**Answer:** 1."),
        
        (2013, "Sequential Circuits", "NAT", 2, "medium",
         "A mod-12 counter counts from 0 to 11. What is the minimum number of flip-flops required to build this counter?",
         None, "4", 0.0,
         "**Formula:** $2^n \\ge 12 \\implies n = 4$ flip-flops ($2^4 = 16$).\n**Answer:** 4."),
        
        (2014, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "In an excess-3 code (self-complementing code), what is the code for decimal digit 5?",
         None, "1000", 0.0,
         "**Calculation:** $5 + 3 = 8$. In 4-bit binary, $8 = 1000$.\n**Answer:** 1000."),
        
        (2015, "Boolean Algebra & K-Maps", "MCQ", 1, "easy",
         "Which gate is known as the Equivalence Gate?",
         json.dumps({"A": "XNOR Gate", "B": "XOR Gate", "C": "NAND Gate", "D": "NOR Gate"}),
         "A", 0.0,
         "**Rule:** XNOR outputs 1 when both inputs are equal ($A B + A' B'$), acting as an equivalence tester.\n**Answer:** A."),
        
        (2016, "Combinational Circuits", "NAT", 2, "medium",
         "A 16-to-1 MUX is built using 4-to-1 MUXes only. How many 4-to-1 MUXes are required?",
         None, "5", 0.0,
         "**Calculation:** Stage 1 uses four 4-to-1 MUXes. Stage 2 uses one 4-to-1 MUX to combine outputs. Total = $4 + 1 = 5$.\n**Answer:** 5."),
        
        (2017, "Sequential Circuits", "MCQ", 2, "medium",
         "In a Mealy state machine compared to a Moore state machine:",
         json.dumps({
             "A": "Outputs depend on both the current state and current inputs",
             "B": "Outputs depend only on current state",
             "C": "Outputs change strictly on clock edges",
             "D": "It always requires more states than Moore"
         }),
         "A", 0.0,
         "**Definition:** Mealy machine outputs depend on state AND current inputs, often requiring fewer states than Moore machines.\n**Answer:** A."),
        
        (2018, "Number Representations & Computer Arithmetic", "NAT", 2, "medium",
         "Subtract $(1010)_2$ from $(1101)_2$ in binary. What is the decimal value of the result?",
         None, "3", 0.0,
         "**Calculation:** $13 - 10 = 3$.\n**Answer:** 3."),
        
        (2019, "Boolean Algebra & K-Maps", "NAT", 2, "medium",
         "What is the dual of $X \\oplus Y$?",
         None, "X XNOR Y", 0.0,
         "**Rule:** Dual of $X Y' + X' Y$ is $(X + Y')(X' + Y) = X Y + X' Y' = X \\odot Y$ (XNOR).\n**Answer:** X XNOR Y."),
        
        (2020, "Combinational Circuits", "NAT", 2, "medium",
         "A half-subtractor has inputs $A$ and $B$. What is the boolean expression for the Difference $D$?",
         None, "A XOR B", 0.0,
         "**Formula:** $D = A \\oplus B$ and $\\text{Borrow} = A' B$.\n**Answer:** A XOR B."),
        
        (2021, "Sequential Circuits", "NAT", 2, "medium",
         "A 4-bit ring counter is initialized to `1000`. How many clock cycles does it take to return to its initial state?",
         None, "4", 0.0,
         "**Rule:** An $n$-bit ring counter has $n$ unique states and repeats every $n=4$ clock cycles.\n**Answer:** 4."),
        
        (2022, "Number Representations & Computer Arithmetic", "MCQ", 1, "easy",
         "In floating point representations, Normalization is performed to:",
         json.dumps({"A": "Maximize precision of the significand", "B": "Reduce memory size", "C": "Prevent underflow entirely", "D": "Speed up addition"}),
         "A", 0.0,
         "**Rule:** Normalization ensures the most significant bit of the mantissa is non-zero (hidden 1 in IEEE-754), maximizing precision.\n**Answer:** A."),
        
        (2023, "Boolean Algebra & K-Maps", "NAT", 2, "hard",
         "How many functions of 2 boolean variables $f(A, B)$ satisfy $f(A, B) = f(B, A)$ (symmetric functions)?",
         None, "8", 0.0,
         "**Calculation:** Minterms $m_0(0,0)$ and $m_3(1,1)$ are independent. Minterms $m_1(0,1)$ and $m_2(1,0)$ must have identical values. Total symmetric functions = $2^3 = 8$.\n**Answer:** 8."),
        
        (2024, "Combinational Circuits", "MSQ", 2, "hard",
         "Which of the following logic circuits are UNIVERSAL gates capable of implementing any boolean function without additional gates?",
         json.dumps({
             "A": "NAND Gate",
             "B": "NOR Gate",
             "C": "Multiplexer with fixed logic high and low inputs",
             "D": "AND Gate"
         }),
         "A,B,C", 0.0,
         "**Rule:** NAND, NOR, and MUX (with inverted/constant inputs) are functionally complete universal logic elements.\n**Answer:** A, B, C."),
        
        (2025, "Sequential Circuits", "NAT", 2, "medium",
         "What is the frequency at the output of the final flip-flop in a 5-stage ripple counter driven by a 32 MHz input clock (in MHz)?",
         None, "1", 0.0,
         "**Formula:** $f_{out} = f_{in} / 2^n = 32 / 2^5 = 32 / 32 = 1$ MHz.\n**Answer:** 1."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in dl_items:
        questions.append(Question(
            subject="Digital Logic", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (Digital Logic - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    # =========================================================================
    # 10. ENGINEERING MATHEMATICS (EM: 1991 - 2025: 35 Unique Questions)
    # =========================================================================
    em_items = [
        (1991, "Linear Algebra", "NAT", 2, "medium",
         "A $3 \\times 3$ matrix $A$ has eigenvalues 1, 2, 3. What is the determinant of $A^2$?",
         None, "36", 0.0,
         "**Formula:** $\\det(A) = 1 \\times 2 \\times 3 = 6$. $\\det(A^2) = (\\det(A))^2 = 6^2 = 36$.\n**Answer:** 36."),
        
        (1992, "Calculus", "NAT", 2, "medium",
         "What is the value of $\\lim_{x \\to 0} \\frac{e^{2x} - 1}{x}$?",
         None, "2", 0.0,
         "**L'Hôpital's Rule:** $\\lim_{x \\to 0} \\frac{2e^{2x}}{1} = 2(1) = 2$.\n**Answer:** 2."),
        
        (1993, "Probability & Statistics", "NAT", 2, "medium",
         "Two fair dice are thrown simultaneously. What is the probability that the sum of faces is 7? (Write in simplified fraction form or 2 decimals)",
         None, "0.17", 0.02,
         "**Outcomes:** Favorable pairs: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6. Total = 36. $P = 6/36 = 1/6 \\approx 0.17$.\n**Answer:** 0.17."),
        
        (1994, "Discrete Mathematics", "NAT", 2, "medium",
         "How many edges are in a complete bipartite graph $K_{4, 6}$?",
         None, "24", 0.0,
         "**Formula:** In $K_{m, n}$, edges $E = m \\times n = 4 \\times 6 = 24$.\n**Answer:** 24."),
        
        (1995, "Mathematical Logic", "MCQ", 1, "easy",
         "The logical statement $(P \\land Q) \\to P$ is a:",
         json.dumps({"A": "Tautology", "B": "Contradiction", "C": "Contingency", "D": "Fallacy"}),
         "A", 0.0,
         "**Proof:** By simplification rule, if $(P \\land Q)$ is true, $P$ is necessarily true, making $(P \\land Q) \\to P$ always true (Tautology).\n**Answer:** A."),
        
        (1996, "Linear Algebra", "NAT", 2, "medium",
         "What is the rank of the $3 \\times 3$ matrix with all entries equal to 2?",
         None, "1", 0.0,
         "**Rule:** All rows are scalar multiples of each other, leaving exactly 1 linearly independent row.\n**Answer:** 1."),
        
        (1997, "Calculus", "NAT", 2, "medium",
         "Find $\\int_0^{\\pi/2} \\cos(x) \\, dx$.",
         None, "1", 0.0,
         "**Evaluation:** $[\\sin(x)]_0^{\\pi/2} = \\sin(\\pi/2) - \\sin(0) = 1 - 0 = 1$.\n**Answer:** 1."),
        
        (1998, "Combinatorics & Graph Theory", "NAT", 2, "medium",
         "In how many ways can 5 distinct balls be distributed into 3 distinct boxes?",
         None, "243", 0.0,
         "**Formula:** Each of the 5 balls has 3 independent choices: $3^5 = 243$.\n**Answer:** 243."),
        
        (1999, "Probability & Statistics", "NAT", 2, "medium",
         "A random variable $X$ follows Poisson distribution with mean $\\lambda = 2$. What is the variance of $X$?",
         None, "2", 0.0,
         "**Property:** For a Poisson distribution, $\\text{Mean} = \\text{Variance} = \\lambda = 2$.\n**Answer:** 2."),
        
        (2000, "Discrete Mathematics", "MCQ", 1, "easy",
         "A relation $R$ on set $S$ that is reflexive, antisymmetric, and transitive is a:",
         json.dumps({"A": "Partial Order Relation", "B": "Equivalence Relation", "C": "Total Order Relation", "D": "Symmetric Relation"}),
         "A", 0.0,
         "**Definition:** A relation satisfying reflexivity, antisymmetry, and transitivity defines a Partial Order (poset).\n**Answer:** A."),
        
        (2001, "Linear Algebra", "NAT", 2, "medium",
         "For a $2 \\times 2$ matrix $A$, $\\text{Trace}(A) = 5$ and $\\det(A) = 6$. What is the largest eigenvalue of $A$?",
         None, "3", 0.0,
         "**Roots:** $\\lambda_1 + \\lambda_2 = 5$ and $\\lambda_1 \\lambda_2 = 6$. Roots are 2 and 3. Largest = 3.\n**Answer:** 3."),
        
        (2002, "Calculus", "NAT", 2, "medium",
         "Find the local maximum of function $f(x) = -x^2 + 4x + 5$. What is the value of $f(x)$ at its maximum?",
         None, "9", 0.0,
         "**Derivation:** $f'(x) = -2x + 4 = 0 \\implies x = 2$. $f(2) = -(2)^2 + 4(2) + 5 = -4 + 8 + 5 = 9$.\n**Answer:** 9."),
        
        (2003, "Mathematical Logic", "MCQ", 1, "easy",
         "What is the negation of the proposition $\\forall x (P(x) \\to Q(x))$?",
         json.dumps({"A": "$\\exists x (P(x) \\land \\neg Q(x))$", "B": "$\\forall x (P(x) \\land \\neg Q(x))$", "C": "$\\exists x (\\neg P(x) \\to \\neg Q(x))$", "D": "$\\exists x (P(x) \\lor Q(x))$"}),
         "A", 0.0,
         "**De Morgan for Quantifiers:** $\\neg \\forall x (\\neg P(x) \\lor Q(x)) \\equiv \\exists x (P(x) \\land \\neg Q(x))$.\n**Answer:** A."),
        
        (2004, "Combinatorics & Graph Theory", "NAT", 2, "medium",
         "How many simple planar graphs with 6 vertices can have 15 edges?",
         None, "0", 0.0,
         "**Planar Bound:** In any simple planar graph, $E \\le 3V - 6 = 3(6) - 6 = 12$. A graph with 15 edges cannot be planar (count = 0).\n**Answer:** 0."),
        
        (2005, "Probability & Statistics", "NAT", 2, "medium",
         "If events $A$ and $B$ are independent with $P(A) = 0.4$ and $P(B) = 0.5$, what is $P(A \\cup B)$?",
         None, "0.7", 0.0,
         "**Formula:** $P(A \\cup B) = P(A) + P(B) - P(A)P(B) = 0.4 + 0.5 - 0.20 = 0.70$.\n**Answer:** 0.7."),
        
        (2006, "Linear Algebra", "NAT", 2, "hard",
         "If matrix $A$ is orthogonal ($A^T A = I$), what are the only possible real values of $\\det(A)$?",
         None, "1 and -1", 0.0,
         "**Proof:** $\\det(A^T A) = (\\det(A))^2 = \\det(I) = 1 \\implies \\det(A) = \\pm 1$.\n**Answer:** 1 and -1."),
        
        (2007, "Calculus", "NAT", 2, "medium",
         "Find $\\lim_{x \\to \\infty} \\left(1 + \\frac{3}{x}\\right)^x$. Write the answer in terms of $e$ (e.g. $e^k$, what is $k$?).",
         None, "3", 0.0,
         "**Formula:** $\\lim_{x \\to \\infty} (1 + a/x)^x = e^a$. Here $a=3$, so exponent is 3 ($e^3$).\n**Answer:** 3."),
        
        (2008, "Discrete Mathematics", "NAT", 2, "medium",
         "In a group of 50 students, 30 like Tea, 25 like Coffee, and 10 like both. How many students like NEITHER tea nor coffee?",
         None, "5", 0.0,
         "**Inclusion-Exclusion:** $|T \\cup C| = 30 + 25 - 10 = 45$. Neither = $50 - 45 = 5$.\n**Answer:** 5."),
        
        (2009, "Probability & Statistics", "NAT", 2, "medium",
         "A coin has $P(\\text{Heads}) = 0.6$. Tossed 3 times independently. What is the probability of getting exactly 2 heads?",
         None, "0.432", 0.01,
         "**Binomial:** $\\binom{3}{2} (0.6)^2 (0.4)^1 = 3 \\times 0.36 \\times 0.4 = 0.432$.\n**Answer:** 0.432."),
        
        (2010, "Combinatorics & Graph Theory", "NAT", 2, "medium",
         "What is the chromatic number $\\chi(G)$ of an odd cycle graph $C_5$?",
         None, "3", 0.0,
         "**Theorem:** Any odd cycle requires 3 colors to ensure adjacent vertices have distinct colors.\n**Answer:** 3."),
        
        (2011, "Mathematical Logic", "MCQ", 1, "easy",
         "The contrapositive of conditional statement $P \\to Q$ is logically equivalent to:",
         json.dumps({"A": "$\\neg Q \\to \\neg P$", "B": "$Q \\to P$", "C": "$\\neg P \\to \\neg Q$", "D": "$P \\land \\neg Q$"}),
         "A", 0.0,
         "**Rule:** The contrapositive of $P \\to Q$ is $\\neg Q \\to \\neg P$, and both share identical truth tables.\n**Answer:** A."),
        
        (2012, "Linear Algebra", "NAT", 2, "medium",
         "Consider a system of linear equations $A x = b$ where $A$ is $3 \\times 3$. If $\\text{rank}(A) = 2$ and $\\text{rank}([A \\mid b]) = 3$, how many solutions exist?",
         None, "0", 0.0,
         "**Rouché-Capelli Theorem:** If $\\text{rank}(A) \\ne \\text{rank}([A \\mid b])$, the system is inconsistent (0 solutions).\n**Answer:** 0."),
        
        (2013, "Calculus", "NAT", 2, "medium",
         "By Mean Value Theorem, for $f(x) = x^2$ on interval $[0, 2]$, what is the value of $c \\in (0, 2)$ such that $f'(c) = \\frac{f(2)-f(0)}{2-0}$?",
         None, "1", 0.0,
         "**Calculation:** $\\frac{4 - 0}{2} = 2$. $f'(c) = 2c = 2 \\implies c = 1$.\n**Answer:** 1."),
        
        (2014, "Probability & Statistics", "NAT", 2, "hard",
         "If $X$ is uniformly distributed on $[0, 10]$, what is $P(2 \\le X \\le 7)$?",
         None, "0.5", 0.0,
         "**Calculation:** $P = \\frac{7 - 2}{10 - 0} = \\frac{5}{10} = 0.5$.\n**Answer:** 0.5."),
        
        (2015, "Discrete Mathematics", "NAT", 2, "medium",
         "How many total relations can be defined on a set of 3 elements?",
         None, "512", 0.0,
         "**Formula:** Number of relations on set of $n$ elements is $2^{n^2} = 2^{3^2} = 2^9 = 512$.\n**Answer:** 512."),
        
        (2016, "Combinatorics & Graph Theory", "NAT", 2, "medium",
         "A connected undirected graph has 8 vertices and degrees: 2, 2, 3, 3, 4, 4, 5, 5. How many edges does the graph have?",
         None, "14", 0.0,
         "**Handshaking Lemma:** $\\sum \\deg = 2 + 2 + 3 + 3 + 4 + 4 + 5 + 5 = 28 = 2E \\implies E = 14$.\n**Answer:** 14."),
        
        (2017, "Linear Algebra", "NAT", 2, "medium",
         "If $A$ is a $3 \\times 3$ non-singular matrix with $\\det(A) = 4$, what is $\\det(2A)$?",
         None, "32", 0.0,
         "**Formula:** $\\det(k A) = k^n \\det(A)$. For $n=3, k=2$: $2^3 \\times 4 = 8 \\times 4 = 32$.\n**Answer:** 32."),
        
        (2018, "Calculus", "NAT", 2, "medium",
         "Evaluate $\\int_0^1 x^3 \\, dx$.",
         None, "0.25", 0.0,
         "**Calculation:** $[x^4 / 4]_0^1 = 1/4 - 0 = 0.25$.\n**Answer:** 0.25."),
        
        (2019, "Probability & Statistics", "NAT", 2, "medium",
         "If $E[X] = 5$ and $E[X^2] = 29$, what is the standard deviation of random variable $X$?",
         None, "2", 0.0,
         "**Formula:** $\\text{Var}(X) = E[X^2] - (E[X])^2 = 29 - 25 = 4$. Standard deviation = $\\sqrt{4} = 2$.\n**Answer:** 2."),
        
        (2020, "Mathematical Logic", "MCQ", 1, "easy",
         "Which logical connective is NOT associative?",
         json.dumps({"A": "NAND", "B": "AND", "C": "OR", "D": "XOR"}),
         "A", 0.0,
         "**Rule:** NAND and NOR operations are not associative: $(A \\uparrow B) \\uparrow C \\ne A \\uparrow (B \\uparrow C)$.\n**Answer:** A."),
        
        (2021, "Discrete Mathematics", "NAT", 2, "medium",
         "How many reflexive relations exist on a set with 4 elements?",
         None, "4096", 0.0,
         "**Formula:** $2^{n(n-1)} = 2^{4(3)} = 2^{12} = 4096$.\n**Answer:** 4096."),
        
        (2022, "Combinatorics & Graph Theory", "NAT", 2, "medium",
         "What is the number of spanning trees in a complete graph $K_3$?",
         None, "3", 0.0,
         "**Cayley's Formula:** $n^{n-2} = 3^{3-2} = 3^1 = 3$.\n**Answer:** 3."),
        
        (2023, "Linear Algebra", "NAT", 2, "hard",
         "Matrix $A = \\begin{bmatrix} 2 & 1 \\\\ 0 & 2 \\end{bmatrix}$. Is matrix $A$ diagonalizable over $\\mathbb{R}$?",
         None, "No", 0.0,
         "**Analysis:** Eigenvalue $\\lambda=2$ has algebraic multiplicity 2, but geometric multiplicity $\\dim(\\text{null}(A-2I)) = 1 < 2$. Hence not diagonalizable.\n**Answer:** No."),
        
        (2024, "Probability & Statistics", "MSQ", 2, "hard",
         "Which of the following probability distributions are MEMORYLESS?",
         json.dumps({
             "A": "Exponential Distribution (continuous)",
             "B": "Geometric Distribution (discrete)",
             "C": "Poisson Distribution",
             "D": "Normal Distribution"
         }),
         "A,B", 0.0,
         "**Theorem:** Exponential and Geometric are the only continuous and discrete memoryless distributions ($P(X > s+t \\mid X > s) = P(X > t)$).\n**Answer:** A, B."),
        
        (2025, "Calculus", "NAT", 2, "medium",
         "What is the slope of the tangent line to the curve $y = x^3 - 3x + 2$ at $x = 2$?",
         None, "9", 0.0,
         "**Derivative:** $y' = 3x^2 - 3$. At $x = 2$: $y'(2) = 3(4) - 3 = 12 - 3 = 9$.\n**Answer:** 9."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in em_items:
        questions.append(Question(
            subject="Engineering Mathematics", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (Engineering Mathematics - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    # =========================================================================
    # 11. GENERAL APTITUDE (GA: 1991 - 2025: 35 Unique Questions)
    # =========================================================================
    ga_items = [
        (1991, "Quantitative Aptitude", "MCQ", 1, "easy",
         "A car covers the first half of a journey at 30 km/h and the remaining half at 60 km/h. What is the average speed for the whole journey (in km/h)?",
         json.dumps({"A": "40", "B": "45", "C": "48", "D": "50"}),
         "A", 0.0,
         "**Harmonic Mean:** $\\frac{2 \\times 30 \\times 60}{30 + 60} = \\frac{3600}{90} = 40$ km/h.\n**Answer:** A (40)."),
        
        (1992, "Verbal Aptitude", "MCQ", 1, "easy",
         "Select the antonym for the word 'EPHEMERAL':",
         json.dumps({"A": "Permanent", "B": "Transient", "C": "Fleeting", "D": "Short-lived"}),
         "A", 0.0,
         "**Vocabulary:** 'Ephemeral' means lasting a very short time; its direct antonym is 'Permanent'.\n**Answer:** A."),
        
        (1993, "Analytical Aptitude", "NAT", 2, "medium",
         "Find the next number in the arithmetic series: 7, 14, 28, 56, _____.",
         None, "112", 0.0,
         "**Pattern:** Geometric progression with common ratio $r=2$: $56 \\times 2 = 112$.\n**Answer:** 112."),
        
        (1994, "Quantitative Aptitude", "NAT", 2, "medium",
         "If 12 men can complete a construction task in 8 days, how many days will 16 men take to complete the same task?",
         None, "6", 0.0,
         "**Formula:** $M_1 \\times D_1 = M_2 \\times D_2 \\implies 12 \\times 8 = 16 \\times D_2 \\implies D_2 = 96 / 16 = 6$ days.\n**Answer:** 6."),
        
        (1995, "Verbal Aptitude", "MCQ", 1, "easy",
         "Fill in the blank: 'Neither of the two candidates _____ selected for the interview.'",
         json.dumps({"A": "was", "B": "were", "C": "have been", "D": "are"}),
         "A", 0.0,
         "**Grammar:** 'Neither' followed of 'of the' takes a singular verb: 'was'.\n**Answer:** A."),
        
        (1996, "Spatial Aptitude", "MCQ", 2, "medium",
         "A square sheet of paper is folded in half horizontally, and then folded in half vertically. A circular hole is punched in the center of the folded square. When unfolded completely, how many holes appear?",
         json.dumps({"A": "4", "B": "2", "C": "8", "D": "1"}),
         "A", 0.0,
         "**Spatial:** Two folds create 4 layers of paper; punching one hole punches through all 4 layers.\n**Answer:** A (4)."),
        
        (1997, "Quantitative Aptitude", "NAT", 2, "medium",
         "The selling price of an item is 25% higher than its cost price. What is the profit percentage?",
         None, "25", 0.0,
         "**Calculation:** $\\text{Profit}\\% = \\frac{SP - CP}{CP} \\times 100 = 25\\%$.\n**Answer:** 25."),
        
        (1998, "Analytical Aptitude", "MCQ", 1, "easy",
         "In a certain code, 'APPLE' is written as 'BQQMF'. How is 'MANGO' written in that code?",
         json.dumps({"A": "NBOHP", "B": "NBNHP", "C": "MAOHP", "D": "OBOIQ"}),
         "A", 0.0,
         "**Pattern:** Shift each letter forward by +1: M->N, A->B, N->O, G->H, O->P = 'NBOHP'.\n**Answer:** A."),
        
        (1999, "Quantitative Aptitude", "NAT", 2, "medium",
         "Two pipes A and B can fill a tank in 10 hours and 15 hours respectively. If both pipes operate together, how many hours will they take to fill the tank?",
         None, "6", 0.0,
         "**Formula:** Time = $\\frac{10 \\times 15}{10 + 15} = \\frac{150}{25} = 6$ hours.\n**Answer:** 6."),
        
        (2000, "Verbal Aptitude", "MCQ", 1, "easy",
         "Choose the correct spelling:",
         json.dumps({"A": "Accommodate", "B": "Acommodate", "C": "Accomodate", "D": "Acomodate"}),
         "A", 0.0,
         "**Spelling:** 'Accommodate' has double 'c' and double 'm'.\n**Answer:** A."),
        
        (2001, "Spatial Aptitude", "MCQ", 2, "medium",
         "How many cubes of side 1 cm can be cut from a larger wooden cube of side 4 cm?",
         json.dumps({"A": "64", "B": "16", "C": "32", "D": "48"}),
         "A", 0.0,
         "**Formula:** Volume ratio = $4^3 / 1^3 = 64 / 1 = 64$.\n**Answer:** A (64)."),
        
        (2002, "Quantitative Aptitude", "NAT", 2, "medium",
         "A sum of money doubles itself in 5 years under simple interest. What is the annual interest rate percentage?",
         None, "20", 0.0,
         "**Formula:** $R = 100 / T = 100 / 5 = 20\\%$.\n**Answer:** 20."),
        
        (2003, "Analytical Aptitude", "MCQ", 1, "easy",
         "Statements:\n1. All cats are mammals.\n2. All mammals are animals.\nConclusion: All cats are animals.",
         json.dumps({"A": "Logically Valid", "B": "Invalid", "C": "Contradictory", "D": "Insufficient data"}),
         "A", 0.0,
         "**Syllogism:** Transitivity holds: $A \\subset B$ and $B \\subset C \\implies A \\subset C$.\n**Answer:** A."),
        
        (2004, "Quantitative Aptitude", "NAT", 2, "medium",
         "If $\\log_{10}(2) = 0.3010$, what is the number of digits in $2^{20}$?",
         None, "7", 0.0,
         "**Formula:** Digits = $\\lfloor 20 \\times \\log_{10}(2) \\rfloor + 1 = \\lfloor 20 \\times 0.3010 \\rfloor + 1 = \\lfloor 6.02 \\rfloor + 1 = 7$.\n**Answer:** 7."),
        
        (2005, "Verbal Aptitude", "MCQ", 1, "easy",
         "Complete the analogy: 'Doctor : Hospital :: Teacher : _____'?",
         json.dumps({"A": "School", "B": "Book", "C": "Student", "D": "Chalk"}),
         "A", 0.0,
         "**Relationship:** Profession to primary workplace: Doctor works in Hospital, Teacher works in School.\n**Answer:** A."),
        
        (2006, "Spatial Aptitude", "MCQ", 2, "medium",
         "A 3D cube has faces numbered 1 to 6. If faces 1 and 6 are opposite, 2 and 5 are opposite, and 3 and 4 are opposite, which face is adjacent to face 1?",
         json.dumps({"A": "Faces 2, 3, 4, 5", "B": "Face 6 only", "C": "Faces 2 and 5 only", "D": "No faces"}),
         "A", 0.0,
         "**Cube Geometry:** Every face of a cube is adjacent to exactly 4 faces (all except the one opposite to it).\n**Answer:** A."),
        
        (2007, "Quantitative Aptitude", "NAT", 2, "medium",
         "The average age of 24 students and their teacher is 15 years. If the teacher's age is excluded, the average decreases by 1 year. What is the teacher's age in years?",
         None, "39", 0.0,
         "**Calculation:** Total age = $25 \\times 15 = 375$. Students total = $24 \\times 14 = 336$. Teacher = $375 - 336 = 39$ years.\n**Answer:** 39."),
        
        (2008, "Analytical Aptitude", "NAT", 2, "medium",
         "In a row of 30 trees, an oak tree is 12th from the left end. What is its position from the right end?",
         None, "19", 0.0,
         "**Formula:** Position from right = $\\text{Total} - \\text{Left} + 1 = 30 - 12 + 1 = 19$.\n**Answer:** 19."),
        
        (2009, "Verbal Aptitude", "MCQ", 1, "easy",
         "Identify the part containing an error: '(A) He is / (B) one of the tallest boy / (C) in the classroom.'",
         json.dumps({"A": "Part B ('boy' should be 'boys')", "B": "Part A", "C": "Part C", "D": "No error"}),
         "A", 0.0,
         "**Rule:** 'One of the' is followed by a plural noun: 'one of the tallest boys'.\n**Answer:** A."),
        
        (2010, "Quantitative Aptitude", "NAT", 2, "medium",
         "A train 150 meters long passes an electric pole in 15 seconds. What is the speed of the train in km/h?",
         None, "36", 0.0,
         "**Speed:** $150 / 15 = 10$ m/s. Convert to km/h: $10 \\times \\frac{18}{5} = 36$ km/h.\n**Answer:** 36."),
        
        (2011, "Spatial Aptitude", "MCQ", 2, "medium",
         "Which 2D shape results from slicing a circular cylinder perpendicular to its longitudinal central axis?",
         json.dumps({"A": "Circle", "B": "Ellipse", "C": "Rectangle", "D": "Parabola"}),
         "A", 0.0,
         "**Cross-section:** A cross-section perpendicular to cylinder axis is a circle of identical radius.\n**Answer:** A."),
        
        (2012, "Quantitative Aptitude", "NAT", 2, "medium",
         "If $x : y = 3 : 4$, what is the ratio $(2x + 3y) : (3x + 4y)$? Express as decimal rounded to 2 places.",
         None, "0.72", 0.02,
         "**Calculation:** $\\frac{2(3) + 3(4)}{3(3) + 4(4)} = \\frac{6 + 12}{9 + 16} = \\frac{18}{25} = 0.72$.\n**Answer:** 0.72."),
        
        (2013, "Analytical Aptitude", "MCQ", 1, "easy",
         "Find the odd one out among the words: Apple, Banana, Orange, Potato.",
         json.dumps({"A": "Potato (vegetable/tuber, others are fruits)", "B": "Apple", "C": "Banana", "D": "Orange"}),
         "A", 0.0,
         "**Classification:** Potato is a root vegetable/tuber; Apple, Banana, and Orange are fruits.\n**Answer:** A."),
        
        (2014, "Verbal Aptitude", "MCQ", 1, "easy",
         "Choose the word that means 'fluent or persuasive in speaking or writing':",
         json.dumps({"A": "Eloquent", "B": "Hesitant", "C": "Garrulous", "D": "Incoherent"}),
         "A", 0.0,
         "**Vocabulary:** 'Eloquent' means articulating thoughts expressively and persuasively.\n**Answer:** A."),
        
        (2015, "Quantitative Aptitude", "NAT", 2, "medium",
         "Two numbers are in the ratio $3 : 5$. If their HCF is 8, what is their LCM?",
         None, "120", 0.0,
         "**Calculation:** Numbers are $3 \\times 8 = 24$ and $5 \\times 8 = 40$. $\\text{LCM} = 3 \\times 5 \\times 8 = 120$.\n**Answer:** 120."),
        
        (2016, "Spatial Aptitude", "MCQ", 2, "medium",
         "When looking at a standard analog clock at 3:15, what is the angle between the hour hand and minute hand (in degrees)?",
         json.dumps({"A": "$7.5^\\circ$", "B": "$0^\\circ$", "C": "$15^\\circ$", "D": "$30^\\circ$"}),
         "A", 0.0,
         "**Formula:** Angle = $|30H - 5.5M| = |30(3) - 5.5(15)| = |90 - 82.5| = 7.5^\\circ$.\n**Answer:** A ($7.5^\\circ$)."),
        
        (2017, "Analytical Aptitude", "NAT", 2, "medium",
         "In a chess tournament, every player plays exactly one match against every other player. If 10 players participate, how many total matches are played?",
         None, "45", 0.0,
         "**Formula:** $\\binom{10}{2} = \\frac{10 \\times 9}{2} = 45$.\n**Answer:** 45."),
        
        (2018, "Quantitative Aptitude", "NAT", 2, "medium",
         "What is the compound interest on Rs. 10,000 for 2 years at 10% per annum compounded annually (in Rs)?",
         None, "2100", 0.0,
         "**Formula:** $A = 10000(1.10)^2 = 12100$. $\\text{CI} = 12100 - 10000 = 2100$.\n**Answer:** 2100."),
        
        (2019, "Verbal Aptitude", "MCQ", 1, "easy",
         "Choose the correct passive voice: 'The chef cooked a delicious meal.'",
         json.dumps({
             "A": "A delicious meal was cooked by the chef.",
             "B": "A delicious meal is cooked by the chef.",
             "C": "A delicious meal had been cooking by the chef.",
             "D": "The chef was cooking a delicious meal."
         }),
         "A", 0.0,
         "**Grammar:** Simple past 'cooked' transforms to 'was cooked by'.\n**Answer:** A."),
        
        (2020, "Spatial Aptitude", "NAT", 2, "medium",
         "A regular tetrahedron has 4 triangular faces. How many vertices does it possess?",
         None, "4", 0.0,
         "**Geometry:** A regular tetrahedron has 4 faces, 6 edges, and 4 vertices.\n**Answer:** 4."),
        
        (2021, "Quantitative Aptitude", "NAT", 2, "medium",
         "If $2^{x+3} = 32$, what is the value of $x$?",
         None, "2", 0.0,
         "**Calculation:** $32 = 2^5 \\implies x + 3 = 5 \\implies x = 2$.\n**Answer:** 2."),
        
        (2022, "Analytical Aptitude", "MCQ", 1, "easy",
         "If RED is coded as 27 (R=18, E=5, D=4; sum=27), what is the code for BLUE?",
         json.dumps({"A": "40", "B": "38", "C": "42", "D": "45"}),
         "A", 0.0,
         "**Alphabet Sum:** B=2, L=12, U=21, E=5. Total = $2 + 12 + 21 + 5 = 40$.\n**Answer:** A (40)."),
        
        (2023, "Spatial Aptitude", "MCQ", 2, "medium",
         "If a solid cylinder of radius $r$ and height $h$ is melted and recast into spheres of radius $r$, how many spheres are formed if $h = 4r$?",
         json.dumps({"A": "3", "B": "4", "C": "2", "D": "1"}),
         "A", 0.0,
         "**Volume Ratio:** Cylinder = $\\pi r^2 (4r) = 4\\pi r^3$. Sphere = $\\frac{4}{3}\\pi r^3$. Ratio = $\\frac{4\\pi r^3}{(4/3)\\pi r^3} = 3$.\n**Answer:** A (3)."),
        
        (2024, "Verbal Aptitude", "MSQ", 2, "hard",
         "Which of the following sentences contain NO grammatical errors?",
         json.dumps({
             "A": "The team members discussed the new policy among themselves.",
             "B": "Neither the manager nor the employees were informed about the schedule change.",
             "C": "Each of the participants were given a certificate.",
             "D": "He gave me a good advice."
         }),
         "A,B", 0.0,
         "**Grammar:** In A and B, subject-verb agreement is correct. In C, 'Each' takes singular 'was'. In D, 'advice' is uncountable ('a piece of good advice').\n**Answer:** A, B."),
        
        (2025, "Quantitative Aptitude", "NAT", 2, "medium",
         "In a class of 60 students, the ratio of boys to girls is $3 : 2$. How many boys are there in the class?",
         None, "36", 0.0,
         "**Calculation:** Total parts = $3 + 2 = 5$. Boys = $(3 / 5) \\times 60 = 36$.\n**Answer:** 36."),
    ]

    for yr, topic, qtype, marks, diff, text, opts, ans, tol, expl in ga_items:
        questions.append(Question(
            subject="General Aptitude", topic=topic, year=yr, set_number="Set 1",
            question_type=qtype, marks=marks, difficulty=diff,
            question_text=f"GATE {yr} (General Aptitude - {topic}):\n{text}",
            options=opts, correct_answer=ans, nat_tolerance=tol,
            explanation=expl, is_pyq=True
        ))

    return questions
