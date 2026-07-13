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

          <!-- Charts -->
          <div class="row mt-4">
            <div class="col-md-6 mb-4">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title mb-3">Student Placement Statistics</h5>
                  <div style="position: relative; height: 280px;">
                    <canvas ref="pieChartCanvas"></canvas>
                  </div>
                </div>
              </div>
            </div>
            <div class="col-md-6 mb-4">
              <div class="card border-0 shadow-sm h-100">
                <div class="card-body">
                  <h5 class="card-title mb-3">Monthly Placement Drives</h5>
                  <div style="position: relative; height: 280px;">
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
    total_students: 0,
    total_companies: 0,
    total_drives: 0,
    total_applications: 0,
    drives_this_month: 0,
    pie_chart: null,
    monthly_drives: []
})

const pieChartCanvas = ref(null)
const lineChartCanvas = ref(null)
let pieChartInstance = null
let lineChartInstance = null

onMounted(async () => {
    try {
        const response = await api.get("/admin/dashboard", {
            headers: {
                Authorization: `Bearer ${localStorage.getItem("token")}`
            }
        })

        Object.assign(stats, response.data)

        // Render Pie Chart
        if (stats.pie_chart && pieChartCanvas.value) {
            pieChartInstance = new Chart(pieChartCanvas.value, {
                type: 'pie',
                data: {
                    labels: ['Placed', 'Rejected', 'Not Applied', 'Other'],
                    datasets: [{
                        data: [
                            stats.pie_chart.placed,
                            stats.pie_chart.rejected,
                            stats.pie_chart.not_applied,
                            stats.pie_chart.other
                        ],
                        backgroundColor: ['#198754', '#dc3545', '#6c757d', '#ffc107']
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false
                }
            })
        }

        // Render Line Chart
        if (stats.monthly_drives && lineChartCanvas.value) {
            const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            lineChartInstance = new Chart(lineChartCanvas.value, {
                type: 'line',
                data: {
                    labels: months,
                    datasets: [{
                        label: 'Drives Launched',
                        data: stats.monthly_drives,
                        borderColor: '#0d6efd',
                        backgroundColor: 'rgba(13, 110, 253, 0.1)',
                        borderWidth: 2,
                        tension: 0.3,
                        fill: true,
                        pointBackgroundColor: '#0d6efd',
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