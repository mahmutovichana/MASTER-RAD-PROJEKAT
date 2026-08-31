using System.Net.Http.Headers;
using RBBH.TestAutomation.Api.Auth;
using Microsoft.AspNetCore.Authentication;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.Extensions.Options;

namespace RBBH.TestAutomation.Api.Middlewares
{
    public class RequestMessageHandler : DelegatingHandler
    {
        private readonly ILogger<RequestMessageHandler> _logger;
        private readonly IHttpContextAccessor _httpContextAccessor;
        private readonly CookieOidcRefresher? _cookieOidcRefresher;
        private readonly IOptionsMonitor<CookieAuthenticationOptions> _cookieOptionsMonitor;
        private readonly string _oidcScheme;

        public RequestMessageHandler(
            IHttpContextAccessor httpContextAccessor,
            ILogger<RequestMessageHandler> logger,
            CookieOidcRefresher? cookieOidcRefresher,
            IOptionsMonitor<CookieAuthenticationOptions> cookieOptionsMonitor,
            string oidcScheme
        )
        {
            _httpContextAccessor = httpContextAccessor;
            _logger = logger;
            _cookieOidcRefresher = cookieOidcRefresher;
            _cookieOptionsMonitor = cookieOptionsMonitor;
            _oidcScheme = oidcScheme;
        }

        protected override async Task<HttpResponseMessage> SendAsync(
            HttpRequestMessage request,
            CancellationToken cancellationToken
        )
        {
            try
            {
                var httpContext = _httpContextAccessor.HttpContext;

                // If there's no HttpContext (e.g., during app startup warmup), proceed without authentication
                if (httpContext == null)
                {
                    return await base.SendAsync(request, cancellationToken);
                }

                // Only refresh token if OIDC is configured (production)
                if (_cookieOidcRefresher != null)
                {
                    var authenticateResult = await httpContext.AuthenticateAsync(
                        CookieAuthenticationDefaults.AuthenticationScheme
                    );
                    if (authenticateResult.Succeeded)
                    {
                        // Get required parameters for CookieValidatePrincipalContext
                        var scheme = new AuthenticationScheme(
                            CookieAuthenticationDefaults.AuthenticationScheme,
                            CookieAuthenticationDefaults.AuthenticationScheme,
                            typeof(CookieAuthenticationHandler)
                        );
                        var cookieOptions = _cookieOptionsMonitor.Get(
                            CookieAuthenticationDefaults.AuthenticationScheme
                        );
                        var ticket = authenticateResult.Ticket;
                        var cookieValidatePrincipalContext = new CookieValidatePrincipalContext(
                            httpContext,
                            scheme,
                            cookieOptions,
                            ticket
                        );
                        await _cookieOidcRefresher.ValidateOrRefreshCookieAsync(
                            cookieValidatePrincipalContext,
                            _oidcScheme
                        );
                    }
                }

                string? token = await httpContext.GetTokenAsync("access_token");
                if (!string.IsNullOrEmpty(token))
                {
                    request.Headers.Authorization = new AuthenticationHeaderValue("Bearer", token);
                }

                return await base.SendAsync(request, cancellationToken);
            }
            catch (Exception ex)
            {
                _logger.LogError(
                    ex,
                    ex.Message,
                    $"{nameof(RequestMessageHandler)}: {nameof(SendAsync)}"
                );
                throw;
            }
        }
    }
}
