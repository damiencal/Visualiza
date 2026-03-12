<template>
    <footer class="border-t border-border mt-16 py-6 text-center text-sm text-muted-foreground">
        &copy; {{ year }} Visualisa. All rights reserved.
    </footer>
</template>
<script setup lang="ts">
const year = new Date().getFullYear()
</script>
