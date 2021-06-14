<template>
    <div>
        <v-col cols="12" sm="6" md="4">
            <v-text-field label="Legal first name*" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
            <v-text-field label="Legal middle name" hint="example of helper text only on focus"></v-text-field>
        </v-col>
        <v-col cols="12" sm="6" md="4">
            <v-text-field label="Legal last name*" hint="example of persistent helper text" persistent-hint required></v-text-field>
        </v-col>
        <v-col cols="12">
            <v-text-field label="Email*" required></v-text-field>
        </v-col>
        <v-col cols="12">
            <v-text-field label="Password*" type="password" required></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
            <v-select :items="['0-17', '18-29', '30-54', '54+']" label="Age*" required></v-select>
        </v-col>
        <v-col cols="12" sm="6">
            <v-autocomplete :items="['Skiing', 'Ice hockey', 'Soccer', 'Basketball', 'Hockey', 'Reading', 'Writing', 'Coding', 'Basejump']" label="Interests" multiple></v-autocomplete>
        </v-col>
    </div>
</template>

<script>
export default {
    props: ['id', 'name', 'company', 'line', 'prefecture', 'lat', 'lng']
}
</script>