<!-- src/components/Auth/StudentRegister.vue -->
<template>
  <div class = "student-register">
    <h2>Student Registration</h2>
    <form @submit.prevent = "handleSubmit">
      <div>
        <label for = "email">Email:</label>
        <input type = "email" id = "email" v-model = "email" required>
      </div>
      <div>
        <label for = "username">Username:</label>
        <input type = "text" id = "username" v-model = "username" required>
      </div>
      <div>
        <label for = "password">Password:</label>
        <input type = "password" id = "password" v-model = "password" required>
      </div>
      <div>
        <label for = "group">Group:</label>
        <input type = "number" id = "group" v-model = "group" required>
      </div>
      <button type = "submit">Register</button>
    </form>
  </div>
</template>

<script>
import {ref} from 'vue';
import {useStore} from 'vuex';
import {useRouter} from 'vue-router';

export default {
  name: 'StudentRegister',
  setup() {
    const store = useStore();
    const router = useRouter();
    const email = ref('');
    const username = ref('');
    const password = ref('');
    const group = ref('');

    const handleSubmit = async () => {
      const success = await store.dispatch('registerStudent', {
        email: email.value,
        username: username.value,
        password: password.value,
        group: parseInt(group.value)
      });
      if (success) {
        alert('Registration successful! Please login.');
        router.push('/login');
      } else {
        alert('Registration failed. Please try again.');
      }
    };

    return {
      email,
      username,
      password,
      group,
      handleSubmit
    };
  }
};
</script>