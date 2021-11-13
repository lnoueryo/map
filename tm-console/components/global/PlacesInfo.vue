<template>
    <div>
        <div class="places" v-if="placesData">
            <!-- <h2 class="text-center">{{placesData.name}}</h2> -->
            <v-carousel hide-delimiters v-if="photos.length !== 0" :height="height">
                <v-carousel-item v-for="(item,i) in photos" :key="i" :src="item"></v-carousel-item>
            </v-carousel>
            <div>
            </div>
            <div class="reviews-container" v-if="placesData.reviews">
                <div class="reviews-top">
                <div class="average-score">{{placesData.rating}}</div>
                <span class="star5_rating" :data-rate="roundHalf(placesData.rating)"></span>
                </div>
                <div>
                <div class="review" v-for="(review, i) in placesData.reviews" :key="i">
                    <div class="d-flex">
                    <img class="avatar" :src="review.profile_photo_url">
                    <div class="rating-container">
                        <div>{{review.author_name}}</div>
                        <div>
                        <span class="star5_rating" :data-rate="review.rating"></span>
                        <span>{{review.relative_time_description}}</span>
                        </div>
                    </div>
                    </div>
                    <div>
                    <p class="review-comment">{{review.text}}</p>
                    </div>
                </div>
                </div>
            </div>
            <!-- {{placesData}} -->
        </div>
    </div>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
    props: ['placesData', 'height'],
    // data() {
    //     return {
    //         placesData: {
    //             "business_status": "OPERATIONAL",
    //             "geometry": { "location": { "lat": 35.6815604, "lng": 139.7654768 },
    //             "viewport": { "south": 35.6803229197085, "west": 139.7637324197085, "north": 35.68302088029149, "east": 139.7664303802915 } },
    //             "icon": "https://maps.gstatic.com/mapfiles/place_api/icons/v1/png_71/generic_business-71.png",
    //             "icon_background_color": "#13B5C7",
    //             "icon_mask_base_uri": "https://maps.gstatic.com/mapfiles/place_api/icons/v2/generic_pinlet",
    //             "name": "東京駅丸の内駅前広場",
    //             "photos": [ { "height": 5472, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/107100879015383217735\">Zhenxi Li</a>" ], "width": 3648 }, { "height": 3024, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/107534026239032847747\">飯野博之</a>" ], "width": 4032 }, { "height": 3024, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/112919347860249593221\">あい</a>" ], "width": 4032 }, { "height": 3024, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/106986579069823166050\">S T</a>" ], "width": 4032 }, { "height": 5304, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/108956831964921348934\">hikoasis HIKO</a>" ], "width": 7952 }, { "height": 812, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/108099695809898769895\">Takeshi Kawaguchi</a>" ], "width": 1273 }, { "height": 5333, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/100687654252760844590\">550329 kuma</a>" ], "width": 3000 }, { "height": 2160, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/105645305350059415885\">toshiyuki aoki</a>" ], "width": 3840 }, { "height": 5480, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/108858409606141400205\">大野茂</a>" ], "width": 2740 }, { "height": 5504, "html_attributions": [ "<a href=\"https://maps.google.com/maps/contrib/118351018620963383908\">itsuro itu</a>" ], "width": 3096 } ], "plus_code": { "compound_code": "MQJ8+J5 日本、東京都千代田区", "global_code": "8Q7XMQJ8+J5" }, "types": [ "tourist_attraction", "point_of_interest", "establishment" ], "url": "https://maps.google.com/?cid=8146915592005061530", "vicinity": "千代田区丸の内１丁目９", "html_attributions": []
    //         },
    //         photos: [ "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uECqDyQ9W4z7DfUYu83Z-B86KBzyQO3z5Rjy3H6yBfEozgCA5NSI1XiifOH7FqDjA2ucP4ZF5Iu5w7XWfxKBGFK4L7YJSn9vJQTmpFPPhuzAjVMuJMx-N5bU_TnHLLJofNH6nNlSPcVi5UKZ41dg8jEx8vY8rm6Q7Xy9woKltNUGqHKD&3u1248&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=15366", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uEBU6RWHIFDcdCI7gG3WWMHWSMPa_8krJazy9CYmrnM_sT-3ht_JXqGYPYV941HebE5OsgY7PIwcze3jfLGXEpakCuW1DNyjzi8-3OcpVkE_JhvZZkfM8N4RLNNhYtUKMIWRxmOMotPW0Fi2lbrYtR6pfuz_phXCLLJAwt9R0ZULf-Ja&3u1280&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=99469", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uED4dd0ri7vjbkRwWZut4P2k3ofb84QGgmbtp1KK8H3ETci8OTN4YPX8ezlsd5m-DTebxcj-sUaW8SSKJ14T_KyAgF4SVKGNo9AO3DRX_1lwaJg2gj_b42c09XrxFrvT6__63W2i3JKCBNbXX3e0sGShPpq_ASu3DyOm4e1jk3ThmFY9&3u1600&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=36964", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uEAEic9aLDGDGHDC8TbfDIp0KTVmZjrbNCFolxS7Hyf1nkZkG8H_M9i9sArBoSCi1a2xMlEbOmX3tUh7T6s2Zek_PQHmilHGXczxCED1Ag2BZx-rpj5hQz66KS9rWmy_kBjY64rv2STsNJzuDi8Hhdq93C6qouXDFWeaSOu_1P-21-g9&3u2048&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=81056", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uECub5UJxcbuxTc9gPagAmEEBRHM0yGHy9HNF0EeJQqea_jkCbMG9gJbRiKoGrjWKpF17yfGrfO0v0DsUwvluDMWxnMpvS_ppigTwt_kfr_1JFSTuAlhg_8vabHckSVL_6Viwlx2mqsKSI0SsISMoSKjITV2PWwMp6POxhqIUNOJKa0&3u3840&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=61531", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uECZFHEDetVa_a2V9Bws_S6NtrfXwvygu8oxR6rIiHE0EwCCMiNRnFoKnXMQd_bgSiE6wN2QDxUI0tJF86drfBHyAxRcwpRP_sMcT-ynv3lRuEM-xj2jw447OQmhjFKiWvkB6WSIB8roX2dYSbn61Tyg8rDANKIHrFRgYSnPaczjivUo&3u1280&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=87782", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uEB0ZWyjZMKQEe_iCAqtr0lKwGaIylfpBAv2mGT9IvLWzu9Blmle5ed_HF61fs_ADWpfCli5ObcWu45l3UoWo5q4Y5NCEP0HHSXmgkLWktdTBhs9MjyWXDaHE2nGIrbICvnQ4zNpuGHE3u000bXPEZUnNf9hT2xHmzD0uYLFzhIOi7vS&3u640&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=11434", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uEBu5C8TjNR6sv78wpNaXSO1jIDpsl9y_KvYeYECAtmhIjvqWB-HthFlEc_17WybJyR7mqLNgto3VZKtQs-lwJbmhFBWIuT4mNPixRQ98An6McOo_AJJF0gUMtDM2lOwIH1keOvD9b2N8fhMdvVrkz7uIzsMGrJKCDfBVUjzXCCHdsSc&3u5184&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=123037", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uED73vy9a2yQELsi3pt5Aobz56dyWao8bWWfdSCibYv6FsYpC-2GmLoDFEjFuiPbJVrQ9DN821ACR9qcA4MEOQ8flRukFs51Tok3gGuc9Ay80qI8r-lEih6GY7jm8KzWIiNjQy9ZXqeKypjzzowtpEhJ99CGVVuRNjmbyXqPi-AhPtxI&3u1024&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=62123", "https://maps.googleapis.com/maps/api/place/js/PhotoService.GetPhoto?1sAap_uEC2aJR_OtflKSus6EqL_sGpcjHG5lxPKVmu95BMtP0MW7NJjrpBs2CgGct6P8-ea4LdKhMFHIx5EA0IFw8w9t8_tEm8qDan3zyoc0kUVLRYsy0niaXUJm2RgMQAfFv3NzXbEQVjYo5xU3QEQjj-MgbIr-jedupB7fdEBHiW5y3Az6aP&3u1024&5m1&2e1&callback=none&key=AIzaSyD9HrNKbbZYgXvtJ3t-1tDoj3J1FHoL_C8&token=97177" ]
    //     }
    // },
    computed: {
        photos() {
            if (this.placesData) {
                const photos = this.placesData?.photos.map((photo: google.maps.places.PlacePhoto) => {
                    return photo.getUrl();
                })
                console.log(photos)
                return photos;
            }
            return [];
        }
    },
    methods: {
        roundHalf(num: number) {
            return Math.round(num * 2) / 2;
        }
    }
})
</script>

