(function () {
  
  // Shared assistants catalogue used by the chat workspace.
  const assistants = {
  clientpulse: {
    name: "ClientPulse",
    desc: "Client sentiment & signals",
    endpoint: "/clientpulse/chat",
    avatar: "CP",
  },
  cohortanalyst: {
    name: "CohortAnalyst",
    desc: "Cohort & retention analysis",
    endpoint: "/cohortanalyst/chat",
    avatar: "CA",
  },
  csplaybook: {
    name: "CSPlaybook",
    desc: "Customer success playbooks",
    endpoint: "/csplaybook/chat",
    avatar: "CS",
  },
  datascout: {
    name: "DataScout",
    desc: "Data summaries & anomalies",
    endpoint: "/datascout/chat",
    avatar: "DS",
  },
  diarybuddy: {
    name: "DiaryBuddy",
    desc: "Diary reminders & day planning",
    endpoint: "/diarybuddy/chat",
    avatar: "DB",
  },
  docdraft: {
    name: "DocDraft",
    desc: "Policy & procedure drafting",
    endpoint: "/docdraft/chat",
    avatar: "DD",
  },
  docguard: {
    name: "DocGuard",
    desc: "Contract & doc review",
    endpoint: "/docguard/chat",
    avatar: "DG",
  },
  excelwizard: {
    name: "ExcelWizard",
    desc: "Excel formulas & spreadsheet productivity",
    endpoint: "/excelwizard/chat",
    avatar: "EW",
  },
  fcaregwatch: {
    name: "FCARegWatch",
    desc: "UK FCA regulatory updates",
    endpoint: "/fcaregwatch/chat",
    avatar: "FC",
  },
  finres: {
    name: "FinRes",
    desc: "Financial analysis & ratios",
    endpoint: "/finres/chat",
    avatar: "FR",
  },
  finstatanalyst: {
    name: "FinStatAnalyst",
    desc: "Financial statements & KPI analysis",
    endpoint: "/finstatanalyst/chat",
    avatar: "FS",
  },
  flowdesigner: {
    name: "FlowDesigner",
    desc: "Visio-style process flow design",
    endpoint: "/flowdesigner/chat",
    avatar: "FD",
  },
  focusinbox: {
    name: "FocusInbox",
    desc: "Outlook-ready email triage & response drafting",
    endpoint: "/focusinbox/chat",
    avatar: "FI",
  },
  forecastlab: {
    name: "ForecastLab",
    desc: "Platinum forecasting & trend analysis",
    endpoint: "/forecastlab/chat",
    avatar: "FL",
  },
  globalrisk: {
    name: "GlobalRisk",
    desc: "Global macro & risk radar",
    endpoint: "/globalrisk/chat",
    avatar: "GR",
  },
  hrbuddy: {
    name: "HRBuddy",
    desc: "HR workflows & policies",
    endpoint: "/hrbuddy/chat",
    avatar: "HR",
  },
  invoicevision: {
    name: "InvoiceVision",
    desc: "Invoices & AP automation",
    endpoint: "/invoicevision/chat",
    avatar: "IV",
  },
  knowbase: {
    name: "KnowBase",
    desc: "Policy & knowledge Q&A",
    endpoint: "/knowbase/chat",
    avatar: "KB",
  },
  leadforge: {
    name: "LeadForge",
    desc: "Sales & lead intelligence",
    endpoint: "/leadforge/chat",
    avatar: "LF",
  },
  marketlens: {
    name: "MarketLens",
    desc: "Market & competitor insight",
    endpoint: "/marketlens/chat",
    avatar: "ML",
  },
  meetscribe: {
    name: "MeetScribe",
    desc: "Meeting notes & actions",
    endpoint: "/meetscribe/chat",
    avatar: "MS",
  },
  onboardingcoach: {
    name: "OnboardingCoach",
    desc: "New-hire onboarding plans",
    endpoint: "/onboardingcoach/chat",
    avatar: "OC",
  },
  opsdoctrine: {
    name: "OpsDoctrine",
    desc: "Operations doctrine & playbooks",
    endpoint: "/opsdoctrine/chat",
    avatar: "OD",
  },
  pensionscenario: {
    name: "PensionScenario",
    desc: "Pensions scenarios & flows",
    endpoint: "/pensionscenario/chat",
    avatar: "PS",
  },
  policydraftfca: {
    name: "PolicyDraftFCA",
    desc: "FCA-aligned policy drafting",
    endpoint: "/policydraftfca/chat",
    avatar: "PD",
  },
  portfoliostress: {
    name: "PortfolioStress",
    desc: "Portfolio stress & risk factors",
    endpoint: "/portfoliostress/chat",
    avatar: "PS",
  },
  pricelens: {
    name: "PriceLens",
    desc: "Pricing & packaging strategy",
    endpoint: "/pricelens/chat",
    avatar: "PL",
  },
  processflow: {
    name: "ProcessFlow",
    desc: "Process control & optimisation",
    endpoint: "/processflow/chat",
    avatar: "PF",
  },
  projman: {
    name: "ProjMan",
    desc: "Project planning & delivery",
    endpoint: "/projman/chat",
    avatar: "PM",
  },
  qcrisk: {
    name: "QCRisk",
    desc: "Quality & risk scoring",
    endpoint: "/qcrisk/chat",
    avatar: "QC",
  },
  regwatch: {
    name: "RegWatch",
    desc: "Risk & compliance insight",
    endpoint: "/regwatch/chat",
    avatar: "RW",
  },
  rendercraft: {
    name: "RenderCraft",
    desc: "3D rendering briefs & scene design",
    endpoint: "/rendercraft/chat",
    avatar: "RC",
  },
  riskscenario: {
    name: "RiskScenario",
    desc: "Scenario planning & stress tests",
    endpoint: "/riskscenario/chat",
    avatar: "RS",
  },
  salesgen: {
    name: "SalesGen",
    desc: "Sales copy & cadences",
    endpoint: "/salesgen/chat",
    avatar: "SG",
  },
  seoarchitect: {
    name: "SEOArchitect",
    desc: "SEO strategy & content architecture",
    endpoint: "/seoarchitect/chat",
    avatar: "SE",
  },
  supplychainpro: {
    name: "SupplyChainPro",
    desc: "Supply chain optimisation",
    endpoint: "/supplychainpro/chat",
    avatar: "SC",
  },
  supportdesk: {
    name: "SupportDesk",
    desc: "Customer support & triage",
    endpoint: "/supportdesk/chat",
    avatar: "SD",
  },
  taskflow: {
    name: "TaskFlow",
    desc: "Process & SOP automation",
    endpoint: "/taskflow/chat",
    avatar: "TF",
  },
  uxcopy: {
    name: "UXCopy",
    desc: "UX & product copywriting",
    endpoint: "/uxcopy/chat",
    avatar: "UX",
  },
};


  // --- Chat workspace wiring (index page) ---
  const historyEl = document.getElementById("chat-history");
  const inputEl = document.getElementById("chat-input");
  const formEl = document.getElementById("chat-form");
  const assistantNameEl = document.getElementById("chat-assistant-name");
  const assistantDescEl = document.getElementById("chat-assistant-desc");
  const sidebarTabs = Array.from(document.querySelectorAll(".assistant-tab"));

  let activeKey = "leadforge";
  let isSending = false;

  function setActiveAssistant(key) {
    if (!assistants[key]) return;
    activeKey = key;

    // Update sidebar active state (for pages that have it)
    sidebarTabs.forEach((tab) => {
      const id = tab.getAttribute("data-assistant");
      if (!id) return;
      tab.classList.toggle("active", id === key);
    });

    if (assistantNameEl) {
      assistantNameEl.textContent = assistants[key].name;
    }
    if (assistantDescEl) {
      assistantDescEl.textContent = assistants[key].desc;
    }

    if (historyEl) {
      const bubble = document.createElement("div");
      bubble.className = "chat-message chat-message-ai";
      bubble.innerHTML = `
        <div class="chat-avatar">${assistants[key].avatar || "AI"}</div>
        <div class="chat-bubble">
          You are now chatting with <strong>${assistants[key].name}</strong>. Ask a question in this domain and I’ll respond with expert, practical guidance.
        </div>
      `;
      historyEl.appendChild(bubble);
      historyEl.scrollTop = historyEl.scrollHeight;
    }
  }

  function addMessage(role, text) {
    if (!historyEl) return;
    const msgEl = document.createElement("div");
    msgEl.className =
      role === "user" ? "chat-message chat-message-user" : "chat-message chat-message-ai";

    if (role === "user") {
      msgEl.innerHTML = `
        <div class="chat-bubble">${text}</div>
      `;
    } else {
      const avatar = assistants[activeKey]?.avatar ?? "AI";
      msgEl.innerHTML = `
        <div class="chat-avatar">${avatar}</div>
        <div class="chat-bubble">${text}</div>
      `;
    }
    historyEl.appendChild(msgEl);
    historyEl.scrollTop = historyEl.scrollHeight;
  }

  async function send(message) {
    if (!message.trim() || isSending) return;
    const currentAssistant = assistants[activeKey];
    if (!currentAssistant) return;

    addMessage("user", message);
    if (inputEl) inputEl.value = "";
    isSending = true;

    try {
      const res = await fetch(currentAssistant.endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",\n          ...(window.SERVINATION_API_KEY ? { "X-API-Key": window.SERVINATION_API_KEY } : {}),
        },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        throw new Error("Request failed with status " + res.status);
      }

      const data = await res.json();
      const content =
        data.content ||
        data.assessment ||
        data.analysis ||
        data.summary ||
        data.response ||
        JSON.stringify(data);
      addMessage("assistant", content);
    } catch (err) {
      console.error(err);
      addMessage(
        "assistant",
        "Sorry, something went wrong talking to this assistant. Please try again shortly."
      );
    } finally {
      isSending = false;
    }
  }

  if (historyEl && formEl && inputEl) {
    formEl.addEventListener("submit", (e) => {
      e.preventDefault();
      const value = inputEl.value;
      if (value.trim()) {
        send(value.trim());
      }
    });

    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const value = inputEl.value;
        if (value.trim()) {
          send(value.trim());
        }
      }
    });
  }

  sidebarTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const key = tab.getAttribute("data-assistant");
      if (key) setActiveAssistant(key);
    });
  });

  if (historyEl) {
    // We are on the main chat page; ensure a sane default
    setActiveAssistant("leadforge");
  }

  // --- Assistants catalogue (assistants.html) ---
  const assistantsDetailContainer = document.getElementById("assistants-detail-container");
  const assistantsPanelTitle = document.getElementById("assistants-panel-title");
  const assistantsPanelSubtitle = document.getElementById("assistants-panel-subtitle");

  if (assistantsDetailContainer) {
    const detailBlocks = Array.from(
      assistantsDetailContainer.querySelectorAll(".assistant-detail")
    );

    function activateDetail(key) {
      const meta = assistants[key];
      if (!meta) return;
      detailBlocks.forEach((blk) => {
        const id = blk.getAttribute("data-assistant");
        blk.classList.toggle("active", id === key);
      });
      if (assistantsPanelTitle) assistantsPanelTitle.textContent = meta.name;
      if (assistantsPanelSubtitle) assistantsPanelSubtitle.textContent = meta.desc;
    }

    // Wire up tabs in the assistants sidebar for the catalogue page
    const catalogueTabs = Array.from(
      document.querySelectorAll(".assistants-sidebar .assistant-tab")
    );
    catalogueTabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        const key = tab.getAttribute("data-assistant");
        catalogueTabs.forEach((t) => t.classList.toggle("active", t === tab));
        if (key) activateDetail(key);
      });
    });

    // Default to the first assistant if available
    if (catalogueTabs.length > 0) {
      const firstKey = catalogueTabs[0].getAttribute("data-assistant");
      if (firstKey) {
        catalogueTabs[0].classList.add("active");
        activateDetail(firstKey);
      }
    }
  }

