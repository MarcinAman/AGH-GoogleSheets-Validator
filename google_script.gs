function redValidator() {
 var ss = SpreadsheetApp.getActiveSpreadsheet();

 var active_sheet = ss.getSheets()[0];
 var error_sheet = ss.getSheetByName("Errors")

 var cell_error = error_sheet.getDataRange().getValues()
 for(i = 1;i<cell_error.length;i++){
   last_column = active_sheet.getLastColumn()
   last_column = String.fromCharCode(last_column+64)
   cell = active_sheet.getRange("A"+i+":"+last_column+""+i)

   if(cell_error[i][0] == "E"){
     cell.setBackground("red");
   }
   else{
     cell.setBackground("white");
   }
 }
}
