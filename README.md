# CodeGuard

An AI code review agent that runs on every pull request. Three specialist
LLM agents (bug, security, code-quality) independently review each changed
file, and an aggregator merges their findings into a single GitHub PR review
with inline comments.

Built with [LangGraph](https://langchain-ai.github.io/langgraph/) for
multi-agent orchestration and [Groq](https://groq.com) for fast LLM
inference. Runs entirely inside a GitHub Actions workflow — no server to
host.

## How it works

```
PR opened/updated
      │
      ▼
GitHub Actions workflow (.github/workflows/code-review.yml)
      │
      ▼
main.py: fetch PR file diffs via GitHub REST API
      │
      ▼
diff_parser: annotate each diff line with its real file line number
      │
      ▼
LangGraph pipeline (graph.py)
   ┌──────────┬──────────────┬──────────────┐
   │ bug_agent│security_agent│quality_agent │  (run in parallel, each calls Groq)
   └──────────┴──────────────┴──────────────┘
      │
      ▼
aggregator: dedupe overlapping findings, cap volume, format comments
      │
      ▼
GitHub REST API: post one PR review with inline comments
```

## Setup

1. Add a Groq API key as a repository secret named `GROQ_API_KEY`
   (Settings → Secrets and variables → Actions).
2. Make sure Actions has write permission for pull requests: Settings →
   Actions → General → Workflow permissions → "Read and write permissions".
3. Open or update a PR — the `CodeGuard Review` workflow runs automatically.

## Local development

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in GROQ_API_KEY and a GITHUB_TOKEN (repo scope)

# Dry-run against a real PR: prints findings instead of posting comments
python -m src.codeguard.main --dry-run --owner <owner> --repo <repo> --pr <number>
```

Run the test suite:

```bash
pytest
```

## Configuration

Environment variables (see `config.py`):

| Variable | Purpose |
| --- | --- |
| `GROQ_API_KEY` | Groq API key used by all three agents |
| `GITHUB_TOKEN` | Token used to read PR diffs and post the review |
| `GROQ_MODEL` | Override the model (default: `llama-3.3-70b-versatile`) |
| `CODEGUARD_MAX_COMMENTS` | Cap on inline comments per review (default: 15) |

CodeGuard never fails the Action on LLM or GitHub API errors — it's a
review aid, not a merge gate.
