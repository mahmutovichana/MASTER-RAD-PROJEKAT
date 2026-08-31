.PHONY: restore build test run-api run-web

restore:
	dotnet restore PropertyValuation/PropertyValuation.slnx --configfile PropertyValuation/nuget.config
	cd src/Web && pnpm install

build:
	dotnet build PropertyValuation/PropertyValuation.slnx -c Release --no-restore
	cd src/Web && pnpm build

test:
	dotnet test PropertyValuation/PropertyValuation.slnx --no-restore
	cd src/Web && pnpm test

run-api:
	dotnet run --project PropertyValuation/PropertyValuation.csproj

run-web:
	cd src/Web && pnpm dev
