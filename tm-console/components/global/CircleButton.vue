<template>
    <div>
        <div class="circle-button" v-ripple>
            <slot></slot>
        </div>
    </div>
</template>

<style lang="scss" scoped>
    .circle-button {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 50px;
        height: 50px;
        border: solid 3px #0044a4;
        border-radius: 50%;
        transition: all .5s;
        cursor: pointer;
    }
    .circle-button:hover {
        background-color: #0044a48e
    }
</style>