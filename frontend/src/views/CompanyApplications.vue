<template>
<div>

  <Navbar />

  <div class="container-fluid mt-4">
    <div class="row">

      <!-- Sidebar -->
      <div class="col-md-2">
        <Sidebar />
      </div>

      <!-- Main Content -->
      <div class="col-md-10">

        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="mb-0">Applications Received</h3>
          <span class="badge bg-secondary fs-6">{{ filtered.length }} applicant(s)</span>
        </div>

        <!-- Search Bar -->
        <div class="input-group mb-4" style="max-width: 400px;">
          <span class="input-group-text">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
              <path d="M11.742 10.344a6.5 6.5 0 1 0-1.397 1.398h-.001q.044.06.098.115l3.85 3.85a1 1 0 0 0 1.415-1.414l-3.85-3.85a1 1 0 0 0-.115-.1zM12 6.5a5.5 5.5 0 1 1-11 0 5.5 5.5 0 0 1 11 0"/>
            </svg>
          </span>
          <input
            type="text"
            class="form-control"
            placeholder="Search by student name..."
            v-model="searchQuery"
          />
          <button
            v-if="searchQuery"
            class="btn btn-outline-secondary"
            @click="searchQuery = ''">
            ✕
          </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-2 text-muted">Loading applications...</p>
        </div>

        <!-- Empty state -->
        <div v-else-if="filtered.length === 0" class="text-center py-5 text-muted">
          <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" fill="currentColor" class="mb-3 opacity-50" viewBox="0 0 16 16">
            <path d="M8 1a2 2 0 0 1 2 2v4H6V3a2 2 0 0 1 2-2m3 6V3a3 3 0 0 0-6 0v4a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2"/>
          </svg>
          <p class="fs-5">{{ searchQuery ? 'No students match your search.' : 'No applications received yet.' }}</p>
        </div>

        <!-- Table -->
        <div v-else class="card shadow-sm">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-dark">
                <tr>
                  <th>#</th>
                  <th>Student Name</th>
                  <th>Branch</th>
                  <th>CGPA</th>
                  <th>Year</th>
                  <th>Drive / Job Title</th>
                  <th>Applied On</th>
                  <th>Resume</th>
                  <th>Status</th>
                  <th>Update Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(app, idx) in filtered" :key="app.application_id">
                  <td class="text-muted small">{{ idx + 1 }}</td>
                  <td class="fw-semibold">{{ app.student_name }}</td>
                  <td>{{ app.branch }}</td>
                  <td>{{ app.cgpa }}</td>
                  <td>{{ app.graduation_year }}</td>
                  <td>
                    <span class="badge bg-light text-dark border">{{ app.job_title }}</span>
                  </td>
                  <td class="text-muted small">{{ app.application_date }}</td>
                  <td>
                    <a v-if="app.resume_path" :href="'http://127.0.0.1:5000' + app.resume_path" target="_blank" class="text-primary text-decoration-none small fw-semibold">
                      👁️ View
                    </a>
                    <span v-else class="text-muted small">—</span>
                  </td>
                  <td>
                    <span
                      class="badge"
                      :class="{
                        'bg-secondary': app.status === 'applied',
                        'bg-warning text-dark': app.status === 'Shortlisted',
                        'bg-success': app.status === 'Selected',
                        'bg-danger': app.status === 'Rejected'
                      }">
                      {{ app.status }}
                    </span>
                  </td>
                  <td>
                    <div class="d-flex gap-1 flex-wrap">
                      <select
                        class="form-select form-select-sm"
                        style="width: 130px;"
                        v-model="app._newStatus">
                        <option value="">-- pick --</option>
                        <option value="Shortlisted">Shortlisted</option>
                        <option value="Selected">Selected</option>
                        <option value="Rejected">Rejected</option>
                      </select>
                      <button
                        class="btn btn-sm btn-primary"
                        :disabled="!app._newStatus || app._updating"
                        @click="updateStatus(app)">
                        <span v-if="app._updating" class="spinner-border spinner-border-sm"></span>
                        <span v-else>Save</span>
                      </button>
                    </div>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Error -->
        <p v-if="error" class="text-danger mt-3">{{ error }}</p>

      </div>
    </div>
  </div>

</div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import api from "../services/api"
import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"

const applications = ref([])
const searchQuery = ref("")
const loading = ref(true)
const error = ref("")

const headers = {
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
}

// Client-side filter by student name
const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return applications.value
  return applications.value.filter(a =>
    a.student_name.toLowerCase().includes(q)
  )
})

async function loadApplications() {
  loading.value = true
  error.value = ""
  try {
    const res = await api.get("/company/applications", headers)
    // Attach reactive UI fields to each record
    applications.value = res.data.map(a => ({
      ...a,
      _newStatus: "",
      _updating: false
    }))
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load applications."
  } finally {
    loading.value = false
  }
}

async function updateStatus(app) {
  if (!app._newStatus) return
  app._updating = true
  try {
    await api.put(
      `/company/application/${app.application_id}/status`,
      { status: app._newStatus, remarks: "" },
      headers
    )
    app.status = app._newStatus
    app._newStatus = ""
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to update status."
  } finally {
    app._updating = false
  }
}

onMounted(loadApplications)
</script>