<template>
    <div>
        <v-card>
          <v-card-title>
            <span class="text-h5">User Profile</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>

              </v-row>
            </v-container>
            <small>*indicates required field</small>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="editDialog = false">
              Close
            </v-btn>
            <v-btn color="blue darken-1" text @click="editDialog = false">
              Save
            </v-btn>
          </v-card-actions>
        </v-card>
    </div>
</template>

<script>
  export default {
    props: [''],
    data () {
      return {
        editIndex: -1,
        editDialog: false
      }
    },
    methods: {
      edit(index){
        this.editIndex = index;
        this.editDialog = true;
        this.editData = this.items.find((_, i)=>{
          return i === index;
        })
      }
    },
  }
</script>