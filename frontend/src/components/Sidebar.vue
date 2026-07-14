<template>
  <div class="list-group">

    <!-- Admin -->
    <template v-if="role === 'admin'">
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/admin')">
        Dashboard
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/admin/students')">
        Students
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/admin/companies')">
        Companies
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/admin/drives')">
        Placement Drives
      </button>
    </template>

    <!-- Company -->
    <template v-else-if="role === 'company'">
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/company')">
        Dashboard
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/company/create-drive')">
        Create Drive
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/company/drives')">
        My Drives
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/company/applications')">
        Applications
      </button>
    </template>

    <!-- Student -->
    <template v-else-if="role === 'student'">
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/student')">
        Dashboard
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/student/drives')">
        Browse Drives
      </button>
      <button
        class="list-group-item list-group-item-action"
        @click="$router.push('/student/applications')">
        My Applications
      </button>
    </template>

  </div>
</template>

<script setup>
import { ref } from "vue"

const role = ref(localStorage.getItem("role"))
</script>