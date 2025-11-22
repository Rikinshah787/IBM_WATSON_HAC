import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`[API] ${config.method.toUpperCase()} ${config.url}`, config.data);
    return config;
  },
  (error) => {
    console.error('[API] Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for logging
api.interceptors.response.use(
  (response) => {
    console.log(`[API] Response:`, response.data);
    return response;
  },
  (error) => {
    console.error('[API] Response error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const apiService = {
  // Process a query through the agent
  processQuery: async (query, sector = null, context = {}) => {
    return api.post('/query', {
      query,
      sector,
      context,
    });
  },

  // Get dashboard data for a sector
  getDashboardData: async (sector) => {
    return api.get(`/dashboard/${sector}`);
  },

  // Get list of sectors
  getSectors: async () => {
    return api.get('/sectors');
  },

  // Health check
  healthCheck: async () => {
    return api.get('/health');
  },
};

// Export default for convenience
export default apiService;

