const SHEET_NAME = "Applications";
const HEADERS = [
  "Timestamp", "Name", "Roll Number", "Branch", "Year",
  "Email", "Phone", "Domain", "Why KMS", "Previous Experience", "Portfolio"
];

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents || "{}");
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheet = ss.getSheetByName(SHEET_NAME) || ss.insertSheet(SHEET_NAME);

    if (sheet.getLastRow() === 0) {
      sheet.appendRow(HEADERS);
      sheet.setFrozenRows(1);
    }

    sheet.appendRow([
      new Date(),
      data.name || "",
      data.roll_no || "",
      data.branch || "",
      data.year || "",
      data.email || "",
      data.phone || "",
      data.domain || "",
      data.reason || "",
      data.experience || "",
      data.portfolio || ""
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
