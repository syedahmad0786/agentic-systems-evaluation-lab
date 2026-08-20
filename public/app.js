const evaluationForm = document.querySelector("#evaluation-form");
const evaluationStatus = document.querySelector("#status");
const evaluationResult = document.querySelector("#result");

evaluationForm?.addEventListener("submit", async event => {
  event.preventDefault();
  const button = evaluationForm.querySelector("button");
  const values = new FormData(evaluationForm);
  button.disabled = true;
  evaluationStatus.textContent = "Running seven checks against the live deployment...";
  evaluationResult.hidden = true;

  try {
    const response = await fetch("/api/v1/evaluations/run", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        system: values.get("system"),
        scenario: values.get("scenario"),
      }),
    });
    if (!response.ok) throw new Error(`Evaluation failed (${response.status})`);

    const data = await response.json();
    document.querySelector("#score").textContent = data.score;
    document.querySelector("#grade").textContent = data.grade.replace("-", " ");
    document.querySelector("#checks").innerHTML = data.checks.map(check => `
      <div class="check">
        <strong class="${check.passed ? "pass" : "fail"}">${check.passed ? "✓" : "×"}</strong>
        <span>${check.name}</span>
        <strong>${check.earned}/${check.weight}</strong>
        <span class="evidence">${check.evidence}</span>
      </div>
    `).join("");
    evaluationResult.hidden = false;
    evaluationStatus.textContent = `Completed ${data.fault_injected ? "with an explicit simulated fault" : "against the live baseline"} at ${new Date(data.evaluated_at).toLocaleString()}.`;
    evaluationResult.scrollIntoView({ behavior: "smooth" });
  } catch (error) {
    evaluationStatus.textContent = error.message;
  } finally {
    button.disabled = false;
  }
});

const crewRun = document.querySelector("#crew-run");
const crewStatus = document.querySelector("#crew-status");
const crewAgents = [...document.querySelectorAll("[data-crew-step]")];
const traceRows = [...document.querySelectorAll("[data-trace-step]")];
const humanGate = document.querySelector("#human-gate");
const gateState = humanGate?.querySelector(".gate-state");
const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

const teachingTrace = [
  {
    active: "Evidence Scout is checking the supplied source packet.",
    complete: "Supported claims separated from inference and open questions.",
    trace: "Claim ledger ready",
  },
  {
    active: "Systems Mapper received the evidence ledger as task context.",
    complete: "Roles, handoffs, gate, action, and receipt mapped.",
    trace: "System map ready",
  },
  {
    active: "Field Note Editor is drafting two deliberately different channels.",
    complete: "Personal Field Note and AiXCEL adaptation drafted.",
    trace: "Draft pack ready",
  },
  {
    active: "Claims Gate is checking every factual sentence against the ledger.",
    complete: "Release packet prepared. No publishing action was taken.",
    trace: "Human review required",
  },
];

const wait = milliseconds => new Promise(resolve => window.setTimeout(resolve, milliseconds));

function resetTeachingTrace() {
  crewAgents.forEach(agent => agent.classList.remove("is-active", "is-complete"));
  traceRows.forEach((row, index) => {
    row.classList.remove("is-active", "is-complete");
    row.querySelector("em").textContent = index === 0 ? "Queued" : "Waiting for context";
  });
  humanGate?.classList.remove("is-waiting");
  if (gateState) gateState.textContent = "LOCKED";
}

crewRun?.addEventListener("click", async () => {
  resetTeachingTrace();
  crewRun.disabled = true;
  crewRun.setAttribute("aria-busy", "true");
  crewRun.querySelector("span:first-child").textContent = "Trace running";
  const stepDelay = reduceMotion ? 80 : 720;

  for (let index = 0; index < crewAgents.length; index += 1) {
    const agent = crewAgents[index];
    const row = traceRows[index];
    const event = teachingTrace[index];
    agent.classList.add("is-active");
    row.classList.add("is-active");
    row.querySelector("em").textContent = "Running";
    crewStatus.textContent = event.active;
    await wait(stepDelay);
    agent.classList.remove("is-active");
    agent.classList.add("is-complete");
    row.classList.remove("is-active");
    row.classList.add("is-complete");
    row.querySelector("em").textContent = event.trace;
    crewStatus.textContent = event.complete;
    await wait(reduceMotion ? 40 : 240);
  }

  humanGate?.classList.add("is-waiting");
  if (gateState) gateState.textContent = "DECISION REQUIRED";
  crewStatus.textContent = "Crew stopped at the human gate. Ahmad decides whether anything is published.";
  crewRun.disabled = false;
  crewRun.removeAttribute("aria-busy");
  crewRun.querySelector("span:first-child").textContent = "Replay teaching trace";
});
