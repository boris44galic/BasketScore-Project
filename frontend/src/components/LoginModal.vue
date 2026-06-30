<template>
  <Teleport to="body">
    <Transition name="backdrop">
      <div
        v-if="modelValue"
        class="fixed inset-0 z-[60] flex items-center justify-center p-4"
        @click.self="close"
      >
        <div class="absolute inset-0 bg-black/60 backdrop-blur-sm" @click="close" />

        <Transition name="slide-up">
          <div
            v-if="modelValue"
            class="relative z-10 w-full max-w-[480px] max-h-[90vh] overflow-y-auto rounded-2xl border border-[#1e293b] bg-[#0f172a] p-8 shadow-2xl scrollbar-hide"
          >
            <!-- Close -->
            <button
              @click="close"
              class="absolute right-4 top-4 flex h-8 w-8 items-center justify-center rounded-full text-[#64748b] transition hover:bg-[#1e293b] hover:text-white"
              type="button"
            >
              <X class="h-4 w-4" />
            </button>

            <!-- Back to login -->
            <button
              v-if="step === 'register'"
              @click="step = 'login'; error = ''"
              class="absolute left-4 top-4 flex h-8 w-8 items-center justify-center rounded-full text-[#64748b] transition hover:bg-[#1e293b] hover:text-white"
              type="button"
            >
              <ChevronLeft class="h-4 w-4" />
            </button>

            <!-- Logo -->
            <div class="mb-6 text-center">
              <div class="mb-3 text-4xl">🏀</div>
              <h2 class="text-xl font-extrabold text-[#f1f5f9]">
                {{ step === 'login' ? 'Sign in to BasketScore' : 'Create your account' }}
              </h2>
              <p class="mt-1 text-sm text-[#64748b]">
                {{ step === 'login' ? 'Track your favourite teams' : 'Join and follow every game' }}
              </p>
            </div>

            <!-- Error -->
            <p v-if="error" class="mb-4 rounded-xl bg-red-500/10 px-4 py-2.5 text-sm text-red-400">
              {{ error }}
            </p>

            <!-- ── Login form -->
            <form v-if="step === 'login'" @submit.prevent="handleLogin" class="flex flex-col gap-3">
              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Email</label>
                <input
                  v-model="loginEmail"
                  type="email"
                  placeholder="example@email.com"
                  autocomplete="email"
                  class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                />
              </div>

              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Password</label>
                <div class="relative">
                  <input
                    v-model="loginPassword"
                    :type="showPassword ? 'text' : 'password'"
                    placeholder="Password"
                    autocomplete="current-password"
                    class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 pr-11 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                  />
                  <button
                    @click="showPassword = !showPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-[#475569] hover:text-[#94a3b8]"
                    type="button"
                  >
                    <EyeOff v-if="!showPassword" class="h-4 w-4" />
                    <Eye v-else class="h-4 w-4" />
                  </button>
                </div>
              </div>

              <button
                :disabled="loading"
                class="mt-1 rounded-xl bg-[#00d4aa] py-3 text-[15px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50 cursor-pointer"
                type="submit"
              >
                <span v-if="!loading">Sign In</span>
                <span v-else>Signing in...</span>
              </button>

              <p class="text-center text-[13px] text-[#64748b]">
                No account?  
                <button
                  @click="step = 'register'; error = ''"
                  class="font-semibold text-[#00d4aa] hover:underline"
                  type="button"
                >
                   Register
                </button>
              </p>
            </form>

            <!-- ── Register form   -->
            <form v-else @submit.prevent="handleRegister" class="flex flex-col gap-3">
              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Username</label>
                <input
                  v-model="regForm.username"
                  type="text"
                  placeholder="username"
                  autocomplete="username"
                  class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                />
              </div>

              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Email</label>
                <input
                  v-model="regForm.email"
                  type="email"
                  placeholder="example@email.com"
                  autocomplete="email"
                  class="w-full rounded-xl border bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                  :class="touched.email && emailError ? 'border-red-500/60' : 'border-[#1e293b]'"
                  @blur="touched.email = true"
                />
                <p v-if="touched.email && emailError" class="mt-1 text-[12px] text-red-400">
                  {{ emailError }}
                </p>
              </div>

              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Password</label>
                <div class="relative">
                  <input
                    v-model="regForm.password"
                    :type="showRegPassword ? 'text' : 'password'"
                    placeholder="Enter your password"
                    autocomplete="new-password"
                    class="w-full rounded-xl border bg-[#1e293b] px-4 py-3 pr-11 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                    :class="touched.password && !passwordValid ? 'border-red-500/60' : 'border-[#1e293b]'"
                    @blur="touched.password = true"
                  />
                  <button
                    @click="showRegPassword = !showRegPassword"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-[#475569] hover:text-[#94a3b8]"
                    type="button"
                  >
                    <EyeOff v-if="!showRegPassword" class="h-4 w-4" />
                    <Eye v-else class="h-4 w-4" />
                  </button>
                </div>
                <div v-if="regForm.password || touched.password" class="mt-2 flex flex-col gap-1 pl-2">
                  <div class="text-[13px]" :class="rules.length ? 'text-[#22c55e]' : 'text-[#64748b]'">
                    Minimum 8 characters
                  </div>
                  <div class="text-[12px]" :class="rules.upper ? 'text-[#22c55e]' : 'text-[#64748b]'">
                     Uppercase letter
                  </div>
                  <div class="text-[13px]" :class="rules.number ? 'text-[#22c55e]' : 'text-[#64748b]'">
                     Number
                  </div>
                </div>
              </div>

              <div>
                <label class="mb-1 block pl-2 text-[13px] font-semibold text-[#94a3b8]">Confirm password</label>
                <div class="relative">
                  <input
                    v-model="regForm.password_confirm"
                    :type="showRegPassword2 ? 'text' : 'password'"
                    placeholder="Repeat password"
                    autocomplete="new-password"
                    class="w-full rounded-xl border bg-[#1e293b] px-4 py-3 pr-11 text-[15px] text-[#f1f5f9] outline-none placeholder:text-[#475569] focus:border-[#00d4aa] transition"
                    :class="touched.password_confirm && matchError ? 'border-red-500/60' : 'border-[#1e293b]'"
                    @blur="touched.password_confirm = true"
                  />
                  <button
                    @click="showRegPassword2 = !showRegPassword2"
                    class="absolute right-3 top-1/2 -translate-y-1/2 text-[#475569] hover:text-[#94a3b8]"
                    type="button"
                  >
                    <Eye v-if="!showRegPassword2" class="h-4 w-4" />
                    <EyeOff v-else class="h-4 w-4" />
                  </button>
                </div>
                <p v-if="touched.password_confirm && matchError" class="mt-1 text-[12px] text-red-400">
                  {{ matchError }}
                </p>
              </div>

              <button
                :disabled="loading"
                class="mt-1 rounded-xl bg-[#00d4aa] py-3 text-[15px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50"
                type="submit"
              >
                <span v-if="!loading">Create Account</span>
                <span v-else>Creating account...</span>
              </button>

              <p class="text-center text-[13px] text-[#64748b]">
                Already a member?
                <button
                  @click="step = 'login'; error = ''"
                  class="font-semibold text-[#00d4aa] hover:underline"
                  type="button"
                >
                  Sign in
                </button>
              </p>
            </form>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { X, Eye, EyeOff, ChevronLeft } from 'lucide-vue-next'
import { login, register } from '../api'
import { useAuth } from '../composables/useAuth'

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue'])

const { loadUser } = useAuth()

const step = ref('login')
const error = ref('')
const loading = ref(false)

// Login
const loginEmail = ref('')
const loginPassword = ref('')
const showPassword = ref(false)

// Register
const regForm = ref({ username: '', email: '', password: '', password_confirm: '' })
const showRegPassword = ref(false)
const showRegPassword2 = ref(false)
const touched = ref({ email: false, password: false, password_confirm: false })

const emailError = computed(() => {
  const v = regForm.value.email
  if (!v) return 'Email is required'
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) return 'Enter a valid email'
  return ''
})

