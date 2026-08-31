FROM artifacts.rbi.tech/mcr.microsoft.com-docker-proxy/dotnet/aspnet:10.0 AS base
USER $APP_UID
WORKDIR /app
EXPOSE 8080

FROM artifacts.rbi.tech/mcr.microsoft.com-docker-proxy/dotnet/sdk:10.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY PropertyValuation/PropertyValuation.csproj PropertyValuation/
COPY PropertyValuation/Application/RBBH.CollateralAppraisal.Application.csproj PropertyValuation/Application/
COPY PropertyValuation/Domain/RBBH.CollateralAppraisal.Domain.csproj PropertyValuation/Domain/
COPY PropertyValuation/Infrastructure/RBBH.CollateralAppraisal.Infrastructure.csproj PropertyValuation/Infrastructure/
COPY PropertyValuation/nuget.config PropertyValuation/
RUN dotnet restore "PropertyValuation/PropertyValuation.csproj" --configfile "PropertyValuation/nuget.config"
COPY PropertyValuation/. PropertyValuation/
WORKDIR /src/PropertyValuation
RUN dotnet publish "PropertyValuation.csproj" -c $BUILD_CONFIGURATION -o /app/publish --no-restore /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
RUN mkdir -p /app/storage
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "PropertyValuation.dll"]
