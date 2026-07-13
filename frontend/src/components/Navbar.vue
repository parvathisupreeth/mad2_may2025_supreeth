<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container-fluid">

      <span class="navbar-brand fw-bold">
        Placement Portal
      </span>

      <button
        class="btn btn-light"
        @click="logout">
        Logout
      </button>

    </div>
  </nav>
</template>

<script setup>
import { useRouter } from "vue-router"

const router = useRouter()

function logout() {
    localStorage.removeItem("token")
    localStorage.removeItem("role")
    router.push("/login")
}
</script>