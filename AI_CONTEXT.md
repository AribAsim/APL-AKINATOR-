# AI Context: IPL Akinator Project

## Overview
This document tracks the current system design, technical decisions, and ongoing changes for the AI IPL Akinator project. It is intended to provide immediate context to any AI model assisting with this repository.

## Goal
Design and develop an AI-powered interactive guessing system that identifies an IPL cricketer (past or present) within a maximum of 8 questions or ≥80% confidence, using probabilistic reasoning (no hardcoded trees).

## System Design

### 1. Component Breakdown
- **Frontend (Web App)**: React/Next.js. Manages user session, captures inputs (Yes/No/Maybe/Don't Know), and displays AI questions and final guess.
- **Backend (API Service)**: Python (FastAPI). Orchestrates the game loop, handles probability updating, and interacts with the database and AI models.
- **AI Decision Engine**:
  - *Bayesian Candidate Tracker*: Maintains player probability distributions.
  - *Entropy Calculator*: Identifies the attribute offering the highest information gain.
  - *Question Generator*: Uses Gemini API to construct dynamic, context-aware questions based on the selected attribute.
- **Database**:
  - *Player DB (e.g., PostgreSQL/BigQuery)*: Stores IPL player profiles, attributes, and stats.
  - *Session DB (e.g., Firebase/Redis)*: Stores active session state, candidate probabilities, and past interactions.

### 2. Data Flow
1. Session start → Full player pool loaded with equal probabilities.
2. AI identifies the optimal attribute to query (highest information gain) → Gemini formulates the question.
3. User responds → Backend applies Bayesian update to probabilities.
4. Evaluation: 
   - If confidence ≥ 80% or 8 questions asked → Return highest probability player.
   - Else → Repeat from step 2.
5. User provides feedback on the final guess, used for future learning.

## Recent Changes & Changelog
- **[2026-05-03]**: Initial system architecture, data flow, and component breakdown documented based on project brief. Awaiting technical stack and dataset confirmation from the user.
- **[2026-05-03]**: Phase 1-3 completed. Created `schema.json` with 33 binary attributes and generated a validated 250-player dataset (`players.json`) balanced across roles.
- **[2026-05-03]**: Phase 4-5 completed. Implemented Bayesian Probability Engine (`probability.py`) with 0.98/0.02 update likelihoods and Information Gain Question Selector (`selector.py`) that minimizes `abs(mass_true - 0.5)`. Ran test simulation successfully.
- **[2026-05-03]**: Phase 6-7 completed. Implemented FastAPI backend (`main.py`, `routes.py`, `models.py`) with in-memory session management. Integrated `QuestionGenerator` via Gemini API for natural language question generation, complete with a dictionary fallback for all 33 attributes. Implemented a disambiguation fallback triggered after 8 questions.

---
*Note: This file should be updated by the AI agent whenever structural changes, new dependencies, or significant design decisions are implemented.*
