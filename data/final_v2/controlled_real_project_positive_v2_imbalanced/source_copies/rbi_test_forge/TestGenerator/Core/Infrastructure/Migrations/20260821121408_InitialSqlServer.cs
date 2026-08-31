using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RBBH.TestAutomation.Core.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class InitialSqlServer : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "audit_log",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    entity_type = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    entity_id = table.Column<Guid>(type: "uniqueidentifier", nullable: true),
                    action = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                    changed_by = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    changed_by_name = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    changed_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    old_values = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    new_values = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_audit_log", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "security_audit_log",
                columns: table => new
                {
                    id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    timestamp_utc = table.Column<DateTime>(type: "datetime2", nullable: false),
                    event_type = table.Column<string>(type: "nvarchar(80)", maxLength: 80, nullable: false),
                    username = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: false),
                    ip_address = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                    failure_reason = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_security_audit_log", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "sifarnici_kategorije",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    naziv = table.Column<string>(type: "nvarchar(160)", maxLength: 160, nullable: false),
                    slug = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    opis = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    active = table.Column<bool>(type: "bit", nullable: false),
                    kreiran_at = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_sifarnici_kategorije", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "tf_api_keys",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    Name = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                    KeyHash = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: false),
                    Prefix = table.Column<string>(type: "nvarchar(12)", maxLength: 12, nullable: false),
                    ExpiresAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    IsRevoked = table.Column<bool>(type: "bit", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    CreatedBy = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    LastUsedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tf_api_keys", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "tf_groups",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    Naziv = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                    Opis = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    Boja = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: true),
                    Tag = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    Prioritet = table.Column<int>(type: "int", nullable: false),
                    RunConfiguration = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    ParentGroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: true),
                    NotificationConfigJson = table.Column<string>(type: "text", nullable: true),
                    KreiranOd = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    KreiranAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    IzmjenjenOd = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    IzmjenjenAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tf_groups", x => x.Id);
                    table.ForeignKey(
                        name: "FK_tf_groups_tf_groups_ParentGroupId",
                        column: x => x.ParentGroupId,
                        principalTable: "tf_groups",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "sifarnici_vrijednosti",
                columns: table => new
                {
                    id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    kategorija_id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    naziv = table.Column<string>(type: "nvarchar(160)", maxLength: 160, nullable: false),
                    kod = table.Column<string>(type: "nvarchar(80)", maxLength: 80, nullable: true),
                    redoslijed = table.Column<int>(type: "int", nullable: false),
                    active = table.Column<bool>(type: "bit", nullable: false),
                    kreiran_od = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    kreiran_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    izmjenjen_od = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    izmjenjen_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_sifarnici_vrijednosti", x => x.id);
                    table.ForeignKey(
                        name: "FK_sifarnici_vrijednosti_sifarnici_kategorije_kategorija_id",
                        column: x => x.kategorija_id,
                        principalTable: "sifarnici_kategorije",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tf_run_results",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    GroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    State = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    Duration = table.Column<TimeSpan>(type: "time", nullable: false),
                    PassRate = table.Column<double>(type: "float", nullable: false),
                    TotalCount = table.Column<int>(type: "int", nullable: false),
                    PassedCount = table.Column<int>(type: "int", nullable: false),
                    FailedCount = table.Column<int>(type: "int", nullable: false),
                    ThroughputPerSecond = table.Column<double>(type: "float", nullable: false),
                    TriggerType = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    StartedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    CompletedAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    OptionsJson = table.Column<string>(type: "text", nullable: true),
                    DetailsJson = table.Column<string>(type: "text", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tf_run_results", x => x.Id);
                    table.ForeignKey(
                        name: "FK_tf_run_results_tf_groups_GroupId",
                        column: x => x.GroupId,
                        principalTable: "tf_groups",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tf_scenarios",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    GroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    Naziv = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                    Tip = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: false),
                    Target = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    Arrange = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Act = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Assert = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Redoslijed = table.Column<int>(type: "int", nullable: false),
                    RunSequentially = table.Column<bool>(type: "bit", nullable: false, defaultValue: false),
                    KreiranOd = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    KreiranAt = table.Column<DateTime>(type: "datetime2", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tf_scenarios", x => x.Id);
                    table.ForeignKey(
                        name: "FK_tf_scenarios_tf_groups_GroupId",
                        column: x => x.GroupId,
                        principalTable: "tf_groups",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "tf_schedules",
                columns: table => new
                {
                    Id = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    GroupId = table.Column<Guid>(type: "uniqueidentifier", nullable: false),
                    CronExpression = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    IsActive = table.Column<bool>(type: "bit", nullable: false),
                    Timezone = table.Column<string>(type: "nvarchar(60)", maxLength: 60, nullable: false),
                    NotificationConfig = table.Column<string>(type: "nvarchar(max)", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_tf_schedules", x => x.Id);
                    table.ForeignKey(
                        name: "FK_tf_schedules_tf_groups_GroupId",
                        column: x => x.GroupId,
                        principalTable: "tf_groups",
                        principalColumn: "Id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_audit_log_entity_type_entity_id_changed_at",
                table: "audit_log",
                columns: new[] { "entity_type", "entity_id", "changed_at" });

            migrationBuilder.CreateIndex(
                name: "IX_security_audit_log_timestamp_utc",
                table: "security_audit_log",
                column: "timestamp_utc");

            migrationBuilder.CreateIndex(
                name: "IX_sifarnici_kategorije_slug",
                table: "sifarnici_kategorije",
                column: "slug",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_sifarnici_vrijednosti_kategorija_id_naziv",
                table: "sifarnici_vrijednosti",
                columns: new[] { "kategorija_id", "naziv" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tf_api_keys_KeyHash",
                table: "tf_api_keys",
                column: "KeyHash",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_tf_groups_ParentGroupId",
                table: "tf_groups",
                column: "ParentGroupId");

            migrationBuilder.CreateIndex(
                name: "IX_tf_run_results_GroupId",
                table: "tf_run_results",
                column: "GroupId");

            migrationBuilder.CreateIndex(
                name: "IX_tf_scenarios_GroupId",
                table: "tf_scenarios",
                column: "GroupId");

            migrationBuilder.CreateIndex(
                name: "IX_tf_schedules_GroupId",
                table: "tf_schedules",
                column: "GroupId");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "audit_log");

            migrationBuilder.DropTable(
                name: "security_audit_log");

            migrationBuilder.DropTable(
                name: "sifarnici_vrijednosti");

            migrationBuilder.DropTable(
                name: "tf_api_keys");

            migrationBuilder.DropTable(
                name: "tf_run_results");

            migrationBuilder.DropTable(
                name: "tf_scenarios");

            migrationBuilder.DropTable(
                name: "tf_schedules");

            migrationBuilder.DropTable(
                name: "sifarnici_kategorije");

            migrationBuilder.DropTable(
                name: "tf_groups");
        }
    }
}
