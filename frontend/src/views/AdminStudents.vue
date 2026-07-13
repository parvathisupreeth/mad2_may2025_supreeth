<template>
  <div>
    <Navbar />

    <div class="container-fluid mt-4">
      <div class="row">

        <div class="col-md-2">
          <Sidebar />
        </div>

        <div class="col-md-10">

          <h3 class="mb-4">Students</h3>

          <div class="row mb-3">
            <div class="col-md-4">
              <input
                type="text"
                class="form-control"
                placeholder="Search by Name or Branch..."
                v-model="search"
              >
            </div>
          </div>

          <table class="table table-bordered table-hover">

            <thead class="table-dark">
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Branch</th>
                <th>CGPA</th>
                <th>Graduation Year</th>
                <th>Status</th>
                <th width="150">Action</th>
              </tr>
            </thead>

            <tbody>

              <tr
                v-for="student in filteredStudents"
                :key="student.id">

                <td>{{ student.id }}</td>
                <td>{{ student.name }}</td>
                <td>{{ student.branch }}</td>
                <td>{{ student.cgpa }}</td>
                <td>{{ student.graduation_year }}</td>

                <td>
                  <span
                    :class="student.is_active ? 'text-success' : 'text-danger'">

                    {{ student.is_active ? "Active" : "Inactive" }}

                  </span>
                </td>

                <td>

                  <button
                    v-if="student.is_active"
                    class="btn btn-danger btn-sm"
                    @click="deactivateStudent(student.id)">

                    Deactivate

                  </button>

                  <button
                    v-else
                    class="btn btn-success btn-sm"
                    @click="activateStudent(student.id)">

                    Activate

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

import { ref, computed, onMounted } from "vue"
import api from "../services/api"

import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"

const students = ref([])
const search = ref("")

const filteredStudents = computed(() => {

    return students.value.filter(student =>

        student.name.toLowerCase().includes(search.value.toLowerCase()) ||

        student.branch.toLowerCase().includes(search.value.toLowerCase())

    )

})

async function loadStudents(){

    try{

        const response = await api.get(
            "/admin/students",
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )

        students.value = response.data

    }

    catch(err){

        console.log(err)

    }

}

async function activateStudent(id){

    try{

        await api.put(
            `/admin/student/${id}/activate`,
            {},
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )

        await loadStudents()

    }

    catch(err){

        console.log(err)

    }

}

async function deactivateStudent(id){

    try{

        await api.put(
            `/admin/student/${id}/deactivate`,
            {},
            {
                headers:{
                    Authorization:`Bearer ${localStorage.getItem("token")}`
                }
            }
        )

        await loadStudents()

    }

    catch(err){

        console.log(err)

    }

}

onMounted(loadStudents)

</script>