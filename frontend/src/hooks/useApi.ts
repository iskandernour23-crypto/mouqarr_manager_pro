import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export const useApi = () => {
  const client = axios.create({ baseURL: API_URL });
  return client;
};
