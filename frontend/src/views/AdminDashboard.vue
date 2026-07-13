<template>
  <div>
    <Navbar/>

    <div class="container-fluid mt-4">

      <div class="row">

        <div class="col-md-2">

          <Sidebar/>

        </div>

        <div class="col-md-10">

          <h3 class="mb-4">

            Admin Dashboard

          </h3>

          <div class="row">

            <div class="col-md-3">

              <DashboardCard
                title="Students"
                :value="stats.total_students"/>

            </div>

            <div class="col-md-3">

              <DashboardCard
                title="Companies"
                :value="stats.total_companies"/>

            </div>

            <div class="col-md-3">

              <DashboardCard
                title="Drives"
                :value="stats.total_drives"/>

            </div>

            <div class="col-md-3">

              <DashboardCard
                title="Applications"
                :value="stats.total_applications"/>

            </div>

          </div>

        </div>

      </div>

    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from "vue"
import api from "../services/api"

import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"
import DashboardCard from "../components/DashboardCard.vue"

const stats = reactive({
    total_students: 0,
    total_companies: 0,
    total_drives: 0,
    total_applications: 0
})

onMounted(async () => {
    try {
        const response = await api.get("/admin/dashboard", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        })

        Object.assign(stats, response.data)
    } catch (err) {
        console.log(err)
    }
})
</script>