// Subject definitions matching backend database names
export const SUBJECTS = [
  {
    id: 'GA',
    name: 'General Aptitude',
    displayName: 'General Aptitude',
    subtitle: 'Verbal, Quantitative, Analytical & Spatial',
    icon: 'Brain',
    color: 'text-violet-500',
    bg: 'bg-violet-100',
    gradient: 'from-violet-500 to-purple-600'
  },
  {
    id: 'EM',
    name: 'Engineering Mathematics',
    displayName: 'Engineering Mathematics',
    subtitle: 'Discrete Math, Linear Algebra, Calculus, Probability',
    icon: 'Calculator',
    color: 'text-blue-500',
    bg: 'bg-blue-100',
    gradient: 'from-blue-500 to-indigo-600'
  },
  {
    id: 'DL',
    name: 'Digital Logic',
    displayName: 'Digital Logic',
    subtitle: 'Boolean Algebra, Combinational & Sequential Circuits',
    icon: 'CircuitBoard',
    color: 'text-cyan-500',
    bg: 'bg-cyan-100',
    gradient: 'from-cyan-500 to-blue-600'
  },
  {
    id: 'COA',
    name: 'COA',
    displayName: 'Computer Organization & Architecture',
    subtitle: 'Pipelining, Cache Memory, Addressing Modes, I/O',
    icon: 'Cpu',
    color: 'text-orange-500',
    bg: 'bg-orange-100',
    gradient: 'from-orange-500 to-red-600'
  },
  {
    id: 'PDS',
    name: 'Programming & DS',
    displayName: 'Programming & Data Structures',
    subtitle: 'C Programming, Recursion, Arrays, Trees, Stacks, Queues',
    icon: 'Code',
    color: 'text-green-500',
    bg: 'bg-green-100',
    gradient: 'from-green-500 to-emerald-600'
  },
  {
    id: 'ALGO',
    name: 'Algorithms',
    displayName: 'Algorithms',
    subtitle: 'Asymptotic Analysis, Greedy, DP, Graph Algorithms, Sorting',
    icon: 'GitBranch',
    color: 'text-emerald-500',
    bg: 'bg-emerald-100',
    gradient: 'from-emerald-500 to-teal-600'
  },
  {
    id: 'TOC',
    name: 'TOC',
    displayName: 'Theory of Computation',
    subtitle: 'DFA/NFA, Regular Expressions, CFG, PDA, Turing Machines',
    icon: 'Infinity',
    color: 'text-purple-500',
    bg: 'bg-purple-100',
    gradient: 'from-purple-500 to-violet-600'
  },
  {
    id: 'CD',
    name: 'Compiler Design',
    displayName: 'Compiler Design',
    subtitle: 'Lexical Analysis, LL/LR Parsing, SDT, Runtime Environments',
    icon: 'Layers',
    color: 'text-pink-500',
    bg: 'bg-pink-100',
    gradient: 'from-pink-500 to-rose-600'
  },
  {
    id: 'OS',
    name: 'OS',
    displayName: 'Operating Systems',
    subtitle: 'Processes, CPU Scheduling, Deadlocks, Paging, Virtual Memory',
    icon: 'Monitor',
    color: 'text-amber-500',
    bg: 'bg-amber-100',
    gradient: 'from-amber-500 to-orange-600'
  },
  {
    id: 'DBMS',
    name: 'DBMS',
    displayName: 'Database Management Systems',
    subtitle: 'ER Model, Relational Algebra, SQL, Normalization, Transactions',
    icon: 'Database',
    color: 'text-indigo-500',
    bg: 'bg-indigo-100',
    gradient: 'from-indigo-500 to-blue-600'
  },
  {
    id: 'CN',
    name: 'Computer Networks',
    displayName: 'Computer Networks',
    subtitle: 'IPv4 Subnetting, Routing, TCP Congestion, Data Link Layer',
    icon: 'Network',
    color: 'text-teal-500',
    bg: 'bg-teal-100',
    gradient: 'from-teal-500 to-cyan-600'
  },
];

export const SUBJECT_FULL_NAMES = {
  'General Aptitude': 'General Aptitude',
  'Engineering Mathematics': 'Engineering Mathematics',
  'Digital Logic': 'Digital Logic',
  'COA': 'Computer Organization & Architecture',
  'Programming & DS': 'Programming & Data Structures',
  'Algorithms': 'Algorithms',
  'TOC': 'Theory of Computation',
  'Compiler Design': 'Compiler Design',
  'OS': 'Operating Systems',
  'DBMS': 'Database Management Systems',
  'Computer Networks': 'Computer Networks',
};

export const DIFFICULTY_COLORS = {
  easy: 'bg-emerald-100 text-emerald-700 border-emerald-200',
  medium: 'bg-amber-100 text-amber-700 border-amber-200',
  hard: 'bg-red-100 text-red-700 border-red-200',
};

export const QUESTION_TYPES = {
  MCQ: { label: 'Multiple Choice', abbr: 'MCQ', color: 'bg-blue-100 text-blue-700' },
  MSQ: { label: 'Multiple Select', abbr: 'MSQ', color: 'bg-purple-100 text-purple-700' },
  NAT: { label: 'Numerical Answer', abbr: 'NAT', color: 'bg-teal-100 text-teal-700' },
};