<style lang="scss" scoped>
.reviews-container {
    padding: 10px;
}
.places {
    background-color: white;
    color: black;
}
/* レビュー */
.reviews-top {
  display: flex;
  align-items: baseline;
  p {
    margin-left: 5px;
  }
  .average-score {
    font-size: 37px;
    font-weight: bold;
  }
  .star5_rating {
    margin-left: 15px;
  }
}
.review {
  margin: 20px 0;
  .review-comment {
    font-size: 14px;
  }
}
.d-flex {
  display: flex;
}
.avatar {
  width: 48px;
  height: 48px;
}
.rating-container {
  margin-left: 10px;
  font-size: 15px;
}
/* レート */
.star5_rating {
  position: relative;
  z-index: 0;
  display: inline-block;
  white-space: nowrap;
  margin-right: 10px;
  color: #CCCCCC;
}
.star5_rating:before, .star5_rating:after {
  content: '★★★★★';
}
.star5_rating:after {
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  overflow: hidden;
  white-space: nowrap;
  color: #ffcf32;
}
/* 星5 */
.star5_rating[data-rate="5"]:after {
  width: 100%;
}
/* 星4.5 */
.star5_rating[data-rate="4.5"]:after {
  width: 90%;
}
/* 星4 */
.star5_rating[data-rate="4"]:after {
  width: 80%;
}
/* 星3.5 */
.star5_rating[data-rate="3.5"]:after {
  width: 70%;
}
/* 星3 */
.star5_rating[data-rate="3"]:after {
  width: 60%;
}
/* 星2.5 */
.star5_rating[data-rate="2.5"]:after {
  width: 50%;
}
/* 星2 */
.star5_rating[data-rate="2"]:after {
  width: 40%;
}
/* 星1.5 */
.star5_rating[data-rate="1.5"]:after {
  width: 30%;
}
/* 星1 */
.star5_rating[data-rate="1"]:after {
  width: 20%;
}
/* 星0.5 */
.star5_rating[data-rate="0.5"]:after {
  width: 10%;
}
/* 星0 */
.star5_rating[data-rate="0"]:after {
  width: 0%;
}</style>