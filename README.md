# TakeMeter: computer science topic routing

## What This Does

TakeMeter routes public questions from [Computer Science Stack Exchange](https://cs.stackexchange.com/) into `algorithm` and `formal_language`. It measures topic, not quality or factual correctness. It is scoped to questions in these two subject areas; it is not a general classifier for all CS posts.

**Submission status:** The implementation and data preparation were delegated to an AI assistant. The five criteria were AI-drafted, all 200 labels are tag-assisted pre-labels, and the student has not supplied 20 unaided cold labels or reviewed every pre-label. Those assignment requirements are incomplete. The independent agreement audit is also pending. No student reading session or annotation work is claimed.

## Label Taxonomy

### algorithm

A question primarily about designing, explaining, implementing, or analyzing a computational procedure or data structure, except when its requested result concerns a formal language, grammar, or recognizing automaton.

**Real example 1**

> Is there a name for the class of algorithms that are the most efficient for a particular task?
>
> This would be analogous to the Kolmogorov complexity of a string, except that in this case, I'm interested in the algorithm that solves a given problem using the least number of steps.
>
>
>
> We would therefore have to be able to show that any other algorithm is at best of the same order of complexity as the algorithm in question.
>
>
>
> I'm asking because I'm working on a paper that makes use of this concept, and I was surprised when I realized that I'm not aware of any name for this concept, though I'll concede I'm risking embarrassment if there is such a name that I'm simply unaware of.

Source: [Feynmanfan85](https://cs.stackexchange.com/questions/120810/is-there-a-name-for-the-class-of-algorithms-that-are-the-most-efficient-for-a-pa), CC BY-SA 4.0.

**Real example 2**

> Is there an algorithm whose time complexity is between polynomial time and exponential time？
>
> We often hear about some algorithms' running time that is polynomial, and some algorithms' running time that is exponential.
> But is there an algorithm whose time complexity is between polynomial time and exponential time?

Source: [lz9866](https://cs.stackexchange.com/questions/147873/is-there-an-algorithm-whose-time-complexity-is-between-polynomial-time-and-expon), CC BY-SA 4.0.

### formal_language

A question primarily about properties, representations, classification, or recognizing machines of formal languages or grammars, including algorithms whose requested result concerns those objects.

**Real example 1**

> Are modern programming languages context-free?
>
> Which language class are today's modern programming languages like Java, JavaScript, and Python in?
>
>
> It appears (?) they are not context-free and not regular languages.
>
>
> Are these programming languages context-sensitive or decidable languages? I am very confused!
>
>
> I know that context-free is more powerful than regular languages and that context-sensitive is more powerful than context-free.
>
>
> Are modern programming languages both context-free and context-sensitive?

Source: [Jonte YH](https://cs.stackexchange.com/questions/140078/are-modern-programming-languages-context-free), CC BY-SA 4.0.

**Real example 2**

> Proof of Brzozowski's algorithm for DFA minimization?
>
> Brzozowki's algorithm is cited widely.  Several questions here give examples or discuss its complexity. But I haven't been able to find a proof of correctness for the algorithm. How do we prove it correct?
> Any proof accessible to CS undergraduates would be very welcome.

Source: [vonbrand](https://cs.stackexchange.com/questions/105574/proof-of-brzozowskis-algorithm-for-dfa-minimization), CC BY-SA 4.0.

### The hardest boundary

The hardest boundary is algorithms operating on automata or grammars. Classify by the requested object: language classification, grammar construction, automaton transformation, or recognizing power takes `formal_language`, even if an algorithm, complexity bound, or correctness proof is requested. A general algorithm that happens to manipulate strings or encode a problem as a language stays `algorithm`. Thus Brzozowski DFA minimization goes to `formal_language`, while finding unmatched-parenthesis indices goes to `algorithm`.

The [reading notes](data/reading_notes.md) record three candidate distinctions. The [eight synthetic boundary tests](data/taxonomy_stress_test.md) are excluded from the real dataset. Two labels were chosen because conceptual explanation versus construction/proof overlaps both topics, making a third category less consistent.

## The Dataset

**Source:** One public community, Computer Science Stack Exchange. `scripts/collect_posts.py` collects up to 200 highly voted questions for each of the `algorithms` and `formal-languages` tags, posted from September 1, 2018 through October 16, 2026 UTC. The raw snapshot contains 400 distinct questions. Collection occurred October 17, 2026. The tag-stratified, popularity-selected sample is not representative of community traffic.

**Preparation:** `scripts/prepare_dataset.py` selects 100 questions per topic after the documented exclusion list. Titles and full bodies are retained as text; HTML markup is stripped, mathematical source and code text are retained, and no length-based trimming is applied. Original HTML remains in `data/collected_posts.json`; images and link destinations are available there but are not text model inputs. Each source row in [data/sources.csv](data/sources.csv) maps to the corresponding logical CSV row in labels.csv (starting at 1), with question ID, URL, author, author URL, license, tags, and collection timestamp. Reuse is under each row's stated CC BY-SA license; text extraction is a transformation. Preserve these attributions with redistribution.

**Annotation:** Initial labels are derived from community tags, with formal-language priority. The assistant reviewed titles and a 36-question full-text sample, excluded eleven broad or out-of-scope questions, and examined the three cases below. This is weak supervision, not 200 independently hand-verified labels. Every note marks AI pre-labeling and pending student review. There are **zero cold rows**. Tags, attribution, notes, and source metadata are not fed into the model; only title and body text are inputs. Tag-derived targets still create selection bias and do not establish human agreement.

| Label | Count | Share |
|---|---:|---:|
| algorithm | 100 | 50% |
| formal_language | 100 | 50% |
| **Total** | **200** | **100%** |

There are no blank texts or exact duplicate texts. Semantically related questions can remain; this small sample has not been audited for near-duplicate leakage. The CSV is a single unsplit input. The notebook alone creates the splits.

**Three hard cases (assistant decisions)**

1. [Proof of Brzozowski's algorithm for DFA minimization?](https://cs.stackexchange.com/questions/105574) could be `algorithm` because it asks for a correctness proof. Chosen: `formal_language`, because the requested result concerns a recognizing automaton preserving a language.
2. [How can you find all unbalanced parens in a string in linear time with constant memory?](https://cs.stackexchange.com/questions/103018) could be `formal_language` because balanced parentheses define a familiar formal language. Chosen: `algorithm`, because the request is to return unmatched positions under time and memory constraints.
3. [What is the computational complexity of real-life regular expressions?](https://cs.stackexchange.com/questions/127579) could be `algorithm` based on the title's complexity wording. Chosen: `formal_language`, because the full body asks about expressive power and Chomsky classes, rather than a matching implementation's runtime.

## The Training Run

**Base model:** `distilbert-base-uncased`, fine-tuned locally with the starter notebook's Trainer pipeline. Only notebook sections 1-5 are executed. Criteria were committed in `9c594e9`, and the dataset in `b6e591a`, before training started.

**Settings:** 3 epochs; learning rate 2e-5; training and evaluation batch size 16; maximum 128 tokens; seed 42. No training hyperparameters were changed. Full post text is stored, but the tokenizer truncates model input to 128 tokens; long technical questions can lose important context. No stretch feature or hyperparameter comparison was attempted.

**Device:** CPU, PyTorch 2.14.1+cpu, Python 3.13.2 on Windows. Environment check: 9 passed, 0 failed; expected baseline-model cache warning for next unit. `pip check` reports no broken requirements. Installed versions are in requirements-lock.txt.

**Splits:** The starter's sequential stratified 70/15/15 procedure gives 139 training, 31 validation, and 30 test rows (floating-point rounding means these are not 140/30/30).

| Label | Train | Validation | Test |
|---|---:|---:|---:|
| algorithm | 69 | 16 | 15 |
| formal_language | 70 | 15 | 15 |

Neither test class is below eight examples, but 15 remains a small denominator. Next unit's three-seed evaluation and baseline are not part of this run.

**Completed run:** Held-out accuracy 0.9667; macro F1 0.9666. Actual metrics are in [results.json](results.json), the 30 held-out rows are in [test_split.csv](test_split.csv), and executed cell outputs are saved in [takemeter.ipynb](takemeter.ipynb). Training completed 27 optimizer steps in about 109 seconds, excluding model download. This score is against tag-assisted labels on a selected two-topic sample, not independent human ground truth or evidence of performance on all CS questions. Targets have not been revised after seeing results.

Run `scripts/verify_submission.py` with the project Python to check artifact consistency, attribution, split overlap, and locally saved weights. [data/run_manifest.json](data/run_manifest.json) records input/output hashes and the unresolved annotation requirements.

**Reproduce in PowerShell:**

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe test.py
.\.venv\Scripts\python.exe -X utf8 scripts/run_notebook.py
```

The existing labels.csv is sufficient to reproduce training; live recollection can change the sample. Optional recollection: run scripts/collect_posts.py then scripts/prepare_dataset.py. The notebook runner executes actual notebook code cells and writes their outputs back into takemeter.ipynb. Model weights and tokenizer are saved locally in takemeter_out/final and intentionally excluded from Git because of their size. results.json and test_split.csv are committed evidence for next unit. Hugging Face downloads pretrained weights once; training and predictions run locally with no hosted inference or API key.

## How I Used AI

**Moment 1:** The student asked the assistant to complete the assignment and later selected computer science as the subject. The assistant read a community sample, proposed the two-topic taxonomy, compared the algorithm/automata boundary, and generated eight synthetic boundary tests. The resulting priority rule uses the requested object rather than the presence of the word algorithm. These are assistant decisions, not student-authored reading notes.

**Moment 2:** The student authorized the assistant to handle the rest. The assistant drafted numeric criteria before training, built collection and dataset scripts, configured and executed the notebook, and wrote this documentation. This exceeds the assignment's suggested AI role for criteria; the criteria are disclosed as AI-drafted rather than represented as independently student-written.

**Pre-labeling disclosure:** All 200 labels began as community-tag-assisted pre-labels created by the assistant's script. The assistant reviewed titles, a full-text sample, and hard cases; the student has not reviewed/corrected every row. No annotations are marked cold, no independent human agreement score is claimed, and no AI-generated posts are included in labels.csv. The next step toward assignment compliance is the student's own criteria and unaided labeling/review, followed by a new documented run if data changes. Existing criteria and results should be preserved in Git history.

Repository: https://github.com/munsakad/ai201-project3-takemeter-starter-v2026
Submit that URL through the Course Portal; portal submission has not been performed by this assistant.

## Part 2 testing plan

Prediction recorded before reading baseline output: the fine-tuned model should beat zero-shot classification on automata questions phrased as algorithm problems because it learned the topic priority boundary.

Keep criteria.md, label_definitions.txt, and labels.csv frozen. Run seeds 42, 7, and 2024 with original settings first. Diagnose those results before choosing one training change. Confidence is already criterion 5, not a new stretch feature. No optional stretch is claimed.

The staff answer key is not present. Student-authored staff labels, staff comparison/adjudication, and the independent human audit remain pending; AI labels cannot establish human agreement.

### One improvement selected before the after-run

The tokenizer audit found 153/200 posts exceed 128 tokens; 81 exceed 256.
Seed 42 before has one algorithm -> formal_language error, at low confidence
(mean confidence for the wrong prediction 0.5039). The topic decision can depend
on a requested object late in a technical question. Test one change only:
MAX_LENGTH 128 -> 256, retaining all labels, definitions, criteria, epochs,
learning rate, batches, and seeds. This is a hypothesis about lost context,
not proof that truncation caused the error. Longer input may hurt or fail to
help. The other two before trials finish with the original 128-token setting.

<!-- generated-part2-report -->

# Part 2 measured report

Generated by scripts/report_testing.py. Missing evidence remains pending.

## Baseline vs. Trained

| Measure | Baseline | Trained | Difference |
|---|---|---|---|
| Overall accuracy | 0.500 | 0.967 | +0.467 |
| Macro F1 | 0.384 | 0.967 | +0.582 |
| F1 — `algorithm` | 0.118 | 0.966 | +0.848 |
| F1 — `formal_language` | 0.651 | 0.968 | +0.317 |

## Run Log — Before

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.75 | 0.9667 | 0.9333 | 0.9000 | MET |
| 2. Minimum label F1 | >= 0.70 | 0.9655 | 0.9286 | 0.8966 | MET |
| 3. Label shares (dataset check) | 35%-65% each | 0.5000 | 0.5000 | 0.5000 | MET |
| 4. Independent human audit | >= 17/20 | pending | pending | pending | PENDING |
| 5. Most-confident third accuracy | >= 0.80 | 1.0000 | 1.0000 | 1.0000 | MET |

Accuracy spread: 0.0667. Device: CPU; torch 2.14.1+cpu.

Confusion matrices: rows are true labels; columns are predictions.

### Seed 42

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 14 | 1 |
| formal_language | 0 | 15 |

### Seed 7

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 13 | 2 |
| formal_language | 0 | 15 |

### Seed 2024

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 14 | 1 |
| formal_language | 2 | 13 |

## Run Log — After

| Criterion | Target | Seed 42 | Seed 7 | Seed 2024 | Verdict |
|---|---|---|---|---|---|
| 1. Overall accuracy | >= 0.75 | 0.9667 | 0.9667 | 0.9000 | MET |
| 2. Minimum label F1 | >= 0.70 | 0.9655 | 0.9655 | 0.8966 | MET |
| 3. Label shares (dataset check) | 35%-65% each | 0.5000 | 0.5000 | 0.5000 | MET |
| 4. Independent human audit | >= 17/20 | pending | pending | pending | PENDING |
| 5. Most-confident third accuracy | >= 0.80 | 1.0000 | 1.0000 | 1.0000 | MET |

Accuracy spread: 0.0667. Device: CPU; torch 2.14.1+cpu.

Confusion matrices: rows are true labels; columns are predictions.

### Seed 42

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 14 | 1 |
| formal_language | 0 | 15 |

### Seed 7

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 14 | 1 |
| formal_language | 0 | 15 |

### Seed 2024

| true / predicted | algorithm | formal_language |
|---|---|---|
| algorithm | 14 | 1 |
| formal_language | 2 | 13 |

## Verdicts and Diagnoses

1. Accuracy: MET before; every seed is above 0.75. The 0.0667 spread shows some split sensitivity, below the assignment’s ten-point warning.
2. Each-label F1: MET before; the minimum across all labels and seeds is 0.8966, above 0.70.
3. Label balance: MET; both labels have 100/200 rows (50%). This is a frozen dataset check, so retraining does not create three new balance measurements.
4. Independent agreement: PENDING, not established. There are no independent human labels; model metrics cannot diagnose or satisfy this criterion. Obtain the blinded audit rather than lowering the target.
5. Confident-third accuracy: MET before; all three most-confident thirds score 1.0000 against a target of 0.80. Each contains only ten posts, so this does not establish probability calibration.

Across before trials, four algorithm instances were called formal_language, versus two in reverse (test sets overlap, so these are not six unique posts). Seed 42’s largest off-diagonal cell is one algorithm -> formal_language. The matrices show a topic-boundary error but cannot distinguish inconsistent weak labels from model error. No underrepresented label is present; both have 100 examples. The unrelated staff taxonomy cannot establish which CS training labels are inconsistent.

## The Improvement

One change: maximum input length 128 -> 256 tokens. A tokenizer audit found 153/200 posts exceed 128 tokens and 81 exceed 256. Longer context could expose the requested object needed for the CS priority rule. This is a tested hypothesis, not a demonstrated cause of the before errors. Training still starts from pretrained weights for each seed; epochs, learning rate, batch size, data, and criteria stay fixed.

| Seed | Before accuracy | After accuracy | Difference |
|---|---|---|---|
| 42 | 0.9667 | 0.9667 | +0.0000 |
| 7 | 0.9333 | 0.9667 | +0.0333 |
| 2024 | 0.9000 | 0.9000 | +0.0000 |

Mean accuracy changed by +0.0111. The change helped mean accuracy on these splits.
The after-run verdicts use the same thresholds and require all three seeds to pass; see Run Log — After. Three overlapping small test sets do not establish a general improvement beyond this dataset.

## Agreement Report

Pending student annotations and TF-provided data/staff_labels.csv. No agreement rate or human adjudication is claimed. The staff running-forum taxonomy differs from this project’s CS-topic taxonomy; its disagreements cannot directly identify a CS label-pair error.

Criterion 4 separately requires an unaided independent human audit of 20 frozen CS posts. Use data/human_audit_posts.csv, sampled exactly as prescribed; labels and tags are hidden. The staff exercise cannot substitute for it. Criterion 3 is a dataset property repeated for context, not three independent experiments.

## What’s Still Broken

Independent human agreement is unresolved because the required human annotations are unavailable. Next, complete the blinded audit and the staff worksheet, obtain the TF key, run agreement.py, and adjudicate each disagreement by the written rules in piles (a), (b), or (c). No agreement_results.json is fabricated. These human tasks are where automated work stops.

The labels were intended to capture the requested CS object, including algorithms about automata. The off-diagonal counts show the model sometimes routes across that boundary; high scores on tag-assisted labels do not prove it learned that semantic rule or that humans would agree.

## How I Used AI — Part 2

The assistant implemented the runner, executed the local baseline and requested fine-tunes, generated the numeric report, proposed the longer-context hypothesis from tokenizer counts, and wrote the diagnoses. No student-authored annotations, staff key, independent audit, or human adjudication is claimed. Criteria, taxonomy, and existing training labels remain frozen.

## Validation

Run scripts/verify_testing.py after all six trials complete to recompute accuracy/F1, verify frozen input hashes, check paired test sets and settings, and confirm baseline posts exactly match test_split.csv. scripts/test_testing_report.py tests strict all-seeds verdicts and missing evidence. The existing scripts/verify_submission.py passed; original criteria, definitions, labels, results, and held-out file remain unchanged. The environment smoke check reported 8 passes and a disk-space preflight failure (8.5 GB available versus its 9 GB recommendation before baseline download); the actual evaluations ran, but the free-space check remains a limitation.
