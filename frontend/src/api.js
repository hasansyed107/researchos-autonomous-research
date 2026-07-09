import axios from "axios";

const API = axios.create({
  baseURL: "https://researchos-autonomous-research-production.up.railway.app",
});

export default API;