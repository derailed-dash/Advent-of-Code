## Input Files

Eric has requested that we do not commit the input data to our repos.  At least, not encrypted.

My solution:
 
- Use git-crypt
  - sudo apt install git-crypt
  - git-crypt init // generate the secure key
  - git-crypt export-key ../git-crypt-key // generate the key file
  - Store the file securely.
  - Create .gitattributes file in the repo \
    `input.txt filter=git-crypt diff=git-crypt`
  - Commit .gitattributes
    