# Homework 1 — Design and Test a Learning Assistant

## Goal

Create and test one reusable prompt that teaches an AI Engineering topic clearly to an experienced software developer who is new to AI Engineering.

Choose a topic other than “tokens.”

Examples: RAG, MCP, embeddings, agents, context windows, or prompt injection.

## Part 1 — Baseline

Open a new chat and ask:

> Explain [your topic].

Save the response.

## Part 2 — Improved prompt

Write a prompt that defines:

- The assistant’s role
- The learner’s background
- The learning goal
- What the assistant should explain
- What it should do when the question is ambiguous
- What it should avoid
- The required response format
- One practical next step

Your prompt must tell the assistant to avoid inventing facts and to distinguish facts from assumptions.

## Part 3 — Test the prompt

Use the same improved prompt with three questions:

1. A basic “What is this?” question
2. An implementation or architecture question
3. An ambiguous question requiring clarification

Save the three responses.

## Part 4 — Compare

Write a short comparison:

- What improved compared with the baseline?
- Which instruction had the biggest effect?
- Where did the assistant still make assumptions?
- What would you change in the prompt next?
