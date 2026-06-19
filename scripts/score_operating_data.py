import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUTPUTS = ROOT / "analysis" / "outputs"


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def pct(value):
    return round(value, 1)


opportunities = [
    {
        "opportunity_id": "OPP-101",
        "workflow": "AI-assisted interactive question authoring",
        "persona": "Instructional designer",
        "product_area": "Interactive video",
        "problem": "Designers lose time turning existing lecture videos into aligned checks for understanding.",
        "candidate_solution": "Generate draft questions by Bloom level, then require instructor review before publish.",
        "user_pain": 9,
        "adoption_reach": 8,
        "learning_value": 9,
        "sales_pull": 7,
        "cs_friction": 8,
        "engineering_effort": 5,
        "data_risk": 4,
        "confidence": 86,
        "roadmap_window": "Now",
        "primary_metric": "interactive_lesson_publish_rate",
        "guardrail_metric": "question_edit_rate_after_ai_suggestion",
    },
    {
        "opportunity_id": "OPP-102",
        "workflow": "LMS gradebook and assignment sync repair",
        "persona": "District technology admin",
        "product_area": "Integrations",
        "problem": "Admins need fewer manual checks when assignments, rosters, and scores move through the LMS.",
        "candidate_solution": "Add an integration health center with sync status, retry reason, and owner handoff.",
        "user_pain": 8,
        "adoption_reach": 9,
        "learning_value": 7,
        "sales_pull": 8,
        "cs_friction": 9,
        "engineering_effort": 7,
        "data_risk": 6,
        "confidence": 82,
        "roadmap_window": "Next",
        "primary_metric": "successful_lms_sync_rate",
        "guardrail_metric": "manual_roster_correction_rate",
    },
    {
        "opportunity_id": "OPP-103",
        "workflow": "Collaborative student project feedback loop",
        "persona": "K-12 teacher",
        "product_area": "Video creation",
        "problem": "Teachers struggle to monitor group contribution and give feedback before final submission.",
        "candidate_solution": "Create a live collaboration checkpoint with comments, contribution cues, and revision status.",
        "user_pain": 8,
        "adoption_reach": 7,
        "learning_value": 9,
        "sales_pull": 6,
        "cs_friction": 6,
        "engineering_effort": 6,
        "data_risk": 5,
        "confidence": 78,
        "roadmap_window": "Now",
        "primary_metric": "collaborative_project_completion_rate",
        "guardrail_metric": "teacher_review_minutes_per_project",
    },
    {
        "opportunity_id": "OPP-104",
        "workflow": "Learner analytics remediation queue",
        "persona": "Faculty member",
        "product_area": "Analytics",
        "problem": "Instructors can see engagement data but still need help deciding who needs remediation.",
        "candidate_solution": "Rank learners by missed interactions, rewatch gaps, and late completion, with suggested follow-up.",
        "user_pain": 7,
        "adoption_reach": 8,
        "learning_value": 8,
        "sales_pull": 6,
        "cs_friction": 5,
        "engineering_effort": 5,
        "data_risk": 7,
        "confidence": 74,
        "roadmap_window": "Next",
        "primary_metric": "remediation_action_rate",
        "guardrail_metric": "false_positive_remediation_rate",
    },
    {
        "opportunity_id": "OPP-105",
        "workflow": "Accessible captions and transcript QA",
        "persona": "Accessibility coordinator",
        "product_area": "AI Assist",
        "problem": "Teams need faster caption workflows without losing trust in accessibility quality.",
        "candidate_solution": "Add transcript confidence flags, human review states, and export readiness checks.",
        "user_pain": 7,
        "adoption_reach": 7,
        "learning_value": 8,
        "sales_pull": 7,
        "cs_friction": 7,
        "engineering_effort": 4,
        "data_risk": 5,
        "confidence": 80,
        "roadmap_window": "Now",
        "primary_metric": "caption_ready_publish_rate",
        "guardrail_metric": "caption_correction_rate",
    },
    {
        "opportunity_id": "OPP-106",
        "workflow": "Course template reuse and content library governance",
        "persona": "Higher ed program lead",
        "product_area": "Content library",
        "problem": "Program teams want reusable interactive course assets but need ownership, freshness, and usage clarity.",
        "candidate_solution": "Create template library governance with owner, freshness, usage, and update prompts.",
        "user_pain": 6,
        "adoption_reach": 7,
        "learning_value": 7,
        "sales_pull": 5,
        "cs_friction": 5,
        "engineering_effort": 4,
        "data_risk": 4,
        "confidence": 72,
        "roadmap_window": "Later",
        "primary_metric": "template_reuse_rate",
        "guardrail_metric": "stale_template_share",
    },
    {
        "opportunity_id": "OPP-107",
        "workflow": "Live audience response session recovery",
        "persona": "Corporate trainer",
        "product_area": "Audience response",
        "problem": "Facilitators need confidence that live responses are captured and recoverable during sessions.",
        "candidate_solution": "Expose session health, response capture confirmation, and recovery steps during live delivery.",
        "user_pain": 7,
        "adoption_reach": 6,
        "learning_value": 7,
        "sales_pull": 6,
        "cs_friction": 8,
        "engineering_effort": 6,
        "data_risk": 6,
        "confidence": 69,
        "roadmap_window": "Later",
        "primary_metric": "live_response_capture_rate",
        "guardrail_metric": "session_recovery_ticket_rate",
    },
]

