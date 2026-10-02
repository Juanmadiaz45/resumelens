# Professional Profiles

ResumeLens supports four professional profiles. Two of them are fixed by the assignment
(Full Stack Developer and Machine Learning Engineer). The other two were chosen to round out
the coverage of the pipeline: one more profile on the software engineering side and one more
on the AI/data side. The reasoning behind the choice was simple — both profiles share several
qualifications with the predefined ones (Git, SQL, Python), which forces the classification
automata to actually distinguish between overlapping vocabularies instead of just checking for
disjoint keyword sets.

## 1. Full Stack Developer (predefined)

Works across both the client and server side of an application: UI, backend services, APIs,
database access, and integration between components.

Qualifications:
- JavaScript or TypeScript
- React, Angular, or Vue
- Node.js, Django, Spring Boot (or an equivalent backend framework)
- SQL or NoSQL database
- REST APIs
- Git

## 2. Machine Learning Engineer (predefined)

Combines software development, data processing, and machine learning to build systems based
on predictive or learning models.

Qualifications:
- Python
- Pandas or NumPy
- Scikit-learn
- TensorFlow or PyTorch
- Machine learning model development
- SQL
- Git

## 3. DevOps Engineer (team-defined, software engineering)

A DevOps Engineer is responsible for automating the build, deployment, and operation of
software systems, bridging development and infrastructure. This profile was picked because it
shares Git and cloud-adjacent vocabulary with Full Stack Developer, but the core qualifications
(containerization, orchestration, infrastructure as code) are specific enough to require a
separate pattern.

Qualifications:
- Linux
- Docker
- Kubernetes (or K8s)
- A CI/CD tool: Jenkins, GitHub Actions, or GitLab CI
- An infrastructure-as-code tool: Terraform or Ansible
- A cloud provider: AWS, Azure, or GCP
- Git

## 4. Data Engineer (team-defined, AI/data)

A Data Engineer designs and maintains the pipelines and infrastructure used to collect,
transform, and store data at scale, usually as a prerequisite for the work a Machine Learning
Engineer does downstream. This overlap with ML Engineer (Python, SQL) is intentional: it is the
pair of profiles that stress-tests the classification stage the most.

Qualifications:
- Python
- SQL
- Apache Spark
- Airflow
- Kafka
- A data warehouse: Snowflake, BigQuery, or Redshift
- Git

## Shared qualifications across profiles

| Qualification | FS Dev | ML Engineer | DevOps | Data Engineer |
|---|---|---|---|---|
| Git | yes | yes | yes | yes |
| SQL | yes | yes | — | yes |
| Python | — | yes | — | yes |
| Cloud provider | — | — | yes | sometimes (warehouse) |

This table is the reason the canonical ordering and the automata alphabets need to be designed
carefully in stages 2 and 3 — a candidate who only lists `Python, SQL, Git` should not be
blindly accepted into both ML Engineer and Data Engineer; the rest of the sequence has to carry
the distinction.
