<template>
<div class="container mt-5">

    <div class="row justify-content-center">

        <div class="col-md-6">

            <div class="card shadow-sm">

                <div class="card-header text-center">

                    <h3>Company Registration</h3>

                </div>

                <div class="card-body">

                    <div class="mb-3">
                        <label class="form-label">Username</label>
                        <input class="form-control" v-model="company.username">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Company Name</label>
                        <input class="form-control" v-model="company.company_name">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Email</label>
                        <input class="form-control" v-model="company.email">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="company.password">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">HR Name</label>
                        <input class="form-control" v-model="company.hr_name">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">HR Email</label>
                        <input class="form-control" v-model="company.hr_email">
                    </div>

                    <div class="mb-3">
                        <label class="form-label">Website</label>
                        <input class="form-control" v-model="company.website">
                    </div>

                    <button
                        class="btn btn-warning w-100"
                        @click="registerCompany">

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

const company = reactive({

    username:"",
    company_name:"",
    email:"",
    password:"",
    hr_name:"",
    hr_email:"",
    website:""

})

const success = ref("")
const error = ref("")

async function registerCompany(){

    success.value=""
    error.value=""

    try{

        const response = await api.post(
            "/register/company",
            company
        )

        success.value = response.data.message

        setTimeout(()=>{

            window.location.href="/login"

        },1500)

    }

    catch(err){

        error.value = err.response.data.message

    }

}

</script>