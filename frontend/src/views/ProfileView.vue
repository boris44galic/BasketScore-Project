<template>
  <div class="mx-auto max-w-[1280px] px-4 py-10 sm:px-6">
    <h1 class="mb-8 text-2xl font-extrabold text-[#f1f5f9]">My Profile</h1>

    <div v-if="loading" class="text-center text-[#64748b]">Loading...</div>

    <template v-else>
      <!-- Profile info -->
      <div class="mb-6 rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
        <h2 class="mb-4 text-[15px] font-bold text-[#94a3b8] uppercase tracking-wider">Account Info</h2>

        <div v-if="saveSuccess" class="mb-4 rounded-xl bg-[#22c55e]/10 px-4 py-2.5 text-sm text-[#22c55e]">
          Profile updated successfully.
        </div>
        <div v-if="saveError" class="mb-4 rounded-xl bg-red-500/10 px-4 py-2.5 text-sm text-red-400">
          {{ saveError }}
        </div>

        <div class="flex flex-col gap-4">
          <div>
            <label class="mb-1 block text-[13px] font-semibold text-[#64748b]">Username</label>
            <input
              v-model="form.username"
              type="text"
              class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none focus:border-[#00d4aa] transition"
            />
          </div>
          <div>
            <label class="mb-1 block text-[13px] font-semibold text-[#64748b]">Email</label>
            <input
              :value="user?.email"
              type="email"
              disabled
              class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b]/50 px-4 py-3 text-[15px] text-[#475569] outline-none cursor-not-allowed"
            />
          </div>
        </div>

        <button
          @click="saveProfile"
          :disabled="saving"
          class="mt-5 rounded-xl bg-[#00d4aa] px-6 py-2.5 text-[14px] font-bold text-[#0f172a] transition hover:bg-[#00bfa0] disabled:opacity-50"
        >
          {{ saving ? 'Saving...' : 'Save changes' }}
        </button>
      </div>

      <!-- Change password -->
      <div class="rounded-2xl border border-[#1e293b] bg-[#0f172a] p-6">
        <h2 class="mb-4 text-[15px] font-bold text-[#94a3b8] uppercase tracking-wider">Change Password</h2>

        <div v-if="pwSuccess" class="mb-4 rounded-xl bg-[#22c55e]/10 px-4 py-2.5 text-sm text-[#22c55e]">
          Password changed successfully.
        </div>
        <div v-if="pwError" class="mb-4 rounded-xl bg-red-500/10 px-4 py-2.5 text-sm text-red-400">
          {{ pwError }}
        </div>

        <div class="flex flex-col gap-4">
          <div>
            <label class="mb-1 block text-[13px] font-semibold text-[#64748b]">Current password</label>
            <input
              v-model="pwForm.current"
              type="password"
              placeholder="Current password"
              class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none focus:border-[#00d4aa] transition"
            />
          </div>
          <div>
            <label class="mb-1 block text-[13px] font-semibold text-[#64748b]">New password</label>
            <input
              v-model="pwForm.new"
              type="password"
              placeholder="New password"
              class="w-full rounded-xl border border-[#1e293b] bg-[#1e293b] px-4 py-3 text-[15px] text-[#f1f5f9] outline-none focus:border-[#00d4aa] transition"
            />
          </div>
        </div>

        <button
          @click="savePassword"
          :disabled="pwSaving"
          class="mt-5 rounded-xl bg-[#1e293b] px-6 py-2.5 text-[14px] font-bold text-[#f1f5f9] transition hover:bg-[#334155] disabled:opacity-50"
        >
          {{ pwSaving ? 'Saving...' : 'Change password' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { updateMe, changePassword } from '@/api'

const { user, loadUser } = useAuth()

const loading = ref(true)
const form = ref({ username: '' })

const saving = ref(false)
const saveSuccess = ref(false)
const saveError = ref('')

const pwForm = ref({ current: '', new: '' })
const pwSaving = ref(false)
const pwSuccess = ref(false)
const pwError = ref('')

onMounted(async () => {
  await loadUser()
  form.value.username = user.value?.username ?? ''
  loading.value = false
})

async function saveProfile() {
  saveSuccess.value = false
  saveError.value = ''
  saving.value = true
  try {
    await updateMe({ username: form.value.username })
    await loadUser()
    saveSuccess.value = true
  } catch (err) {
    const data = err.response?.data
    if (data) {
      const first = Object.values(data)[0]
      saveError.value = Array.isArray(first) ? first[0] : String(first)
    } else {
      saveError.value = 'Failed to save changes.'
    }
  } finally {
    saving.value = false
  }
}

async function savePassword() {
  pwSuccess.value = false
  pwError.value = ''
  if (!pwForm.value.current || !pwForm.value.new) {
    pwError.value = 'Please fill in both fields.'
    return
  }
  pwSaving.value = true
  try {
    await changePassword(pwForm.value.current, pwForm.value.new)
    pwSuccess.value = true
    pwForm.value = { current: '', new: '' }
  } catch (err) {
    const data = err.response?.data
    if (data?.current_password) {
      pwError.value = data.current_password[0]
    } else if (data?.new_password) {
      pwError.value = data.new_password[0]
    } else {
      pwError.value = 'Failed to change password.'
    }
  } finally {
    pwSaving.value = false
  }
}
</script>
