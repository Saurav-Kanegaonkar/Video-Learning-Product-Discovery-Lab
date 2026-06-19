# Data Dictionary

| Dataset | Grain | Key Fields |
|---|---|---|
| `data/opportunity_backlog.csv` | One row per product opportunity | `opportunity_id`, `workflow`, `persona`, `priority_score`, `decision` |
| `data/discovery_signals.csv` | One discovery signal per opportunity and source | `signal_type`, `severity`, `frequency`, `confidence`, `insight` |
| `data/weekly_product_metrics.csv` | One opportunity per week | `activation_rate`, `repeat_usage_rate`, `support_contacts_per_100_accounts`, `instrumentation_coverage` |
| `data/prd_handoff.csv` | One PRD packet per opportunity | `problem_statement`, `job_to_be_done`, `user_story`, `acceptance_criteria`, `launch_metric` |
| `data/launch_readiness.csv` | One launch-readiness row per opportunity | `metric_readiness`, `qa_readiness`, `gtm_readiness`, `cs_readiness`, `release_gate` |
