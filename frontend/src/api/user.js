import { request } from './request'

export async function register(username, password) {
  return await request('/api/auth/register', {
    method: 'POST',
    body: { username, password }
  })
}

export async function login(username, password) {
  return await request('/api/auth/login', {
    method: 'POST',
    body: { username, password }
  })
}
