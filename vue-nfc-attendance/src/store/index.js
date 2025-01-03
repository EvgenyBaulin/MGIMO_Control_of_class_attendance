// src/store/index.js
import { createStore } from 'vuex';
import auth from '../services/auth';

export default createStore({
  state: {
    user: null,
    isAuthenticated: false,
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
      state.isAuthenticated = !!user;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const { data } = await auth.login(credentials);
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        commit('setUser', { email: credentials.email });
        return true;
      } catch (error) {
        console.error('Login error:', error);
        return false;
      }
    },
    async registerStudent({ commit }, userData) {
      try {
        await auth.registerStudent(userData);
        return true;
      } catch (error) {
        console.error('Student registration error:', error);
        return false;
      }
    },
    async registerInstructor({ commit }, userData) {
      try {
        await auth.registerInstructor(userData);
        return true;
      } catch (error) {
        console.error('Instructor registration error:', error);
        return false;
      }
    },
    logout({ commit }) {
      auth.logout();
      commit('setUser', null);
    },
  },
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
  },
});