// import 'roboto-fontface/css/roboto/roboto-fontface.css'
// import 'material-design-icons-iconfont/dist/material-design-icons.css'

import Vue from "vue";
import App from "./App.vue";

import { BaklavaVuePlugin } from "@baklavajs/plugin-renderer-vue";
import "@baklavajs/plugin-renderer-vue/dist/styles.css";

Vue.use(BaklavaVuePlugin);

Vue.config.productionTip = false;
Vue.config.devtools = false;

Vue.prototype.log = console.log;

/* eslint-disable no-new */
new Vue({
    el: "#app",
    render: h => h(App)
});