const rules = computed(() => {
  const v = regForm.value.password
  return {
    length: v.length >= 8,
    upper: /[A-Z]/.test(v),
    number: /[0-9]/.test(v),
  }
})

const passwordValid = computed(() => Object.values(rules.value).every(Boolean))

const matchError = computed(() => {
  if (!regForm.value.password_confirm) return 'Please confirm your password'
  if (regForm.value.password !== regForm.value.password_confirm) return 'Passwords do not match'
  return ''
})

const reset = () => {
  step.value = 'login'
  error.value = ''
  loading.value = false
  loginEmail.value = ''
  loginPassword.value = ''
  showPassword.value = false
  regForm.value = { username: '', email: '', password: '', password_confirm: '' }
  showRegPassword.value = false
  showRegPassword2.value = false
  touched.value = { email: false, password: false, password_confirm: false }
}

const close = () => {
  emit('update:modelValue', false)
  reset()
}

watch(
  () => props.modelValue,
  (val) => { document.body.style.overflow = val ? 'hidden' : '' },
)

watch(step, () => { error.value = '' })

const handleLogin = async () => {
  error.value = ''
  if (!loginEmail.value.trim() || !loginPassword.value) {
    error.value = 'Please fill in all fields.'
    return
  }
  loading.value = true
  try {
    await login(loginEmail.value.trim(), loginPassword.value)
    await loadUser()
    close()
  } catch {
    error.value = 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}

const handleRegister = async () => {
  error.value = ''
  touched.value = { email: true, password: true, password_confirm: true }
  if (!regForm.value.username.trim()) { error.value = 'Username is required.'; return }
  if (emailError.value || !passwordValid.value || matchError.value) return
  loading.value = true
  try {
    await register({
      username: regForm.value.username.trim(),
      email: regForm.value.email.trim(),
      password: regForm.value.password,
      password_confirm: regForm.value.password_confirm,
    })
    await loadUser()
    close()
  } catch (err) {
    const data = err.response?.data
    if (data) {
      const first = Object.values(data)[0]
      error.value = Array.isArray(first) ? first[0] : String(first)
    } else {
      error.value = 'Registration failed. Please try again.'
    }
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus {
  -webkit-box-shadow: 0 0 0px 1000px #1e293b inset;
  -webkit-text-fill-color: #f1f5f9;
  caret-color: #f1f5f9;
  transition: background-color 5000s ease-in-out 0s;
}

.backdrop-enter-active,
.backdrop-leave-active {
  transition: opacity 0.25s ease;
}
.backdrop-enter-from,
.backdrop-leave-to {
  opacity: 0;
}
.slide-up-enter-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}
.slide-up-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}
.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(16px);
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
