## Input Files

Eric has requested that we do not commit the input data to our repos.  At least, not encrypted.

My solution:

## Use Git-Crypt

### Install

On Linux / WSL:
- sudo apt install git-crypt

Alas, this is not installed in Windows, and therefore the git integration in Windows VS Code will break. To fix:
- download the x86_64.exe from the latest tag here: https://github.com/AGWA/git-crypt/tags
- Rename it to git-crypt.exe and store it in a location in your path.

### Setup

We can do this per repo, but we can also use the same key between multiple repos.

- git-crypt init // generate the secure key
- git-crypt export-key ../git-crypt-key // exports the symmetric key
- Store the symmetric key securely!

### Use in Repo

- Create .gitattributes file in the repo \
`input.txt filter=git-crypt diff=git-crypt`

- Commit .gitattributes

- git-crypt status // check what will be encrypted
- git-crypt status -e  // show only encrypted [and should be encrypted]

- git-crypt lock // lock all files locally. (This happens transparently on push to remote.)
- git-crypt unlock [path to keyfile] // unlock all encrypted local files. (Transparent on pull.)

### Retrospective Encryption

- git-crypt status -f  // FIX, i.e. retrospectively encrypt files that were previous staged / committed
- git commit -m "Retrofix"
- git push 
