(() => {
  const state = {
    lang: "en",
    latest: null,
    stage2: null,
  };

  const te = {
    appTitle: "స్మార్ట్ నీటి నాణ్యత & పంట సూచన",
    liveReadings: "లైవ్ రీడింగ్స్",
    controls: "సిఫార్సులు",
    season: "సీజన్",
    desiredCrop: "కావలసిన పంట (ఐచ్ఛికం)",
    getRecs: "సిఫార్సులు పొందండి",
    topCrops: "సిఫార్సు చేసిన పంటలు",
    insight: "ఇన్‌సైట్",
    treatment: "చర్య సూచనలు",
    seasons: { Kharif: "ఖరీఫ్", Rabi: "రబీ", Summer: "వేసవి" },
    crops: {
      Banana: "అరటి",
      "Bengal Gram": "సెనగలు",
      Castor: "ఆముదం",
      Chillies: "మిర్చి",
      Cotton: "పత్తి",
      Groundnut: "వేరుశనగ",
      Jowar: "జొన్న",
      Maize: "మొక్కజొన్న",
      Mango: "మామిడి",
      Onion: "ఉల్లిపాయ",
      Paddy: "వరి",
      Pomegranate: "దానిమ్మ",
      "Red Gram": "కంది",
      Sunflower: "పొద్దుతిరుగుడు",
      "Sweet Orange": "కమలపండు",
      Tomato: "టమాట",
    },
    status: {
      0: "అననుకూలం",
      1: "జాగ్రత్త",
      2: "అనుకూలం",
    },
  };

  const $ = (id) => document.getElementById(id);

  function setText(id, value) {
    const el = $(id);
    if (el) el.textContent = value;
  }

  function formatKnn(knnStatus) {
    const labelEn = { 0: "Unsuitable", 1: "Caution", 2: "Suitable" }[knnStatus] ?? "—";
    const labelTe = te.status[knnStatus] ?? "—";
    return state.lang === "te" ? labelTe : labelEn;
  }

  function applyLang() {
    setText("appTitle", state.lang === "te" ? te.appTitle : "Smart Water Quality & Crop Advisor");
    setText("liveReadingsTitle", state.lang === "te" ? te.liveReadings : "Live Readings");
    setText("controlsTitle", state.lang === "te" ? te.controls : "Recommendations");
    setText("seasonLabel", state.lang === "te" ? te.season : "Season");
    setText("desiredCropLabel", state.lang === "te" ? te.desiredCrop : "Desired Crop (optional)");
    setText("recommendBtn", state.lang === "te" ? te.getRecs : "Get recommendations");
    setText("topCropsTitle", state.lang === "te" ? te.topCrops : "Top crops");
    setText("insightTitle", state.lang === "te" ? te.insight : "Insight");
    setText("treatmentTitle", state.lang === "te" ? te.treatment : "Treatment advice");

    const seasonSelect = $("seasonSelect");
    if (seasonSelect && state.lang === "te") {
      [...seasonSelect.options].forEach((opt) => {
        opt.textContent = te.seasons[opt.value] ?? opt.value;
      });
    } else if (seasonSelect) {
      [...seasonSelect.options].forEach((opt) => (opt.textContent = opt.value));
    }

    const desiredSelect = $("desiredCropSelect");
    if (desiredSelect && state.lang === "te") {
      [...desiredSelect.options].forEach((opt) => {
        if (!opt.value) return;
        opt.textContent = te.crops[opt.value] ?? opt.value;
      });
    } else if (desiredSelect) {
      [...desiredSelect.options].forEach((opt) => {
        if (!opt.value) return;
        opt.textContent = opt.value;
      });
    }

    renderStage2();
  }

  function renderLatest() {
    const d = state.latest;
    if (!d || !d.sensor_data) return;

    setText("ph", d.sensor_data.pH?.toFixed?.(2) ?? d.sensor_data.pH ?? "--");
    setText("tds", d.sensor_data.TDS?.toFixed?.(0) ?? d.sensor_data.TDS ?? "--");
    setText("turbidity", d.sensor_data.turbidity?.toFixed?.(0) ?? d.sensor_data.turbidity ?? "--");
    setText("temperature", d.sensor_data.temperature?.toFixed?.(0) ?? d.sensor_data.temperature ?? "--");
    setText("lastUpdated", d.last_updated ? `Updated: ${d.last_updated}` : "--");

    const knnStatus = d.sensor_data.knn_status;
    const chip = $("knnChip");
    if (chip) {
      chip.textContent = `Water: ${formatKnn(knnStatus)}`;
      chip.className = `statusbar__chip status-${knnStatus ?? "x"}`;
    }

    setText("legacyPrediction", d.ml_prediction ?? "—");
  }

  function renderStage2() {
    const res = state.stage2;
    const cropsGrid = $("cropsGrid");
    if (!cropsGrid) return;
    cropsGrid.innerHTML = "";

    if (!res || !res.ok) return;

    if (res.halt) {
      setText("insightBox", state.lang === "te" ? res.insight?.te : res.insight?.en);
      setText("treatmentBox", "—");
      return;
    }

    const recs = res.recommendations ?? [];
    recs.forEach((r) => {
      const card = document.createElement("div");
      card.className = "cropCard";

      const name = state.lang === "te" ? (r.crop_te ?? te.crops[r.crop_en] ?? r.crop_en) : r.crop_en;
      const score = typeof r.score === "number" ? r.score : null;

      card.innerHTML = `
        <div class="cropCard__name">${name}</div>
        <div class="cropCard__meta">${state.lang === "te" ? "స్కోరు" : "Score"}: ${
          score !== null ? score.toFixed(3) : "—"
        }</div>
      `;
      cropsGrid.appendChild(card);
    });

    setText("insightBox", state.lang === "te" ? res.insight?.te : res.insight?.en);

    const desired = res.desired_crop;
    if (desired?.advice) {
      setText("treatmentBox", state.lang === "te" ? desired.advice.te : desired.advice.en);
    } else {
      setText("treatmentBox", "—");
    }
  }

  async function fetchLatest() {
    const r = await fetch("/iot/latest");
    state.latest = await r.json();
    renderLatest();
  }

  async function fetchStage2FromLatest() {
    const season = $("seasonSelect")?.value ?? "Kharif";
    const desired = $("desiredCropSelect")?.value ?? "";
    const qs = new URLSearchParams();
    qs.set("season", season);
    if (desired) qs.set("desired_crop", desired);

    const r = await fetch(`/api/stage2/recommend/latest?${qs.toString()}`);
    state.stage2 = await r.json();
    renderStage2();
  }

  function wire() {
    const toggle = $("langToggle");
    if (toggle) {
      toggle.addEventListener("change", () => {
        state.lang = toggle.checked ? "te" : "en";
        applyLang();
      });
    }

    const btn = $("recommendBtn");
    if (btn) btn.addEventListener("click", fetchStage2FromLatest);

    applyLang();
  }

  wire();
  fetchLatest().then(fetchStage2FromLatest);
  setInterval(() => {
    fetchLatest().then(fetchStage2FromLatest);
  }, 5000);
})();

