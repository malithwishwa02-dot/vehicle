param(
    [string]$Out = "d:\vehicle\aged_profile_demo",
    [int]$Days = 180,
    [int]$Seed = 42
)

python .\scripts\generate_aged_profile.py --out $Out --age-days $Days --seed $Seed --populate
Write-Host "Done. Inspect $Out" -ForegroundColor Green
