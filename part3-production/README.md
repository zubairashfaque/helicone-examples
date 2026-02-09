# Part 3: Production Best Practices

Complete production-ready examples for deploying LLM applications with Helicone.

## Files Overview

### 1. `autogen_multi_agent.py` (142 lines)
Complete healthcare AI system demonstrating:
- **Multi-agent workflow:** Triage → Emergency/Routine Specialist → Report Generator
- **Conditional routing:** Emergency cases use GPT-4o, routine use GPT-4o-mini
- **Hierarchical session paths:** `/triage`, `/triage/emergency-specialist`, `/triage/report`
- **Per-agent cost attribution:** Track which agent consumes budget
- **Department tagging:** Segment by emergency-dept, primary-care, medical-records

**Run:**
```bash
python autogen_multi_agent.py
```

### 2. `security_integration.py` (74 lines)
Two-tier LLM security protection:
- **Meta Llama Guard:** 14-category threat detection (hate, violence, criminal planning, etc.)
- **Meta Prompt Guard:** Prompt injection and jailbreak detection
- **Examples:** Safe requests, prompt injection attempts, harmful content requests
- **Dashboard integration:** View flagged requests, track per-user threat patterns

**Run:**
```bash
python security_integration.py
```

### 3. `posthog_integration.py` (44 lines)
Combine LLM observability with product analytics:
- **Dual tracking:** Helicone (LLM metrics) + PostHog (user behavior)
- **Correlate data:** Link LLM costs with feature adoption, retention, funnels
- **Event tracking:** Log custom events like `llm_report_generated`

**Setup:**
Add PostHog API key to `.env`:
```
POSTHOG_API_KEY=phc_...
```

**Run:**
```bash
python posthog_integration.py
```

### 4. `docker-compose.yml` (77 lines)
Self-hosted Helicone deployment:
- **PostgreSQL:** User data, configuration, sessions
- **ClickHouse:** Analytics database for request logs
- **Helicone API:** Backend service
- **Helicone Web:** Dashboard interface

**Deploy:**
```bash
# Create .env file with passwords
cat > .env << EOF
POSTGRES_PASSWORD=your_postgres_password
CLICKHOUSE_PASSWORD=your_clickhouse_password
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
JWT_SECRET=your_jwt_secret
EOF

# Start the stack
docker-compose up -d

# Access dashboard
open http://localhost:3000

# Point your app to self-hosted gateway
# base_url="http://localhost:8080"
```

### 5. `cost_optimization.py` (87 lines)
Five proven cost reduction strategies:
1. **Aggressive caching:** 30-50% savings for common queries
2. **Model routing:** Use GPT-4o-mini first (10x cheaper than GPT-4o)
3. **Cost-based rate limiting:** Enforce $5/day budgets per user
4. **Prompt optimization:** Reduce input tokens by 80%
5. **Batch processing:** 20-30% savings for bulk operations

**Example savings:**
- Baseline: $1,200/month
- Optimized: $450/month
- **Total savings: $750/month (62.5% reduction)**

**Run:**
```bash
python cost_optimization.py
```

### 6. `production_checklist.py` (74 lines)
Production-ready template with all features enabled:
- ✅ Session tracing
- ✅ Caching (1-hour TTL)
- ✅ Rate limiting (100 req/hour per user)
- ✅ Security scanning (Llama Guard + Prompt Guard)
- ✅ Retry + fallback (GPT-4o → Claude)
- ✅ Prompt versioning
- ✅ Custom properties
- ✅ PostHog integration

**Run:**
```bash
python production_checklist.py
```

## Key Concepts

### Production Readiness Checklist
- [ ] Enable LLM security headers (Llama Guard + Prompt Guard)
- [ ] Configure alerting thresholds
- [ ] Set up PostHog integration (optional)
- [ ] Deploy self-hosted instance (for compliance/data residency)
- [ ] Implement structured custom properties
- [ ] Establish per-user cost budgets
- [ ] Enable session tracing for all agents
- [ ] Configure caching for deterministic prompts
- [ ] Set up retry + fallback for critical paths
- [ ] Plan data retention and compliance (GDPR/HIPAA/SOC2)

### When to Self-Host
**Consider self-hosting if:**
- HIPAA/GDPR compliance requires data residency
- You handle >1M requests/month (cost-effective at scale)
- Network latency to cloud is problematic
- You need custom retention policies

**Use cloud if:**
- Just getting started (<100K requests/month)
- Don't have DevOps resources for infrastructure
- Want automatic updates and zero maintenance

## Cost Optimization Summary

| Strategy | Savings | Difficulty |
|----------|---------|------------|
| Aggressive caching | 30-50% | Easy |
| Model routing (mini first) | 40-60% | Easy |
| Cost-based rate limiting | 20-30% | Easy |
| Prompt optimization | 15-25% | Medium |
| Batch processing | 20-30% | Medium |

**Combined:** 62.5% cost reduction achievable with all strategies.

## Security Categories (Llama Guard)

1. Violence and Hate
2. Sexual Content
3. Criminal Planning
4. Guns and Illegal Weapons
5. Regulated or Controlled Substances
6. Self-Harm
7. Jailbreaking and Prompt Injection
8. Privacy Violations
9. Intellectual Property
10. Indiscriminate Weapons
11. Hate Speech
12. Terrorism
13. Sexual Crimes
14. Child Safety

## Next Steps

1. **Test locally:** Run all examples with your Helicone API key
2. **Review dashboard:** Check session trees, security flags, cost analytics
3. **Deploy to staging:** Test with real traffic patterns
4. **Set up monitoring:** Configure alerts for errors, cost spikes, security threats
5. **Go to production:** Enable all features for your production application

## Resources

- **Helicone Docs:** https://docs.helicone.ai
- **GitHub Issues:** https://github.com/Helicone/helicone/issues
- **Discord Community:** https://discord.gg/helicone
- **Blog Series:** Part 1 (Getting Started) → Part 2 (Features) → Part 3 (Production)
