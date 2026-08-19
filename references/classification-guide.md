# Classification Guide

Use a method tag for the principal procedure actually carried out in the supplied solution, not merely a keyword mentioned in the prompt. A "method" is the reusable way a problem gets solved: a theorem, a technique, a procedure, or an approach. This guide applies to every subject.

## What Is A Method Tag?

- **Primary method**: the step that makes the solution work. Examples:
  - Math: integration by parts; Lagrange multipliers; diagonalization.
  - Physics: free-body diagram + Newton's second law; energy conservation.
  - Chemistry: balancing redox by half-reactions; ICE table for equilibrium.
  - English / language: scanning for topic sentence; subject-verb agreement check; paraphrasing with synonyms.
  - History / humanities: compare-and-contrast structure; sourcing (who-when-why) analysis.
  - Coding: binary search; dynamic programming with memoization; recursion with a base case.
- **Secondary method**: a substantial additional procedure, such as changing to polar coordinates after applying Green's theorem (math), or drawing a circuit diagram after setting up Kirchhoff's laws (physics).
- **Strategy**: a tactical concern rather than the main engine, such as boundary orientation, excluding a singularity, handling an edge case, symmetry, or re-reading the question stem for a hidden constraint.

## Tag Discipline

Prefer an existing active tag with the same meaning. Create a new tag only when it names a reusable technique likely to occur in multiple problems. Keep names concise and canonical (e.g. `method_integration_by_parts`, `method_redox_half_reaction`, `method_topic_sentence`); add common phrasings as aliases.

## No Solution Supplied

When a solution is not supplied, classify conservatively from the prompt, set `provisional` to `true`, use lower confidence, and state that the method has not been solution-verified.