// --- Client workspace wiring (client.html) ---
const clientAssistantListEl = document.getElementById("assistant-list");
const clientChatWindowEl = document.getElementById("chat-window");
const clientChatFormEl = document.getElementById("chat-form");
const clientChatInputEl = document.getElementById("chat-input");
const clientAssistantTitleEl = document.getElementById("chat-assistant-title");
const clientAssistantDescEl = document.getElementById("chat-assistant-description");

if (clientAssistantListEl && clientChatWindowEl && clientChatFormEl && clientChatInputEl) {
  const planAssistants = {
    bronze: [
      "csplaybook",
      "knowbase",
      "supportdesk",
      "hrbuddy",
      "regwatch",
    ],
    standard: [
      "csplaybook",
      "knowbase",
      "supportdesk",
      "hrbuddy",
      "regwatch",
      "diarybuddy",
      "focusinbox",
      "meetscribe",
      "docdraft",
      "uxcopy",
      "excelwizard",
    ],
  };

  const goldExtras = [
    "leadforge",
    "invoicevision",
    "taskflow",
    "qcrisk",
    "clientpulse",
    "salesgen",
    "finres",
    "docguard",
    "projman",
    "datascout",
    "marketlens",
    "seoarchitect",
    "supplychainpro",
    "rendercraft",
    "flowdesigner",
    "onboardingcoach",
    "pricelens",
    "opsdoctrine",
    "processflow",
    "finstatanalyst",
    "fcaregwatch",
    "policydraftfca",
  ];

  const platinumExtras = [
    "riskscenario",
    "cohortanalyst",
    "pensionscenario",
    "portfoliostress",
  ];

  const diamondExtras = [
    "forecastlab",
    "globalrisk",
  ];

  function unique(list) {
    const seen = new Set();
    const out = [];
    list.forEach((item) => {
      if (!item || seen.has(item) || !assistants[item]) return;
      seen.add(item);
      out.push(item);
    });
    return out;
  }

  function getAssistantsForPlan(planRaw) {
    const plan = (planRaw || "").toLowerCase();
    if (plan === "bronze") return unique(planAssistants.bronze);
    if (plan === "standard") return unique(planAssistants.standard);

    if (plan === "gold") {
      return unique([
        ...planAssistants.bronze,
        ...planAssistants.standard,
        ...goldExtras,
      ]);
    }

    if (plan === "platinum") {
      return unique([
        ...planAssistants.bronze,
        ...planAssistants.standard,
        ...goldExtras,
        ...platinumExtras,
      ]);
    }

    if (plan === "diamond" || plan === "enterprise") {
      // All assistants
      return unique(Object.keys(assistants));
    }

    // Default: small curated subset if plan unknown
    return unique([
      "leadforge",
      "invoicevision",
      "knowbase",
      "supportdesk",
      "regwatch",
    ]);
  }

  let clientActiveKey = null;
  let clientIsSending = false;
  let clientPlan = (window.SERVINATION_PLAN || "").toLowerCase();

  function clientSetActiveAssistant(key) {
    if (!assistants[key]) return;
    clientActiveKey = key;

    Array.from(clientAssistantListEl.querySelectorAll("button")).forEach((btn) => {
      const k = btn.getAttribute("data-assistant");
      btn.classList.toggle("active", k === key);
    });

    if (clientAssistantTitleEl) {
      clientAssistantTitleEl.textContent = assistants[key].name;
    }
    if (clientAssistantDescEl) {
      clientAssistantDescEl.textContent = assistants[key].desc;
    }

    if (clientChatWindowEl) {
      clientChatWindowEl.innerHTML = "";
      const bubble = document.createElement("div");
      bubble.className = "chat-message chat-message-ai";
      bubble.innerHTML = `
        <div class="chat-avatar">${assistants[key].avatar || "AI"}</div>
        <div class="chat-bubble">
          You are now chatting with <strong>${assistants[key].name}</strong>. Ask me a question in this domain and I’ll respond with expert, practical guidance.
        </div>
      `;
      clientChatWindowEl.appendChild(bubble);
    }
  }

  function clientAddMessage(role, text) {
    if (!clientChatWindowEl) return;
    const msgEl = document.createElement("div");
    msgEl.className =
      role === "user" ? "chat-message chat-message-user" : "chat-message chat-message-ai";

    if (role === "user") {
      msgEl.innerHTML = `<div class="chat-bubble">${text}</div>`;
    } else {
      const avatar = assistants[clientActiveKey]?.avatar ?? "AI";
      msgEl.innerHTML = `
        <div class="chat-avatar">${avatar}</div>
        <div class="chat-bubble">${text}</div>
      `;
    }

    clientChatWindowEl.appendChild(msgEl);
    clientChatWindowEl.scrollTop = clientChatWindowEl.scrollHeight;
  }

  async function clientSend(message) {
    if (!message.trim() || clientIsSending) return;
    if (!clientActiveKey) return;

    const currentAssistant = assistants[clientActiveKey];
    if (!currentAssistant) return;

    clientAddMessage("user", message);
    if (clientChatInputEl) clientChatInputEl.value = "";
    clientIsSending = true;

    try {
      const headers = {
        "Content-Type": "application/json",
      };
      if (window.SERVINATION_API_KEY) {
        headers["X-API-Key"] = window.SERVINATION_API_KEY;
      }

      const res = await fetch(currentAssistant.endpoint, {
        method: "POST",
        headers,
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        throw new Error("Request failed with status " + res.status);
      }

      const data = await res.json();
      const content =
        data.content ||
        data.assessment ||
        data.analysis ||
        data.summary ||
        data.response ||
        JSON.stringify(data);
      clientAddMessage("assistant", content);
    } catch (err) {
      console.error(err);
      clientAddMessage(
        "assistant",
        "Sorry, something went wrong talking to this assistant. Please try again shortly."
      );
    } finally {
      clientIsSending = false;
    }
  }

  function renderClientAssistantList() {
    const plan = clientPlan || (window.SERVINATION_PLAN || "").toLowerCase();
    const keys = getAssistantsForPlan(plan);

    clientAssistantListEl.innerHTML = "";
    keys.forEach((key) => {
      const info = assistants[key];
      if (!info) return;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "assistant-tab";
      btn.setAttribute("data-assistant", key);
      btn.innerHTML = `
        <span class="assistant-name">${info.name}</span>
        <span class="assistant-meta">${info.desc}</span>
      `;
      btn.addEventListener("click", () => {
        clientSetActiveAssistant(key);
      });
      clientAssistantListEl.appendChild(btn);
    });

    if (keys.length > 0) {
      clientSetActiveAssistant(keys[0]);
    } else {
      clientAssistantListEl.innerHTML = "<p class=\"muted small\">No assistants available for this plan.</p>";
    }
  }

  if (clientChatFormEl && clientChatInputEl) {
    clientChatFormEl.addEventListener("submit", (e) => {
      e.preventDefault();
      const value = clientChatInputEl.value;
      if (value && value.trim()) {
        clientSend(value.trim());
      }
    });

    clientChatInputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        const value = clientChatInputEl.value;
        if (value && value.trim()) {
          clientSend(value.trim());
        }
      }
    });
  }

  function initClientWorkspace(planRaw) {
    clientPlan = (planRaw || clientPlan || "").toLowerCase();
    renderClientAssistantList();
  }

  // Expose a hook for the login page to call after successful login
  window.ServinationClient = window.ServinationClient || {};
  window.ServinationClient.onLogin = function (opts) {
    if (opts && opts.plan) {
      clientPlan = (opts.plan || "").toLowerCase();
    }
    if (opts && opts.apiKey) {
      window.SERVINATION_API_KEY = opts.apiKey;
    }
    initClientWorkspace(clientPlan);
  };

  // Initialise immediately if a plan is already present (eg from a pre-filled global)
  if (window.SERVINATION_PLAN) {
    initClientWorkspace(window.SERVINATION_PLAN);
  } else {
    // Fallback to a curated default if not logged in
    initClientWorkspace(clientPlan);
  }
}


})();
