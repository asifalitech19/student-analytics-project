import axios from "axios";

const api = axios.create({
  baseURL: "https://asif-ai-backend-e4fhhxe4bkgrgyge.centralus-01.azurewebsites.net",
});

export default api;