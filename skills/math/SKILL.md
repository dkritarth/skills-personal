---
name: math
version: 0.2.0
description: Enforces structured mathematical proof formatting (Claim, Assumptions, Proof, Where Used) and runs symbolic and numeric verification on extracted sub-claims using SymPy.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Grep, Glob]
disable-model-invocation: true
---

# Math

Mechanical proof verification and structural auditing for mathematical writeups.

This skill extracts algebraic, numeric, and analytic sub-claims from proof drafts and checks them against SymPy to catch calculation bugs before submission.

## When to use

- Reviewing proof drafts containing algebraic expansions, trigonometric identities, summations, matrix operations, or inequality bounds.
- Checking that a proof states all necessary assumptions upfront rather than introducing unstated premises mid-argument.

## When not to use

- Informal or philosophical arguments with no checkable symbolic math.
- Complete formal verification in interactive theorem provers (Lean, Coq, Isabelle). This skill flags candidates for formal proofs but does not generate Lean code.
- General prose edits. Delegate to `academic-humanizer`.

## Process

### 1. Extract claims
Isolate mathematical assertions into a scratch file using the syntax expected by `scripts/sympy_verify.py`:

```text
CLAIM <id>: <lhs> <op> <rhs> [assuming <var><cmp><bound>, ...]
```

Supported comparison operators: `==`, `!=`, `>=`, `<=`, `>`, `<`.

Example:
```text
CLAIM 1: (x + y)**2 == x**2 + 2*x*y + y**2
CLAIM 2: exp(x) >= 1 + x assuming x > 0
```

### 2. Run verification
Execute the verification script:

```bash
python3 scripts/sympy_verify.py path/to/claims.txt
```

Interpret results:
- `PASS (proved)`: Symbolically confirmed by SymPy over the specified domain.
- `PASS (numeric only)`: Sampled points satisfied the condition, but no analytical proof was derived. Treat as supporting evidence, not strict formal proof.
- `FAIL`: A counterexample was identified. Output the counterexample values immediately.
- `UNVERIFIABLE`: Expression could not be evaluated by SymPy. Requires manual check.

### 3. Verify proof structure
Confirm that the proof follows standard sequential sections:
1. **Claim**: Clear theorem, lemma, or proposition statement.
2. **Assumptions**: Complete declaration of bounds, spaces, and initial conditions stated before the derivation begins.
3. **Proof**: Step-by-step argument with explicit references to established theorems.
4. **Where used**: Explicit mention of downstream theorems or application contexts relying on this lemma.
