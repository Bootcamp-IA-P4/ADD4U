// Mock authentication service
class AuthService {
  constructor() {
    this.users = [
      { id: 1, email: 'admin@minicelia.es', password: 'admin123', role: 'admin', name: 'Administrador' },
      { id: 2, email: 'user@minicelia.es', password: 'user123', role: 'user', name: 'Usuario' }
    ]
  }

  async login(credentials) {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const { email, password } = credentials
    const user = this.users.find(u => u.email === email && u.password === password)
    
    if (!user) {
      throw new Error('Credenciales inválidas')
    }

    const { password: _, ...userWithoutPassword } = user
    const token = btoa(JSON.stringify({ userId: user.id, exp: Date.now() + 24 * 60 * 60 * 1000 }))
    
    localStorage.setItem('auth_token', token)
    localStorage.setItem('user_data', JSON.stringify(userWithoutPassword))
    
    return userWithoutPassword
  }

  logout() {
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user_data')
  }

  getCurrentUser() {
    try {
      const token = localStorage.getItem('auth_token')
      const userData = localStorage.getItem('user_data')
      
      if (!token || !userData) return null
      
      const tokenData = JSON.parse(atob(token))
      if (tokenData.exp < Date.now()) {
        this.logout()
        return null
      }
      
      return JSON.parse(userData)
    } catch (error) {
      this.logout()
      return null
    }
  }

  isAuthenticated() {
    return !!this.getCurrentUser()
  }
}

export const authService = new AuthService()
