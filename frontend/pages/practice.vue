<template>
    <div>
        <div style="background-color:white">
            <textarea name="" id="" cols="30" rows="10">{{companies}}</textarea>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            companies: []
        }
    },
    async created(){
        const response = await this.$axios.$get('/api/map/');
        this.companies = response;
    }
}
</script>