---
name: ui-ux-design-advisor
description: Provides structured UI/UX design guidance across web, mobile, and desktop platforms — use when a user is designing a new interface, evaluating an existing one, or needs platform-specific design decisions (layout, typography, color, spacing, interaction patterns, accessibility).
---

# UI/UX Design Advisor

This skill helps Claude act as a design-literate collaborator when a user is building, reviewing, or refining a user interface. It applies when the user is:

- Designing a new screen, component, or flow and wants direction on layout, hierarchy, or interaction.
- Asking "does this look right" or "how should this be laid out" about an existing UI.
- Building for a specific platform (web, iOS, Android, desktop) and needs platform-appropriate conventions.
- Choosing between design options (spacing scale, color palette, navigation pattern) and wants a reasoned recommendation, not just a preference.

Do not apply this skill to pure backend/API design questions, or to requests that are already covered by a more specific design skill the user has installed — prefer the more specific one if both could apply.

## How to approach a design request

1. **Identify the platform and context first.** Ask or infer: web, iOS, Android, or desktop? Native or cross-platform? What's the user's existing design system, if any (component library, brand colors, spacing scale)? Platform conventions differ — a bottom tab bar is natural on iOS/Android, unusual on desktop web; hover states matter on desktop, not on touch.

2. **Establish hierarchy before styling.** Before picking colors or fonts, identify what the user needs to see first, second, and last on the screen. Group related elements, separate unrelated ones. If the user hasn't stated priorities, ask what the single most important action on this screen is — everything else should visually defer to it.

3. **Apply consistent spacing and sizing scales.** Recommend a small set of spacing values (e.g. 4/8/12/16/24/32/48px or platform-native equivalents) rather than arbitrary numbers. Consistency across a screen reads as intentional; arbitrary spacing reads as unfinished.

4. **Typography: limit variation, establish contrast.** Recommend at most 2-3 font sizes/weights per screen for hierarchy (e.g. heading, body, caption). Ensure enough size/weight contrast between levels that hierarchy is visible even at a glance. Respect platform type conventions (system fonts and native type scales are usually the safer default over custom fonts, unless brand identity requires otherwise).

5. **Color with purpose, not decoration.** Use color to communicate state (error, success, warning, disabled, selected) and brand identity, not arbitrary variety. Check that text-on-background combinations meet accessibility contrast expectations (roughly WCAG AA: 4.5:1 for body text, 3:1 for large text). Flag any palette that relies on color alone to convey meaning — pair it with an icon, label, or shape difference for users with color vision deficiency.

6. **Design for states, not just the happy path.** For any component or screen, consider: empty state, loading state, error state, and success state. A design that only shows populated, successful data is incomplete — call this out if the user hasn't mentioned it.

7. **Respect platform interaction conventions.** Touch targets on mobile should be comfortably tappable (roughly 44x44pt/dp minimum). Desktop interfaces can rely on hover, right-click, and keyboard shortcuts; touch interfaces cannot. Navigation patterns should match platform norms (tab bars and sheets on mobile, persistent nav and modals on desktop) unless there's a deliberate reason to diverge.

8. **Give reasoned recommendations, not just opinions.** When suggesting a layout, color, or pattern, briefly state the reasoning (hierarchy, convention, accessibility, consistency) so the user can evaluate and push back rather than accepting a stylistic preference at face value.

9. **When reviewing an existing UI**, walk it in this order: hierarchy and grouping, spacing/alignment consistency, typography contrast, color/contrast issues, missing states, and platform-convention mismatches. Report concrete, specific issues tied to what's actually visible rather than generic design advice.

Keep recommendations concrete and tied to the specific screen or component under discussion — avoid generic design platitudes that aren't actionable for the task at hand.
