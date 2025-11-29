# Script to replace all PH Shorts / PHShorts references with RedLight DL

$files = Get-ChildItem -Path "d:\PornHub-Shorts" -Recurse -Include *.md,*.py -Exclude ".venv\*","build\*","dist\*"

foreach ($file in $files) {
    $content = Get-Content $file.FullName -Raw -Encoding UTF8
    
    # Skip if no changes needed
    if (-not ($content -match "PH Shorts|PHShorts|PornHub-Shorts")) {
        continue
    }
    
    Write-Host "Updating: $($file.Name)"
    
    # Replace references
    $content = $content -replace "PH Shorts Downloader", "RedLight DL"
    $content = $content -replace "PH Shorts DL", "RedLight DL"
    $content = $content -replace "PH Shorts", "RedLight DL"
    $content = $content -replace "PHShorts", "RedLight"
    $content = $content -replace "ph-shorts-dl", "ph-shorts"
    
    # Replace GitHub links
    $content = $content -replace "github\.com/diastom/PornHub-Shorts", "github.com/diastom/RedLightDL"
    $content = $content -replace "PornHub-Shorts", "RedLightDL"
    
    # Replace specific PornHub references (keep technical ones like URLs but update project name)
    $content = $content -replace "Download PornHub Shorts", "Professional Adult Content Downloader"
    $content = $content -replace "for PornHub Shorts", "for adult content"
    $content = $content -replace "Specialized.*PornHub Shorts", "Professional adult content downloader"
    
    # Save file
    Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
}

Write-Host "Done!"
