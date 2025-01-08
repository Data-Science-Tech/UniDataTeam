<script setup>
// 保持最小必要的引用
import { useLayout } from '@/layout/composables/layout';

const { getPrimary } = useLayout();
</script>

<template>
    <div class="card flex justify-center items-center" style="min-height: 80vh">
        <h1 class="text-6xl font-bold text-primary">敬请期待</h1>
    </div>
</template>
