# Helicone Examples - Complete Tutorial Series

This repository contains all code examples from the 3-part Helicone blog series on LLM observability. Each example is production-ready and demonstrates a specific Helicone feature or integration pattern.

## Blog Series

- **Part 1**: [Getting Started with Helicone — LLM Observability in One Line of Code](https://zubairashfaque.github.io/blog/helicone-getting-started.html)
- **Part 2**: [Helicone Features Deep Dive — From Tracing to Prompt Management](https://zubairashfaque.github.io/blog/helicone-features-deep-dive.html)
- **Part 3**: [Production Use Cases and Best Practices with Helicone](https://zubairashfaque.github.io/blog/helicone-production-best-practices.html)

## Prerequisites

- **Python**: 3.10 or higher
- **Node.js**: 18 or higher (for TypeScript examples)
- **Helicone Account**: Free tier includes 10,000 requests/month — [Sign up here](https://helicone.ai)
- **API Keys**: OpenAI, Anthropic, or other LLM provider keys

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/zubairashfaque/helicone-examples.git
cd helicone-examples
```

### 2. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Helicone API Key (required)
HELICONE_API_KEY=sk-helicone-xxxxxxxxxxxxx

# LLM Provider Keys (add the ones you need)
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxx
GOOGLE_API_KEY=xxxxxxxxxxxxx
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 4. Install TypeScript Dependencies (optional)

```bash
npm install
```

### 5. Run Your First Example

```bash
cd part1-getting-started
python healthcare_triage.py
```

## Repository Structure

```
helicone-examples/
├── part1-getting-started/
│   ├── healthcare_triage.py          # Complete healthcare AI triage example
│   ├── multi_provider_routing.py     # Switch between OpenAI, Claude, Gemini
│   ├── async_logging_example.py      # Zero-latency async logging
│   └── framework_integrations/
│       ├── langchain_example.py      # LangChain integration
│       ├── crewai_example.py         # CrewAI integration
│       ├── autogen_example.py        # Microsoft AutoGen integration
│       └── vercel_ai_sdk.ts          # Vercel AI SDK integration
│
├── part2-features/
│   ├── session_tracing.py            # Multi-agent session tracing
│   ├── caching_examples.py           # Response caching configurations
│   ├── rate_limiting.py              # Rate limit policies (global, per-user, cost-based)
│   ├── retry_fallback.py             # Retry + provider fallback chains
│   ├── prompt_management.py          # Prompt versioning and deployment
│   └── kitchen_sink.py               # All features combined in one request
│
├── part3-production/
│   ├── autogen_multi_agent.py        # Complete multi-agent AutoGen workflow
│   ├── security_integration.py       # Llama Guard + Prompt Guard
│   ├── posthog_integration.py        # PostHog analytics integration
│   ├── docker-compose.yml            # Self-hosted deployment
│   └── cost_optimization.py          # Production cost reduction techniques
│
├── .env.example                      # Template for environment variables
├── requirements.txt                  # Python dependencies
├── package.json                      # TypeScript dependencies
└── README.md                         # This file
```

## Part 1: Getting Started Examples

### Healthcare Triage Assistant (`healthcare_triage.py`)

A complete example demonstrating:
- AI Gateway integration
- Custom property tagging (department, environment)
- User tracking (per-patient analytics)
- Prompt versioning

**Expected Output:**
```
Classification: EMERGENCY
Rationale: Symptoms are consistent with acute coronary syndrome...
Cost: $0.004
Latency: 1,230ms
```

### Multi-Provider Routing (`multi_provider_routing.py`)

Switch between OpenAI, Claude, and Gemini using the same client:

```python
# Same client, different models
response = client.chat.completions.create(
    model="gpt-4o",  # or "claude-sonnet-4", or "gemini-2.0-flash"
    messages=[{"role": "user", "content": "Your prompt"}]
)
```

### Framework Integrations

- **LangChain**: Use Helicone with LangChain/LangGraph
- **CrewAI**: Multi-agent CrewAI workflows
- **AutoGen**: Microsoft AutoGen v0.4+ integration
- **Vercel AI SDK**: Next.js streaming with Helicone

## Part 2: Advanced Features Examples

### Session Tracing (`session_tracing.py`)

Visualize multi-step agent workflows as hierarchical trees:

```python
# Parent agent
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Analyze patient symptoms"}],
    extra_headers={
        "Helicone-Session-Id": "session-001",
        "Helicone-Session-Path": "/triage",
    }
)

# Child agent
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Generate report"}],
    extra_headers={
        "Helicone-Session-Id": "session-001",
        "Helicone-Session-Path": "/triage/report",  # Hierarchical path
    }
)
```

### Caching (`caching_examples.py`)

Reduce costs by 20-30% with response caching:

```python
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "What is diabetes?"}],
    extra_headers={
        "Helicone-Cache-Enabled": "true",  # Enable caching
        "Cache-Control": "max-age=86400",   # Cache for 24 hours
    }
)
```

### Rate Limiting (`rate_limiting.py`)

Prevent cost overruns with flexible rate limiting:

```python
# Per-user cost limit: $5 per day
extra_headers={
    "Helicone-RateLimit-Policy": "500;w=86400;u=cents;s=user",
    "Helicone-User-Id": "user-123",
}

