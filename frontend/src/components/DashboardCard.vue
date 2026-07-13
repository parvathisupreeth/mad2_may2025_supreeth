<template>

<!-- <div class="card shadow-sm text-center"> -->

<div class="card shadow-sm dashboard-card">

<div class="card-body">

<h6>{{ title }}</h6>

<h2>{{ value }}</h2>

</div>

</div>

</template>

<script setup>

defineProps({

    title:String,

    value:[String,Number]

})

</script>