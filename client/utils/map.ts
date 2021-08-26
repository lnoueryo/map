import { $axios } from '~/utils/api';
export class Map {
    public mapElement;
    public map;
    constructor(mapElement: HTMLDivElement){
        this.mapElement = mapElement;
        this.map = this.makeMap()
    }
    makeMap(){
        const TOKYO_BOUNDS = {
            north: 35.860687,
            south: 35.530351,
            west: 138.9403931,
            east: 139.9368243,
        };
        const mapOptions = {
            center: new google.maps.LatLng( 35.6729712, 139.7585771 ),
            restriction: {
                latLngBounds: TOKYO_BOUNDS,
                strictBounds: false,
            },
            zoom: 12,
        };
        return new google.maps.Map(this.mapElement as HTMLElement, {
            ...mapOptions,
        });
    }
}
