import axios from 'axios';

const chatbotApi = axios.create({
  baseURL: `http://localhost:${import.meta.env.VITE_BACKEND_PORT}/api/`,
  timeout: 180000,
    headers: {
    'Content-Type': 'application/json',
  },
});

chatbotApi.interceptors.response.use(
  (response) => response,
  (error) => {
    const message = error.response?.data?.detail || 'Ocorreu um erro ao processar sua requisição';
    console.error('API Error:', message);
    return Promise.reject(error);
  }
);

export default chatbotApi;