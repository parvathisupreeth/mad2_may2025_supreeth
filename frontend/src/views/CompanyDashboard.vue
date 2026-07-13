<template>
  <div>
  <Navbar />

  <div class="container-fluid mt-4">

    <div class="row">

      <div class="col-md-2">
        <Sidebar />
      </div>

      <div class="col-md-10">

        <h2>Company Dashboard</h2>

        <div class="row mt-4">

          <div class="col-md-3">
            <DashboardCard
              title="My Drives"
              :value="stats.drives"
            />
          </div>

          <div class="col-md-3">
            <DashboardCard
              title="Applications"
              :value="stats.applications"
            />
          </div>

          <div class="col-md-3">
            <DashboardCard
              title="Interviews"
              :value="stats.interviews"
            />
          </div>

        </div>

        <hr>

        <div class="mt-4">

          <button
            class="btn btn-primary me-2"
            @click="$router.push('/company/create-drive')">

            Create Drive

          </button>

          <button
            class="btn btn-success me-2"
            @click="$router.push('/company/drives')">

            My Drives

          </button>

          <button
            class="btn btn-warning"
            @click="$router.push('/company/applications')">

            Applications

          </button>

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

    drives:0,
    applications:0,
    interviews:0

})

onMounted(async()=>{

    try{

        const res = await api.get("/company/dashboard",{

            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }

        })

        Object.assign(stats,res.data)

    }

    catch(err){

        console.log(err)

    }

})
</script>