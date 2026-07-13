<template>
  <div class="list-group">

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

  </div>
</template>

<script setup>
</script>