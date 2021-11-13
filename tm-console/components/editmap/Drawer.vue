<template>
    <div>
        <div style="width:340px">
            <toggle-switch key="1" class="mr-4" v-model="markerSwitch1" id="markerSwitch" background-color="#ff9800">マーカー</toggle-switch>
            <text-box ref="textBox" :map="map" :switch="markerSwitch1"></text-box>
        </div>
    </div>
</template>