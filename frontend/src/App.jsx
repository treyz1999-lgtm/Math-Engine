import { useEffect, useMemo, useState } from "react";
import { AppHeader } from "./components/AppHeader";
import { Sidebar } from "./components/Sidebar";
import { Card } from "./components/Card";
import { CalculatorPanel } from "./features/calculator/CalculatorPanel";
import { ResultDisplay } from "./features/calculator/ResultDisplay";
import { HistoryPanel } from "./features/history/HistoryPanel";
import { SettingsPanel } from "./features/settings/SettingsPanel";
import { calculatorConfigs, categoryDefaults, categories } from "./features/calculator/calculatorConfig";
import { settingsOptions } from "./features/settings/settingsConfig";
import { parseFieldValue, parseSettingValue } from "./utils/parsers";
import { labelize } from "./utils/formatters";
import {
  clearHistory,
  deleteHistoryEntry,
  getHistorySummary,
  replayHistory,
  resetSettings,
  runCalculation,
  updateSetting,
} from "./services/api";

function initialInputs(config) {
  return Object.fromEntries(config.fields.map((field) => [field.name, ""]));
}

function isPlotResult(result) {
  return Boolean(result?.plot_type);
}

export default function App() {
  const [mode, setMode] = useState("calculator");
  const [activeCategory, setActiveCategory] = useState("arithmetic");
  const [subcategory, setSubcategory] = useState(categoryDefaults.arithmetic);
  const [operation, setOperation] = useState(calculatorConfigs.arithmetic.binary.operations[0]);
  const [inputs, setInputs] = useState(initialInputs(calculatorConfigs.arithmetic.binary));
  const [result, setResult] = useState(null);
  const [plot, setPlot] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [settingsCategory, setSettingsCategory] = useState("general");
  const [setting, setSetting] = useState(settingsOptions.general[0]);
  const [settingValue, setSettingValue] = useState("");

  const categoryConfig = calculatorConfigs[activeCategory];
  const config = categoryConfig[subcategory];
  const activeLabel = useMemo(() => categories.find((item) => item.id === activeCategory)?.label || labelize(activeCategory), [activeCategory]);

  function resetForConfig(nextCategory, nextSubcategory) {
    const nextConfig = calculatorConfigs[nextCategory][nextSubcategory];
    setSubcategory(nextSubcategory);
    setOperation(nextConfig.operations[0]);
    setInputs(initialInputs(nextConfig));
    setError("");
  }

  function selectCategory(category) {
    setActiveCategory(category);
    setMode("calculator");
    resetForConfig(category, categoryDefaults[category]);
  }

  function changeSubcategory(nextSubcategory) {
    resetForConfig(activeCategory, nextSubcategory);
  }

  function buildPayload() {
    const payload = { operation };
    for (const field of config.fields) {
      const parsedValue = parseFieldValue(field, inputs[field.name] || "");
      if (parsedValue !== undefined) payload[field.name] = parsedValue;
    }
    return payload;
  }

  async function submitCalculation(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPlot(null);

    try {
      const payload = buildPayload();
      const data = await runCalculation(config.endpoint, payload);
      if (isPlotResult(data.result)) {
        setResult("Plot generated.");
        setPlot(data.result);
      } else {
        setResult(data.result);
      }
      await refreshHistory({ quiet: true });
    } catch (caught) {
      setResult(null);
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  async function refreshHistory({ quiet = false } = {}) {
    if (!quiet) setLoading(true);
    try {
      const data = await getHistorySummary();
      setHistory(data.history || []);
    } catch (caught) {
      setError(caught.message);
    } finally {
      if (!quiet) setLoading(false);
    }
  }

  async function showHistory() {
    setMode("history");
    setPlot(null);
    setError("");
    await refreshHistory();
  }

  async function handleReplay(index) {
    setLoading(true);
    setError("");
    setPlot(null);

    try {
      const replay = await replayHistory(index);
      const data = await runCalculation(replay.endpoint, replay.request);
      if (isPlotResult(data.result)) {
        setResult("Plot generated.");
        setPlot(data.result);
      } else {
        setResult(data.result);
      }
      setMode("calculator");
      await refreshHistory({ quiet: true });
    } catch (caught) {
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleDeleteHistory(index) {
    setLoading(true);
    setError("");
    try {
      await deleteHistoryEntry(index);
      await refreshHistory({ quiet: true });
    } catch (caught) {
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleClearHistory() {
    setLoading(true);
    setError("");
    try {
      await clearHistory();
      setHistory([]);
    } catch (caught) {
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleUpdateSetting(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setPlot(null);

    try {
      const data = await updateSetting({
        category: settingsCategory,
        setting,
        value: parseSettingValue(settingValue),
      });
      setResult(data);
      setSettingValue("");
    } catch (caught) {
      setResult(null);
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  async function handleResetSettings() {
    setLoading(true);
    setError("");
    setPlot(null);

    try {
      const data = await resetSettings();
      setResult(data);
      setSettingValue("");
    } catch (caught) {
      setResult(null);
      setError(caught.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setSetting(settingsOptions[settingsCategory][0]);
  }, [settingsCategory]);

  return (
    <div className="app-shell">
      <Sidebar
        activeCategory={activeCategory}
        mode={mode}
        onSelectCategory={selectCategory}
        onShowHistory={showHistory}
        onShowSettings={() => {
          setMode("settings");
          setError("");
          setPlot(null);
        }}
      />

      <main className="workspace">
        <AppHeader activeLabel={activeLabel} mode={mode} />

        <div className="workspace-grid">
          <Card title={mode === "calculator" ? activeLabel : labelize(mode)} eyebrow={mode === "calculator" ? "Input" : "Controls"}>
            {mode === "calculator" && (
              <CalculatorPanel
                category={activeCategory}
                subcategory={subcategory}
                config={config}
                inputs={inputs}
                operation={operation}
                categoryConfig={categoryConfig}
                onSubcategoryChange={changeSubcategory}
                onOperationChange={setOperation}
                onInputChange={(name, value) => setInputs((current) => ({ ...current, [name]: value }))}
                onSubmit={submitCalculation}
                loading={loading}
              />
            )}

            {mode === "history" && (
              <HistoryPanel
                entries={history}
                loading={loading}
                onReplay={handleReplay}
                onDelete={handleDeleteHistory}
                onRefresh={refreshHistory}
                onClear={handleClearHistory}
              />
            )}

            {mode === "settings" && (
              <SettingsPanel
                category={settingsCategory}
                setting={setting}
                value={settingValue}
                onCategoryChange={setSettingsCategory}
                onSettingChange={setSetting}
                onValueChange={setSettingValue}
                onUpdate={handleUpdateSetting}
                onReset={handleResetSettings}
                loading={loading}
              />
            )}
          </Card>

          <Card title="Output" eyebrow="Result">
            <ResultDisplay result={result} plot={plot} error={error} loading={loading && mode === "calculator"} />
          </Card>
        </div>
      </main>
    </div>
  );
}
