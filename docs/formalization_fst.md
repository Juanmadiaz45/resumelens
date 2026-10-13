# Formalization of Stage 2: Finite-State Transducers

For each transducer: the complete 7-tuple M = (Q, Σ, Γ, δ, ω, q0, F), a diagram, and a pointer
to its implementation in `resumelens/normalization/transducers.py` (pyformlang).

This matches the definition used in class (see `class_notation_reference.md`) exactly, including
the tuple order. Per that definition: δ : Q × (Σ ∪ {λ}) → Q and ω : Q × (Σ ∪ {λ}) → Γ for a
deterministic FST; for a non-deterministic one, δ : Q × (Σ ∪ {λ}) → ℘(Q) and
ω : Q × (Σ ∪ {λ}) → Γ ∪ {λ}. Use λ (not ε) consistently, same as the automata docs.

## Design decision: one transition per token, not per character

Stage 1 already splits a résumé into discrete qualification strings (`"JS"`, `"React.js"`,
`"Postgres"`, ...). By the time stage 2 sees them, there's no reason to process a term
character by character. The normalization problem is lexical substitution (map a whole token
to its canonical spelling), not pattern matching inside a string. So every transducer below uses
the same shape: two states, `q0` and `qf`, and one transition per recognized synonym, each
reading the *entire* raw token in a single step and emitting the canonical term as its output.
This is the same thing the professor's own FST example does with whole-syllable transitions
(`"llor"`, `"ar"`) instead of single characters, and pyformlang places no restriction on how long an
input symbol string is.

This also gives a direct, intuitive meaning to the accepting state: **a token is successfully
normalized if and only if reading it leaves the machine in `qf`.** If a token isn't one of the
recognized synonyms, no transition is defined for it, the machine stays stuck in `q0`
(non-accepting), and that's exactly the "term not recognized" case from `test_cases.md` (N2).
Rejection isn't a special case to code around; it falls directly out of δ being a **partial**
function.

One more modeling note: most of stage 1's regexes are case-insensitive, so the raw string
captured for, say, Django could show up as `Django`, `django`, or `DJANGO` depending on how the
candidate wrote it. Rather than listing every casing variant in Σ, each Σ below lists one
representative spelling, and the implementation casefolds both the transition symbols and the
input before the lookup. That keeps Σ finite and readable here while still handling arbitrary
capitalization in practice. It is a gap between the formal model and the code, and it is stated
here openly instead of pretending Σ has one entry per possible casing.

