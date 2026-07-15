<template>
<div>

    <Navbar />

    <div class="container-fluid mt-4">

        <div class="row">

            <div class="col-md-2">
                <Sidebar />
            </div>

            <div class="col-md-10">

                <div class="card shadow-sm">

                    <div class="card-header">
                        <h4>Create Placement Drive</h4>
                    </div>

                    <div class="card-body">

                        <div class="mb-3">
                            <label>Job Title</label>
                            <input
                                class="form-control"
                                v-model="drive.job_title">
                        </div>

                        <div class="mb-3">
                            <label>Job Description</label>
                            <textarea
                                class="form-control"
                                rows="4"
                                v-model="drive.job_description">
                            </textarea>
                        </div>

                        <div class="mb-3">
                            <label class="form-label">Eligible Branch</label>
                            <div class="d-flex flex-wrap gap-2">
                                <div
                                    v-for="branch in allBranches"
                                    :key="branch"
                                    class="form-check form-check-inline">
                                    <input
                                        class="form-check-input"
                                        type="checkbox"
                                        :id="'branch-' + branch"
                                        :value="branch"
                                        v-model="selectedBranches">
                                    <label
                                        class="form-check-label"
                                        :for="'branch-' + branch">
                                        {{ branch }}
                                    </label>
                                </div>
                            </div>
                        </div>

                        <div class="mb-3">
                            <label>Minimum CGPA</label>
                            <input
                                type="number"
                                step="0.1"
                                class="form-control"
                                v-model="drive.minimum_cgpa">
                        </div>

                        <div class="mb-3">
                            <label>Eligible Year</label>
                            <input
                                type="number"
                                class="form-control"
                                v-model="drive.eligible_year">
                        </div>

                        <div class="mb-3">
                            <label>Application Deadline</label>
                            <input
                                type="date"
                                class="form-control"
                                v-model="drive.application_deadline">
                        </div>

                        <button
                            class="btn btn-primary"
                            @click="createDrive">

                            Create Drive

                        </button>

                        <p class="text-success mt-3">
                            {{ success }}
                        </p>

                        <p class="text-danger">
                            {{ error }}
                        </p>

                    </div>

                </div>

            </div>

        </div>

    </div>

</div>
</template>

<script setup>
import { reactive, ref } from "vue"
import { useRouter } from "vue-router"
import api from "../services/api"

import Navbar from "../components/Navbar.vue"
import Sidebar from "../components/Sidebar.vue"

const router = useRouter()

const allBranches = [
    "CSE",
    "ECE",
    "EEE",
    "IT",
    "Mechanical",
    "Civil",
    "Chemical",
    "Biotechnology",
    "MBA",
    "MCA",
    "Foundation",
    "Diploma",
    "BSc Data Science"
]

const selectedBranches = ref([])

const drive = reactive({
    job_title: "",
    job_description: "",
    minimum_cgpa: "",
    eligible_year: "",
    application_deadline: ""
})

const success = ref("")
const error = ref("")

const currentYear = new Date().getFullYear()
const today = new Date().toISOString().split("T")[0]

function clearForm() {
    drive.job_title = ""
    drive.job_description = ""
    drive.minimum_cgpa = ""
    drive.eligible_year = ""
    drive.application_deadline = ""
    selectedBranches.value = []
}

async function createDrive() {

    success.value = ""
    error.value = ""

    // Job Title
    if (!drive.job_title.trim()) {
        error.value = "Job Title is required."
        return
    }

    // Description
    if (drive.job_description.trim().length < 20) {
        error.value = "Job Description should contain at least 20 characters."
        return
    }

    // Branches
    if (selectedBranches.value.length === 0) {
        error.value = "Select at least one eligible branch."
        return
    }

    // CGPA
    const cgpa = parseFloat(drive.minimum_cgpa)

    if (isNaN(cgpa) || cgpa < 0 || cgpa > 10) {
        error.value = "Minimum CGPA must be between 0 and 10."
        return
    }

    // Graduation Year
    const year = parseInt(drive.eligible_year)

    if (isNaN(year) || year < currentYear || year > currentYear + 5) {
        error.value = `Eligible Year should be between ${currentYear} and ${currentYear + 5}.`
        return
    }

    // Deadline
    if (!drive.application_deadline) {
        error.value = "Select application deadline."
        return
    }

    if (drive.application_deadline < today) {
        error.value = "Application deadline cannot be in the past."
        return
    }

    try {

        const response = await api.post(
            "/company/drive",
            {
                ...drive,
                minimum_cgpa: cgpa,
                eligible_year: year,
                eligible_branch: selectedBranches.value.join(",")
            },
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`
                }
            }
        )

        success.value = response.data.message

        clearForm()

        setTimeout(() => {
            router.push("/company/drives")
        }, 1200)

    } catch (err) {

        error.value =
            err.response?.data?.message ||
            "Unable to create placement drive."

    }
}
</script>

