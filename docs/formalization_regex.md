# Formalization — Stage 1: Regular Expressions

This is a first pass at the categories stage 1 needs to extract and a draft pattern for each
one. These are not final — they still need to be run against the sample résumés in
`data/sample_resumes/` and tightened up once real edge cases show up (that's day 3's job). The
point here is to pin down the language each pattern is supposed to recognize before writing the
`re` code.

All patterns below are meant to be used with `re.IGNORECASE` unless noted otherwise, since
résumés are inconsistent about capitalization (`git` vs `Git`, `python` vs `Python`).

## Contact information

- **Email:** `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}`
  Recognizes a local part made of letters, digits, and the usual separator characters (`.`,
  `_`, `%`, `+`, `-`), followed by `@`, a domain, and a top-level domain of at least two letters.
- **Phone number:** `\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}`
  Loosely matches an optional country code followed by groups of digits separated by spaces,
  dots, or dashes. This one is intentionally permissive — phone formats vary too much across
  countries to lock down further without seeing real samples.
- **LinkedIn / GitHub profile:** `(linkedin\.com/in/[\w-]+|github\.com/[\w-]+)`
  Matches a LinkedIn or GitHub profile URL fragment, ignoring the protocol (`http://`, `https://`)
  since résumés often paste just the path.

## Years of professional experience

- **Pattern:** `(\d+)\+?\s*years?\s+of\s+experience`
  Captures the number right before the phrase "year(s) of experience", allowing an optional `+`
  (for "5+ years") and tolerating singular/plural. Matches both of the assignment's examples
  ("3 years of experience", "2 years of experience").

## Programming languages

- **Pattern:** `\b(JavaScript|Javascript|JS|TypeScript|TS|Python|Java|C\+\+|C#|Go|Ruby|PHP)\b`
  A plain alternation of the language names and abbreviations expected across the four
  profiles. Word boundaries keep it from matching `JS` inside another word. This list grows as
  more sample résumés are reviewed — it's deliberately not meant to be exhaustive on the first
  pass.

## Frameworks and libraries

- **Pattern:** `\b(React(?:\.js)?|ReactJS|Angular|Vue(?:\.js)?|Node(?:\.js)?|NodeJS|Django|Spring\s?Boot|Flask|Express(?:\.js)?|Pandas|NumPy|Scikit-learn|sklearn|scikit\s?learn|Tensor\s?Flow|Py\s?Torch|Keras)\b`
  Covers both the web frameworks (Full Stack profile) and the ML libraries (ML Engineer
  profile) in one pattern, since at the extraction stage the system doesn't yet care which
  profile a term belongs to — that distinction only shows up later, in classification. The
  optional `\s?` and `(?:\.js)?` groups account for spacing and suffix variants like
  `Spring Boot` / `SpringBoot` or `React` / `React.js`.

## Databases

- **Pattern:** `\b(Postgres|PostgreSQL|MySQL|MongoDB|SQLite|Redis|Cassandra|SQL|NoSQL)\b`
  Matches both specific database products and the generic `SQL`/`NoSQL` terms some résumés use
  instead of naming a product.

## Cloud and DevOps tools

- **Pattern:** `\b(Docker|Kubernetes|K8s|Terraform|Ansible|Jenkins|GitHub\s?Actions|GitLab\s?CI|AWS|Azure|GCP|Google\s?Cloud|Linux)\b`
  Supports the DevOps Engineer profile. `K8s` is included alongside `Kubernetes` because it's a
  very common shorthand that normalization will later collapse into one canonical term.

## Data engineering tools

- **Pattern:** `\b(Spark|Apache\s?Spark|Airflow|Kafka|Snowflake|BigQuery|Redshift)\b`
  Supports the Data Engineer profile. Kept separate from the "frameworks and libraries" category
  because these tools are closer to infrastructure than to application code, which matters when
  the canonical ordering per profile gets defined in stage 2.

## Academic qualifications

- **Pattern:** `\b(Bachelor|Master|PhD|B\.?Sc\.?|M\.?Sc\.?)\b(?:\s+(?:of|in))?\s+([A-Za-z\s]+)`
  Looks for a degree keyword (allowing common abbreviations) followed by an optional
  "of"/"in" and the field of study. This is the roughest draft of the set — degree phrasing
  tends to be the least standardized part of a résumé, so it will likely need several more
  passes once sample data with an education section is reviewed.

## Tools and version control

- **Pattern:** `\bGit\b` and, separately, `REST\s?API`
  `Git` is split out from the DevOps/cloud list because it shows up in every single profile and
  is treated as its own category for readability in the extracted output, even though nothing
  stops it from living in the same regex as the others.

## Notes for stage 3 (day 3)

- Every pattern above still needs to be tried against all 10 files in
  `data/sample_resumes/` before being considered final.
- The academic qualifications pattern is the weakest one so far and is the first candidate for
  rework once real wording is tested.
- Deciding what happens to a term that matches none of these patterns (silently dropped vs.
  logged) is left open for day 3, once `extract_all` is actually implemented.
