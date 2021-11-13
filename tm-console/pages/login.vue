<template>
  <div>
    <v-main>
      <v-container>
        <div class="form-container">
          <v-form class="form">
            <h4 class="py-2">ログイン</h4>
            <div class="py-2">
              <div class="py-3" style="position: relative">
                <v-text-field
                  color="orange"
                  name="email"
                  label="email"
                  id="email"
                  v-model="loginRequired.email"
                  @keyup.enter.exact="$refs.password.focus()"
                ></v-text-field>
                <transition name="fade">
                  <div v-if="emailValidation" :class="['message', validationColor(emailValidation)]">{{emailValidation}}</div>
                </transition>
              </div>
              <div class="py-3" style="position: relative">
                <v-text-field
                  ref="password"
                  color="orange"
                  name="password"
                  label="password"
                  id="password"
                  v-model="loginRequired.password"
                  @keyup.enter.exact="login"
                ></v-text-field>
                <transition name="fade">
                  <div v-if="passwordValidation" :class="['message', validationColor(passwordValidation)]">{{passwordValidation}}</div>
                </transition>
              </div>
            </div>
            <div class="d-flex align-center justify-space-between wrap">
              <div class="py-2 all-error">
                <transition name="fade">
                  <div v-show="error">{{ error }}</div>
                </transition>
              </div>
              <div class="py-2 btn-container">
                <v-btn ref="submita" style="transition: all .2s" color="orange" @click="login" :disabled="validateAll(emailValidation, passwordValidation)">login</v-btn>
              </div>
            </div>
          </v-form>
        </div>
      </v-container>
    </v-main>
  </div>
</template>
<script lang="ts">
import Vue from "vue";

interface User {
  firstName: string;
  lastName: string;
}
interface DataType {
  loginRequired: {name: string, email: string, password: string};
  error: string | null;
}

export default Vue.extend({
  data(): DataType {
    return {
      loginRequired: {
        name: 'admin',
        email: 'admin@jounetsism.biz',
        password: 'admin',
      },
      error: '',
    };
  },
  computed: {
    emailValidation() {
      const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      const check = re.test(String(this.loginRequired.email).toLowerCase());
      if (check) return 'OK'
      if(!this.loginRequired.email) return ''
      return 'メールアドレスの形式を入力してください';
    },
    passwordValidation() {
      const passwordLength = this.loginRequired.password.length;
      if (passwordLength > 4) return 'OK'
      if(passwordLength == 0) return ''
      return 'パスワードの長さが足りていません';
    },
  },
  methods: {
    async login() {
      const check = this.validateAll(this.emailValidation, this.passwordValidation);
      if(!check) {
        this.error = null;
        const response = await this.$store.dispatch('login', this.loginRequired);
        if(response.status) this.$router.push('/');
        else {
          this.error = response.message;
          this.loginRequired.password = '';
        }
      }
    },
    validationColor(message: string) {
      if (message == 'OK') return 'v-success';
      else if(!message) return '';
      else return 'v-error';
    },
    validateAll(emailValidation: string, passwordValidation: string) {
      if(emailValidation == 'OK' && passwordValidation == 'OK') return false;
      return true;
    }
  },
});
</script>

<style lang="scss">
    .form-container {
      width: 100%;
      max-width: 600px;
      padding: 5px;
      position: fixed;
      left: 50%;
      top: 50%;
      transform: translateX(-50%) translateY(-50%);
    }
  .form {
    padding: 50px;
    background-color: #414141;
    border-radius: 10px;
  }
  .message {
    font-weight: bold;
    position: absolute;
    bottom: 0;
    font-size: 14px;
  }
  .v-success {
    color: #ff9800;
  }
  .v-error {
    color: rgb(255, 0, 0);
  }
  .btn-container {
    text-align: right;
    margin-left: 10px
  }
  .all-error {
    transition: all 1s;
    color: red;
    font-weight: bold;
    font-size: 14px;
    margin-right: 10px
  }
  @media screen and (max-width: 500px) {
    .form {
      padding: 25px;
      .wrap {
        flex-wrap: wrap;
      }
      .btn-container {
        text-align: right;
        margin-left: 0;
        width: 100%;
      }
      .all-error {
        transition: all 1s;
        color: red;
        font-weight: bold;
        font-size: 14px;
        margin-right: 0;
      }
    }
  }
  input:-webkit-autofill {
    transition: background-color 5000s ease-in-out 0s !important;
    -webkit-text-fill-color: white !important;
    -webkit-font-size: 16px !important;
    -webkit-font-family: "Roboto", sans-serif !important;
  }
</style>