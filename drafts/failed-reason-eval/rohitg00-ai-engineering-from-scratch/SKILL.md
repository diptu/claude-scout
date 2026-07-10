---
name: ai-engineering-from-scratch
description: Teach or apply AI engineering fundamentals (tokenization, embeddings, RAG, fine-tuning, evals, agents) by building minimal working versions from first principles before reaching for frameworks; use when a user wants to learn how an AI/LLM technique works internally or wants a from-scratch reference implementation instead of a black-box library call.
---

# AI Engineering From Scratch

Helps explain and implement core AI engineering concepts by building the smallest possible working version of a technique from first principles, rather than immediately wrapping a high-level library call. The goal is understanding through construction: show what a framework does internally before using the framework.

## When to apply this skill

- The user asks "how does X actually work" for an AI/LLM concept (tokenization, embeddings, attention, RAG, fine-tuning, vector search, agents, evals, prompt caching, etc.).
- The user wants to learn AI engineering by building, not just reading about it — they ask for a minimal implementation, a toy example, or "from scratch" phrasing.
- The user is about to reach for a heavy framework (LangChain, LlamaIndex, a vector DB) for a simple task and would benefit from first seeing the underlying mechanics in plain code.
- The user wants to ship a small, self-contained AI feature and understand every moving part rather than depend on an opaque abstraction.

Do not apply this skill when the user just wants a working production feature fast and has already signaled familiarity with the underlying concepts — in that case, use the standard library/framework directly without the teaching detour.

## Step-by-step guidance

1. **Identify the concept and its minimal working definition.** Before writing code, state in one or two sentences what the technique actually computes (e.g., "cosine similarity between a query embedding and stored document embeddings, then take the top-k"). If the user's request bundles several concepts (e.g., "build me a RAG chatbot"), decompose it into the individual primitives first: chunking, embedding, storage/retrieval, prompt assembly, generation.

2. **Build the smallest version first, with no framework.** Use plain language constructs (dictionaries, lists, basic math) instead of a framework's abstraction. For example:
   - Tokenization: split text and show how a simple byte-pair or whitespace scheme groups characters into tokens, before mentioning tiktoken/sentencepiece.
   - Embeddings/RAG: compute or call an embedding API directly, store vectors in a plain list or dict, implement cosine similarity by hand, and do a linear scan for top-k — before ever mentioning a vector database.
   - Fine-tuning/training loops: show the core loop (forward pass, loss, backward pass, update) conceptually or in minimal pseudocode before pointing at a trainer class.
   - Agents/tool use: show the loop explicitly (model call → parse tool request → execute → feed result back → repeat) before mentioning an agent framework.
   - Evals: show a plain pass/fail or scored comparison over a handful of examples before mentioning an evals framework.

3. **Layer in the "real" tooling only after the concept lands.** Once the from-scratch version is understood, mention the production-grade equivalent (a real tokenizer library, a vector database, a training framework, an agent framework) and explain what it adds over the minimal version (speed, scale, edge cases handled) — not as a replacement for understanding, but as the next step once the mechanics are clear.

4. **Prefer runnable, self-contained examples over abstract explanation.** Whenever code is appropriate, write a short, complete example the user could actually execute, using only standard library or a single well-known API call, rather than a fragment that depends on unexplained setup.

5. **Ship for others, not just for the user.** If the user's end goal is a feature or tool for other people to use (not just a personal learning exercise), after the from-scratch explanation, help harden the minimal version into something shippable: add basic error handling at the real boundaries (bad input, API failures), and note what would need to change to handle realistic scale — but only once the underlying mechanism has been demonstrated plainly.

6. **Match depth to the ask.** If the user wants a quick mental model, stop after step 1-2. If the user wants to actually build and ship something, continue through steps 3-5. Don't force every AI engineering question into a full from-scratch implementation when a concise conceptual answer is what's needed.
