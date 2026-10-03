# Sample résumés

Ten résumé fragments used for development and testing across all four pipeline stages. Each one
targets a specific scenario described in `docs/test_cases.md`.

| File | Intended profile(s) | Notes |
|---|---|---|
| `wednesday_addams.txt` | Full Stack Developer | from the assignment statement |
| `mary_jane_watson.txt` | Machine Learning Engineer | from the assignment statement |
| `peter_parker.txt` | Full Stack Developer | different stack (Angular/Spring Boot/MongoDB) than the reference example |
| `tony_stark.txt` | DevOps Engineer | |
| `michael_scott.txt` | DevOps Engineer | different tool combo (Azure/Ansible/GitHub Actions) |
| `hermione_granger.txt` | Data Engineer | |
| `walter_white.txt` | Data Engineer | different tool combo (Kafka/BigQuery/Redshift) |
| `daenerys_targaryen.txt` | Full Stack Developer + DevOps Engineer | has the full required chain for both — Docker/Kubernetes/Terraform/Jenkins/AWS alone wasn't enough for DevOps until Terraform and Jenkins were added, see below |
| `eleven.txt` | Machine Learning Engineer + Data Engineer | has the full required chain for both — TensorFlow had to be added for the ML Engineer chain to complete, see below |
| `rick_sanchez.txt` | none | too few qualifications to satisfy any of the four profiles |

Classification is verified end to end (stages 1–3) against the four automata in
`docs/formalization_automata.md`'s worked-examples table — that table is the source of truth for
which profile(s) each résumé actually gets accepted into. The "mixed" cases above weren't
accepted into two profiles by accident: an earlier version of `daenerys_targaryen.txt` only had
Docker/Kubernetes/AWS, which satisfies Full Stack but is missing an infrastructure-as-code tool
and a CI/CD tool, both required by the DevOps Engineer automaton — so it was rejected for DevOps
until Terraform and Jenkins were added. Likewise, `eleven.txt` originally had no TensorFlow or
PyTorch, which the Machine Learning Engineer automaton requires regardless of how many other ML
qualifications are present — it was only accepted for Data Engineer until TensorFlow was added.
