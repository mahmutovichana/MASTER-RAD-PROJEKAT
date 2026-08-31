import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api/http-client";
export type UserProfile = Readonly<Record<string, unknown>>;
export function useProfile() {
  return useQuery({
    queryKey: ["me"],
    queryFn: async () => {
      const raw = await apiClient.getLegacy<unknown>("/api/me");
      return ((raw as UserProfile)?.["data"] ?? raw) as UserProfile;
    },
    staleTime: 60_000,
  });
}
export function profileList(profile: UserProfile | undefined, key: string) {
  const value = profile?.[key] ?? profile?.[key[0]!.toUpperCase() + key.slice(1)];
  return Array.isArray(value) ? value.map(String) : [];
}
