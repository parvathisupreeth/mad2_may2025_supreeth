<template>

<div class="container vh-100 d-flex justify-content-center align-items-center">

<div class="card shadow p-4" style="width: 450px; max-width: 100%;">

<div class="card-header text-center">

<h3 class="text-center">
  Placement Portal Login
</h3>

<p class="text-center text-muted">
  login
</p>

</div>

<div class="card-body">

<div class="mb-3">

<label>Email</label>

<input
type="email"
class="form-control"
v-model="email">

</div>

<div class="mb-3">

<label>Password</label>

<input
type="password"
class="form-control"
v-model="password">

</div>

<button
class="btn btn-primary w-100"
@click="login">

Login

</button>

<p class="text-danger mt-3">

{{ error }}

</p>

<hr>

<button
class="btn btn-success w-100 mb-2"
@click="$router.push('/register/student')">

Student Registration

</button>

<button
class="btn btn-warning w-100"
@click="$router.push('/register/company')">

Company Registration

</button>

</div>

</div>

</div>

</template>

<script setup>

import { ref } from "vue"

import { useRouter } from "vue-router"

import api from "../services/api"

const router = useRouter()

const email = ref("")

const password = ref("")

const error = ref("")

async function login(){

    try{

        const response = await api.post("/login",{

            email:email.value,

            password:password.value

        })

        const { role, approval_status, is_blacklisted } = response.data

        // Block pending / blacklisted companies before storing anything
        if(role === "company"){
            if(is_blacklisted){
                error.value = "Your company has been blacklisted. Please contact the administrator."
                return
            }
            if(approval_status !== "approved"){
                error.value = "Your registration is pending admin approval. Please wait for approval before logging in."
                return
            }
        }

        localStorage.setItem("token", response.data.access_token)
        localStorage.setItem("role", role)

        if(role === "admin"){
            router.push("/admin")
        }
        else if(role === "student"){
            router.push("/student")
        }
        else{
            router.push("/company")
        }

    }

    catch(err){

        error.value = err.response?.data?.message || "Login failed"

    }

}

</script>