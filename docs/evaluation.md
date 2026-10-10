# Evaluation Report — Starter Template

## Scope
The prototype uses a small curated FAQ/case-study library and synthetic intern records. It has not been tested on real Ezitech portal data.

## Automated starter checks
- Known FAQ retrieves a source.
- Unknown portal-specific questions do not receive invented answers.
- A known intern receives a learning plan.

Run `python -m pytest` after installing pytest.

## Manual evaluation plan
Prepare 20–30 questions covering FAQs, case studies, debugging, feedback, and unknown topics. Record correct-source retrieval, groundedness, abstention correctness, clarity, and response latency. Useful metrics include Recall@3 and source-grounded answer rate. Do not claim accuracy figures until measured on a test set.
