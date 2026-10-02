# Formalization — Stage 4: Candidate Profile DSL (textX)

## Grammar (EBNF)

> Definir en `resumelens/dsl/candidate.tx`. Resumen EBNF aquí, identificando terminales y
> no-terminales.

```
CandidateProfile ::= PersonalInfo ContactInfo Experience* Education* Skills ClassificationResult+
...
```

_(completar con la gramática real una vez implementada)_

### Terminales

- _(pendiente, p. ej. STRING, INT, EMAIL, etc.)_

### No-terminales

- _(pendiente, p. ej. PersonalInfo, ContactInfo, Experience, Education, Skills, ClassificationResult)_

## Características estructurales del lenguaje

- _(soporta elementos repetidos: múltiples experiencias, educación, skills)_
- _(reglas léxicas/sintácticas que generan rechazo)_

## Validación

- Casos válidos: _(pendiente)_
- Casos que deben ser rechazados: _(pendiente — violaciones léxicas/sintácticas)_

## Visualización

- Salida: HTML o Markdown generado desde el modelo validado (`render_html` / `render_markdown`)
- _(agregar ejemplo de salida una vez implementado)_
