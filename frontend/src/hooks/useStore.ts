import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { User } from '../types'

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  login: (user: User, token: string) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => {
        localStorage.setItem('token', token)
        set({ user, token, isAuthenticated: true })
      },
      logout: () => {
        localStorage.removeItem('token')
        set({ user: null, token: null, isAuthenticated: false })
      }
    }),
    {
      name: 'auth-storage'
    }
  )
)

// Chat store
interface ChatState {
  messages: Array<{ role: string; content: string }>
  isLoading: boolean
  addMessage: (role: string, content: string) => void
  setLoading: (loading: boolean) => void
  clear: () => void
}

export const useChatStore = create<ChatState>()(
  persist(
    (set) => ({
      messages: [],
      isLoading: false,
      addMessage: (role, content) =>
        set((state) => ({
          messages: [...state.messages, { role, content }]
        })),
      setLoading: (isLoading) => set({ isLoading }),
      clear: () => set({ messages: [] })
    }),
    {
      name: 'chat-storage',
      partialize: (state) => ({ messages: state.messages })
    }
  )
)
