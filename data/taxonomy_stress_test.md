# AI boundary stress test

These eight synthetic questions test the definitions; none belongs in labels.csv.
All decisions below were made by the assistant, not in a student breakout.

| Synthetic question | Label | Reason |
|---|---|---|
| How can I minimize a DFA faster? | formal_language | The requested output is an automaton. |
| Prove this graph shortest-path routine is correct. | algorithm | A proof request alone does not make this language theory. |
| Is the set of balanced-parenthesis strings context-free? | formal_language | The requested result is a language classification. |
| Return all unmatched-parenthesis indices in constant extra space. | algorithm | The output is positions in data, not a recognizing machine or language property. |
| What language class includes regexes with backreferences? | formal_language | Expressive power of language representations. |
| How can I reduce cache misses in a string-search routine? | algorithm | Implementation cost of a general procedure. |
| Construct a grammar for strings with twice as many a's as b's. | formal_language | The requested object is a grammar. |
| Represent TSP as a decision language, then give a faster solver. | algorithm | Language notation is incidental to solving the optimization problem. |

Strongest competing cases for DFA minimization: it is an algorithm with a
correctness proof (algorithm); its input and output are recognizing machines
and its proof concerns the language preserved (formal_language). Both are
reasonable without a priority rule. The written taxonomy resolves this in favor
of formal_language based on the requested object, even for a complexity question.

The labels cover two selected CS subject areas. Questions about unrelated CS
topics need an out-of-scope decision before using this classifier in practice.
