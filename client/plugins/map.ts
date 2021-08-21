interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number,city_code: string}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Polygon {"lat":number,"lng":number}

export class MapConfig {
    private options: any
    private markerIcons = {
        jr: '../assets/img/jr.png',
        metro: '../assets/img/metro.png',
        toei: '../assets/img/toei.png',
        keio: '../assets/img/keio.png',
        tokyu: '../assets/img/tokyu.png'
    }
    public map: any | google.maps.Map = null
    public polygons: any | google.maps.Polygon[][] = null
    constructor(options: any) {
      this.options = options
    }

    mapOptions(): any {
        return this.options
    }
    async makeMap(el: HTMLElement) {
        this.map = new google.maps.Map(el, this.mapOptions())
        return this.map
    }
    makePolygon(coordinates: {lat: number,lng: number}[], i: number){
        const polygon = new google.maps.Polygon({
            paths: coordinates,
            strokeColor: "red",
            strokeOpacity: 0.5,
            strokeWeight: 2,
            fillColor: "#00bb93",
            fillOpacity: 0.3,
        });
        polygon.setMap(this.map);
        return polygon
    }
    makeMarker(station: Station, icon: string){
        const marker = new google.maps.Marker({
            map: this.map,
            position: new google.maps.LatLng(station.lat, station.lng),
            icon: icon,
            // optimized: true,
        });
        return marker
    }
    makePolyline(path: {color: string, polygon: google.maps.LatLng[]}){
        const polyline = new google.maps.Polyline({
            map: this.map,
            path:path.polygon,
            strokeColor: path.color,
            strokeOpacity: 0.9,
            strokeWeight: 3
        });
        return polyline;
    }
    resetPolygon(polygons: google.maps.Polygon[][]){
        polygons.forEach(cityPolygon => {
            cityPolygon.forEach(polygon => {
                polygon.setMap(null)
            });
        });
    }
    changeIcon(markers_obj: google.maps.Marker[][], icon: string) {
        markers_obj.forEach((markers)=>{
            markers.forEach((marker)=>{
                marker.setIcon(icon);
            })
        })
    }
    currentBounds(map: google.maps.Map){
        const bounds = map.getBounds() as google.maps.LatLngBounds;
        const north = bounds.getNorthEast().lat();
        const south = bounds.getSouthWest().lat();
        const east = bounds.getNorthEast().lng();
        const west = bounds.getSouthWest().lng();
        return {south: south, north: north,east: east, west: west};
    }
    focusMarker(station: Station, num: number){
        this.map.setZoom(num);
        const latLng = new google.maps.LatLng(station.lat, station.lng);
        this.map.panTo(latLng);
    }
    resetPolyline(payload: google.maps.Polyline[]){
        payload.forEach(polyline => {
            polyline.setMap(null);
        });
    }
    async resetMarkers(payload: google.maps.Marker[][]){
        payload.forEach((markers)=>{
            markers.forEach((marker)=>{
                marker.setMap(null);
            })
        })
    }
  }
  
  // plugin
  export default ({ app }: any, inject: any) => {
    // ... get status logic
    const tokyoBounds = {north: 35.860687,south: 35.530351, west: 138.9403931, east: 139.9368243}
    const options = {
        center: new google.maps.LatLng( 35.6729712, 139.7585771 ),
        restriction: {latLngBounds: tokyoBounds, strictBounds: false,},
        zoom: 14,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false,
        zoomControl: false,
        styles: [
            {
                "featureType": "administrative.country",
                "elementType": "geometry",
                "stylers": [
                    {
                        "visibility": "simplified"
                    },
                    {
                        "hue": "#ff0000"
                    }
                ]
            },
            {
                "featureType": "poi",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.attraction",
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.attraction",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.attraction",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.attraction",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.business",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.business",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.government",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.medical",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.park",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.school",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.school",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.school",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "elementType": "labels.text.fill",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "elementType": "labels.text.stroke",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "poi.sports_complex",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            }
        ]
    };

    inject('mapConfig', new MapConfig(options));
  };