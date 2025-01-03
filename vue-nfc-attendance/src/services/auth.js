// src/services/auth.js
import api from './api';

export default {
    login(credentials) {
        return api.post('/login/', credentials);
    },
    registerStudent(userData) {
        return api.post('/register/student/', userData);
    },
    registerInstructor(userData) {
        return api.post('/register/instructor/', userData);
    },
    logout() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
    }
};