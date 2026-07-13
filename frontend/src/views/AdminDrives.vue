<template>
  <div>
    <Navbar />

    <div class="container-fluid mt-4">
      <div class="row">

        <div class="col-md-2">
          <Sidebar />
        </div>

        <div class="col-md-10">

          <h3 class="mb-4">Placement Drives</h3>

          <table class="table table-bordered table-hover">

            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Company</th>
                <th>Job Title</th>
                <th>Eligible Branch</th>
                <th>Min CGPA</th>
                <th>Eligible Year</th>
                <th>Deadline</th>
                <th>Status</th>
                <th width="180">Action</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="drive in drives"
                :key="drive.id">

                <td>{{ drive.id }}</td>
                <td>{{ drive.company_name }}</td>
                <td>{{ drive.job_title }}</td>
                <td>{{ drive.eligible_branch }}</td>
                <td>{{ drive.minimum_cgpa }}</td>
                <td>{{ drive.eligible_year }}</td>
                <td>{{ drive.application_deadline }}</td>
                <td>
                  <span :class="{
                    'text-warning': drive.status === 'pending',
                    'text-success': drive.status === 'approved',
                    'text-danger': drive.status === 'rejected'
                  }">
                    {{ drive.status }}
                  </span>
                </td>
                <td>
                  <button
                    class="btn btn-success btn-sm me-2"
                    v-if="drive.status=='pending'"
                    @click="approveDrive(drive.id)">
                    Approve
                  </button>
                  <button
                    class="btn btn-danger btn-sm"
                    v-if="drive.status=='pending'"
                    @click="rejectDrive(drive.id)">
                    Reject
                  </button>
                </td>
              </tr>
            </tbody>

          </table>

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

const drives = ref([])

async function loadDrives(){
    try {
        const response = await api.get(
            "/admin/drives",
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )
        drives.value = response.data
    } catch(err) {
        console.error(err)
    }
}

async function approveDrive(id){
    try {
        await api.put(
            `/admin/drive/${id}/approve`,
            {},
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )
        loadDrives()
    } catch(err) {
        console.error(err)
    }
}

async function rejectDrive(id){
    try {
        await api.put(
            `/admin/drive/${id}/reject`,
            {},
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )
        loadDrives()
    } catch(err) {
        console.error(err)
    }
}

onMounted(loadDrives)
</script>
