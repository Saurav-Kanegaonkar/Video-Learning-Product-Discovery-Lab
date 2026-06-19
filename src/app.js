const state = {
  payload: null,
  view: "cockpit",
  selectedOpportunityId: null,
};

const view = document.querySelector("#view");

const fmt = new Intl.NumberFormat("en-US", {
  maximumFractionDigits: 1,
});

function esc(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function metric(label, value, note) {
  return `
    <article class="metric-card">
      <span>${esc(label)}</span>
      <strong>${esc(value)}</strong>
      <small>${esc(note)}</small>
    </article>
  `;
}

function selectedOpportunity() {
  return state.payload.opportunities.find((row) => row.opportunity_id === state.selectedOpportunityId) || state.payload.opportunities[0];
}

function selectedPrd() {
  const selected = selectedOpportunity();
  return state.payload.prd.find((row) => row.opportunity_id === selected.opportunity_id);
}

function selectedLaunch() {
  const selected = selectedOpportunity();
  return state.payload.launch.find((row) => row.opportunity_id === selected.opportunity_id);
}

function evidenceForSelected() {
  const selected = selectedOpportunity();
  return state.payload.evidence.filter((row) => row.opportunity_id === selected.opportunity_id);
}

function renderMetricStrip() {
  const summary = state.payload.summary;
  document.querySelector("#recommendedMove").textContent = summary.recommended_move;
  document.querySelector("#metricStrip").innerHTML = [
    metric("Top score", fmt.format(summary.top_score), summary.top_opportunity),
    metric("Commit-ready", summary.now_count, "roadmap candidates"),
    metric("Evidence", summary.evidence_signals, "tagged discovery signals"),
    metric("Instrumentation", `${fmt.format(summary.average_instrumentation)}%`, "latest average coverage"),
  ].join("");
}

function renderOpportunityRow(row, index) {
  const selected = row.opportunity_id === selectedOpportunity().opportunity_id ? " selected" : "";
  return `
    <button class="opportunity-row${selected}" type="button" data-opportunity="${esc(row.opportunity_id)}">
      <span class="rank">${index + 1}</span>
      <span>
        <strong>${esc(row.workflow)}</strong>
        <small>${esc(row.persona)} · ${esc(row.product_area)}</small>
      </span>
      <span class="score">${esc(row.priority_score)}</span>
      <span class="pill ${row.decision === "Commit to PRD" ? "good" : ""}">${esc(row.decision)}</span>
    </button>
  `;
}

function renderCockpit() {
  const selected = selectedOpportunity();
  const launch = selectedLaunch();
  view.innerHTML = `
    <div class="surface-grid cockpit-grid">
      <section class="panel queue-panel">
        <div class="section-heading">
          <p class="eyebrow">Roadmap queue</p>
          <h2>Opportunity Cockpit</h2>
        </div>
        <div class="opportunity-list">
          ${state.payload.opportunities.map(renderOpportunityRow).join("")}
        </div>
      </section>
      <section class="panel detail-panel">
        <div class="section-heading">
          <p class="eyebrow">${esc(selected.roadmap_window)} · ${esc(selected.product_area)}</p>
          <h2>${esc(selected.workflow)}</h2>
        </div>
        <p class="problem">${esc(selected.problem)}</p>
        <div class="score-grid">
          ${metric("User pain", selected.user_pain, "discovery severity")}
          ${metric("Adoption reach", selected.adoption_reach, "affected accounts")}
          ${metric("Learning value", selected.learning_value, "outcome alignment")}
          ${metric("Delivery risk", selected.engineering_effort + selected.data_risk, "effort plus data risk")}
        </div>
        <div class="strategy-note">
          <strong>Candidate solution</strong>
          <p>${esc(selected.candidate_solution)}</p>
        </div>
        <div class="strategy-note">
          <strong>Release gate</strong>
          <p>${esc(launch.release_gate)} · ${esc(launch.top_launch_risk)}</p>
        </div>
      </section>
    </div>
  `;
}

function renderEvidence() {
  const selected = selectedOpportunity();
  const evidence = evidenceForSelected();
  view.innerHTML = `
    <div class="surface-grid evidence-grid">
      <section class="panel">
        <div class="section-heading">
          <p class="eyebrow">Discovery synthesis</p>
          <h2>Evidence Board</h2>
        </div>
        <p class="problem">${esc(selected.workflow)} is backed by ${evidence.length} synthetic signals across research, CS, telemetry, sales, design, and engineering.</p>
        <div class="signal-board">
          ${evidence.map((row) => `
            <article class="signal-card">
              <div>
                <span class="pill">${esc(row.signal_type)}</span>
                <strong>${esc(row.source)}</strong>
              </div>
              <p>${esc(row.insight)}</p>
              <div class="signal-meta">
                <span>Severity ${esc(row.severity)}/5</span>
                <span>${esc(row.frequency)} mentions</span>
                <span>${esc(row.confidence)}% confidence</span>
              </div>
            </article>
          `).join("")}
        </div>
      </section>
      <section class="panel">
        <div class="section-heading">
          <p class="eyebrow">Decision lens</p>
          <h2>What Changes The Roadmap</h2>
        </div>
        <table>
          <thead>
            <tr><th>Signal</th><th>PM Interpretation</th></tr>
          </thead>
          <tbody>
            <tr><td>User pain</td><td>${esc(selected.user_pain)}/10 means the workflow deserves problem validation before solution polish.</td></tr>
            <tr><td>Customer-success friction</td><td>${esc(selected.cs_friction)}/10 keeps enablement and support deflection in scope.</td></tr>
            <tr><td>Evidence score</td><td>${esc(selected.evidence_score)} makes this a defendable candidate, not a loud one-off request.</td></tr>
            <tr><td>Confidence</td><td>${esc(selected.confidence)}% supports PRD review while keeping assumptions visible.</td></tr>
          </tbody>
        </table>
      </section>
    </div>
  `;
}

function renderPrd() {
  const selected = selectedOpportunity();
  const prd = selectedPrd();
  view.innerHTML = `
    <div class="surface-grid prd-grid">
      <section class="panel prd-panel">
        <div class="section-heading">
          <p class="eyebrow">${esc(prd.agile_handoff)}</p>
          <h2>PRD Handoff Builder</h2>
        </div>
        <div class="brief-stack">
          <article>
            <span>Problem statement</span>
            <p>${esc(prd.problem_statement)}</p>
          </article>
          <article>
            <span>Job to be done</span>
            <p>${esc(prd.job_to_be_done)}</p>
          </article>
          <article>
            <span>User story</span>
            <p>${esc(prd.user_story)}</p>
          </article>
          <article>
            <span>Acceptance criteria</span>
            <p>${esc(prd.acceptance_criteria)}</p>
          </article>
        </div>
      </section>
      <section class="panel">
        <div class="section-heading">
          <p class="eyebrow">Measurement contract</p>
          <h2>Launch Metrics</h2>
        </div>
        <div class="metric-list">
          <div><span>Primary metric</span><strong>${esc(prd.launch_metric)}</strong></div>
          <div><span>Guardrail</span><strong>${esc(prd.guardrail_metric)}</strong></div>
          <div><span>Instrumentation event</span><strong>${esc(prd.analytics_event)}</strong></div>
          <div><span>Non-goal</span><strong>${esc(prd.non_goal)}</strong></div>
        </div>
      </section>
    </div>
  `;
}

function readinessBar(label, value) {
  return `
    <div class="bar-row">
      <div><span>${esc(label)}</span><strong>${esc(value)}%</strong></div>
      <div class="bar"><span style="width:${Math.max(0, Math.min(100, value))}%"></span></div>
    </div>
  `;
}

function renderLaunch() {
  const selected = selectedOpportunity();
  const launch = selectedLaunch();
  const weekly = state.payload.weeklyMetrics.filter((row) => row.opportunity_id === selected.opportunity_id).slice(-4);
  view.innerHTML = `
    <div class="surface-grid launch-grid">
      <section class="panel">
        <div class="section-heading">
          <p class="eyebrow">Readiness review</p>
          <h2>Launch Gate</h2>
        </div>
        <div class="readiness">
          ${readinessBar("Metric readiness", launch.metric_readiness)}
          ${readinessBar("QA readiness", launch.qa_readiness)}
          ${readinessBar("GTM readiness", launch.gtm_readiness)}
          ${readinessBar("CS readiness", launch.cs_readiness)}
        </div>
        <div class="strategy-note">
          <strong>${esc(launch.release_gate)}</strong>
          <p>Top risk: ${esc(launch.top_launch_risk)}. Keep this visible during roadmap tradeoff and sprint planning.</p>
        </div>
      </section>
      <section class="panel">
        <div class="section-heading">
          <p class="eyebrow">Recent telemetry</p>
          <h2>Metric Trend Packet</h2>
        </div>
        <table>
          <thead>
            <tr>
              <th>Week</th>
              <th>Activation</th>
              <th>Repeat use</th>
              <th>CS contacts</th>
              <th>Coverage</th>
            </tr>
          </thead>
          <tbody>
            ${weekly.map((row) => `
              <tr>
                <td>${esc(row.week)}</td>
                <td>${esc(row.activation_rate)}%</td>
                <td>${esc(row.repeat_usage_rate)}%</td>
                <td>${esc(row.support_contacts_per_100_accounts)}</td>
                <td>${esc(row.instrumentation_coverage)}%</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </section>
    </div>
  `;
}

function render() {
  if (!state.payload) return;
  renderMetricStrip();
  document.querySelectorAll(".tab").forEach((button) => {
    button.classList.toggle("active", button.dataset.view === state.view);
  });
  if (state.view === "evidence") renderEvidence();
  else if (state.view === "prd") renderPrd();
  else if (state.view === "launch") renderLaunch();
  else renderCockpit();
  bindOpportunityRows();
}

function bindOpportunityRows() {
  document.querySelectorAll("[data-opportunity]").forEach((button) => {
    button.addEventListener("click", () => {
      state.selectedOpportunityId = button.dataset.opportunity;
      render();
    });
  });
}

document.querySelectorAll(".tab").forEach((button) => {
  button.addEventListener("click", () => {
    state.view = button.dataset.view;
    render();
  });
});

fetch("analysis/outputs/app_payload.json")
  .then((response) => response.json())
  .then((payload) => {
    state.payload = payload;
    state.selectedOpportunityId = payload.opportunities[0].opportunity_id;
    render();
  })
  .catch(() => {
    view.innerHTML = `<section class="panel"><h2>Unable to load analysis payload</h2><p>Run <code>python3 scripts/score_operating_data.py</code> and restart the local server.</p></section>`;
  });
