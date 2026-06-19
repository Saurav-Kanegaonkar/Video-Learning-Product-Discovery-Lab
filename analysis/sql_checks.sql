-- SQL checks mirror the generated CSV outputs in this public portfolio artifact.

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
