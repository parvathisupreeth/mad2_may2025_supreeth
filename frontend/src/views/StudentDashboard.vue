<template>
<div>

  <Navbar />

  <div class="container-fluid mt-4">
    <div class="row">

      <div class="col-md-2">
        <Sidebar />
      </div>

      <div class="col-md-10">

        <!-- Loading -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
        </div>

        <template v-else-if="profile">

          <!-- Welcome header -->
          <div class="d-flex align-items-center gap-3 mb-4">
            <div
              class="rounded-circle bg-primary text-white d-flex align-items-center justify-content-center fw-bold fs-3"
              style="width:60px;height:60px;flex-shrink:0;">
              {{ profile.name.charAt(0).toUpperCase() }}
            </div>
            <div>
              <h3 class="mb-0">Welcome, {{ profile.name }} 👋</h3>
              <small class="text-muted">{{ profile.email }}</small>
            </div>
          </div>

          <!-- Profile cards -->
          <div class="row g-3 mb-4">

            <div class="col-md-3">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                  <div class="text-muted small mb-1">Branch</div>
                  <div class="fw-bold fs-5">{{ profile.branch }}</div>
                </div>
              </div>
            </div>

            <div class="col-md-3">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                  <div class="text-muted small mb-1">CGPA</div>
                  <div class="fw-bold fs-5">{{ profile.cgpa }}</div>
                </div>
              </div>
            </div>

            <div class="col-md-3">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                  <div class="text-muted small mb-1">Graduation Year</div>
                  <div class="fw-bold fs-5">{{ profile.graduation_year }}</div>
                </div>
              </div>
            </div>

            <div class="col-md-3">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body text-center">
                  <div class="text-muted small mb-1">Phone</div>
                  <div class="fw-bold fs-5">{{ profile.phone || '—' }}</div>
                </div>
              </div>
            </div>

          </div>

          <!-- Quick actions -->
          <div class="d-flex gap-2 flex-wrap">
            <button
              class="btn btn-primary"
              @click="$router.push('/student/drives')">
              🔍 Browse Drives
            </button>
            <button
              class="btn btn-outline-secondary"
              @click="$router.push('/student/applications')">
              📋 My Applications
            </button>
          </div>

        </template>

        <p v-if="error" class="text-danger mt-3">{{ error }}</p>

      </div>
    </div>
  </div>

</div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import api from "../services/api"
import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"

const profile = ref(null)
const loading = ref(true)
const error = ref("")

const headers = { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }

onMounted(async () => {
  try {
    const res = await api.get("/student/profile", headers)
    profile.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load profile."
  } finally {
    loading.value = false
  }
})
</script>