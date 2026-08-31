FROM artifacts.rbi.tech/mcr.microsoft.com-docker-proxy/dotnet/aspnet:10.0 AS base
USER $APP_UID
WORKDIR /app
EXPOSE 8080

FROM artifacts.rbi.tech/mcr.microsoft.com-docker-proxy/dotnet/sdk:10.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY TestGenerator/TestGenerator.csproj TestGenerator/
COPY TestGenerator/Core/RBBH.TestAutomation.Core.csproj TestGenerator/Core/
COPY TestGenerator/nuget.config TestGenerator/
RUN dotnet restore "TestGenerator/TestGenerator.csproj" --configfile "TestGenerator/nuget.config"
COPY TestGenerator/. TestGenerator/
WORKDIR /src/TestGenerator
RUN dotnet publish "TestGenerator.csproj" -c $BUILD_CONFIGURATION -o /app/publish --no-restore /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=build /app/publish .
ENV ASPNETCORE_URLS=http://+:8080
ENTRYPOINT ["dotnet", "TestGenerator.dll"]
