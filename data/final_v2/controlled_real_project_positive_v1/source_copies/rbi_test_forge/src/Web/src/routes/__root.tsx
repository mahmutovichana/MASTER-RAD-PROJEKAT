import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import {
  Outlet,
  Link,
  createRootRouteWithContext,
  useRouter,
  useRouterState,
} from "@tanstack/react-router";

import { Toaster } from "../components/ui/sonner";
import { ThemeProvider } from "../design-system/theme";
import {
  LocalizationProvider,
  LocalizationLoadingState,
  LocalizationErrorState,
} from "../localization";

function NotFoundComponent() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-7xl font-bold text-foreground">404</h1>
        <h2 className="mt-4 text-xl font-semibold text-foreground">Stranica nije pronađena</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Tražena stranica ne postoji ili je premještena.
        </p>
        <div className="mt-8">
          <Link
            to="/"
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Nazad na početnu
          </Link>
        </div>
      </div>
    </div>
  );
}

function ErrorComponent({ error, reset }: { error: Error; reset: () => void }) {
  console.error(error);
  const router = useRouter();

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="max-w-md text-center">
        <h1 className="text-xl font-semibold tracking-tight text-foreground">
          Stranicu nije moguće učitati
        </h1>
        <p className="mt-2 text-sm text-muted-foreground">
          Pokušajte ponovo. Ako se problem nastavi, obratite se administratoru aplikacije.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-2">
          <button
            onClick={() => {
              router.invalidate();
              reset();
            }}
            className="inline-flex items-center justify-center rounded-md bg-primary px-4 py-2 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Pokušaj ponovo
          </button>
          <a
            href="/"
            className="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium text-foreground transition-colors hover:bg-accent"
          >
            Nazad na početnu
          </a>
        </div>
      </div>
    </div>
  );
}

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  head: () => ({
    meta: [
      { charSet: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { title: "RBBH Generator automatizovanih testova" },
      {
        name: "description",
        content: "Upravljanje, generisanje i izvršavanje automatizovanih API i UI testova.",
      },
      { name: "author", content: "Hana Mahmutović" },
      { property: "og:title", content: "RBBH Generator automatizovanih testova" },
      {
        property: "og:description",
        content: "Upravljanje, generisanje i izvršavanje automatizovanih API i UI testova.",
      },
      { property: "og:type", content: "website" },
      { name: "twitter:card", content: "summary_large_image" },
    ],
  }),
  component: RootComponent,
  notFoundComponent: NotFoundComponent,
  errorComponent: ErrorComponent,
});

function RootComponent() {
  const { queryClient } = Route.useRouteContext();
  const pathname = useRouterState({ select: (state) => state.location.pathname });

  return (
    <ThemeProvider>
    <QueryClientProvider client={queryClient}>
      {/* Wording is loaded from the active localization release at runtime. */}
      <LocalizationProvider
        pathname={pathname}
        loadingFallback={<LocalizationLoadingState />}
        errorFallback={({ error, retry }) => <LocalizationErrorState error={error} retry={retry} />}
      >
        {/* Required: nested routes render here. Removing <Outlet /> breaks all child routes. */}
        <Outlet />
      </LocalizationProvider>
      <Toaster position="bottom-right" richColors closeButton />
    </QueryClientProvider>
    </ThemeProvider>
  );
}
