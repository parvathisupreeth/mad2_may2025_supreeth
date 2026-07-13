import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import StudentRegister from "../views/StudentRegister.vue";
import CompanyRegister from "../views/CompanyRegister.vue";

import AdminDashboard from "../views/AdminDashboard.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";

import AdminCompanies from "../views/AdminCompanies.vue";
import AdminStudents from "../views/AdminStudents.vue"
import AdminDrives from "../views/AdminDrives.vue"

const routes = [
    {
        path: "/",
        redirect: "/login"
    },

    {
        path: "/login",
        component: LoginView
    },

    {
        path: "/register/student",
        component: StudentRegister
    },

    {
        path: "/register/company",
        component: CompanyRegister
    },

    {
        path: "/admin",
        component: AdminDashboard
    },

    {
        path: "/student",
        component: StudentDashboard
    },

    {
        path: "/company",
        component: CompanyDashboard
    },

    {
        path: "/admin/students",
        component: AdminStudents
    },

    {
        path: "/admin/companies",
        component: AdminCompanies
    },

    {
        path: "/admin/drives",
        component: AdminDrives
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

export default router;