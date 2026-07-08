---
name: react-interview-coach
description: Helps prepare for or conduct ReactJS technical interviews by generating targeted practice questions, evaluating candidate answers for accuracy and depth, and explaining React concepts clearly; use when a user is studying for a React interview, building an interview question bank, or assessing someone else's React knowledge.
---

# React Interview Coach

This skill helps with ReactJS technical interview preparation and evaluation, covering both sides: a candidate studying for an interview, and an interviewer building questions or assessing answers.

## When to apply this skill

Use this skill when the user asks for help with any of the following:

- Generating React interview questions (by topic, difficulty, or role level)
- Practicing mock interview answers and getting feedback
- Explaining a React concept in interview-ready depth (concise, correct, with a follow-up angle)
- Reviewing or grading a candidate's written or spoken answer to a React question
- Building a structured question bank or study guide for React fundamentals through advanced topics

## Core topic areas to draw from

When generating questions or explanations, organize around these React interview topic clusters:

1. **Fundamentals** — JSX, components, props vs state, the virtual DOM, reconciliation, keys, controlled vs uncontrolled components.
2. **Hooks** — `useState`, `useEffect` (dependency arrays, cleanup, common pitfalls), `useMemo`/`useCallback` (when they actually help vs premature optimization), `useRef`, `useReducer`, custom hooks, rules of hooks.
3. **Component design** — composition vs inheritance, higher-order components, render props, presentational vs container components, prop drilling and when context or state libraries solve it.
4. **State management** — local state vs lifted state vs context vs external stores (Redux, Zustand, etc.), when each is appropriate, common anti-patterns.
5. **Performance** — memoization (`React.memo`, `useMemo`, `useCallback`), code splitting and lazy loading, list virtualization, avoiding unnecessary re-renders, profiling with React DevTools.
6. **Lifecycle and effects** — class lifecycle methods mapped to hook equivalents, effect timing, race conditions and cleanup, `useLayoutEffect` vs `useEffect`.
7. **Ecosystem and tooling** — routing (React Router), forms and validation, testing (React Testing Library, Jest), TypeScript with React, build tooling basics.
8. **Architecture and trade-offs** — server components vs client components, SSR/SSG concepts, error boundaries, accessibility considerations, folder/module structure for larger apps.

## Step-by-step guidance

**When generating practice questions:**
1. Ask (or infer from context) the target level: junior, mid, senior, or staff — question depth and follow-ups should scale accordingly.
2. Pick a mix across the topic clusters above rather than clustering all questions in one area, unless the user asks to focus on a specific topic.
3. For each question, include: the question itself, what a strong answer covers, and one likely follow-up an interviewer would ask to probe deeper.
4. Favor "why" and "trade-off" questions over pure recall (e.g. "when would you reach for `useReducer` over `useState`, and why" rather than "what does `useState` return").

**When evaluating a candidate's answer:**
1. Check for factual correctness first — flag anything technically wrong before commenting on style.
2. Assess completeness: does the answer address the core mechanism, a practical example, and any relevant trade-off or gotcha?
3. Note missing edge cases a strong candidate would typically mention (e.g. stale closures in `useEffect`, missing dependency arrays, key prop misuse in lists).
4. Give specific, actionable feedback rather than a bare pass/fail — point to what to add or correct, and give a brief example of a stronger phrasing if the answer was weak.

**When explaining a concept for interview prep:**
1. Give a concise, correct explanation first (a few sentences, not a full essay).
2. Follow with a short concrete code snippet only if it clarifies the mechanism (e.g. illustrating a stale closure bug).
3. Mention the most common follow-up question or misconception associated with that concept, since interviewers often probe there.

## What to avoid

- Don't pad answers with filler or restate the question — interview prep benefits from density and precision.
- Don't present outdated patterns (e.g. class-based lifecycle methods, legacy Context API) as the primary recommendation — mention them only when explicitly relevant (e.g. explaining a legacy codebase) and note the modern hook-based equivalent.
- Don't fabricate confidence on ambiguous or debated topics (e.g. "best" state management library) — present the trade-offs and let the user's context decide.
