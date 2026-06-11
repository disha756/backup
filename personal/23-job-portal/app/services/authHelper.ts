export function setToken(token: string) {
  if (typeof window === "undefined") return;

  localStorage.setItem("token", token);
}

export function logout() {
  if (typeof window === "undefined") return;

  localStorage.removeItem("token");
}

export function getToken() {
  if (typeof window === "undefined") return null;

  return localStorage.getItem("token");
}
