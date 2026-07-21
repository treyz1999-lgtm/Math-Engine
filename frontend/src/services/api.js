const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

function normalizeErrorDetail(detail) {
  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg || JSON.stringify(item)).join("; ");
  }

  if (detail && typeof detail === "object") {
    return detail.message || JSON.stringify(detail);
  }

  return detail;
}

export async function request(endpoint, { method = "POST", payload = null } = {}) {
  const options = {
    method,
    headers: {
      "Content-Type": "application/json",
    },
  };

  if (payload !== null && method !== "GET") {
    options.body = JSON.stringify(payload);
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  } catch {
    throw new Error("Unable to reach the Math Engine API. Confirm the FastAPI server is running.");
  }

  const contentType = response.headers.get("content-type") || "";
  const data = contentType.includes("application/json") ? await response.json() : null;

  if (!response.ok) {
    throw new Error(normalizeErrorDetail(data?.detail) || data?.message || "API request failed.");
  }

  return data;
}

export function runCalculation(endpoint, payload) {
  return request(endpoint, { payload });
}

export function updateSetting(payload) {
  return request("/settings/update", { payload });
}

export function resetSettings() {
  return request("/settings/reset", { payload: {} });
}

export function getHistorySummary() {
  return request("/history/summary", { method: "GET" });
}

export function getHistoryEntry(index) {
  return request(`/history/${index}`, { method: "GET" });
}

export function replayHistory(index) {
  return request(`/history/replay/${index}`, { payload: {} });
}

export function deleteHistoryEntry(index) {
  return request(`/history/${index}`, { method: "DELETE" });
}

export function clearHistory() {
  return request("/history/clear", { payload: {} });
}
