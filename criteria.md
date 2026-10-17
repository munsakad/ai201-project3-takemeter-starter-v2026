# Acceptance criteria ? TakeMeter

These targets were drafted by the assistant at the student's request and committed before training. They have not been independently written or defended by the student as the assignment requires. No training results informed these targets. Model-performance targets apply to the untouched held-out split; in unit 6 they must hold separately for seeds 42, 7, and 2024.

1. **Overall accuracy is at least 0.75.**

   Why: Two balanced labels make 0.50 the majority baseline. Three correct routes in four would be useful while allowing for questions mixing automata and algorithms.

2. **Each label has F1 of at least 0.70.**

   Why: Overall accuracy should not conceal failure on either topic. About 15 test examples per label makes a stricter floor vulnerable to a handful of ambiguous questions.

3. **Each label represents between 35% and 65% of labels.csv, inclusive.**

   Why: This balanced two-topic sample should support both labels, with a tighter range than the assignment's 70% ceiling. It does not estimate natural community topic frequencies.

4. **An independent human agrees with the frozen labels on at least 17 of 20 sampled posts.**

   Measurement: Sample row indices without replacement using Python random.Random(31415).sample(range(len(rows)), 20). Hide labels and tags. A human applies label_definitions.txt without AI assistance; compare exact labels before adjudication. This audit is pending and does not substitute for the separate cold-label requirement.

   Why: 85% agreement would suggest a usable boundary while allowing three ambiguous cases.

5. **Accuracy in the most-confident held-out third is at least 0.80.**

   Measurement: Read confidence.accuracy_most_confident_third in results.json. The notebook ranks maximum softmax probability and takes floor(n_test/3) examples, using its NumPy tie behavior.

   Why: The routing aid should be dependable when most confident. With about ten examples in this third, two errors are allowed; calibrated probabilities are not assumed.
