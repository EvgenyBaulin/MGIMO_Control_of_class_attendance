<!-- src/components/Auth/InstructorRegister.vue -->
<template>
  <div class = "instructor-register">
    <h2>Instructor Registration</h2>
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
        <label for = "secretKey">Secret Key:</label>
        <input type = "password" id = "secretKey" v-model = "secretKey" required>
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
  name: 'InstructorRegister',
  setup() {
    const store = useStore();
    const router = useRouter();
    const email = ref('');
    const username = ref('');
    const password = ref('');
    const secretKey = ref('');

    const handleSubmit = async () => {
      const success = await store.dispatch('registerInstructor', {
        email: email.value,
        username: username.value,
        password: password.value,
        secret_key: secretKey.value
      });
      if (success) {
        alert('Registration successful! Please login.');
        router.push('/login');
      } else {
        alert('Registration failed. Please check your secret key and try again.');
      }
    };

    return {
      email,
      username,
      password,
      secretKey,
      handleSubmit
    };
  }
};
</script>