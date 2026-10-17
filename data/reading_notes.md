# Community reading notes

Community: https://cs.stackexchange.com/ (public Computer Science Stack Exchange).
The assistant collected questions through the public Stack Exchange API and read
a 36-question sample (18 from each collection stratum). This was not a student
twenty-minute reading exercise.

Observed candidate distinctions:

1. Some questions request a procedure or a faster implementation; others ask
   whether a language belongs to a mathematical class.
2. Algorithm questions discuss running time and memory; language questions often
   discuss closure, pumping lemmas, grammars, and recognizing machines.
3. Some questions ask for conceptual explanations, others for constructions or
   proofs. This is an alternative taxonomy, but overlaps both topic groups.

Chosen distinction: algorithms versus formal languages. This is topic routing,
not a claim to measure post quality. The two labels do not cover every CS topic;
collection is explicitly limited to these two subject areas.

Hard boundary: automata algorithms. A question whose requested result is about
a grammar, language, or recognizing automaton goes to formal_language even when
it asks for an algorithm. General algorithmic problems merely represented as
languages go to algorithm. Incidental terminology does not decide the label.

Tag-based initial labels are weak supervision. The assistant will document
exclusions and corrections; student review and the 20 cold labels remain undone.
