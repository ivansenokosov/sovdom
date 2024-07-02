import loadDataAPI from '../api/index'

export default {
    install(Vue) {
        Vue.prototype.$api = loadDataAPI
    }
}