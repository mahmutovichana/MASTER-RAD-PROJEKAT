using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.IdentityModel.Protocols.OpenIdConnect;

namespace RBBH.TestAutomation.Api.Auth
{
    internal static partial class CookieOidcServiceCollectionExtensions
    {
        public static IServiceCollection ConfigureCookieOidcRefresh(
            this IServiceCollection services,
            string cookieScheme,
            string oidcScheme
        )
        {
            services.AddSingleton<CookieOidcRefresher>();
            services
                .AddOptions<CookieAuthenticationOptions>(cookieScheme)
                .Configure<CookieOidcRefresher>(
                    (cookieOptions, refresher) =>
                    {
                        cookieOptions.Events.OnValidatePrincipal = context =>
                            refresher.ValidateOrRefreshCookieAsync(context, oidcScheme);
                    }
                );
            services
                .AddOptions<OpenIdConnectOptions>(oidcScheme)
                .Configure(oidcOptions =>
                {
                    // offline_access se NE dodaje (vidi napomenu u Program.cs) —
                    // Keycloak ga odbija za importovane korisnike. Session refresh
                    // token je dovoljan; SaveTokens ostaje da CookieOidcRefresher
                    // ima refresh_token.
                    oidcOptions.SaveTokens = true;
                });
            return services;
        }
    }
}
