// ============================================================
// Compliance Cove — Tracking Endpoint
// ============================================================
// Deploy as: Web App → Execute as Me → Anyone can access
// This receives POST requests from demo pages and appends
// rows to the "Views" sheet.
// ============================================================

const SHEET_ID = '1PbxMHjbUJKKNZZdCLg8smlJvOsCLAl3xV8w55mlNc88';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const sheet = SpreadsheetApp.openById(SHEET_ID).getSheetByName('Views');
    
    sheet.appendRow([
      data.timestamp || new Date().toISOString(),
      data.demo || '',
      data.pageUrl || '',
      data.sessionId || '',
      data.userAgent || '',
      data.referrer || '',
      data.screen || '',
    ]);
    
    return ContentService.createTextOutput(JSON.stringify({ status: 'ok' }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ status: 'error', message: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Required for CORS preflight
function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({ status: 'ok', service: 'compliance-cove-tracking' }))
    .setMimeType(ContentService.MimeType.JSON);
}
