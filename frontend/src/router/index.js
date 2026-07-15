import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import StudentRegister from "../views/StudentRegister.vue";
import CompanyRegister from "../views/CompanyRegister.vue";
import LandingView from "../views/LandingView.vue";

import AdminDashboard from "../views/AdminDashboard.vue";
import StudentDashboard from "../views/StudentDashboard.vue";
import CompanyDashboard from "../views/CompanyDashboard.vue";

import AdminCompanies from "../views/AdminCompanies.vue";
import AdminStudents from "../views/AdminStudents.vue"
import AdminDrives from "../views/AdminDrives.vue"

import CompanyDrives from "../views/CompanyDrives.vue"
import CompanyCreateDrive from "../views/CompanyCreateDrive.vue"
import CompanyApplications from "../views/CompanyApplications.vue"

import StudentBrowseDrives from "../views/StudentBrowseDrives.vue"
import StudentApplications from "../views/StudentApplications.vue"

const routes = [
    {
        path: "/",
        component: LandingView
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
    },

    {
        path: "/company/drives",
        component: CompanyDrives
    },

    {
        path: "/company/create-drive",
        component: CompanyCreateDrive
    },

    {
        path: "/company/applications",
        component: CompanyApplications
    },

    {
        path: "/student/drives",
        component: StudentBrowseDrives
    },

    {
        path: "/student/applications",
        component: StudentApplications
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// Public routes — no authentication needed
const publicRoutes = ["/", "/login", "/register/student", "/register/company"];

// Default dashboard per role
const roleDashboard = {
    admin: "/admin",
    student: "/student",
    company: "/company"
};

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem("token");
    const role  = localStorage.getItem("role");

    // Always allow public pages
    if (publicRoutes.includes(to.path)) {
        return next();
    }

    // Not logged in → send to login
    if (!token) {
        return next("/login");
    }

    // Enforce role-based route access
    if (to.path.startsWith("/admin")   && role !== "admin")   return next(roleDashboard[role] || "/login");
    if (to.path.startsWith("/student") && role !== "student") return next(roleDashboard[role] || "/login");
    if (to.path.startsWith("/company") && role !== "company") return next(roleDashboard[role] || "/login");

    return next();
});

export default router;