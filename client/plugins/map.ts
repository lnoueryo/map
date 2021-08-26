interface Station {id: number, prefecture: string, name: string, lat: number, lng: number, line_id: number, order: number, company_id: number,city_code: string}
interface City {prefecture_id: string, city_code: number, city: string, polygons: Polygon[][]}
interface Polygon {"lat":number,"lng":number}
// import store from '~/store/home'
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
    public infoWindow: any | google.maps.InfoWindow = null
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
    makePolygon(coordinates: {lat: number,lng: number}[], i: number) {
        const polygon = new google.maps.Polygon({
            paths: coordinates,
            strokeColor: "red",
            strokeOpacity: 0.5,
            strokeWeight: 2,
            fillColor: "#00bb93",
            fillOpacity: 0.1,
        });
        polygon.setMap(this.map);
        return polygon
    }
    makeMarker(station: Station, icon: string = '', text: string = '') {
        // var MarkerWithLabel = require('markerwithlabel')(google.maps);
        // const icon = {
        //     url: url,
        //     labelOrigin: new google.maps.Point(-100, -100),
        //     // path: google.maps.SymbolPath.CIRCLE,//シンボル円
        //     // scale: 22,           //サイズ
        //     // fillColor: '#fff',  //塗り潰し色
        //     // fillOpacity: 0.8,   //塗り潰し透過率
        //     // strokeColor: "red", //枠線の色
        //     // strokeWeight: 8,    //枠線の幅
        // }
        // const icon = {
        //     labelOrigin: new google.maps.Point(100, 50),
        //     url: url,
        //     size: new google.maps.Size(100, 40),
        //     Origin: new google.maps.Point(100, 100),
        //     anchor: new google.maps.Point(100, 40),
        //   }
        // const label = text
        //             ? {text:  text, color: '#363636', fontSize: '12px', fontWeight: '900', labelOrigin: new google.maps.Point(50, 9)}
        //             : ''
        const marker = new google.maps.Marker({
            map: this.map,
            position: new google.maps.LatLng(station.lat, station.lng),
            icon: icon,
            // label: label,
            visible: false,
            // opacity: 0.8,
            // optimized: true,
        });
        return marker
    }
    makePolyline(path: {color: string, polygon: google.maps.LatLng[]} ) {
        const polyline = new google.maps.Polyline({
            map: this.map,
            path:path.polygon,
            strokeColor: path.color,
            strokeOpacity: 0.9,
            strokeWeight: 3
        });
        return polyline;
    }
    hideMarkers(payload: google.maps.Marker[][]) {
        payload.forEach((markers) => {
            markers.forEach((marker) => {
                marker.setVisible(false);
            })
        })
    }
    resetPolygon(polygons: google.maps.Polygon[][]) {
        polygons.forEach(cityPolygon => {
            cityPolygon.forEach(polygon => {
                polygon.setMap(null)
            });
        });
    }
    resetPolyline(payload: google.maps.Polyline[]) {
        payload.forEach(polyline => {
            polyline.setMap(null);
        });
    }
    async resetMarkers(payload: google.maps.Marker[][]) {
        payload.forEach((markers) => {
            markers.forEach((marker) => {
                marker.setMap(null);
            })
        })
    }
    changeIcon(markers_obj: google.maps.Marker[][], icon: string) {
        markers_obj.forEach((markers)=>{
            markers.forEach((marker)=>{
                marker.setIcon(icon);
            })
        })
    }
    currentBounds() {
        const bounds = this.map.getBounds() as google.maps.LatLngBounds;
        const north = bounds.getNorthEast().lat();
        const south = bounds.getSouthWest().lat();
        const east = bounds.getNorthEast().lng();
        const west = bounds.getSouthWest().lng();
        return {south: south, north: north,east: east, west: west};
    }
    focusMarker(station: Station, num: number) {
        this.map.setZoom(num);
        const latLng = new google.maps.LatLng(station.lat, station.lng);
        this.map.panTo(latLng);
    }
    boundsFilterForMarker(marker_obj: google.maps.Marker[][], markerSwitch: boolean) {
        if(markerSwitch) {
            const currentBounds = this.currentBounds()
            const markerInFrame: google.maps.Marker[] = []
            marker_obj.forEach((markers) => {
                markers.forEach((marker) => {
                    const lat = marker.getPosition()?.lat() as number;
                    const lng = marker.getPosition()?.lng() as number;
                    const verticalCondition = currentBounds.west < lng && currentBounds.east > lng;
                    const horizontalCondition = currentBounds.south < lat && currentBounds.north > lat;
                    if(verticalCondition && horizontalCondition) {
                        markerInFrame.push(marker)
                        marker.setVisible(true)
                    } else {
                        marker.setVisible(false)
                    }
                })
            })
            return markerInFrame;
        } else {
            marker_obj.forEach((markers) => {
                markers.forEach((marker) => {
                    marker.setVisible(false)
                })
            })
            return;
        }
    }
    cityFilterForMarker(markers: google.maps.Marker[], polygonArray: google.maps.Polygon[][], selectedCityItems: any) {
        if(markers) {
            if(selectedCityItems.length !== 0) {
                markers.forEach((marker) => {
                    const latLng = marker.getPosition() as google.maps.LatLng;
                    const isContain = polygonArray.some((polygons: any) => {
                        return polygons.filter((polygon: google.maps.Polygon) => google.maps.geometry.poly.containsLocation(latLng, polygon)).length !== 0;
                    })
                    isContain ? marker.setVisible(true) : marker.setVisible(false)
                })
            } else {
                markers.forEach((marker) => {
                    marker.setVisible(true)
                })
            }
        }
    }
    createInfoWindow(marker: google.maps.Marker, text: string) {
        const infoWindow = new google.maps.InfoWindow({content: `<h3 style="color:black">${text}</h3>`});

        // mouseoverイベントを取得するListenerを追加
        const that = this;
        google.maps.event.addListener(marker, 'mouseover', function(){
            infoWindow.open(that.map, marker);
          });
  
        // mouseoutイベントを取得するListenerを追加
        google.maps.event.addListener(marker, 'mouseout', function(){
            infoWindow.close();
          });
    }
    createMapInfoWindow(lat: number, lng: number, text: string) {
        const latLng = new google.maps.LatLng(lat, lng)
        this.infoWindow = new google.maps.InfoWindow({
            content: `<h3 style="color:black">${text}</h3>`,
            position: latLng
        });
        this.infoWindow.open(this.map);
    }
    // removeMapInfoWindow(lat: number, lng: number, text: string) {
    //     this.map.removeInf
    // }
  }
  
  // plugin
  export default ({ app }: any, inject: any) => {
    // ... get status logic
    const tokyoBounds = {north: 35.860687,south: 35.530351, west: 138.9403931, east: 139.9368243}
    const options = {
        center: new google.maps.LatLng( 35.6729712, 139.7585771 ),
        restriction: {latLngBounds: tokyoBounds, strictBounds: false,},
        zoom: 15,
        mapTypeControl: false,
        fullscreenControl: false,
        streetViewControl: false,
        zoomControl: false,
        styles: [
            {
                "featureType": "all",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "all",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
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
                "featureType": "landscape",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "on"
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
                "elementType": "geometry.fill",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "geometry.stroke",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "labels",
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
                    },
                    {
                        "saturation": "-100"
                    },
                    {
                        "lightness": "-100"
                    },
                    {
                        "weight": "0.01"
                    }
                ]
            },
            {
                "featureType": "poi.place_of_worship",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    },
                    {
                        "saturation": "1"
                    },
                    {
                        "gamma": "10.00"
                    },
                    {
                        "weight": "0.01"
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
            },
            {
                "featureType": "road",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            },
            {
                "featureType": "road",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.highway",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "road.arterial",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "all",
                "stylers": [
                    {
                        "visibility": "simplified"
                    }
                ]
            },
            {
                "featureType": "transit.line",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "off"
                    }
                ]
            },
            {
                "featureType": "transit.station",
                "elementType": "labels.icon",
                "stylers": [
                    {
                        "visibility": "on"
                    }
                ]
            }
        ]
    };

    inject('mapConfig', new MapConfig(options));
  };