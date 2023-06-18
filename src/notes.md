# General Notes Relating to AoC

## Input Files

Eric has requested that we do not commit the input data to our repos.  At least, not in plain text.

My solution:

### Use Git-Crypt

Git-Crypt performs **transparent encryption and decryption** of selected files, when pushing/pulling from your GitHub repo, respectively.

### Install

On Linux / WSL:

```bash
sudo apt install git-crypt
```

In Windows, there is no equivalent, and even if you install in WSL, then the git integration with (say) Visual Studio Code, will break. To fix:

- Download the x86_64.exe from the latest tag here: https://github.com/AGWA/git-crypt/tags
- Rename it to git-crypt.exe and store it in a location in your path.

### Setup

We can do this per repo, but we can also use the same key between multiple repos.
If you've already got a key, be careful not to overwrite it!

```bash
git-crypt init # generate the secure key
git-crypt export-key ../git-crypt-key # exports the symmetric key
```

Now store the symmetric key securely! If you need to decrypt your repo on another machine, you'll need to supply this key.

### Use Git-Crypt in Your Repo

Create `.gitattributes` file in the root of your repo, alongside your `.gitignore`. This file tells git which files need to be encrypted/decrypted with git-crypt.

If your input files are all named `input.txt`, then your `.gitattributes` would look like this:

```
input.txt filter=git-crypt diff=git-crypt
```

Now commit your `.gitattributes`.

### Useful Git-Crypt Commands

```bash
git-crypt status # check what will be encrypted
git-crypt status -e # show only encrypted [and should be encrypted]

git-crypt lock # lock all files locally. (This happens transparently on push to remote.)
git-crypt unlock [path to keyfile] # unlock all encrypted local files. (Transparent on pull.)
```

For a newly cloned repo, you will need to unlock any encrypted files manually.  E.g.

```bash
git-crypt unlock ../git-crypt-key
```

### Retrospective Encryption

Of course, if you're doing this having previously staged / committed / pushed files, those files will not be encrypted automatically. But you can retrospectively fix this!

```bash
git-crypt status -f  # FIX, i.e. retrospectively encrypt files that were previous staged / committed
git commit -m "My retrofix"
git push
```

Caution: your git history will still contain the unencrypted versions.  You can deal with this if you want.  (If it were sensitive data you really needed to keep secret, you should definitely do this!)
