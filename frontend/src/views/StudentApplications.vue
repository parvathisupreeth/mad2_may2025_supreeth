<template>
<div>

  <Navbar />

  <div class="container-fluid mt-4">
    <div class="row">

      <div class="col-md-2">
        <Sidebar />
      </div>

      <div class="col-md-10">

        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="mb-0">My Applications</h3>
          <div class="d-flex align-items-center gap-2">
            <span class="badge bg-secondary fs-6">{{ filtered.length }} application(s)</span>
            <button
              id="export-csv-btn"
              class="btn btn-outline-success btn-sm"
              :disabled="exporting"
              @click="exportCSV"
            >
              <span v-if="exporting" class="spinner-border spinner-border-sm me-1" role="status"></span>
              <span v-else>📥</span>
              {{ exporting ? 'Sending...' : 'Export CSV' }}
            </button>
          </div>
        </div>

        <!-- Export alert toast -->
        <div
          v-if="exportMsg"
          class="alert d-flex align-items-center gap-2 mb-3"
          :class="exportSuccess ? 'alert-success' : 'alert-danger'"
          role="alert"
        >
          <span>{{ exportSuccess ? '✅' : '❌' }}</span>
          <span>{{ exportMsg }}</span>
          <button type="button" class="btn-close ms-auto" @click="exportMsg = ''"></button>
        </div>

        <!-- Search -->
        <div class="input-group mb-4" style="max-width:420px;">
          <span class="input-group-text">🔍</span>
          <input
            type="text"
            class="form-control"
            placeholder="Search by company or job title..."
            v-model="searchQuery"
          />
          <button
            v-if="searchQuery"
            class="btn btn-outline-secondary"
            @click="searchQuery = ''">✕</button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center py-5">
          <div class="spinner-border text-primary" role="status"></div>
          <p class="mt-2 text-muted">Loading your applications...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="filtered.length === 0" class="text-center py-5 text-muted">
          <p class="fs-5">
            {{ searchQuery ? 'No results match your search.' : "You haven't applied to any drives yet." }}
          </p>
          <button
            v-if="!searchQuery"
            class="btn btn-primary"
            @click="$router.push('/student/drives')">
            Browse Drives
          </button>
        </div>

        <!-- Table -->
        <div v-else class="card shadow-sm">
          <div class="table-responsive">
            <table class="table table-hover align-middle mb-0">
              <thead class="table-dark">
                <tr>
                  <th>#</th>
                  <th>Company</th>
                  <th>Job Title</th>
                  <th>Applied On</th>
                  <th>Status</th>
                  <th>Remarks</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(app, idx) in filtered" :key="app.application_id">
                  <td class="text-muted small">{{ idx + 1 }}</td>
                  <td class="fw-semibold">{{ app.company_name }}</td>
                  <td>{{ app.job_title }}</td>
                  <td class="text-muted small">{{ app.application_date?.slice(0,10) }}</td>
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
                  <td class="text-muted small">{{ app.remarks || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

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

// Export state
const exporting = ref(false)
const exportMsg = ref("")
const exportSuccess = ref(false)

const headers = { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return applications.value
  return applications.value.filter(a =>
    a.company_name.toLowerCase().includes(q) ||
    a.job_title.toLowerCase().includes(q)
  )
})

onMounted(async () => {
  try {
    const res = await api.get("/student/applications", headers)
    applications.value = res.data
  } catch (err) {
    error.value = err.response?.data?.message || "Failed to load applications."
  } finally {
    loading.value = false
  }
})

async function exportCSV() {
  exporting.value = true
  exportMsg.value = ""
  try {
    const res = await api.post("/student/export", {}, headers)
    exportMsg.value = res.data?.message || "Export triggered! Check your email shortly."
    exportSuccess.value = true
  } catch (err) {
    exportMsg.value = err.response?.data?.message || "Failed to trigger export. Try again."
    exportSuccess.value = false
  } finally {
    exporting.value = false
  }
}
</script>
