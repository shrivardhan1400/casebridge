/** Lightweight browser API adapter for connecting the retained CaseBridge UI to FastAPI. */
const request = async (path, options = {}) => {
  const response = await fetch(`/api${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || "CaseBridge request failed");
  return response.json();
};

window.CaseBridgeAPI = {
  createCase: () => request("/cases", { method: "POST" }),
  submitStory: (id, story) => request(`/cases/${id}/story`, { method: "POST", body: JSON.stringify({ story }) }),
  nextStep: (id) => request(`/cases/${id}/next-step`),
  guidance: (id) => request(`/cases/${id}/documents/guidance`),
  assistant: (case_id, question) => request("/assistant", { method: "POST", body: JSON.stringify({ case_id, question }) }),
};
