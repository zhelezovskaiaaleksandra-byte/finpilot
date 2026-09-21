# FinPilot — Project Brief

*Working title: FinPilot (temporary). Last updated 2026-09-21.*

## Mission

An AI-powered financial companion that helps young adults understand investing, make better financial decisions, and build wealth according to their personal goals. Investing should feel accessible, educational, and personalized for beginners.

FinPilot is **not** another brokerage platform, and it is **not** trying to beat the market. It answers one question: *"What investment strategy makes sense for me?"*

## The problem

Most investment platforms are built for experienced investors. Young adults face financial jargon, information overload, fear of making mistakes, no personalized guidance, the belief that investing requires a lot of money, and difficulty connecting investments to real-life goals. Many people delay investing for years simply because they don't know where to start.

## Target users

Students, first-time investors, and young professionals aged 18–30, typically investing relatively small amounts. The platform should always stay beginner-friendly.

## Product philosophy

The founding insight: an early idea to build ML models that predict stock prices was dropped after realizing that predicting markets isn't where the value lies. The product should understand *people* — their situation, goals, and risk — rather than try to predict markets.

Priorities, in order: education over hype, long-term investing over speculation, transparency over complexity, goals over products. It should never feel like Wall Street software — it should feel like a modern consumer app.

## Core user journey

1. **Personal profile** — age, country, occupation, income, expenses, savings, debt, investment experience, monthly amount available to invest, risk tolerance, investment horizon.
2. **Financial goals** — not "what stocks do you want" but "what do you want your money to achieve": emergency fund, house, car, study abroad, retirement, financial independence, passive income, long-term wealth. Goals sit at the center of every recommendation.
3. **Personalized strategy** — recommended asset allocation, suggested monthly contribution, risk explanation, and horizon, always explained in simple language.
4. **Interactive simulator** — the user adjusts contribution, horizon, expected return, and risk level, and instantly sees optimistic/expected/pessimistic scenarios with compound-interest visualization.
5. **Education** — beginner-friendly explanations of concepts (ETFs, diversification, inflation, volatility, index funds, bonds) woven into the product experience rather than taught separately.
6. **AI assistant** *(later — see roadmap)* — behaves like a personal financial coach, answering questions like "why is this portfolio recommended?" or "should I invest or pay off debt first?", adapting explanations to the user's level.

## Technology vision

- **Financial Data Engine** — financial APIs, ETFs, stocks, macroeconomic indicators, historical prices.
- **User Intelligence Engine** — understands financial profile, goals, income, expenses, risk profile.
- **Recommendation Engine** — the core of the platform; recommends personalized strategies instead of predicting prices.
- **AI Assistant** — LLM-based, explains recommendations and answers financial questions.

**Machine learning** is used only where it provides real value (user segmentation, recommendation systems, risk classification, behavioral analysis, probability of achieving goals, portfolio personalization) — never added just because it sounds impressive. Simple solutions are preferred unless there's a clear benefit to ML.

## Long-term vision (beyond investing)

Budgeting, savings planner, portfolio tracking, financial health score, AI-generated monthly reports, behavioral finance insights, goal tracking, automatic rebalancing, retirement planning. Investing is only the first part of a broader financial planning platform.

## Four-year roadmap

- **Year 1** — MVP: rule-based recommendation engine, interactive simulator, deployed public version.
- **Year 2** — Real financial APIs, a real database and data pipelines, improved recommendations, first ML.
- **Year 3** — AI assistant, deeper personalization, natural-language explanations, user testing.
- **Year 4** — Mobile app, scalability, business model, launch.

(See `docs/YEAR1_PLAN.md` for how Year 1 specifically is scoped and phased.)

## What "success" means for this project

My primary goal for FinPilot is not to launch a funded startup — it's to end up with a complete, polished, deployed product that's my main competitive advantage in job applications, mainly targeting a full-time role after graduation, with a secondary goal of having something solid enough to show for a summer internship search along the way.

That shapes what "worth building" means at every stage: a live, working, deployed link matters more than a private code repository, so deploying early and repeatedly beats polishing in private until the end of the year. Depth on a small, polished core loop beats a long feature list — one thing built and explained well outweighs five half-finished features in an interview. Business concerns that only matter for a real company — funding, monetization, user acquisition, full regulatory compliance — are explicitly deprioritized; a clear "educational, not real financial advice" disclaimer is enough, since this isn't a live business handling real money. A written narrative of technical decisions (why rules before ML, why this architecture, what trade-offs were made) is itself part of the deliverable, since interviews reward explaining judgment, not just working code. Mobile and other Year 4 items are optional rather than required.

## Background

I'm an Economics student, and I want this project to be the practical, running application of what I study over the next few years — economics, finance, statistics, programming, and machine learning — with the product evolving alongside my coursework.
