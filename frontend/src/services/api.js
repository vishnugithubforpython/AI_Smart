import axios from "axios";

const TOKEN_KEY = "token";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

let onUnauthorized = null;

export function setUnauthorizedHandler(handler) {
  onUnauthorized = handler;
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  } else {
    localStorage.removeItem(TOKEN_KEY);
  }
}

export function extractErrorMessage(error) {
  if (!error.response) {
    return "Network error. Please check your connection and try again.";
  }

  const { status, data } = error.response;
  const detail = data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail.map((item) => item.msg ?? JSON.stringify(item)).join(", ");
  }

  if (status === 401) {
    return "Invalid email or password.";
  }

  if (status === 403) {
    return "You do not have permission to perform this action.";
  }

  if (status >= 500) {
    return "Server error. Please try again later.";
  }

  return "Something went wrong. Please try again.";
}

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status;

    if (status === 401 && getStoredToken()) {
      setStoredToken(null);
      onUnauthorized?.();
    }

    return Promise.reject(error);
  }
);

export async function loginUser(email, password) {
  const { data } = await api.post("/auth/login", { email, password });
  return data;
}

export async function signupUser(username, email, password) {
  const { data } = await api.post("/auth/signup", {
    username,
    email,
    password,
  });
  return data;
}

export async function fetchProfile() {
  const { data } = await api.get("/profile");
  return data;
}

/**
 * Send a question to FastAPI POST /ask
 */
export async function askQuestion(question) {
  const { data } = await api.post("/ask", { question });

  const sources = data.sources ?? [];
  const answer =
    typeof data.answer === "string" && data.answer.trim()
      ? data.answer
      : "No answer received from the server.";

  return {
    answer,
    sources,
    sourceType: sources.length > 0 ? "document" : "web",
  };
}

/**
 * Upload a file to FastAPI POST /upload/
 */
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const { data } = await api.post("/upload/", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return data;
}

export default api;
