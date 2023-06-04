# Create an "AoC" folder for the specified year, based on the template folder
# To use the script:
# .\create_year.ps1 <year>

param(
    [Parameter(Mandatory=$true, HelpMessage="Enter a year to use as a path suffix")]
    [ValidateNotNullOrEmpty()]
    [string]$year
)

$dest_folder = "..\src\AoC_$year"
1..25 | ForEach-Object {
    $prefix = "d{0:d2}" -f $_
    $Destination = "${dest_folder}\${prefix}"
    Copy-Item -Path "..\src\template_folder\" -Destination $Destination -Recurse
}