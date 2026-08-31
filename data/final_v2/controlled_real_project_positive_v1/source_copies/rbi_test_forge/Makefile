.PHONY: restore build test run-api run-web

restore:
	dotnet restore TestGenerator/TestGenerator.slnx --configfile TestGenerator/nuget.config
	cd src/Web && pnpm install

build:
	dotnet build TestGenerator/TestGenerator.slnx -c Release --no-restore
	cd src/Web && pnpm build

test:
	dotnet test TestGenerator/TestGenerator.slnx --no-restore
	cd src/Web && pnpm test

run-api:
	dotnet run --project TestGenerator/TestGenerator.csproj

run-web:
	cd src/Web && pnpm dev