signal_templates = [
    ("Interview", "User research", "Users asked for a clearer workflow before adding another creation tool.", 5),
    ("Support ticket", "Customer Success", "Support volume spikes when setup steps and LMS states are unclear.", 4),
    ("Product telemetry", "Product analytics", "Activation improves when the workflow moves from draft to publish in one sitting.", 4),
    ("Sales note", "Sales", "Buyers ask how the platform proves learning impact and reduces instructor workload.", 3),
    ("Usability test", "Design", "Participants understand the value but hesitate when ownership or next step is hidden.", 5),
    ("Release review", "Engineering", "The team needs clearer acceptance criteria before committing scope.", 3),
]

evidence_rows = []
for opp in opportunities:
    for idx, (signal_type, source, note, base_severity) in enumerate(signal_templates, start=1):
        severity = min(5, max(1, base_severity + ((opp["user_pain"] + idx) % 3) - 1))
        frequency = 18 + opp["adoption_reach"] * 7 + idx * 5 + (opp["cs_friction"] if signal_type == "Support ticket" else 0)
        confidence = min(95, opp["confidence"] - idx + severity * 2)
        evidence_rows.append(
            {
                "signal_id": f"SIG-{opp['opportunity_id'][-3:]}-{idx:02d}",
                "opportunity_id": opp["opportunity_id"],
                "signal_type": signal_type,
                "source": source,
                "persona": opp["persona"],
                "workflow": opp["workflow"],
                "severity": severity,
                "frequency": frequency,
                "confidence": confidence,
                "insight": note,
                "pm_decision": "prioritize" if opp["roadmap_window"] == "Now" else "sequence",
            }
        )

weekly_rows = []
for opp in opportunities:
    for week in range(1, 9):
        base = opp["adoption_reach"] * 5 + week * 2
        weekly_rows.append(
            {
                "week": f"2026-W{week:02d}",
                "opportunity_id": opp["opportunity_id"],
                "activation_rate": pct(38 + base * 0.45 - opp["engineering_effort"] * 0.4),
                "repeat_usage_rate": pct(29 + base * 0.36 + opp["learning_value"] * 0.8),
                "support_contacts_per_100_accounts": pct(18 - week * 0.4 + opp["cs_friction"] * 0.9),
                "creator_minutes_to_publish": pct(42 - week * 0.8 + opp["engineering_effort"] * 1.2),
                "learner_completion_rate": pct(54 + opp["learning_value"] * 2.5 + week * 0.7),
                "instrumentation_coverage": pct(64 + week * 2.8 - opp["data_risk"] * 1.3),
            }
        )

prd_rows = []
for opp in opportunities:
    prd_rows.append(
        {
            "prd_id": f"PRD-{opp['opportunity_id'][-3:]}",
            "opportunity_id": opp["opportunity_id"],
            "problem_statement": opp["problem"],
            "job_to_be_done": f"When using {opp['workflow'].lower()}, a {opp['persona'].lower()} needs a reliable next step so they can improve learning outcomes without adding manual coordination.",
            "non_goal": "Do not create bespoke behavior for one institution until repeated signal appears across segments.",
            "user_story": f"As a {opp['persona'].lower()}, I can use {opp['candidate_solution'].lower()}",
            "acceptance_criteria": "Workflow state, owner, success event, error state, and customer-facing explanation are visible before launch.",
            "analytics_event": opp["primary_metric"],
            "launch_metric": opp["primary_metric"],
            "guardrail_metric": opp["guardrail_metric"],
            "agile_handoff": "Ready for refinement" if opp["roadmap_window"] == "Now" else "Discovery follow-up",
        }
    )

