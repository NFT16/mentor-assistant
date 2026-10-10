# Prompt Engineering and Response Policy

This starter does not call an external LLM; answers are constructed from retrieved local knowledge to keep the demo free and easy to run.

If an LLM is added later, use instructions such as:
- Answer only from supplied retrieved context and verified intern fields.
- If evidence is missing, say so and direct the user to the official portal or mentor.
- Never invent deadlines, portal rules, grades, or performance facts.
- Explain debugging steps rather than completing restricted assignments.
- Label recommendations as suggestions for mentor review.

Keep retrieved text separate from system instructions and evaluate groundedness before deployment.
