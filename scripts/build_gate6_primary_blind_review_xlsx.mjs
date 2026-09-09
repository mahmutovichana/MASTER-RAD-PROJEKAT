import crypto from "node:crypto";
import fs from "node:fs/promises";
import path from "node:path";
import { FileBlob, SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = process.argv[2] || "C:/MRF";
const reviewDir = path.join(root, "reports/final_v2/gate6/review");
const csvPath = path.join(reviewDir, "gate6_primary_blind_review.csv");
const xlsxPath = path.join(reviewDir, "gate6_primary_blind_review.xlsx");
const manifestPath = path.join(reviewDir, "gate6_primary_blind_review_manifest.json");
const previewPath = path.join(root, "work/gate6_review/gate6_primary_blind_review_preview.png");

function verifyFrozenReviewValues(values) {
  const rows = values.slice(1);
  const normalized = (value) => value === null || value === undefined ? "" : String(value).trim();
  const noOutputRows = rows.filter((row) => normalized(row[7]) === "NO_OUTPUT_SYSTEM_FAILURE");
  const scorableRows = rows.filter((row) => normalized(row[7]) === "pending");
  const ratingIndexes = [8, 9, 10, 11, 12, 13];
  const noHumanScores = scorableRows.every(
    (row) => ratingIndexes.every((index) => normalized(row[index]) === ""),
  ) && noOutputRows.every(
    (row) => ratingIndexes.every((index) => normalized(row[index]) === "N/A"),
  );
  if (rows.length !== 100 || noOutputRows.length !== 86 || scorableRows.length !== 14 || !noHumanScores) {
    throw new Error("Frozen review values failed the 100/86/14 no-human-scores contract.");
  }
}

const csvText = (await fs.readFile(csvPath, "utf8")).replace(/^\uFEFF/, "");
const workbook = await Workbook.fromCSV(csvText, { sheetName: "Primary review" });
const sheet = workbook.worksheets.getItem("Primary review");
sheet.showGridLines = false;
sheet.freezePanes.freezeRows(1);
sheet.freezePanes.freezeColumns(2);
sheet.tabColor = "#1F4E78";

const used = sheet.getRange("A1:O101");
used.format.font = { name: "Arial", size: 10, color: "#1F2937" };
used.format.verticalAlignment = "top";
used.format.wrapText = true;
used.format.borders = { preset: "all", style: "thin", color: "#D9E2F3" };

const header = sheet.getRange("A1:O1");
header.format.fill = "#1F4E78";
header.format.font = { name: "Arial", size: 10, bold: true, color: "#FFFFFF" };
header.format.verticalAlignment = "center";
header.format.rowHeight = 36;

const widths = {
  A: 20, B: 13, C: 28, D: 62, E: 54, F: 28, G: 54, H: 29,
  I: 20, J: 22, K: 21, L: 16, M: 16, N: 20, O: 40,
};
for (const [column, width] of Object.entries(widths)) {
  sheet.getRange(`${column}:${column}`).format.columnWidth = width;
}
sheet.getRange("2:101").format.rowHeight = 72;

const statuses = sheet.getRange("H2:H101").values.flat().map(String);
let noOutputCount = 0;
let scorableCount = 0;
for (let index = 0; index < statuses.length; index += 1) {
  const excelRow = index + 2;
  if (statuses[index] === "NO_OUTPUT_SYSTEM_FAILURE") {
    noOutputCount += 1;
    sheet.getRange(`H${excelRow}:O${excelRow}`).format.fill = "#E7E6E6";
    sheet.getRange(`H${excelRow}:O${excelRow}`).format.font = { name: "Arial", size: 10, color: "#666666" };
  } else if (statuses[index] === "pending") {
    scorableCount += 1;
    sheet.getRange(`H${excelRow}:O${excelRow}`).format.fill = "#FFF2CC";
    sheet.getRange(`I${excelRow}:M${excelRow}`).dataValidation = {
      rule: { type: "whole", operator: "between", formula1: 1, formula2: 5 },
    };
    sheet.getRange(`N${excelRow}`).dataValidation = {
      rule: { type: "list", values: ["yes", "no"] },
    };
  } else {
    throw new Error(`Unexpected review status at row ${excelRow}: ${statuses[index]}`);
  }
}
if (noOutputCount !== 86 || scorableCount !== 14) {
  throw new Error(`Expected 86 no-output and 14 scorable rows, got ${noOutputCount}/${scorableCount}`);
}

workbook.recalculate();
const verificationRows = sheet.getRange("A1:O101").values;
if (verificationRows.length !== 101 || verificationRows[0].length !== 15) {
  throw new Error("Pre-export workbook dimensions differ from the 100-row, 15-column contract.");
}
verifyFrozenReviewValues(verificationRows);

await fs.mkdir(path.dirname(previewPath), { recursive: true });
const preview = await workbook.render({ sheetName: "Primary review", range: "A1:O12", scale: 1 });
await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));

const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(xlsxPath);

const imported = await SpreadsheetFile.importXlsx(await FileBlob.load(xlsxPath));
const importedSheet = imported.worksheets.getItem("Primary review");
const importedValues = importedSheet.getRange("A1:O101").values;
if (importedValues.length !== 101 || importedValues[0].length !== 15) {
  throw new Error("Post-export workbook dimensions differ from the 100-row, 15-column contract.");
}
verifyFrozenReviewValues(importedValues);
const xlsxBytes = await fs.readFile(xlsxPath);
const xlsxSha = crypto.createHash("sha256").update(xlsxBytes).digest("hex");
const manifest = JSON.parse(await fs.readFile(manifestPath, "utf8"));
manifest.review_sheet_sha256.xlsx = xlsxSha;
manifest.xlsx_verification = {
  worksheet_count: 1,
  worksheet_name: "Primary review",
  data_row_count: 100,
  no_output_system_failure_count: noOutputCount,
  scorable_output_count: scorableCount,
  rating_validation: "1_TO_5_ON_OUTPUT_ROWS_ONLY",
  accept_validation: "YES_NO_ON_OUTPUT_ROWS_ONLY",
  post_export_import_check: "PASS",
};
await fs.writeFile(manifestPath, `${JSON.stringify(manifest, null, 2)}\n`, "utf8");
await fs.rm(`${xlsxPath}.inspect.ndjson`, { force: true });
console.log(JSON.stringify({ xlsxPath, xlsxSha, previewPath, noOutputCount, scorableCount }, null, 2));
