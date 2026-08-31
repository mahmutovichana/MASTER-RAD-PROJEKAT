using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace RBBH.CollateralAppraisal.Infrastructure.Persistence.Migrations
{
    /// <inheritdoc />
    public partial class InitialSqlServer : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "appraisers",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    city = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    legal_form = table.Column<int>(type: "int", nullable: false),
                    client_scope = table.Column<int>(type: "int", nullable: false),
                    supported_property_types = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    supported_cities = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    is_on_leave = table.Column<bool>(type: "bit", nullable: false, defaultValue: false),
                    is_blacklisted = table.Column<bool>(type: "bit", nullable: false, defaultValue: false),
                    contact_email = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    contact_phone = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    notes = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    is_active = table.Column<bool>(type: "bit", nullable: false, defaultValue: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_appraisers", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "audit_logs",
                columns: table => new
                {
                    Id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    TimestampUtc = table.Column<DateTime>(type: "datetime2", nullable: false),
                    ActorUserId = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: false),
                    ActorUsername = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: false),
                    ActorEmail = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    ActorFullName = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    ActorRole = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    ActiveRole = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    Action = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: false),
                    OperationType = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: false),
                    Module = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: false),
                    SourceSystem = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    SourceConnectionName = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    SourceDatabase = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    SourceSchema = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                    SourceTable = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    EntityType = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: false),
                    EntityKey = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    EntityDisplayName = table.Column<string>(type: "nvarchar(512)", maxLength: 512, nullable: true),
                    OldValuesJson = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    NewValuesJson = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    ChangedFieldsJson = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    Status = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: false),
                    Severity = table.Column<string>(type: "nvarchar(32)", maxLength: 32, nullable: false),
                    Reason = table.Column<string>(type: "nvarchar(1024)", maxLength: 1024, nullable: true),
                    IntegrationDirection = table.Column<string>(type: "nvarchar(16)", maxLength: 16, nullable: true),
                    ExternalRequestId = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: true),
                    ExternalResponseStatus = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                    CorrelationId = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                    RequestPath = table.Column<string>(type: "nvarchar(1024)", maxLength: 1024, nullable: true),
                    HttpMethod = table.Column<string>(type: "nvarchar(10)", maxLength: 10, nullable: true),
                    IpAddress = table.Column<string>(type: "nvarchar(64)", maxLength: 64, nullable: true),
                    UserAgent = table.Column<string>(type: "nvarchar(512)", maxLength: 512, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_audit_logs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "AuditOutbox",
                columns: table => new
                {
                    Id = table.Column<long>(type: "bigint", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Payload = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    ProcessedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_AuditOutbox", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "cities",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    name = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    UpdatedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_cities", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "codebook_values",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    CodebookKey = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Code = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Label = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    Description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    SortOrder = table.Column<int>(type: "int", nullable: false),
                    IsActive = table.Column<bool>(type: "bit", nullable: false),
                    IsSystem = table.Column<bool>(type: "bit", nullable: false),
                    IsCritical = table.Column<bool>(type: "bit", nullable: false),
                    CreatedByUserId = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    UpdatedByUserId = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    DeactivatedAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    DeactivatedByUserId = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    DeactivationReason = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    DeletedAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    DeletedByUserId = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    UpdatedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_codebook_values", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "codebooks",
                columns: table => new
                {
                    Id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    Code = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    Name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false),
                    Description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    Category = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    IsActive = table.Column<bool>(type: "bit", nullable: false),
                    IsSystem = table.Column<bool>(type: "bit", nullable: false),
                    CreatedByUserId = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    UpdatedByUserId = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    DeletedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: true),
                    DeletedByUserId = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    CreatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: false),
                    UpdatedAt = table.Column<DateTime>(type: "timestamp with time zone", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_codebooks", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "document_templates",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    code = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    category = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false),
                    file_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    content_type = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    file_size = table.Column<long>(type: "bigint", nullable: false),
                    storage_path = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    sort_order = table.Column<int>(type: "int", nullable: false),
                    is_active = table.Column<bool>(type: "bit", nullable: false, defaultValue: true),
                    allowed_roles = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_document_templates", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "documents",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    appraisal_order_id = table.Column<int>(type: "int", nullable: false),
                    document_type_id = table.Column<int>(type: "int", nullable: true),
                    file_name = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    original_file_name = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    content_type = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    file_size = table.Column<long>(type: "bigint", nullable: false),
                    storage_path = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                    uploaded_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    uploaded_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    version = table.Column<int>(type: "int", nullable: false),
                    previous_version_id = table.Column<int>(type: "int", nullable: true),
                    change_reason = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    deactivated_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deactivated_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    deactivation_reason = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    is_deleted = table.Column<bool>(type: "bit", nullable: false),
                    deleted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deleted_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_documents", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "notifications",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    recipient_user_id = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    recipient_role = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    channel = table.Column<int>(type: "int", nullable: false),
                    subject = table.Column<string>(type: "nvarchar(256)", maxLength: 256, nullable: false),
                    message = table.Column<string>(type: "nvarchar(max)", nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    sent_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    retry_count = table.Column<int>(type: "int", nullable: false, defaultValue: 0),
                    error_message = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    related_entity_type = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    related_entity_id = table.Column<string>(type: "nvarchar(128)", maxLength: 128, nullable: true),
                    is_read = table.Column<bool>(type: "bit", nullable: false, defaultValue: false),
                    read_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deduplication_key = table.Column<string>(type: "nvarchar(512)", maxLength: 512, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_notifications", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "order_declined_appraisers",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    appraisal_order_id = table.Column<int>(type: "int", nullable: false),
                    appraiser_id = table.Column<int>(type: "int", nullable: false),
                    declined_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    reason = table.Column<int>(type: "int", nullable: false),
                    free_text = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    is_timeout = table.Column<bool>(type: "bit", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_order_declined_appraisers", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "order_opinions",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    appraisal_order_id = table.Column<int>(type: "int", nullable: false),
                    opinion_type = table.Column<int>(type: "int", nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    document_id = table.Column<int>(type: "int", nullable: true),
                    imported_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    imported_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    comment = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_order_opinions", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "permission_definitions",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    code = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    display_name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false),
                    description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    module = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_permission_definitions", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "quote_requests",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    appraisal_order_id = table.Column<int>(type: "int", nullable: false),
                    appraiser_id = table.Column<int>(type: "int", nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    sent_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    deadline = table.Column<DateTime>(type: "datetime2", nullable: false),
                    sent_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    offered_price = table.Column<decimal>(type: "decimal(18,2)", precision: 18, scale: 2, nullable: true),
                    offered_days = table.Column<int>(type: "int", nullable: true),
                    responded_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    thank_you_sent_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_quote_requests", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "role_definitions",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    name = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: false),
                    display_name = table.Column<string>(type: "nvarchar(250)", maxLength: 250, nullable: false),
                    description = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: true),
                    is_system = table.Column<bool>(type: "bit", nullable: false),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    created_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    updated_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    deleted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deleted_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_role_definitions", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "shared_documents",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    title = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    category = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    file_name = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    original_file_name = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    content_type = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    file_size = table.Column<long>(type: "bigint", nullable: false),
                    storage_path = table.Column<string>(type: "nvarchar(1000)", maxLength: 1000, nullable: false),
                    uploaded_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    uploaded_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    is_active = table.Column<bool>(type: "bit", nullable: false),
                    deactivated_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deactivated_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_shared_documents", x => x.id);
                });

            migrationBuilder.CreateTable(
                name: "appraisal_orders",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    order_number = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: false),
                    title = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    workflow_type = table.Column<int>(type: "int", nullable: true),
                    client_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    client_type = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    client_identifier = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    contact_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    contact_phone = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    contact_email = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    branch = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    branch_address = table.Column<string>(type: "nvarchar(400)", maxLength: 400, nullable: true),
                    city = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    city_id = table.Column<int>(type: "int", nullable: true),
                    branch_id = table.Column<int>(type: "int", nullable: true),
                    collateral_type_id = table.Column<int>(type: "int", nullable: true),
                    combined_collateral_type_id = table.Column<int>(type: "int", nullable: true),
                    property_address = table.Column<string>(type: "nvarchar(500)", maxLength: 500, nullable: true),
                    property_city = table.Column<string>(type: "nvarchar(150)", maxLength: 150, nullable: true),
                    created_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    created_by_role = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    created_by_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    created_by_email = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: true),
                    delivery_contact_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    am_recipient_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    accepted_by_ca_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    accepted_by_ca_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    accepted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    submitted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    documentation_review_status = table.Column<string>(type: "nvarchar(30)", maxLength: 30, nullable: true),
                    appraiser_id = table.Column<int>(type: "int", nullable: true),
                    is_deleted = table.Column<bool>(type: "bit", nullable: false),
                    deleted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    deleted_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    square_meters_commercial = table.Column<decimal>(type: "decimal(18,2)", nullable: true),
                    square_meters_residential = table.Column<decimal>(type: "decimal(18,2)", nullable: true),
                    internal_note = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    payment_consent_status = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    final_appraisal_document_id = table.Column<int>(type: "int", nullable: true),
                    co_approved_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    co_approved_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    ready_for_procedure_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    original_received_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    original_received_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    correction_count = table.Column<int>(type: "int", nullable: false, defaultValue: 0),
                    appraiser_reminder_count = table.Column<int>(type: "int", nullable: false, defaultValue: 0),
                    appraiser_reminder_last_sent_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    opinions_completed_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    request_received_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    request_sent_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    invoice_sent_date = table.Column<DateTime>(type: "datetime2", nullable: true),
                    invoice_received_date = table.Column<DateTime>(type: "datetime2", nullable: true),
                    invoice_status = table.Column<int>(type: "int", nullable: false, defaultValue: 0),
                    invoice_document_id = table.Column<int>(type: "int", nullable: true),
                    invoice_uploaded_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    invoice_uploaded_by_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    invoice_uploaded_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    invoice_sent_for_payment_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    invoice_sent_for_payment_by_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    invoice_sent_for_payment_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    invoice_paid_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    invoice_paid_by_name = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: true),
                    invoice_paid_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    appraiser_visit_date = table.Column<DateTime>(type: "datetime2", nullable: true),
                    appraiser_rating = table.Column<int>(type: "int", nullable: true),
                    esg_certificate = table.Column<string>(type: "nvarchar(50)", maxLength: 50, nullable: true),
                    co_documentation_review_started_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    co_opinion_sent_to_am_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    appraisal_fee = table.Column<decimal>(type: "decimal(18,2)", nullable: true),
                    collateral_status = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    order_sent_to_appraiser_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    signed_documents_received_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    documentation_supplement_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    appraisal_delivered_to_co_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    correction_requested_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    corrected_appraisal_received_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    SalesConsentSigned = table.Column<bool>(type: "bit", nullable: false),
                    SalesConsentSignedAt = table.Column<DateTime>(type: "datetime2", nullable: true),
                    SalesConsentSignedByName = table.Column<string>(type: "nvarchar(max)", nullable: true),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_appraisal_orders", x => x.id);
                    table.ForeignKey(
                        name: "FK_appraisal_orders_appraisers_appraiser_id",
                        column: x => x.appraiser_id,
                        principalTable: "appraisers",
                        principalColumn: "id",
                        onDelete: ReferentialAction.SetNull);
                });

            migrationBuilder.CreateTable(
                name: "branches",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    code = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    name = table.Column<string>(type: "nvarchar(200)", maxLength: 200, nullable: false),
                    address = table.Column<string>(type: "nvarchar(400)", maxLength: 400, nullable: false),
                    city_id = table.Column<int>(type: "int", nullable: false),
                    CreatedAt = table.Column<DateTime>(type: "datetime2", nullable: false),
                    UpdatedAt = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_branches", x => x.id);
                    table.ForeignKey(
                        name: "FK_branches_cities_city_id",
                        column: x => x.city_id,
                        principalTable: "cities",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "role_permissions",
                columns: table => new
                {
                    role_definition_id = table.Column<int>(type: "int", nullable: false),
                    permission_definition_id = table.Column<int>(type: "int", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    created_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_role_permissions", x => new { x.role_definition_id, x.permission_definition_id });
                    table.ForeignKey(
                        name: "FK_role_permissions_permission_definitions_permission_definition_id",
                        column: x => x.permission_definition_id,
                        principalTable: "permission_definitions",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                    table.ForeignKey(
                        name: "FK_role_permissions_role_definitions_role_definition_id",
                        column: x => x.role_definition_id,
                        principalTable: "role_definitions",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateTable(
                name: "order_protocol_entries",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    order_id = table.Column<int>(type: "int", nullable: false),
                    protocol_number = table.Column<string>(type: "nvarchar(20)", maxLength: 20, nullable: false),
                    protocol_year = table.Column<int>(type: "int", nullable: false),
                    protocol_sequence = table.Column<int>(type: "int", nullable: false),
                    generated_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    generated_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: false),
                    status = table.Column<int>(type: "int", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_order_protocol_entries", x => x.id);
                    table.ForeignKey(
                        name: "FK_order_protocol_entries_appraisal_orders_order_id",
                        column: x => x.order_id,
                        principalTable: "appraisal_orders",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Restrict);
                });

            migrationBuilder.CreateTable(
                name: "task_items",
                columns: table => new
                {
                    id = table.Column<int>(type: "int", nullable: false)
                        .Annotation("SqlServer:Identity", "1, 1"),
                    row_version = table.Column<long>(type: "bigint", rowVersion: true, nullable: false),
                    appraisal_order_id = table.Column<int>(type: "int", nullable: false),
                    task_type = table.Column<int>(type: "int", nullable: false),
                    title = table.Column<string>(type: "nvarchar(300)", maxLength: 300, nullable: false),
                    description = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    assigned_role = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    assigned_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    status = table.Column<int>(type: "int", nullable: false),
                    accepted_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    accepted_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    completed_at = table.Column<DateTime>(type: "datetime2", nullable: true),
                    completed_by_user_id = table.Column<string>(type: "nvarchar(100)", maxLength: 100, nullable: true),
                    due_date = table.Column<DateTime>(type: "datetime2", nullable: true),
                    comment = table.Column<string>(type: "nvarchar(2000)", maxLength: 2000, nullable: true),
                    is_locked = table.Column<bool>(type: "bit", nullable: false),
                    created_at = table.Column<DateTime>(type: "datetime2", nullable: false),
                    updated_at = table.Column<DateTime>(type: "datetime2", nullable: true)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_task_items", x => x.id);
                    table.ForeignKey(
                        name: "FK_task_items_appraisal_orders_appraisal_order_id",
                        column: x => x.appraisal_order_id,
                        principalTable: "appraisal_orders",
                        principalColumn: "id",
                        onDelete: ReferentialAction.Cascade);
                });

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_appraiser_id",
                table: "appraisal_orders",
                column: "appraiser_id");

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_appraiser_id_status",
                table: "appraisal_orders",
                columns: new[] { "appraiser_id", "status" });

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_city",
                table: "appraisal_orders",
                column: "city");

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_created_by_user_id",
                table: "appraisal_orders",
                column: "created_by_user_id");

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_is_deleted",
                table: "appraisal_orders",
                column: "is_deleted");

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_order_number",
                table: "appraisal_orders",
                column: "order_number",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_status",
                table: "appraisal_orders",
                column: "status");

            migrationBuilder.CreateIndex(
                name: "IX_appraisal_orders_status_city",
                table: "appraisal_orders",
                columns: new[] { "status", "city" });

            migrationBuilder.CreateIndex(
                name: "ix_orders_created_at",
                table: "appraisal_orders",
                column: "created_at");

            migrationBuilder.CreateIndex(
                name: "ix_orders_owner_deleted",
                table: "appraisal_orders",
                columns: new[] { "created_by_user_id", "is_deleted" });

            migrationBuilder.CreateIndex(
                name: "ix_orders_owner_status",
                table: "appraisal_orders",
                columns: new[] { "created_by_user_id", "status" });

            migrationBuilder.CreateIndex(
                name: "IX_appraisers_city",
                table: "appraisers",
                column: "city");

            migrationBuilder.CreateIndex(
                name: "IX_appraisers_is_active",
                table: "appraisers",
                column: "is_active");

            migrationBuilder.CreateIndex(
                name: "IX_appraisers_is_blacklisted",
                table: "appraisers",
                column: "is_blacklisted");

            migrationBuilder.CreateIndex(
                name: "IX_appraisers_is_on_leave",
                table: "appraisers",
                column: "is_on_leave");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_action",
                table: "audit_logs",
                column: "Action");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_active_role",
                table: "audit_logs",
                column: "ActiveRole");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_actor_user_id",
                table: "audit_logs",
                column: "ActorUserId");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_correlation_id",
                table: "audit_logs",
                column: "CorrelationId");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_entity_type_key",
                table: "audit_logs",
                columns: new[] { "EntityType", "EntityKey" });

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_module",
                table: "audit_logs",
                column: "Module");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_severity",
                table: "audit_logs",
                column: "Severity");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_source_system",
                table: "audit_logs",
                column: "SourceSystem");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_status",
                table: "audit_logs",
                column: "Status");

            migrationBuilder.CreateIndex(
                name: "ix_audit_logs_timestamp_utc",
                table: "audit_logs",
                column: "TimestampUtc");

            migrationBuilder.CreateIndex(
                name: "IX_AuditOutbox_Unprocessed",
                table: "AuditOutbox",
                columns: new[] { "ProcessedAt", "CreatedAt" },
                filter: "[ProcessedAt] IS NULL");

            migrationBuilder.CreateIndex(
                name: "ix_branches_city_id",
                table: "branches",
                column: "city_id");

            migrationBuilder.CreateIndex(
                name: "uix_branches_code",
                table: "branches",
                column: "code",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "uix_cities_name",
                table: "cities",
                column: "name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "ix_codebook_values_key",
                table: "codebook_values",
                column: "CodebookKey");

            migrationBuilder.CreateIndex(
                name: "ix_codebook_values_key_active",
                table: "codebook_values",
                columns: new[] { "CodebookKey", "IsActive" });

            migrationBuilder.CreateIndex(
                name: "uix_codebook_values_key_code_active",
                table: "codebook_values",
                columns: new[] { "CodebookKey", "Code" },
                unique: true,
                filter: "\"DeletedAt\" IS NULL");

            migrationBuilder.CreateIndex(
                name: "ix_codebooks_category",
                table: "codebooks",
                column: "Category");

            migrationBuilder.CreateIndex(
                name: "ix_codebooks_is_active",
                table: "codebooks",
                column: "IsActive");

            migrationBuilder.CreateIndex(
                name: "uix_codebooks_code_active",
                table: "codebooks",
                column: "Code",
                unique: true,
                filter: "\"DeletedAt\" IS NULL");

            migrationBuilder.CreateIndex(
                name: "IX_document_templates_category",
                table: "document_templates",
                column: "category");

            migrationBuilder.CreateIndex(
                name: "IX_document_templates_code",
                table: "document_templates",
                column: "code",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_documents_appraisal_order_id",
                table: "documents",
                column: "appraisal_order_id");

            migrationBuilder.CreateIndex(
                name: "IX_documents_is_active",
                table: "documents",
                column: "is_active");

            migrationBuilder.CreateIndex(
                name: "IX_documents_is_deleted",
                table: "documents",
                column: "is_deleted");

            migrationBuilder.CreateIndex(
                name: "IX_documents_previous_version_id",
                table: "documents",
                column: "previous_version_id");

            migrationBuilder.CreateIndex(
                name: "IX_notifications_deduplication_key",
                table: "notifications",
                column: "deduplication_key");

            migrationBuilder.CreateIndex(
                name: "IX_notifications_recipient_user_id",
                table: "notifications",
                column: "recipient_user_id");

            migrationBuilder.CreateIndex(
                name: "IX_notifications_recipient_user_id_is_read",
                table: "notifications",
                columns: new[] { "recipient_user_id", "is_read" });

            migrationBuilder.CreateIndex(
                name: "IX_notifications_status",
                table: "notifications",
                column: "status");

            migrationBuilder.CreateIndex(
                name: "ix_order_declined_appraisers_order_appraiser",
                table: "order_declined_appraisers",
                columns: new[] { "appraisal_order_id", "appraiser_id" });

            migrationBuilder.CreateIndex(
                name: "ix_order_declined_appraisers_order_id",
                table: "order_declined_appraisers",
                column: "appraisal_order_id");

            migrationBuilder.CreateIndex(
                name: "IX_order_opinions_appraisal_order_id",
                table: "order_opinions",
                column: "appraisal_order_id");

            migrationBuilder.CreateIndex(
                name: "IX_order_opinions_appraisal_order_id_opinion_type",
                table: "order_opinions",
                columns: new[] { "appraisal_order_id", "opinion_type" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_order_protocol_entries_order_id",
                table: "order_protocol_entries",
                column: "order_id",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_order_protocol_entries_protocol_number",
                table: "order_protocol_entries",
                column: "protocol_number",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_order_protocol_entries_protocol_year",
                table: "order_protocol_entries",
                column: "protocol_year");

            migrationBuilder.CreateIndex(
                name: "IX_order_protocol_entries_protocol_year_protocol_sequence",
                table: "order_protocol_entries",
                columns: new[] { "protocol_year", "protocol_sequence" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_permission_definitions_code",
                table: "permission_definitions",
                column: "code",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_permission_definitions_module",
                table: "permission_definitions",
                column: "module");

            migrationBuilder.CreateIndex(
                name: "IX_quote_requests_appraisal_order_id",
                table: "quote_requests",
                column: "appraisal_order_id");

            migrationBuilder.CreateIndex(
                name: "IX_quote_requests_appraisal_order_id_appraiser_id",
                table: "quote_requests",
                columns: new[] { "appraisal_order_id", "appraiser_id" },
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_role_definitions_is_active",
                table: "role_definitions",
                column: "is_active");

            migrationBuilder.CreateIndex(
                name: "IX_role_definitions_is_system",
                table: "role_definitions",
                column: "is_system");

            migrationBuilder.CreateIndex(
                name: "IX_role_definitions_name",
                table: "role_definitions",
                column: "name",
                unique: true,
                filter: "deleted_at IS NULL");

            migrationBuilder.CreateIndex(
                name: "IX_role_permissions_permission_definition_id",
                table: "role_permissions",
                column: "permission_definition_id");

            migrationBuilder.CreateIndex(
                name: "IX_role_permissions_role_definition_id",
                table: "role_permissions",
                column: "role_definition_id");

            migrationBuilder.CreateIndex(
                name: "IX_shared_documents_category",
                table: "shared_documents",
                column: "category");

            migrationBuilder.CreateIndex(
                name: "IX_shared_documents_is_active",
                table: "shared_documents",
                column: "is_active");

            migrationBuilder.CreateIndex(
                name: "IX_task_items_appraisal_order_id",
                table: "task_items",
                column: "appraisal_order_id");

            migrationBuilder.CreateIndex(
                name: "IX_task_items_assigned_role",
                table: "task_items",
                column: "assigned_role");

            migrationBuilder.CreateIndex(
                name: "IX_task_items_assigned_user_id",
                table: "task_items",
                column: "assigned_user_id");

            migrationBuilder.CreateIndex(
                name: "IX_task_items_status",
                table: "task_items",
                column: "status");
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "audit_logs");

            migrationBuilder.DropTable(
                name: "AuditOutbox");

            migrationBuilder.DropTable(
                name: "branches");

            migrationBuilder.DropTable(
                name: "codebook_values");

            migrationBuilder.DropTable(
                name: "codebooks");

            migrationBuilder.DropTable(
                name: "document_templates");

            migrationBuilder.DropTable(
                name: "documents");

            migrationBuilder.DropTable(
                name: "notifications");

            migrationBuilder.DropTable(
                name: "order_declined_appraisers");

            migrationBuilder.DropTable(
                name: "order_opinions");

            migrationBuilder.DropTable(
                name: "order_protocol_entries");

            migrationBuilder.DropTable(
                name: "quote_requests");

            migrationBuilder.DropTable(
                name: "role_permissions");

            migrationBuilder.DropTable(
                name: "shared_documents");

            migrationBuilder.DropTable(
                name: "task_items");

            migrationBuilder.DropTable(
                name: "cities");

            migrationBuilder.DropTable(
                name: "permission_definitions");

            migrationBuilder.DropTable(
                name: "role_definitions");

            migrationBuilder.DropTable(
                name: "appraisal_orders");

            migrationBuilder.DropTable(
                name: "appraisers");
        }
    }
}
