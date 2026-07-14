<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary shadow-sm">
    <div class="container-fluid">

      <span class="navbar-brand fw-bold">
        Placement Portal
      </span>

      <div class="d-flex align-items-center gap-2 ms-auto">
        <!-- Profile Button -->
        <button
          v-if="role"
          class="btn btn-outline-light d-flex align-items-center gap-2"
          @click="openProfile"
        >
          <div
            class="rounded-circle bg-white text-primary d-flex align-items-center justify-content-center fw-bold"
            style="width:28px;height:28px;font-size:13px;flex-shrink:0;"
          >
            {{ avatarLetter }}
          </div>
          <span>Profile</span>
        </button>

        <button class="btn btn-light" @click="logout">Logout</button>
      </div>
    </div>
  </nav>

  <!-- Profile Modal Backdrop -->
  <Teleport to="body">
    <div v-if="showModal" class="profile-modal-backdrop" @click.self="closeModal">
      <div class="profile-modal-card">
        <!-- Header -->
        <div class="profile-modal-header">
          <div class="profile-avatar">{{ avatarLetter }}</div>
          <div>
            <h5 class="mb-0 fw-bold">Edit Profile</h5>
            <small class="text-muted">{{ role === 'student' ? 'Student' : 'Company' }} Account</small>
          </div>
          <button class="btn-close ms-auto" @click="closeModal"></button>
        </div>

        <!-- Loading spinner -->
        <div v-if="loadingProfile" class="text-center py-4">
          <div class="spinner-border text-primary" role="status"></div>
        </div>

        <!-- Error -->
        <div v-if="profileError" class="alert alert-danger mx-3 mt-3 mb-0">{{ profileError }}</div>
        <div v-if="successMsg" class="alert alert-success mx-3 mt-3 mb-0">{{ successMsg }}</div>

        <!-- Student Form -->
        <form v-if="!loadingProfile && role === 'student'" @submit.prevent="saveProfile" class="profile-modal-body">
          <div class="mb-3">
            <label class="form-label fw-semibold">Full Name</label>
            <input v-model="form.name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold">Branch</label>
            <input v-model="form.branch" type="text" class="form-control" required />
          </div>
          <div class="row g-3 mb-3">
            <div class="col-6">
              <label class="form-label fw-semibold">CGPA</label>
              <input v-model.number="form.cgpa" type="number" step="0.01" min="0" max="10" class="form-control" required />
            </div>
            <div class="col-6">
              <label class="form-label fw-semibold">Graduation Year</label>
              <input v-model.number="form.graduation_year" type="number" min="2020" max="2035" class="form-control" required />
            </div>
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold">Phone</label>
            <input v-model="form.phone" type="tel" class="form-control" placeholder="Optional" />
          </div>
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="button" class="btn btn-outline-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
              Save Changes
            </button>
          </div>
        </form>

        <!-- Company Form -->
        <form v-if="!loadingProfile && role === 'company'" @submit.prevent="saveProfile" class="profile-modal-body">
          <div class="mb-3">
            <label class="form-label fw-semibold">Company Name</label>
            <input v-model="form.company_name" type="text" class="form-control" required />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold">HR Name</label>
            <input v-model="form.hr_name" type="text" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold">HR Email</label>
            <input v-model="form.hr_email" type="email" class="form-control" />
          </div>
          <div class="mb-3">
            <label class="form-label fw-semibold">Website</label>
            <input v-model="form.website" type="url" class="form-control" placeholder="https://example.com" />
          </div>
          <div class="row g-3 mb-3">
            <div class="col-6">
              <label class="form-label fw-semibold">Approval Status</label>
              <input :value="form.approval_status" class="form-control" disabled />
            </div>
            <div class="col-6">
              <label class="form-label fw-semibold">Blacklisted</label>
              <input :value="form.is_blacklisted ? 'Yes' : 'No'" class="form-control" disabled />
            </div>
          </div>
          <div class="d-flex justify-content-end gap-2 mt-4">
            <button type="button" class="btn btn-outline-secondary" @click="closeModal">Cancel</button>
            <button type="submit" class="btn btn-primary" :disabled="saving">
              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useRouter, useRoute } from "vue-router"
import api from "../services/api"

const router = useRouter()
const route  = useRoute()


const role = ref(localStorage.getItem("role"))
watch(route, () => {
  role.value = localStorage.getItem("role")
})

const showModal    = ref(false)
const loadingProfile = ref(false)
const saving       = ref(false)
const profileError = ref("")
const successMsg   = ref("")
const form         = ref({})

const avatarLetter = computed(() => {
  if (role.value === "student") return (form.value.name        || "S").charAt(0).toUpperCase()
  if (role.value === "company") return (form.value.company_name || "C").charAt(0).toUpperCase()
  return "U"
})

const authHeaders = () => ({
  headers: { Authorization: `Bearer ${localStorage.getItem("token")}` }
})

async function openProfile() {
  showModal.value    = true
  loadingProfile.value = true
  profileError.value = ""
  successMsg.value   = ""
  form.value         = {}
  try {
    const endpoint = role.value === "student" ? "/student/profile" : "/company/profile"
    const res = await api.get(endpoint, authHeaders())
    form.value = { ...res.data }
  } catch (err) {
    profileError.value = err.response?.data?.message || "Failed to load profile."
  } finally {
    loadingProfile.value = false
  }
}

async function saveProfile() {
  saving.value       = true
  profileError.value = ""
  successMsg.value   = ""
  try {
    const endpoint = role.value === "student" ? "/student/profile" : "/company/profile"

    let payload
    if (role.value === "student") {
      payload = {
        name:            form.value.name,
        branch:          form.value.branch,
        cgpa:            form.value.cgpa,
        graduation_year: form.value.graduation_year,
        phone:           form.value.phone
      }
    } else {
      payload = {
        company_name: form.value.company_name,
        hr_name:      form.value.hr_name,
        hr_email:     form.value.hr_email,
        website:      form.value.website
      }
    }

    await api.put(endpoint, payload, authHeaders())
    successMsg.value = "Profile updated successfully!"
    setTimeout(() => { successMsg.value = "" }, 3000)
  } catch (err) {
    profileError.value = err.response?.data?.message || "Failed to save profile."
  } finally {
    saving.value = false
  }
}

function closeModal() {
  showModal.value    = false
  profileError.value = ""
  successMsg.value   = ""
}

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  role.value = null
  router.push("/login")
}
</script>

<style scoped>
.profile-modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  backdrop-filter: blur(3px);
  z-index: 1050;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.profile-modal-card {
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 520px;
  max-height: 90vh;
  overflow-y: auto;
  animation: slideUp 0.25s ease;
}

@keyframes slideUp {
  from { transform: translateY(30px); opacity: 0; }
  to   { transform: translateY(0);    opacity: 1; }
}

.profile-modal-header {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 1.4rem 1.5rem 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.profile-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: #0d6efd;
  color: #fff;
  font-size: 1.3rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.profile-modal-body {
  padding: 1.4rem 1.5rem 1.5rem;
}
</style>