import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000,
});

/**
 * Send a question to FastAPI POST /ask
 * React → api.js → FastAPI → { answer, sources }
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

export default api;
