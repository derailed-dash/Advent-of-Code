# Create the target folder at same level as the template folder.
# Run this script from the folder above.

$dest_folder = "AoC_2022"
1..25 | ForEach-Object {
    $prefix = "d{0:d2}" -f $_
    $Destination = "${dest_folder}\${prefix}"
    Copy-Item -Path ".\template_folder\" -Destination $Destination -Recurse
}