const API_BASE = "https://surplus-food-platform-iv6y.onrender.com/api";

function saveTokens(access, refresh) {
  localStorage.setItem("access", access);
  localStorage.setItem("refresh", refresh);
}

function getAccessToken() {
  return localStorage.getItem("access");
}

function logout() {
  localStorage.removeItem("access");
  localStorage.removeItem("refresh");
  window.location.href = "index.html";
}

async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  const token = getAccessToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;
  if (options.body && !(options.body instanceof FormData)) {
    headers["Content-Type"] = "application/json";
  }
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (res.status === 401) {
    logout();
    throw new Error("Unauthorized");
  }
  return res;
}