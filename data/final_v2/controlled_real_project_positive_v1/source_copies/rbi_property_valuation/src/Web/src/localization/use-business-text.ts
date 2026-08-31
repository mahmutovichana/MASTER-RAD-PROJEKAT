import { useTranslation } from "react-i18next";

/**
 * Small typed helper for feature copy that is still co-located with a screen.
 * Shared shell copy remains in versioned localization bundles; feature copy can
 * use this helper without duplicating API/domain terminology in global files.
 */
export function useBusinessText() {
  const { i18n } = useTranslation();
  const isBosnian = i18n.resolvedLanguage?.toLowerCase().startsWith("bs") ?? true;

  return (bosnian: string, english: string) => (isBosnian ? bosnian : english);
}
