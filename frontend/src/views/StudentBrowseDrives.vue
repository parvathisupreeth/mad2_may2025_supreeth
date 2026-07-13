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
          <h3 class="mb-0">Browse Placement Drives</h3>
          <span class="badge bg-secondary fs-6">{{ filtered.length }} drive(s)</span>
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
          <p class="mt-2 text-muted">Loading drives...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="filtered.length === 0" class="text-center py-5 text-muted">
          <p class="fs-5">{{ searchQuery ? 'No drives match your search.' : 'No approved drives available right now.' }}</p>
        </div>

        <!-- Drive cards -->
        <div v-else class="row g-3">
          <div
            v-for="drive in filtered"
            :key="drive.drive_id"
            class="col-md-6 col-lg-4">
            <div class="card h-100 shadow-sm border-0">
              <div class="card-body d-flex flex-column">

                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h5 class="card-title mb-0">{{ drive.job_title }}</h5>
                </div>
                <p class="text-muted small mb-1">🏢 {{ drive.company_name }}</p>

                <hr class="my-2">

                <div class="row g-1 small mb-3">
                  <div class="col-6">
                    <span class="text-muted">Branch:</span>
                    <span class="fw-semibold ms-1">{{ drive.eligible_branch }}</span>
                  </div>
                  <div class="col-6">
                    <span class="text-muted">Min CGPA:</span>
                    <span class="fw-semibold ms-1">{{ drive.minimum_cgpa }}</span>
                  </div>
                  <div class="col-6">
                    <span class="text-muted">Year:</span>
                    <span class="fw-semibold ms-1">{{ drive.eligible_year }}</span>
                  </div>
                  <div class="col-6">
                    <span class="text-muted">Deadline:</span>
                    <span class="fw-semibold ms-1">{{ drive.application_deadline }}</span>
                  </div>
                </div>

                <div class="mt-auto">
                  <button
                    class="btn w-100"
                    :class="appliedIds.has(drive.drive_id) ? 'btn-success disabled' : 'btn-primary'"
                    :disabled="appliedIds.has(drive.drive_id) || applying === drive.drive_id"
                    @click="applyForDrive(drive.drive_id)">
                    <span v-if="applying === drive.drive_id" class="spinner-border spinner-border-sm me-1"></span>
                    {{ appliedIds.has(drive.drive_id) ? '✓ Applied' : 'Apply Now' }}
                  </button>
                </div>

              </div>
            </div>
          </div>
        </div>

        <p v-if="applyError" class="text-danger mt-3">{{ applyError }}</p>

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

const drives = ref([])
const searchQuery = ref("")
const loading = ref(true)
const applying = ref(null)
const applyError = ref("")
const appliedIds = ref(new Set())

const headers = { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }

const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return drives.value
  return drives.value.filter(d =>
    d.job_title.toLowerCase().includes(q) ||
    d.company_name.toLowerCase().includes(q)
  )
})

async function loadDrives() {
  loading.value = true
  try {
    const [drivesRes, appsRes] = await Promise.all([
      api.get("/drives", headers),
      api.get("/student/applications", headers)
    ])
    drives.value = drivesRes.data
    // Track which drive IDs the student already applied to
    appliedIds.value = new Set(appsRes.data.map(a => a.drive_id))
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

async function applyForDrive(driveId) {
  applying.value = driveId
  applyError.value = ""
  try {
    await api.post(`/student/apply/${driveId}`, {}, headers)
    appliedIds.value = new Set([...appliedIds.value, driveId])
  } catch (err) {
    applyError.value = err.response?.data?.message || "Application failed."
  } finally {
    applying.value = null
  }
}

onMounted(loadDrives)
</script>
