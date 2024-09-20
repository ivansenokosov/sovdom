<script setup lang="ts">
  import {computed, ref, inject} from 'vue'
  import { useUserStore } from '@/stores/user';  
  import { useRouter } from 'vue-router';
  import { useBaseUrl } from '@/stores/baseUrl'
  import InputMask from 'primevue/inputmask';
  import Button from 'primevue/button';
  import InputOtp from 'primevue/inputotp';


  const baseUrl     = useBaseUrl()
  const phone       = ref<string>('')      // телефон для отправки кода
  const code        = ref<string>('')       // введённый код 
  const code_sent   = ref<string>('')  // отправленный код
  const step        = ref<number>(0)        // этап авторизации 0 - телефон не введён, код не отправлен, 1 - телефон введён, код отправлен, 2 - код введён
  const isLoading   = ref<boolean>(false)
  const errCodeMsg  = ref<string>('')
  const router      = useRouter()
  const userStore   = useUserStore()

  const axios: any = inject('axios')

  function randomInteger(min : number, max : number) {
    let rand = min + Math.random() * (max - min);
    return Math.floor(rand);
  }

  const phone_enter_complete = computed(() => {
    const phone_plain = phone.value.replace(/[^+\d]/g, '')
    return phone_plain.length > 11 ? true : false
  })

  const code_enter_complete = computed(() => {
    const code_plain = code.value.replace(/[^+\d]/g, '')
    if (code_plain.length < 4) { errCodeMsg.value = ''}
    return code_plain.length > 3 ? true : false
  })

  const send_sms = () => {
    code_sent.value = String(randomInteger(1000, 9999))
    step.value = 1
  }

  const back = () => {
    phone.value = ''
    code_sent.value = ''
    errCodeMsg.value = ''
    step.value = 0
  }

  const getCitizen = ():void => {
      axios.get(baseUrl.baseUrl + 'catalogs/cities/')
           .then((response: { data: any }) => {
        console.log(response.data)
      })
  }


  const submitForm = () : void => {

    // проверяем на правильность ввода кода

    if (code.value != code_sent.value) {
      errCodeMsg.value = 'Код введён неверно'
    } else {
      isLoading.value = true
      errCodeMsg.value = ''
      step.value = 2
      
      try {
        // создание нового пользователя или авторизация в имеющемся
        userStore.userId = '111' // устанавливаем id пользователя
        router.push('/cabinet')
      } catch (error: unknown) {
        if (error instanceof Error) {
          console.log(error.message)
        }
      } finally {
        isLoading.value = false
      }
    }
  }
</script>

<template>
  <div class="flex justify-content-center p-2">
      <div class="surface-card p-4 shadow-1 border-round w-full lg:w-6" style="background-color: blueviolet">
        <div class="text-center mb-3">
          <h1 class="font-bold text-center text-2xl mb-10">Вход в Совдом</h1>
        </div>

          <form @submit.prevent="submitForm">
            <div class="w-full flex justify-content-center" v-if="step === 0">
                <InputMask id="phone" inputStyleClass="text-base text-color surface-overlay p-2 border-1 border-solid surface-border border-round appearance-none outline-none focus:border-primary w-full" size="large" v-model="phone" mask="+7 (999) 999-99-99" placeholder="Телефон"/>
            </div>              
            <div class="w-full flex justify-content-center mb-2 mt-2" v-if="step === 1">
              <span>Отпрален код {{ code_sent }} на {{ phone }}<br></span>
            </div>
            <div class="w-full flex justify-content-center" v-if="step === 1">
                <!-- <InputMask id="code" v-model="code" mask="9999" placeholder="Код"/> -->
                <InputOtp v-model="code" />
            </div>              
            <div class="flex justify-content-center mt-1" v-if="code_enter_complete">
              <div style="color: red">{{ errCodeMsg }}</div>
            </div>
            <div class="card flex justify-center" v-if="step === 2">
                <span>Отпрален код {{ code_sent }} на {{ phone }}<br></span>
                <span>Введён код {{ code }}<br></span>
            </div>              
            <div class="pt-5">
              <div class="flex justify-content-center gap-5">
                <Button label="Получить код" class="w-full mt-2" v-if="step === 0 && phone_enter_complete" @click="send_sms"/>
              </div>
              <div class="flex justify-content-center gap-5">
                  <Button type="submit"  class="w-full mt-2" label="Войти" :loading="isLoading" icon="pi pi-user" v-if="step === 1 && code_enter_complete && !errCodeMsg"/>
              </div>
              <div class="flex justify-content-center gap-5">
                <Button link label="Изменить номер"  class="w-full mt-2" v-if="step === 1" @click="back"/>
              </div>
            </div>
          </form>
      </div>
  </div>
</template>
