<template>
<div>

  <Navbar />

  <div class="container-fluid mt-4">
    <div class="row">

      <div class="col-md-2">
        <Sidebar />
      </div>

      <div class="col-md-10">

        <!-- Header row -->
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h3 class="mb-0">My Placement Drives</h3>
          <span class="badge bg-secondary fs-6">{{ filtered.length }} drive(s)</span>
        </div>

        <!-- Search bar -->
        <div class="input-group mb-4" style="max-width:420px;">
          <span class="input-group-text">🔍</span>
          <input
            type="text"
            class="form-control"
            placeholder="Search by job title or branch..."
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
          <p class="mt-2 text-muted">Loading...</p>
        </div>

        <!-- Empty -->
        <div v-else-if="filtered.length === 0" class="text-center py-5 text-muted">
          <p class="fs-5">{{ searchQuery ? 'No drives match your search.' : 'No drives yet. Create one!' }}</p>
          <button
            v-if="!searchQuery"
            class="btn btn-primary"
            @click="$router.push('/company/create-drive')">
            Create Drive
          </button>
        </div>

        <!-- Table -->
        <template v-else>
          <div class="card shadow-sm">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">

                <thead class="table-dark">
                  <tr>
                    <th>ID</th>
                    <th>Job Title</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Year</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Actions</th>
                  </tr>
                </thead>

                <tbody>
                  <template v-for="drive in filtered" :key="drive.id">

                    <!-- Normal row -->
                    <tr>
                      <td class="text-muted small">{{ drive.id }}</td>
                      <td class="fw-semibold">{{ drive.job_title }}</td>
                      <td>{{ drive.eligible_branch }}</td>
                      <td>{{ drive.minimum_cgpa }}</td>
                      <td>{{ drive.eligible_year }}</td>
                      <td class="text-muted small">{{ drive.application_deadline }}</td>
                      <td>
                        <span
                          class="badge"
                          :class="{
                            'bg-warning text-dark': drive.status === 'pending',
                            'bg-success': drive.status === 'approved',
                            'bg-danger': drive.status === 'rejected'
                          }">
                          {{ drive.status }}
                        </span>
                      </td>
                      <td>
                        <div class="d-flex gap-1">
                          <button
                            class="btn btn-sm btn-outline-primary"
                            @click="openEdit(drive)">
                            ✏️ Edit
                          </button>
                          <button
                            class="btn btn-sm btn-danger"
                            @click="deleteDrive(drive.id)">
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>

                    <!-- Inline edit row -->
                    <tr v-if="editingId === drive.id" class="table-light">
                      <td colspan="8">
                        <div class="p-3 border rounded bg-white shadow-sm">
                          <h6 class="mb-3 text-primary">✏️ Edit Drive #{{ drive.id }}</h6>
                          <div class="row g-2">

                            <div class="col-md-4">
                              <label class="form-label small fw-semibold">Job Title</label>
                              <input class="form-control form-control-sm" v-model="editForm.job_title" />
                            </div>

                            <div class="col-md-4">
                              <label class="form-label small fw-semibold">Eligible Branch</label>
                              <input class="form-control form-control-sm" v-model="editForm.eligible_branch" />
                            </div>

                            <div class="col-md-2">
                              <label class="form-label small fw-semibold">Min CGPA</label>
                              <input type="number" step="0.1" class="form-control form-control-sm" v-model="editForm.minimum_cgpa" />
                            </div>

                            <div class="col-md-2">
                              <label class="form-label small fw-semibold">Eligible Year</label>
                              <input type="number" class="form-control form-control-sm" v-model="editForm.eligible_year" />
                            </div>

                            <div class="col-md-4">
                              <label class="form-label small fw-semibold">Application Deadline</label>
                              <input type="date" class="form-control form-control-sm" v-model="editForm.application_deadline" />
                            </div>

                            <div class="col-md-8">
                              <label class="form-label small fw-semibold">Job Description</label>
                              <textarea class="form-control form-control-sm" rows="2" v-model="editForm.job_description"></textarea>
                            </div>

                          </div>

                          <div class="d-flex gap-2 mt-3">
                            <button
                              class="btn btn-primary btn-sm"
                              :disabled="saving"
                              @click="saveEdit(drive.id)">
                              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                              Save Changes
                            </button>
                            <button
                              class="btn btn-outline-secondary btn-sm"
                              @click="cancelEdit">
                              Cancel
                            </button>
                          </div>

                          <p v-if="editError" class="text-danger small mt-2 mb-0">{{ editError }}</p>
                        </div>
                      </td>
                    </tr>

                  </template>
                </tbody>

              </table>
            </div>
          </div>
        </template>

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

// Edit state
const editingId = ref(null)
const editForm = ref({})
const saving = ref(false)
const editError = ref("")

const headers = { headers: { Authorization: `Bearer ${localStorage.getItem("token")}` } }

// Client-side search filter
const filtered = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  if (!q) return drives.value
  return drives.value.filter(d =>
    d.job_title.toLowerCase().includes(q) ||
    d.eligible_branch.toLowerCase().includes(q)
  )
})

async function loadDrives() {
  loading.value = true
  try {
    const res = await api.get("/company/drives", headers)
    drives.value = res.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function openEdit(drive) {
  // If clicking edit on already-open row, close it
  if (editingId.value === drive.id) {
    cancelEdit()
    return
  }
  editingId.value = drive.id
  editError.value = ""
  editForm.value = {
    job_title: drive.job_title,
    job_description: drive.job_description || "",
    eligible_branch: drive.eligible_branch,
    minimum_cgpa: drive.minimum_cgpa,
    eligible_year: drive.eligible_year,
    application_deadline: drive.application_deadline
  }
}

function cancelEdit() {
  editingId.value = null
  editForm.value = {}
  editError.value = ""
}

async function saveEdit(driveId) {
  saving.value = true
  editError.value = ""
  try {
    await api.put(`/company/drive/${driveId}`, editForm.value, headers)
    // Update the local record without a full reload
    const idx = drives.value.findIndex(d => d.id === driveId)
    if (idx !== -1) {
      drives.value[idx] = {
        ...drives.value[idx],
        ...editForm.value,
        // Reset to pending after edit so admin re-approves
        status: "pending"
      }
    }
    cancelEdit()
  } catch (err) {
    editError.value = err.response?.data?.message || "Failed to save changes."
  } finally {
    saving.value = false
  }
}

async function deleteDrive(id) {
  if (!confirm("Delete this drive? This cannot be undone.")) return
  try {
    await api.delete(`/company/drive/${id}`, headers)
    drives.value = drives.value.filter(d => d.id !== id)
    if (editingId.value === id) cancelEdit()
  } catch (err) {
    console.error(err)
  }
}

onMounted(loadDrives)
</script>