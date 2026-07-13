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

            <div class="col-md-12 mt-3">
              <div class="card border-0 shadow-sm">
                <div class="card-body d-flex justify-content-between align-items-center">
                  <div>
                    <h5 class="mb-1">My Resume</h5>
                    <p class="text-muted small mb-0">
                      {{ profile.resume_path ? 'Resume uploaded.' : 'No resume uploaded yet.' }}
                    </p>
                  </div>
                  <div class="d-flex align-items-center gap-3">
                    <a v-if="profile.resume_path" :href="'http://127.0.0.1:5000' + profile.resume_path" target="_blank" class="btn btn-outline-primary">
                      👁️ View Resume
                    </a>
                    <input type="file" ref="resumeInput" class="d-none" accept=".pdf,.doc,.docx" @change="uploadResume" />
                    <button class="btn btn-primary" @click="$refs.resumeInput.click()" :disabled="uploading">
                      <span v-if="uploading" class="spinner-border spinner-border-sm me-1"></span>
                      {{ profile.resume_path ? 'Update Resume' : 'Upload Resume' }}
                    </button>
                  </div>
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
const uploading = ref(false)
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

async function uploadResume(event) {
  const file = event.target.files[0]
  if (!file) return

  uploading.value = true
  error.value = ""

  const formData = new FormData()
  formData.append("resume", file)

  try {
    const res = await api.post("/student/resume", formData, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
        "Content-Type": "multipart/form-data"
      }
    })
    profile.value.resume_path = res.data.resume_path
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to upload resume."
  } finally {
    uploading.value = false
    event.target.value = "" // reset input
  }
}
</script>