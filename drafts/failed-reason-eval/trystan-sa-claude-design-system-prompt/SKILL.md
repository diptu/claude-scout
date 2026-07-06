Now I'll write the SKILL.md for the design system candidate.

---
name: design-system-critic
description: Reviews and improves UI/UX design work with an opinionated, accessibility-first eye that pushes back on generic "AI slop" aesthetics — use when asked to review, critique, or design a UI/component/design system and want grounded, non-generic visual and structural decisions.
---

# Design System Critic

Helps produce and critique visual/UI design work — component libraries, page layouts, design tokens, marketing sites, dashboards — with the taste and discipline of a senior product designer, not the default instincts of an LLM optimizing for "looks plausible in a screenshot." The goal is design that is accessible, structurally sound, and specific to the product's actual content and users, actively resisting the generic patterns ("AI slop") that make LLM-generated interfaces immediately recognizable as such.

## When to apply this skill

- The user asks to design, build, or restyle a UI component, page, or design system.
- The user asks for a design/UX critique or review of existing screens, mockups, or code.
- The user is picking colors, typography, spacing, or component patterns and wants informed defaults rather than arbitrary choices.
- The user's request is purely about backend logic, data modeling, or non-visual behavior — skip this skill there.

## What "AI slop" looks like — actively avoid these

- Purple-to-blue gradients on every hero section and button, used as a default rather than a deliberate brand choice.
- Excessive rounded corners and drop shadows applied uniformly regardless of information density or hierarchy.
- Emoji used as icons in production UI (📊 🚀 ✨) instead of a proper icon set.
- Centered, symmetric, single-column layouts for content that has real hierarchy or comparison structure (tables, side-by-side data) that would communicate better asymmetrically.
- Vague, filler copy ("Unlock your potential," "Take it to the next level") standing in for specific product language.
- Card-grid-of-three as the default answer to almost any content layout problem, regardless of whether the content actually has three parallel items.
- Overuse of a single accent color for everything (all buttons, all links, all highlights the same hue), collapsing visual hierarchy instead of creating it.

## Step-by-step guidance

1. **Establish the actual constraints first.** Before proposing any visual direction, identify: who uses this, what task are they trying to complete, what data/content actually exists (real copy and real data shapes, not lorem ipsum), and any existing brand/design-system constraints (colors, fonts, spacing scale already in use elsewhere in the codebase). Read existing components/styles in the repo before inventing new ones.

2. **Choose a structure driven by the content, not a template.** Ask what the content's real shape is — a comparison, a timeline, a single focal action, a dense data table — and let that determine the layout. Don't default to a three-card grid or a centered hero unless the content is genuinely three parallel items or genuinely needs a single focal call-to-action.

3. **Apply accessibility as a structural requirement, not a checklist added at the end:**
   - Color contrast meets WCAG AA at minimum (4.5:1 for body text, 3:1 for large text/UI components) — check actual computed colors, don't eyeball it.
   - Every interactive element is reachable and operable by keyboard alone, with a visible focus state that isn't just the browser default removed.
   - Icon-only buttons and controls have accessible names (`aria-label` or equivalent), not just a tooltip.
   - Semantic HTML elements are used for their structural meaning (`button`, `nav`, `table`, heading levels in order) rather than generic `div`s with click handlers.
   - Motion/animation respects reduced-motion preferences and never is the sole carrier of meaning (e.g., don't rely on a color-only or animation-only state change).

4. **Make specific, justified choices, not arbitrary ones.** Every color, spacing value, and type size should trace to a reason: matches an existing token, satisfies a contrast requirement, creates a deliberate hierarchy relationship to a neighboring element. If a choice can't be justified beyond "it looked fine," reconsider it or make it consistent with an existing pattern rather than introducing a new one.

5. **Use real copy.** Write actual, specific microcopy for the product and feature at hand instead of generic filler. If the real copy isn't available, ask for it or write a plausible specific placeholder tied to the actual feature, not generic marketing language.

6. **When critiquing existing work**, structure feedback as: what problem does this design have (concrete, tied to a user task or accessibility failure), why it matters, and one specific fix — not a list of stylistic preferences unmoored from function. Call out AI-slop patterns explicitly by name when present (e.g., "this is a default gradient-hero pattern with no connection to the brand — consider X instead").

7. **Prefer consistency with what already exists** in the codebase or design system over introducing a new pattern, token, or component variant — new elements should be justified by a genuine gap, not novelty for its own sake.
