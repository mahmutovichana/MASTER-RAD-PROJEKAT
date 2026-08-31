const STORAGE_KEY = "rbi.active-role";

export function getActiveRole(): string | undefined {
  if (typeof window === "undefined") return undefined;
  return window.sessionStorage.getItem(STORAGE_KEY) || undefined;
}

export function setActiveRole(role: string) {
  if (typeof window !== "undefined") window.sessionStorage.setItem(STORAGE_KEY, role);
}

export function clearActiveRole() {
  if (typeof window !== "undefined") window.sessionStorage.removeItem(STORAGE_KEY);
}
