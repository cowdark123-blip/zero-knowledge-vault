$edgePath = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$testFile = 'file:///C:/Users/xuanhoang/.gemini/antigravity/scratch/zero-knowledge-vault/test_crypto.html'
$outFile = 'C:\Users\xuanhoang\.gemini\antigravity\scratch\zero-knowledge-vault\test_output.txt'

$argList = @(
    '--headless=new',
    '--disable-gpu',
    '--virtual-time-budget=10000',
    '--dump-dom',
    $testFile
)

$p = Start-Process -FilePath $edgePath -ArgumentList $argList -RedirectStandardOutput $outFile -PassThru
Start-Sleep -Seconds 3
$p.WaitForExit(10000)

Get-Content $outFile | Select-String -Pattern 'ALL TESTS PASSED', 'PASS', 'FAIL', 'Test ', 'STATUS'
