
$dir = "C:\Users\강영준\Documents\GitHub\retire-age-kr\work\research\ventures\x-kr-1\out"
$x = New-Object -ComObject Excel.Application; $x.DisplayAlerts = $false
$res = @{}
foreach ($f in "case_1","case_2","case_3","가계부_은퇴나이_2026","미리보기_12달") {
  $wb = $x.Workbooks.Open("$dir\$f.xlsx", 0, $true); Start-Sleep -Seconds 2
  $c = $wb.Worksheets.Item("계산"); $s1 = $wb.Worksheets.Item("월 가계부"); $s2 = $wb.Worksheets.Item("은퇴 나이")
  $o = @{}; foreach ($a in "B6","B7","B8","B9","B37","C37","D37","B93","C93","B149","D149","B20","B30","B31","B32") { $o[$a] = $c.Range($a).Value2 }
  $o["lines"] = @(); foreach ($r in 3..22) { if ($s1.Range("B$r").Value2) { $o["lines"] += ,@($s1.Range("B$r").Value2, $s1.Range("C$r").Value2, $s1.Range("E$r").Text) } }
  $o["s2"] = @{ B4 = $s2.Range("B4").Text; B7 = $s2.Range("B7").Text; B10 = $s2.Range("B10").Text; D10 = $s2.Range("D10").Text; F10 = $s2.Range("F10").Text }
  if ($f -like "가계부*") { $s2.ExportAsFixedFormat(0, "$dir\preview_sheet2.pdf"); $s1.ExportAsFixedFormat(0, "$dir\check_sheet1.pdf") }
  if ($f -like "미리보기*") {  # 그림은 12달 채운 미리보기 파일에서(순돌이 10/5: 막대 10칸 빈 그래프)
    # 대표 이미지 2장째(실제 시트 화면, 순돌이 10/5 ③): 시트 2 B2:H50을 그림으로 복사 → 빈 차트에 붙여 PNG
    foreach ($pair in @(@("은퇴 나이","A1:H50","sheet2.png"), @("월 가계부","A1:K16","sheet1.png"))) {
      $ws = $wb.Worksheets.Item($pair[0]); $ws.Activate() | Out-Null; $rg = $ws.Range($pair[1])
      $rg.CopyPicture(1, 2) | Out-Null
      $co = $ws.ChartObjects().Add(0, 0, $rg.Width, $rg.Height); $co.Activate() | Out-Null; Start-Sleep -Milliseconds 500
      $co.Chart.Paste() | Out-Null; $co.Chart.Export("$dir\" + $pair[2]) | Out-Null; $co.Delete() | Out-Null }
  }
  $res[$f] = $o; $wb.Close($false)
}
$x.Quit()
$res | ConvertTo-Json -Depth 6 | Out-File -Encoding utf8 "$dir\excel_raw.json"
