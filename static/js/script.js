const form = document.getElementById("recruitmentForm");
const steps = [...document.querySelectorAll(".step")];
const progressBar = document.getElementById("progressBar");
const stepLabel = document.getElementById("stepLabel");
const reviewCard = document.getElementById("reviewCard");
const successScreen = document.getElementById("successScreen");

let current = 1;

function showStep(number) {
  current = number;
  steps.forEach(step => step.classList.toggle("active", +step.dataset.step === number));
  progressBar.style.width = `${number * 25}%`;
  stepLabel.textContent = `STEP 0${number}`;

  if (number === 4) buildReview();
  window.scrollTo({top: 0, behavior: "smooth"});
}

function validateStep(number) {
  const step = document.querySelector(`.step[data-step="${number}"]`);
  const inputs = [...step.querySelectorAll("input, select, textarea")];
  for (const input of inputs) {
    if (!input.checkValidity()) {
      input.reportValidity();
      return false;
    }
  }
  return true;
}

document.querySelectorAll(".next-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    if (validateStep(current)) showStep(current + 1);
  });
});

document.querySelectorAll(".back-btn").forEach(btn => {
  btn.addEventListener("click", () => showStep(current - 1));
});

function value(name) {
  const el = form.elements[name];
  if (!el) return "";
  if (el.type === "radio") return form.querySelector(`input[name="${name}"]:checked`)?.value || "";
  return el.value;
}

function buildReview() {
  reviewCard.innerHTML = `
    <div class="review-row"><span>Name</span><strong>${escapeHtml(value("name"))}</strong></div>
    <div class="review-row"><span>Roll Number</span><strong>${escapeHtml(value("roll_no"))}</strong></div>
    <div class="review-row"><span>Branch / Year</span><strong>${escapeHtml(value("branch"))} · ${escapeHtml(value("year"))}</strong></div>
    <div class="review-row"><span>Domain</span><strong class="review-domain">${escapeHtml(value("domain"))}</strong></div>
    <div class="review-row"><span>Email</span><strong>${escapeHtml(value("email"))}</strong></div>
  `;
}

function escapeHtml(text) {
  return text.replace(/[&<>"']/g, c => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#039;"
  }[c]));
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!document.getElementById("consent").checked) return;

  const button = form.querySelector(".submit-btn");
  button.disabled = true;
  button.innerHTML = "Submitting…";

  try {
    const response = await fetch("/apply", {method: "POST", body: new FormData(form)});
    const data = await response.json();
    if (!data.ok) throw new Error(data.message);

    form.style.display = "none";
    document.querySelector(".topbar").style.display = "none";
    successScreen.classList.add("show");
  } catch (err) {
    alert(err.message || "Something went wrong. Please try again.");
    button.disabled = false;
    button.innerHTML = 'Submit Application <span>↗</span>';
  }
});


// KMS theme toggle
(function(){
  const b=document.getElementById("themeToggle");
  if(!b) return;
  const dark=localStorage.getItem("kms-theme")==="dark";
  if(dark) document.body.classList.add("dark-mode");
  const update=()=>{const on=document.body.classList.contains("dark-mode");b.textContent=on?"☀ Light":"☾ Dark";};
  update();
  b.addEventListener("click",()=>{const on=document.body.classList.toggle("dark-mode");localStorage.setItem("kms-theme",on?"dark":"light");update();});
})();
