<template>
  <div class="landing-container min-vh-100 bg-light d-flex align-items-center py-2">
    <div class="container-fluid bg-white rounded shadow-sm border p-3 p-md-4 my-2 mx-auto" style="max-width: 1300px; width: 95%;">
      
      <!-- Top Section: Image left, content right -->
      <div class="row align-items-center mb-2">
        <div class="col-md-4 text-center mb-2 mb-md-0">
          <img src="../assets/placement_hero.png" alt="Placement Portal Logo" class="img-fluid rounded hero-image" style="max-height: 300px;" />
        </div>
        <div class="col-md-8">
          <h1 class="display-5 text-primary fw-bold mb-1">Placement Portal</h1>
          <blockquote class="blockquote border-start border-4 border-primary ps-3 my-2">
            <p class="fst-italic text-secondary fs-6 mb-0">
              "Where students meet opportunities and companies discover talent."
            </p>
          </blockquote>
          <p class="text-muted mb-3" style="font-size: 0.95rem;">
            Welcome to the university placement portal. This portal bridges the gap between students, companies, and campus administrators to streamline the hiring process, internship opportunities, and placement drives.
          </p>
          <div class="d-flex flex-wrap gap-2">
            <router-link to="/login" class="btn btn-primary btn-sm px-3 py-2">Sign In</router-link>
            <router-link to="/register/student" class="btn btn-outline-success btn-sm px-3 py-2">Student Register</router-link>
            <router-link to="/register/company" class="btn btn-outline-warning btn-sm px-3 py-2">Company Register</router-link>
          </div>
        </div>
      </div>

      <hr class="my-3 text-muted">

      <!-- Bottom Section: 3 Steps -->
      <div class="text-center">
        <h5 class="mb-3 fw-bold">Get Placed in Just 3 Simple Steps</h5>
        <div class="row g-3 justify-content-center">
          
          <div class="col-md-4">
            <div class="card border-0 bg-light p-2 shadow-sm-hover step-card">
              <div class="card-body text-center py-1">
                <div class="step-number bg-primary text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-2">1</div>
                <h6 class="card-title fw-bold mb-1">Create Profile</h6>
                <p class="card-text text-muted mb-0" style="font-size: 0.8rem;">Register your account, fill in your details, CGPA, branch, and upload your resume.</p>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card border-0 bg-light p-2 shadow-sm-hover step-card">
              <div class="card-body text-center py-1">
                <div class="step-number bg-success text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-2">2</div>
                <h6 class="card-title fw-bold mb-1">Apply for Drives</h6>
                <p class="card-text text-muted mb-0" style="font-size: 0.8rem;">Browse through the eligible placement drives posted by verified companies and apply with one click.</p>
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <div class="card border-0 bg-light p-2 shadow-sm-hover step-card">
              <div class="card-body text-center py-1">
                <div class="step-number bg-warning text-white rounded-circle d-inline-flex align-items-center justify-content-center mb-2">3</div>
                <h6 class="card-title fw-bold mb-1">Track Status</h6>
                <p class="card-text text-muted mb-0" style="font-size: 0.8rem;">Keep track of your applications, interview schedules, and shortlisting results in real-time.</p>
              </div>
            </div>
          </div>

        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.landing-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}
.hero-image {
  filter: drop-shadow(0px 8px 16px rgba(0, 0, 0, 0.1));
}
.step-number {
  width: 36px;
  height: 36px;
  font-size: 1.1rem;
  font-weight: bold;
}
.step-card {
  transition: transform 0.2s, box-shadow 0.2s;
}
.step-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 15px rgba(0,0,0,0.08) !important;
}
</style>
