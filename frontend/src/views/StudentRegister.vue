<template>
<div class="container mt-5">

    <div class="row justify-content-center">

        <div class="col-md-6">

            <div class="card shadow-sm">

                <div class="card-header text-center">

                    <h3>Student Registration</h3>

                </div>

                <div class="card-body">

                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input class="form-control" v-model="student.username">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Full Name</label>
                        <input class="form-control" v-model="student.name">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input class="form-control" v-model="student.email">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="student.password">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Branch</label>
                        <input class="form-control" v-model="student.branch">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">CGPA</label>
                        <input type="number" step="0.1" class="form-control" v-model="student.cgpa">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Graduation Year</label>
                        <input type="number" class="form-control" v-model="student.graduation_year">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Phone</label>
                        <input class="form-control" v-model="student.phone">
                    </div>

                    <button
                        class="btn btn-success w-100"
                        @click="registerStudent">

                        Register

                    </button>

                    <p class="text-success mt-3">
                        {{ success }}
                    </p>

                    <p class="text-danger">
                        {{ error }}
                    </p>

                    <hr>

                    <button
                        class="btn btn-secondary w-100"
                        @click="$router.push('/login')">

                        Back to Login

                    </button>

                </div>

            </div>

        </div>

    </div>

</div>
</template>

<script setup>

import { reactive, ref } from "vue"
import api from "../services/api"

const student = reactive({

    username:"",
    name:"",
    email:"",
    password:"",
    branch:"",
    cgpa:"",
    graduation_year:"",
    phone:""

})

const success = ref("")
const error = ref("")

async function registerStudent(){

    success.value=""
    error.value=""

    try{

        const response = await api.post(
            "/register/student",
            student
        )

        success.value = response.data.message

        setTimeout(() => {

            window.location.href="/login"

        },1500)

    }

    catch(err){

        error.value = err.response.data.message

    }

}

</script>