launch_rows = []
for opp in opportunities:
    metric_readiness = 100 - opp["data_risk"] * 7 + opp["confidence"] * 0.2
    qa_readiness = 100 - opp["engineering_effort"] * 8 + opp["confidence"] * 0.15
    gtm_readiness = 44 + opp["sales_pull"] * 5 + (8 if opp["roadmap_window"] == "Now" else 0)
    cs_readiness = 48 + opp["cs_friction"] * 4 + (6 if opp["roadmap_window"] != "Later" else 0)
    launch_rows.append(
        {
            "opportunity_id": opp["opportunity_id"],
            "metric_readiness": round(metric_readiness, 1),
            "qa_readiness": round(qa_readiness, 1),
            "gtm_readiness": round(gtm_readiness, 1),
            "cs_readiness": round(cs_readiness, 1),
            "top_launch_risk": "Instrumentation gap" if opp["data_risk"] >= 6 else "Scope creep" if opp["engineering_effort"] >= 6 else "Enablement clarity",
            "release_gate": "Ready for PRD review" if min(metric_readiness, qa_readiness, gtm_readiness, cs_readiness) >= 60 else "Needs risk burn-down",
        }
    )

scored_opportunities = []
for opp in opportunities:
    evidence = [row for row in evidence_rows if row["opportunity_id"] == opp["opportunity_id"]]
    evidence_score = sum(row["severity"] * row["frequency"] * row["confidence"] / 100 for row in evidence) / 100
    impact = opp["user_pain"] * 1.35 + opp["adoption_reach"] * 1.2 + opp["learning_value"] * 1.25 + opp["sales_pull"] * 0.7 + opp["cs_friction"] * 0.8
    drag = opp["engineering_effort"] * 1.15 + opp["data_risk"] * 0.85
    priority_score = round(impact + evidence_score - drag, 1)
    scored = dict(opp)
    scored["evidence_score"] = round(evidence_score, 1)
    scored["priority_score"] = priority_score
    scored["decision"] = "Commit to PRD" if priority_score >= 35 and opp["roadmap_window"] == "Now" else "Continue discovery" if priority_score >= 28 else "Monitor"
    scored_opportunities.append(scored)

scored_opportunities.sort(key=lambda row: row["priority_score"], reverse=True)
top = scored_opportunities[0]
now_count = sum(1 for row in scored_opportunities if row["roadmap_window"] == "Now")
average_instrumentation = round(sum(row["instrumentation_coverage"] for row in weekly_rows[-len(opportunities):]) / len(opportunities), 1)
avg_cs_contacts = round(sum(row["support_contacts_per_100_accounts"] for row in weekly_rows[-len(opportunities):]) / len(opportunities), 1)

payload = {
    "summary": {
        "top_opportunity": top["workflow"],
        "top_persona": top["persona"],
        "top_score": top["priority_score"],
        "now_count": now_count,
        "evidence_signals": len(evidence_rows),
        "average_instrumentation": average_instrumentation,
        "avg_cs_contacts": avg_cs_contacts,
        "recommended_move": "Move the highest-confidence AI-assisted authoring workflow into PRD review while burning down LMS sync and data-risk dependencies.",
        "data_note": "Deterministic synthetic data modeled on interactive video learning SaaS discovery, adoption, support, sales, and launch-readiness workflows.",
    },
    "opportunities": scored_opportunities,
    "evidence": evidence_rows,
    "prd": prd_rows,
    "launch": launch_rows,
    "weeklyMetrics": weekly_rows,
}

write_csv(DATA / "opportunity_backlog.csv", scored_opportunities)
write_csv(DATA / "discovery_signals.csv", evidence_rows)
write_csv(DATA / "weekly_product_metrics.csv", weekly_rows)
write_csv(DATA / "prd_handoff.csv", prd_rows)
write_csv(DATA / "launch_readiness.csv", launch_rows)

OUTPUTS.mkdir(parents=True, exist_ok=True)
write_csv(OUTPUTS / "opportunity_priority_queue.csv", scored_opportunities)
write_csv(OUTPUTS / "evidence_signal_matrix.csv", evidence_rows)
write_csv(OUTPUTS / "prd_story_map.csv", prd_rows)
write_csv(OUTPUTS / "launch_readiness_queue.csv", launch_rows)

with (OUTPUTS / "app_payload.json").open("w") as f:
    json.dump(payload, f, indent=2)

with (OUTPUTS / "summary.json").open("w") as f:
    json.dump(payload["summary"], f, indent=2)