# Per-department request limit: 1000 requests per hour
extra_headers={
    "Helicone-RateLimit-Policy": "1000;w=3600;s=property",
    "Helicone-Property-Department": "cardiology",
}
```

## Part 3: Production Examples

### Multi-Agent AutoGen Workflow (`autogen_multi_agent.py`)

Complete healthcare AI system with:
- Triage agent
- Specialist agents (emergency, routine)
- Report generator
- Full session tracing across agents
- Per-agent cost attribution

**Expected Output:**
```
Session: /triage (total: 4,200ms, cost: $0.082)
├── /triage/intake (400ms, $0.008)
├── /triage/analysis (1,200ms, $0.045)
│   └── /triage/analysis/lab-review (600ms, $0.018)
└── /triage/report (800ms, $0.011)
```

### LLM Security (`security_integration.py`)

Protect against prompt injection with two-tier security:

```python
extra_headers={
    "Helicone-LLM-Security-Enabled": "true",  # Enable both guards
}

# If malicious input detected:
# Response: PROMPT_THREAT_DETECTED
# Details: "Indirect injection attempt detected"
```

### Self-Hosted Deployment (`docker-compose.yml`)

Deploy Helicone on your infrastructure:

```bash
docker-compose up -d

# Exposed ports:
# - 3000: Web UI (dashboard)
# - 8585: API + Proxy
# - 9080: Object storage (Minio)
```

## Configuration Guide

### AI Gateway (Recommended)

The AI Gateway provides unified routing to 100+ models with 1-5ms latency:

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://ai-gateway.helicone.ai",
    api_key=os.getenv("HELICONE_API_KEY"),  # Uses your Helicone key only
)
```

**Configure provider keys** in the Helicone dashboard under "Provider Keys".

### Provider-Specific Proxy

Use if you prefer to manage provider keys locally:

```python
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),  # Your provider key
    base_url="https://oai.helicone.ai/v1",
    default_headers={
        "Helicone-Auth": f"Bearer {os.getenv('HELICONE_API_KEY')}"
    }
)
```

### Async Logging (Zero Latency)

For latency-sensitive applications:

```python
from helicone_async import HeliconeAsyncLogger

logger = HeliconeAsyncLogger(api_key=os.getenv("HELICONE_API_KEY"))
logger.init()  # Patches OpenAI client

# Use client normally — logs ship asynchronously
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
```

## Common Headers Reference

| Header | Purpose | Example |
|--------|---------|---------|
| `Helicone-Auth` | Authentication (proxy mode) | `Bearer sk-helicone-xxx` |
| `Helicone-User-Id` | Track per-user analytics | `user-123` |
| `Helicone-Session-Id` | Group related requests | `session-abc` |
| `Helicone-Session-Path` | Hierarchical tracing | `/triage/analysis` |
| `Helicone-Property-*` | Custom metadata | `Helicone-Property-Department: cardiology` |
| `Helicone-Cache-Enabled` | Enable response caching | `true` |
| `Helicone-RateLimit-Policy` | Set rate limits | `1000;w=3600;s=user` |
| `Helicone-Prompt-Id` | Track prompt versions | `triage-classifier-v1` |
| `Helicone-LLM-Security-Enabled` | Enable security guards | `true` |

## Troubleshooting

### Authentication Errors

**Error**: `401 Unauthorized`

**Solution**: Check that your `HELICONE_API_KEY` is set correctly:

```bash
echo $HELICONE_API_KEY
# Should output: sk-helicone-xxxxxxxxxxxxx
```

### Provider Key Not Found (AI Gateway)

**Error**: `Provider key not configured`

**Solution**: Add your provider keys in the Helicone dashboard:
1. Go to https://helicone.ai/dashboard
2. Navigate to "Provider Keys"
3. Add your OpenAI, Anthropic, or other provider keys

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'openai'`

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

### Rate Limit Exceeded

**Error**: `429 Too Many Requests`

**Solution**: You've hit a rate limit policy. Check response headers:

```python
print(response.headers.get("Helicone-RateLimit-Remaining"))
# Shows remaining quota
```

## Additional Resources

- **Helicone Documentation**: https://docs.helicone.ai/
- **Dashboard**: https://helicone.ai/dashboard
- **Discord Community**: https://discord.gg/helicone
- **GitHub (Main Repo)**: https://github.com/Helicone/helicone
- **Blog Series**: https://zubairashfaque.github.io/

## Cost Estimates

All examples use `gpt-4o-mini` by default for cost efficiency:

- **Healthcare triage**: ~$0.004 per request
- **Multi-agent workflow**: ~$0.08 per complete session (4 agents)
- **Caching enabled**: Reduce costs by 20-30% for repeated queries

## License

MIT License - Feel free to use these examples in your own projects.

## Contributing

Found an issue or want to add an example? Open an issue or pull request!

## Author

**Zubair Ashfaque**
- Portfolio: https://zubairashfaque.github.io/
- GitHub: [@zubairashfaque](https://github.com/zubairashfaque)
