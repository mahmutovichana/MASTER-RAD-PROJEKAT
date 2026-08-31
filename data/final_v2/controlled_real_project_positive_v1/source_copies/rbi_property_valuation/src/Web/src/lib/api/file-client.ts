import { getAccessToken } from "../auth/keycloak";
import { apiBaseUrl } from "./http-client";

export async function downloadAuthenticatedFile(path: string, fallbackName: string) {
  const accessToken = await getAccessToken();
  const response = await fetch(
    `${apiBaseUrl}${path}`,
    accessToken ? { headers: { authorization: `Bearer ${accessToken}` } } : {},
  );
  if (!response.ok) throw new Error(`Preuzimanje nije uspjelo (${response.status}).`);
  const disposition = response.headers.get("content-disposition") ?? "";
  const match = /filename\*?=(?:UTF-8''|")?([^";]+)/i.exec(disposition);
  const name = match ? decodeURIComponent(match[1]!.replaceAll('"', "")) : fallbackName;
  const url = URL.createObjectURL(await response.blob());
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = name;
  anchor.click();
  URL.revokeObjectURL(url);
}
