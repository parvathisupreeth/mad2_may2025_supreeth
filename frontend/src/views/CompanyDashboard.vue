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

          <!-- Line Chart for Selected Students Per Drive -->
          <div class="row mt-4">
            <div class="col-md-12">
              <div class="card border-0 shadow-sm">
                <div class="card-body">
                  <h5 class="card-title mb-3">Selected Students per Drive</h5>
                  <div style="position: relative; height: 300px;">
                    <canvas ref="lineChartCanvas"></canvas>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { reactive, onMounted, ref } from "vue"
import api from "../services/api"
import Chart from "chart.js/auto"

import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"
import DashboardCard from "../components/DashboardCard.vue"

const stats = reactive({
    drives: 0,
    applications: 0,
    interviews: 0,
    drive_stats: []
})

const lineChartCanvas = ref(null)
let chartInstance = null

onMounted(async () => {
    try {
        const res = await api.get("/company/dashboard", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        })

        Object.assign(stats, res.data)

        if (stats.drive_stats && stats.drive_stats.length > 0) {
            const labels = stats.drive_stats.map(item => item.job_title)
            const data = stats.drive_stats.map(item => item.selected_count)

            chartInstance = new Chart(lineChartCanvas.value, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Students Selected',
                        data: data,
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                        pointBackgroundColor: '#198754',
                        pointRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                stepSize: 1
                            }
                        }
                    }
                }
            })
        }
    } catch (err) {
        console.log(err)
    }
})
</script>