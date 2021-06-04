import Vue from 'vue'

export default Vue.extend({
    data() {
        return {
            map: null,
            overview: null,
            polygons: []
        }
    },
    methods:{
        allPolygons(polygons: google.maps.Polygon[][]){
            this.resetPolygons(polygons)
            polygons.forEach((polygon: google.maps.Polygon[]) => {
                polygon.forEach((coordinates) => {
                    coordinates.setMap(this.map)
                });
            });
        },
        resetPolygons(polygons: google.maps.Polygon[][]){
            polygons.forEach(polygon => {
                polygon.forEach(coordinates => {
                    coordinates.setMap(null)
                });
            });
        },
        makePolygon(index: number){
            const polygons: google.maps.Polygon[] = this.polygons[index]
            polygons.forEach((polygon) => {
                polygon.addListener("click", () => {
                    this.resetPoly(index)
                });
                polygon.setMap(this.map);
            });
        },
        resetPoly(index: number){
            const polygons: google.maps.Polygon[] = this.polygons[index]
            polygons.forEach(polygon => {
                polygon.setMap(null)
            });
        },
        clamp(num: number, min: number, max: number) {
            return Math.min(Math.max(num, min), max);
        },
        resetMapListeners(...arg: string[]){
            arg.forEach(event => {
                google.maps.event.clearListeners((this as any).map, event);
            });
        },
        currentPosition(){
            const infoWindow = new google.maps.InfoWindow();
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (position) => {
                        const coordinate = {
                            lat: position.coords.latitude,
                            lng: position.coords.longitude,
                        };
                        const marker = new google.maps.Marker({
                            position: coordinate,
                            map: this.map,
                        });
                        // infoWindow.setPosition(coordinate);
                        // infoWindow.setContent("Location found.");
                        // infoWindow.open(this.map);a
                        (this as any).map.panTo(coordinate);
                    },
                    () => {
                        console.log('hello')
                    // handleLocationError(true, infoWindow, map.getCenter()!);
                    }
                );
            } else {
                // handleLocationError(false, infoWindow, map.getCenter()!);
            }
        }
    }
})