## Transducer 1: Programming Language Normalizer

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {JS, Javascript, JavaScript, TypeScript, TS, Python, Java, C++, C#, Go, Ruby, PHP, Bash}

**Γ** = {JAVASCRIPT, TYPESCRIPT, PYTHON, JAVA, CPP, CSHARP, GO, RUBY, PHP, BASH}

δ and ω share the domain Q × Σ, and every transition starts at q0 and ends at qf, so both are
listed in one table:

| input (Σ) | δ(q0, input) | ω(q0, input) |
|---|---|---|
| JS | qf | JAVASCRIPT |
| Javascript | qf | JAVASCRIPT |
| JavaScript | qf | JAVASCRIPT |
| TypeScript | qf | TYPESCRIPT |
| TS | qf | TYPESCRIPT |
| Python | qf | PYTHON |
| Java | qf | JAVA |
| C++ | qf | CPP |
| C# | qf | CSHARP |
| Go | qf | GO |
| Ruby | qf | RUBY |
| PHP | qf | PHP |
| Bash | qf | BASH |

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: JS / JAVASCRIPT
    q0 --> qf: Javascript / JAVASCRIPT
    q0 --> qf: JavaScript / JAVASCRIPT
    q0 --> qf: TypeScript / TYPESCRIPT
    q0 --> qf: TS / TYPESCRIPT
    q0 --> qf: Python / PYTHON
    q0 --> qf: Java / JAVA
    q0 --> qf: C++ / CPP
    q0 --> qf: C# / CSHARP
    q0 --> qf: Go / GO
    q0 --> qf: Ruby / RUBY
    q0 --> qf: PHP / PHP
    q0 --> qf: Bash / BASH
    qf --> [*]
```

## Transducer 2: Framework & Library Normalizer

Covers both web frameworks and ML libraries in one transducer, mirroring the single "frameworks
and libraries" extraction category from stage 1. Splitting them here would re-introduce a
distinction stage 1 deliberately doesn't make.

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {React, React.js, ReactJS, Angular, Vue, Vue.js, Node, Node.js, NodeJS, Django, Spring Boot, SpringBoot, Flask, Express, Express.js, Pandas, NumPy, Scikit-learn, sklearn, scikit learn, Tensor Flow, TensorFlow, Py Torch, PyTorch, Keras}

**Γ** = {REACT, ANGULAR, VUE, NODE_JS, DJANGO, SPRING_BOOT, FLASK, EXPRESS, PANDAS, NUMPY, SCIKIT_LEARN, TENSORFLOW, PYTORCH, KERAS}

| input (Σ) | ω(q0, input) | | input (Σ) | ω(q0, input) |
|---|---|---|---|---|
| React | REACT | | Pandas | PANDAS |
| React.js | REACT | | NumPy | NUMPY |
| ReactJS | REACT | | Scikit-learn | SCIKIT_LEARN |
| Angular | ANGULAR | | sklearn | SCIKIT_LEARN |
| Vue | VUE | | scikit learn | SCIKIT_LEARN |
| Vue.js | VUE | | Tensor Flow | TENSORFLOW |
| Node | NODE_JS | | TensorFlow | TENSORFLOW |
| Node.js | NODE_JS | | Py Torch | PYTORCH |
| NodeJS | NODE_JS | | PyTorch | PYTORCH |
| Django | DJANGO | | Keras | KERAS |
| Spring Boot | SPRING_BOOT | | | |
| SpringBoot | SPRING_BOOT | | | |
| Flask | FLASK | | | |
| Express | EXPRESS | | | |
| Express.js | EXPRESS | | | |

(δ(q0, input) = qf for every row above; omitted from the table since it never varies.)

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: React, React.js, ReactJS / REACT
    q0 --> qf: Angular / ANGULAR
    q0 --> qf: Vue, Vue.js / VUE
    q0 --> qf: Node, Node.js, NodeJS / NODE_JS
    q0 --> qf: Django / DJANGO
    q0 --> qf: Spring Boot, SpringBoot / SPRING_BOOT
    q0 --> qf: Flask / FLASK
    q0 --> qf: Express, Express.js / EXPRESS
    q0 --> qf: Pandas / PANDAS
    q0 --> qf: NumPy / NUMPY
    q0 --> qf: Scikit-learn, sklearn, scikit learn / SCIKIT_LEARN
    q0 --> qf: Tensor Flow, TensorFlow / TENSORFLOW
    q0 --> qf: Py Torch, PyTorch / PYTORCH
    q0 --> qf: Keras / KERAS
    qf --> [*]
```

(Transitions with more than one input listed on the same arrow are shorthand for several
parallel arrows with the same output, grouped for readability. The underlying relation still
has one pair per raw string, same as the table above.)

## Transducer 3: Database Normalizer

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {Postgres, PostgreSQL, MySQL, MongoDB, SQLite, Redis, Cassandra, SQL, NoSQL}

**Γ** = {POSTGRESQL, MYSQL, MONGODB, SQLITE, REDIS, CASSANDRA, SQL, NOSQL}

| input (Σ) | ω(q0, input) |
|---|---|
| Postgres | POSTGRESQL |
| PostgreSQL | POSTGRESQL |
| MySQL | MYSQL |
| MongoDB | MONGODB |
| SQLite | SQLITE |
| Redis | REDIS |
| Cassandra | CASSANDRA |
| SQL | SQL |
| NoSQL | NOSQL |

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: Postgres, PostgreSQL / POSTGRESQL
    q0 --> qf: MySQL / MYSQL
    q0 --> qf: MongoDB / MONGODB
    q0 --> qf: SQLite / SQLITE
    q0 --> qf: Redis / REDIS
    q0 --> qf: Cassandra / CASSANDRA
    q0 --> qf: SQL / SQL
    q0 --> qf: NoSQL / NOSQL
    qf --> [*]
```

`SQL` and `NoSQL` are already in canonical form, so their transitions are the identity on the
label. It is still a real transition and not a shortcut, because the stage 3 automata only read
tokens that went through stage 2.

## Transducer 4: Cloud & DevOps Tool Normalizer

Supports the DevOps Engineer profile.

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {Docker, Kubernetes, K8s, Terraform, Ansible, Jenkins, GitHub Actions, GitLab CI, AWS, Azure, GCP, Google Cloud, Linux}

**Γ** = {DOCKER, KUBERNETES, TERRAFORM, ANSIBLE, JENKINS, GITHUB_ACTIONS, GITLAB_CI, AWS, AZURE, GCP, LINUX}

| input (Σ) | ω(q0, input) |
|---|---|
| Docker | DOCKER |
| Kubernetes | KUBERNETES |
| K8s | KUBERNETES |
| Terraform | TERRAFORM |
| Ansible | ANSIBLE |
| Jenkins | JENKINS |
| GitHub Actions | GITHUB_ACTIONS |
| GitLab CI | GITLAB_CI |
| AWS | AWS |
| Azure | AZURE |
| GCP | GCP |
| Google Cloud | GCP |
| Linux | LINUX |

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: Docker / DOCKER
    q0 --> qf: Kubernetes, K8s / KUBERNETES
    q0 --> qf: Terraform / TERRAFORM
    q0 --> qf: Ansible / ANSIBLE
    q0 --> qf: Jenkins / JENKINS
    q0 --> qf: GitHub Actions / GITHUB_ACTIONS
    q0 --> qf: GitLab CI / GITLAB_CI
    q0 --> qf: AWS / AWS
    q0 --> qf: Azure / AZURE
    q0 --> qf: GCP, Google Cloud / GCP
    q0 --> qf: Linux / LINUX
    qf --> [*]
```

## Transducer 5: Data Engineering Tool Normalizer

Supports the Data Engineer profile.

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {Spark, Apache Spark, Airflow, Kafka, Snowflake, BigQuery, Redshift}

**Γ** = {SPARK, AIRFLOW, KAFKA, SNOWFLAKE, BIGQUERY, REDSHIFT}

| input (Σ) | ω(q0, input) |
|---|---|
| Spark | SPARK |
| Apache Spark | SPARK |
| Airflow | AIRFLOW |
| Kafka | KAFKA |
| Snowflake | SNOWFLAKE |
| BigQuery | BIGQUERY |
| Redshift | REDSHIFT |

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: Spark, Apache Spark / SPARK
    q0 --> qf: Airflow / AIRFLOW
    q0 --> qf: Kafka / KAFKA
    q0 --> qf: Snowflake / SNOWFLAKE
    q0 --> qf: BigQuery / BIGQUERY
    q0 --> qf: Redshift / REDSHIFT
    qf --> [*]
```

## Transducer 6: Tools Normalizer

The smallest one, covering the two terms stage 1 keeps in its own "tools" bucket. `Git` needs a
transition even though the only change is capitalization, for the same reason `SQL` does in
transducer 3: stage 3's automata only read canonical terms, so every qualification has to pass
through stage 2, including the ones that don't change much.

M = (Q, Σ, Γ, δ, ω, q0, F) with **Q** = {q0, qf}, initial state q0, **F** = {qf}, and

**Σ** = {Git, REST API}

**Γ** = {GIT, REST_API}

| input (Σ) | ω(q0, input) |
|---|---|
| Git | GIT |
| REST API | REST_API |

```mermaid
stateDiagram-v2
    [*] --> q0
    q0 --> qf: Git / GIT
    q0 --> qf: REST API / REST_API
    qf --> [*]
```

## Canonical order per profile (`sort_by_profile_order`)

The canonical order for each profile is just the order its qualifications are listed in
`docs/profiles.md`. Reusing that list means the order used for sorting and the order used to
define the profile are guaranteed to stay in sync instead of drifting apart as two separate
documents.

| Profile | Canonical order (normalized terms) |
|---|---|
| Full Stack Developer | JAVASCRIPT, TYPESCRIPT → REACT, ANGULAR, VUE → NODE_JS, DJANGO, SPRING_BOOT → SQL, NOSQL, POSTGRESQL, MYSQL, MONGODB, SQLITE, REDIS, CASSANDRA → REST_API → GIT |
| Machine Learning Engineer | PYTHON → PANDAS, NUMPY → SCIKIT_LEARN → TENSORFLOW, PYTORCH → SQL, NOSQL, POSTGRESQL, MYSQL, MONGODB, SQLITE, REDIS, CASSANDRA → GIT |
| DevOps Engineer | LINUX → DOCKER → KUBERNETES → TERRAFORM, ANSIBLE → JENKINS, GITHUB_ACTIONS, GITLAB_CI → AWS, AZURE, GCP → GIT |
| Data Engineer | PYTHON → SQL, NOSQL, POSTGRESQL, MYSQL, MONGODB, SQLITE, REDIS, CASSANDRA → SPARK → AIRFLOW → KAFKA → SNOWFLAKE, BIGQUERY, REDSHIFT → GIT |

`sort_by_profile_order(terms, profile)` places each term from the candidate's normalized list
at the position of its category in the table above, and appends anything that doesn't appear in
that profile's list at the end (unsorted). It doesn't drop terms, since a term that's irrelevant
to one profile might still be what makes the candidate accepted by another.

### Worked example (matches the assignment's own example)

Raw qualifications from the résumé, in the order the candidate wrote them:

```
Git, NodeJS, JS, Postgres, React.js
```

After transducers 1 (language), 2 (framework), 3 (database), and 6 (tools):

```
GIT, NODE_JS, JAVASCRIPT, POSTGRESQL, REACT
```

After `sort_by_profile_order(..., "FULL_STACK_DEVELOPER")`:

```
JAVASCRIPT, REACT, NODE_JS, POSTGRESQL, GIT
```

Which is exactly the sequence the assignment statement uses as input to the stage 3 automaton
example, which confirms that the ordering reproduces the expected behavior before any automaton
is involved.
