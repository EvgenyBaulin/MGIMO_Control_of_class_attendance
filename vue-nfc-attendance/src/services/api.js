import axios from 'axios';

const api = axios.create({
    baseURL: 'http://your-api-url.com/api',
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const originalRequest = error.config;
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            try {
                const refreshToken = localStorage.getItem('refresh_token');
                const {data} = await axios.post('/api/token/refresh/', {refresh: refreshToken});
                localStorage.setItem('access_token', data.access);
                api.defaults.headers['Authorization'] = `Bearer ${data.access}`;
                return api(originalRequest);
            } catch (refreshError) {
                // Handle refresh token error (e.g., logout user)
            }
        }
        return Promise.reject(error);
    }
);

export default api;