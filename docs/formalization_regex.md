# Formalization — Stage 1: Regular Expressions

Stage 1 turns a plain-text résumé into raw qualification strings and candidate data. For each
category, this document gives the regular expression as it appears in
`resumelens/extraction/extractor.py`, the language it recognizes, and the design decisions
behind it. The patterns were checked against the ten sample résumés in `data/sample_resumes/`
and against the unit tests in `tests/test_extraction.py`.

All patterns are compiled with Python's `re` module. Matching uses `re.search` for single values
(such as an email or the years of experience) and `re.finditer` for lists. Lists keep the order
of first appearance and drop exact duplicates.

Notation used below: `\b` is a word boundary, `(?:…)` is a non-capturing group, `?` means
optional, `+` means one or more, `*` means zero or more, and `|` is alternation.

## Candidate name

```
^\s*([A-Za-z][A-Za-z.'-]*(?:\s+[A-Za-z][A-Za-z.'-]*)*)\s*$     (multiline)
```

**Language:** a whole line that consists only of words made of letters, dots, apostrophes, and
hyphens, separated by spaces. A line with a colon, a comma, or a digit doesn't match, so
`Technical Skills:` is not taken as a name.

**Decision:** the name is the first such line in the résumé. The sample résumés all start with
the candidate's name, as in the assignment's examples. A résumé that starts with a title line
would extract the wrong name; this is a known limitation.

## Contact information

```
Email     [A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}
Phone     \+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}
LinkedIn  (?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+       (ignore case)
GitHub    (?:https?://)?(?:www\.)?github\.com/[\w-]+           (ignore case)
```

**Email:** a local part, `@`, a domain, and a top-level domain of at least two letters.

**Phone:** an optional country code, then three groups of digits with optional separators.
Phone formats differ too much between countries to make this strict. The pattern can therefore
match a run of digits that isn't a phone number, such as a year range. No sample résumé triggers
this, but it's a known weakness.

**LinkedIn and GitHub:** the path, with or without `https://` and `www.`. Résumés often give
only the path.

## Years of experience

```
(\d+)\+?\s*years?\s+of\s+experience        (ignore case)
```

**Language:** a number, an optional `+`, the word "year" or "years", and "of experience". The
captured number is the value. Covers "3 years of experience", "4+ years of experience", and
"1 year of experience".

## Programming languages

```
\b(?:JavaScript|Javascript|JS|TypeScript|TS|Python|Java|C\+\+|C#|Go|Ruby|PHP|Bash)\b
```

**Language:** one of the listed language names, as a whole word.

**Decision — case-sensitive.** This pattern has no ignore-case flag, unlike the others. `Go` is
also an ordinary English word, and matching it case-insensitively would pick up "go" in prose.
The trade-off is that `python` written in lowercase is not extracted. Résumés in the samples
capitalize language names, so this doesn't affect the tests, but it's a limitation for real
input.

## Frameworks and libraries

```
\b(?:React(?:\.js)?|ReactJS|Angular|Vue(?:\.js)?|Node(?:\.js)?|NodeJS|Django|
   Spring\s?Boot|Flask|Express(?:\.js)?|Pandas|NumPy|Scikit-learn|sklearn|
   scikit\s?learn|Tensor\s?Flow|Py\s?Torch|Keras)\b          (ignore case)
```

**Language:** web frameworks (Full Stack profile) and machine-learning libraries (ML Engineer
profile) in one set. Stage 1 doesn't decide which profile a term belongs to; that happens in
stage 3. The optional `\s?` covers spacing variants such as `Spring Boot` and `SpringBoot`, and
`(?:\.js)?` covers the `.js` suffix.

## Databases

```
\b(?:Postgres|PostgreSQL|MySQL|MongoDB|SQLite|Redis|Cassandra|SQL|NoSQL)\b     (ignore case)
```

**Language:** product names and the generic terms `SQL` and `NoSQL`. The word boundaries keep
`SQL` from matching inside `NoSQL`, and `NoSQL` is matched as its own alternative.

## Cloud and DevOps tools

```
\b(?:Docker|Kubernetes|K8s|Terraform|Ansible|Jenkins|GitHub\s?Actions|
   GitLab\s?CI|AWS|Azure|GCP|Google\s?Cloud|Linux)\b             (ignore case)
```

**Language:** container and orchestration tools, infrastructure-as-code tools, CI/CD tools,
cloud providers, and Linux. `K8s` is recognized as its own term, and stage 2 maps it to
`KUBERNETES`.

## Data engineering tools

```
\b(?:Apache\s?Spark|Spark|Airflow|Kafka|Snowflake|BigQuery|Redshift)\b       (ignore case)
```

**Language:** pipeline and warehouse tools. `Apache Spark` comes before `Spark` in the
alternation, so the longer name is taken when both are present. Kept separate from the frameworks
category because these are infrastructure rather than application code.

## Academic qualifications

```
\b(Bachelor|Master|PhD|B\.?Sc\.?|M\.?Sc\.?)(?:[ \t]+(?:of|in))?[ \t]+
([A-Z][A-Za-z]*(?:[ \t]+[A-Z][A-Za-z]*)*)
```

**Language:** a degree name, an optional "of" or "in", and a field of study made of capitalized
words, as in `B.Sc. in Computer Science` or `Master in Data Science`. The output is a dictionary
with the degree and the field.

**Two corrections made during implementation.**
- The trailing `\b` was removed. `B.Sc.` ends with a period, and a period followed by a space is
  not a word boundary, so the whole pattern silently failed to match on `B.Sc.`.
- The field capture uses `[ \t]` instead of `\s`. With `\s`, the field continued across the line
  break and captured the next heading, `Technical Skills`.

## Tools and version control

```
\bGit\b                  (ignore case)
\bREST\s?API\b           (ignore case)
```

**Language:** the words `Git` and `REST API` (or `RESTAPI`). Each one that appears adds a single
entry, so a résumé that mentions Git three times still produces one `Git`.

## Output

`extract_all(text)` returns one dictionary with these keys: `name`, `contact` (email, phone,
LinkedIn, GitHub), `experience_years`, `languages`, `frameworks`, `databases`, `cloud_tools`,
`data_tools`, `education`, and `tools`. `name` is a string or `None`, `experience_years` is an integer or `None`, `contact` is a
dictionary with four keys that are each a string or `None`, `education` is a list of
dictionaries, and the remaining categories are lists of strings (empty when nothing was found). The output for each sample is
stored in `data/extracted/*.json`.

## Known limitations

- The name rule assumes the name is on the first line.
- Language names are case-sensitive, so lowercase input is missed.
- The phone pattern is loose and can match non-phone digit sequences.
- Only one experience summary is extracted per résumé, because a résumé's employment history is
  not parsed.
- The vocabulary is a fixed list. A tool that isn't in a pattern is not extracted, and it can't
  be classified either. Adding a term requires changing the regex and the matching transducer.
