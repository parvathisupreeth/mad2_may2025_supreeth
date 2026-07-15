<template>
  <div>
    <Navbar />

    <div class="container-fluid mt-4">
      <div class="row">

        <div class="col-md-2">
          <Sidebar />
        </div>

        <div class="col-md-10">

          <h3 class="mb-4">Companies</h3>

          <table class="table table-bordered table-hover">

            <thead class="table-dark">

              <tr>
                <th>ID</th>
                <th>Company</th>
                <th>HR</th>
                <th>Email</th>
                <th>Status</th>
                <th width="180">Action</th>
              </tr>

            </thead>

            <tbody>

              <tr
                v-for="company in companies"
                :key="company.id">

                <td>{{ company.id }}</td>

                <td>{{ company.company_name }}</td>

                <td>{{ company.hr_name }}</td>

                <td>{{ company.email }}</td>

                <td>
                  <span :class="{
                    'text-warning': company.approval_status === 'pending',
                    'text-success': company.approval_status === 'approved' && !company.is_blacklisted,
                    'text-danger': company.approval_status === 'rejected' || company.is_blacklisted
                  }">
                    {{ company.is_blacklisted ? 'Blacklisted' : company.approval_status }}
                  </span>
                </td>

                <td>

                  <button
                    class="btn btn-success btn-sm me-2"
                    v-if="company.approval_status=='pending'"
                    @click="approveCompany(company.id)">

                    Approve

                  </button>

                  <button
                    class="btn btn-danger btn-sm me-2"
                    v-if="company.approval_status=='pending'"
                    @click="rejectCompany(company.id)">

                    Reject

                  </button>

                  <button
                    class="btn btn-dark btn-sm"
                    v-if="company.approval_status=='approved' && !company.is_blacklisted"
                    @click="blacklistCompany(company.id)">

                    Blacklist

                  </button>

                  <button
                    class="btn btn-success btn-sm"
                    v-if="company.is_blacklisted"
                    @click="unblacklistCompany(company.id)">

                    Remove Blacklist

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

const companies = ref([])

async function loadCompanies(){

    const response = await api.get(
        "/admin/companies",
        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }
        }
    )

    companies.value = response.data

}

async function approveCompany(id){

    await api.put(
        `/admin/company/${id}/approve`,
        {},
        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }
        }
    )

    loadCompanies()

}

async function rejectCompany(id){

    await api.put(
        `/admin/company/${id}/reject`,
        {},
        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }
        }
    )

    loadCompanies()

}

async function blacklistCompany(id){

    await api.put(
        `/admin/company/${id}/blacklist`,
        {},
        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }
        }
    )

    loadCompanies()

}

async function unblacklistCompany(id){

    await api.put(
        `/admin/company/${id}/unblacklist`,
        {},
        {
            headers:{
                Authorization:`Bearer ${localStorage.getItem("token")}`
            }
        }
    )

    loadCompanies()

}

onMounted(loadCompanies)

</script>