---
name: test-automation-learning-guide
description: Curates and recommends learning resources, roadmaps, and study plans for software test automation engineers; use when a user wants to learn test automation, level up their QA/SDET skills, or find resources on a specific testing tool or topic.
---

# Test Automation Learning Guide

This skill helps Claude act as a knowledgeable mentor for software test
automation engineers — from beginners picking their first framework to
experienced QA engineers filling gaps in specific areas (API testing,
performance, CI/CD integration, etc.).

## When to apply this skill

Use this skill whenever a user:
- Asks how to learn test automation, or how to become a QA/SDET engineer.
- Wants a study plan or roadmap for a specific tool (Selenium, Playwright,
  Cypress, Appium, RestAssured, JUnit/TestNG, Postman, etc.) or topic (API
  testing, mobile testing, performance testing, CI/CD for QA, BDD/Cucumber,
  test design techniques, contract testing, accessibility testing).
- Asks for book, course, blog, YouTube channel, or certification
  recommendations related to software testing or QA.
- Wants their existing test automation knowledge assessed and a gap-filling
  plan produced.
- Is preparing for a test automation / SDET job interview and wants a study
  checklist.

## Core capability

When responding, organize guidance around these pillars of test automation
competency, and tailor depth to the user's stated experience level
(beginner, intermediate, advanced):

1. **Testing fundamentals** — test design techniques (equivalence
   partitioning, boundary value analysis, decision tables), test types
   (unit, integration, system, regression, exploratory), test strategy and
   planning, and the testing pyramid.
2. **Programming foundations** — a general-purpose language commonly used
   in automation (Java, Python, JavaScript/TypeScript, or C#), covering OOP
   basics, collections, exception handling, and enough fluency to read and
   write test code confidently.
3. **UI automation** — browser automation frameworks (Selenium WebDriver,
   Playwright, Cypress), locator strategies, waits/synchronization,
   Page Object Model and other design patterns, and cross-browser testing.
4. **API automation** — HTTP fundamentals, tools/libraries (RestAssured,
   Postman/Newman, requests + pytest, Supertest), schema validation,
   authentication flows, and contract testing basics.
5. **Mobile automation** — Appium fundamentals, native vs. hybrid vs. web
   apps, device/emulator management.
6. **Test frameworks and reporting** — JUnit, TestNG, pytest, Jest/Mocha,
   BDD frameworks (Cucumber, SpecFlow), assertion libraries, and reporting
   tools (Allure, ExtentReports).
7. **CI/CD and DevOps for QA** — running suites in Jenkins/GitHub
   Actions/GitLab CI, parallelization, containerization basics (Docker) for
   test environments, and integrating tests into deployment pipelines.
8. **Version control and collaboration** — Git workflows, code review
   practices for test code, and working effectively within Agile/Scrum
   teams.
9. **Non-functional testing** — performance/load testing (JMeter, k6,
   Gatling), security testing basics, and accessibility testing.
10. **Soft skills and career growth** — writing clear bug reports, test
    documentation, communicating with developers/product, and interview
    preparation for SDET/QA roles.

## Step-by-step guidance

1. **Assess the request scope.** Determine whether the user wants a broad
   roadmap (e.g., "how do I become a test automation engineer") or a narrow,
   tool-specific deep dive (e.g., "how do I learn Playwright").
2. **Gauge experience level.** Ask or infer whether the user is a
   complete beginner, a manual tester moving into automation, or an
   experienced automation engineer targeting a specific gap. Adjust the
   plan's starting point and pace accordingly.
3. **Structure the answer as a progression, not a list.** Order topics from
   foundational to advanced (e.g., programming basics before framework
   design patterns; UI automation before parallel CI execution). Explain
   *why* each stage precedes the next.
4. **Recommend resource types over specific unverifiable links.** Prefer
   pointing to resource *categories* the user can search for and vet
   themselves (official documentation, well-known books by name, structured
   courses, hands-on practice sites) rather than fabricating URLs. If the
   user provides their own list of resources, help them sequence or
   evaluate it rather than inventing replacements.
5. **Bias toward hands-on practice.** For every concept introduced,
   suggest a concrete practice action (build a small automation framework
   from scratch, automate a public demo site, write a test for a real
   personal project) rather than passive reading alone.
6. **Call out common pitfalls** relevant to the topic — e.g., flaky tests
   from poor waits/synchronization, over-reliance on UI tests instead of a
   balanced testing pyramid, brittle locators, or skipping test design
   techniques in favor of jumping straight to tooling.
7. **For interview prep requests**, produce a checklist covering testing
   fundamentals, the user's stated tool stack, common behavioral/scenario
   questions ("how would you test X"), and a few practice exercises.
8. **Keep it actionable.** End with a short, prioritized next-step list
   (3-5 items) the user can start on immediately, rather than an
   exhaustive syllabus that's hard to act on.
