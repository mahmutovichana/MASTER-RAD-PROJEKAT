import Keycloak from "keycloak-js";
import { runtimeConfig } from "../../runtime-config";

const keycloakUrl = runtimeConfig.KEYCLOAK_URL;
const keycloakRealm = runtimeConfig.KEYCLOAK_REALM;
const keycloakClientId = runtimeConfig.KEYCLOAK_CLIENT_ID;
const keycloakEnabled =
  runtimeConfig.KEYCLOAK_ENABLED?.trim().toLowerCase() === "true";

export const isAuthenticationConfigured = Boolean(
  keycloakEnabled && keycloakUrl && keycloakRealm && keycloakClientId,
);

const keycloak = new Keycloak({
  url: keycloakUrl || "http://localhost",
  realm: keycloakRealm || "not-configured",
  clientId: keycloakClientId || "not-configured",
});

let initialization: Promise<boolean> | undefined;

export function initializeAuthentication(): Promise<boolean> {
  if (!isAuthenticationConfigured) {
    console.warn("Keycloak nije konfigurisan; frontend radi u lokalnom razvojnom režimu.");
    return Promise.resolve(true);
  }
  initialization ??= keycloak.init({
    onLoad: "login-required",
    pkceMethod: "S256",
    checkLoginIframe: false,
  });
  return initialization;
}

export async function getAccessToken(): Promise<string | undefined> {
  if (!isAuthenticationConfigured) return undefined;
  await initializeAuthentication();
  await keycloak.updateToken(30);

  if (!keycloak.token) {
    await keycloak.login({ redirectUri: window.location.href });
    throw new Error("Authentication redirect started.");
  }

  return keycloak.token;
}

export { keycloak };