(ROOT / "analysis" / "analysis_plan.md").write_text(
    """# Analysis Plan

1. Generate deterministic synthetic product-discovery data for an interactive video learning SaaS environment.
2. Score each opportunity using user pain, adoption reach, learning value, sales pull, customer-success friction, engineering effort, data risk, and evidence strength.
3. Convert the top opportunities into PRD-ready problem statements, user stories, acceptance criteria, metrics, guardrails, and Agile handoff states.
4. Validate launch readiness across metric coverage, QA, GTM, and customer-success enablement before recommending a roadmap move.
""",
)

(ROOT / "analysis" / "executive_findings.md").write_text(
    f"""# Executive Findings

- Top recommendation: {top['workflow']} for {top['persona'].lower()}.
- Why it matters: it combines high user pain, high learning value, strong evidence, and manageable implementation risk.
- Near-term roadmap should include {now_count} commit-ready workflows, with dependency work kept visible for integration and instrumentation risks.
- Launch success should be judged by product behavior and customer-success friction together, not by feature shipment alone.
""",
)

(ROOT / "analysis" / "methodology.md").write_text(
    """# Methodology

The artifact uses deterministic synthetic data because real customer interviews, learner analytics, support tickets, sales notes, and LMS integration logs are private.

The generator models common structures in interactive video learning SaaS work: educator interviews, instructional designer workflows, LMS administration, AI-assisted authoring, caption accessibility, customer-success friction, sales objections, telemetry, PRD handoff, and launch-readiness checks.

Opportunity priority score combines positive demand and outcome signals, then subtracts delivery and data risk. Evidence score is derived from signal severity, frequency, and confidence. The score is directional, not a production prioritization formula.
""",
)

(DATA / "README.md").write_text(
    """# Data Sources

All datasets are deterministic synthetic data for a public portfolio artifact. They do not represent real customers, students, teachers, districts, institutions, accounts, support tickets, interviews, product events, revenue, or company performance.

The synthetic structure is modeled on common interactive video learning SaaS workflows:

- Educator and instructional-designer discovery interviews.
- Customer-success tickets and onboarding friction.
- Product telemetry for activation, repeat usage, collaboration, and publishing.
- Sales and buyer feedback around learning impact, integrations, and workflow clarity.
- PRD handoff artifacts for Agile engineering teams.
- Launch-readiness checks for metrics, QA, go-to-market, and customer success.

The generator uses fixed inputs in `scripts/score_operating_data.py`, so the artifact can be rebuilt and explained consistently.
""",
)

(ROOT / "data_dictionary.md").write_text(
    """# Data Dictionary

| Dataset | Grain | Key Fields |
|---|---|---|
| `data/opportunity_backlog.csv` | One row per product opportunity | `opportunity_id`, `workflow`, `persona`, `priority_score`, `decision` |
| `data/discovery_signals.csv` | One discovery signal per opportunity and source | `signal_type`, `severity`, `frequency`, `confidence`, `insight` |
| `data/weekly_product_metrics.csv` | One opportunity per week | `activation_rate`, `repeat_usage_rate`, `support_contacts_per_100_accounts`, `instrumentation_coverage` |
| `data/prd_handoff.csv` | One PRD packet per opportunity | `problem_statement`, `job_to_be_done`, `user_story`, `acceptance_criteria`, `launch_metric` |
| `data/launch_readiness.csv` | One launch-readiness row per opportunity | `metric_readiness`, `qa_readiness`, `gtm_readiness`, `cs_readiness`, `release_gate` |
""",
)

(ROOT / "analysis" / "sql_checks.sql").write_text(
    """-- SQL checks mirror the generated CSV outputs in this public portfolio artifact.

-- 1. Commit-ready opportunities should have a launch metric and guardrail metric.
select opportunity_id, workflow
from opportunity_backlog
where decision = 'Commit to PRD'
  and (primary_metric is null or guardrail_metric is null);

-- 2. PRD handoff rows should map one-to-one to opportunities.
select opportunity_id, count(*) as prd_rows
from prd_handoff
group by opportunity_id
having count(*) <> 1;

-- 3. Launch-ready rows should not pass if instrumentation is below threshold.
select opportunity_id, release_gate, metric_readiness
from launch_readiness
where release_gate = 'Ready for PRD review'
  and metric_readiness < 60;
""",
)

print(f"Generated {len(scored_opportunities)} opportunities, {len(evidence_rows)} evidence signals, and {len(weekly_rows)} weekly metric rows.")
print(f"Top opportunity: {top['workflow']} with score {top['priority_score']}.")
