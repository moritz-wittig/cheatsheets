# General helpers
## Setting up multiple Github users with SSH
1. Checking for existing SSH keys: `ls -al ~/.ssh`
2. Create new SSH: `ssh-keygen -t rsa -b 4096 -C "personalEmail@gmail.com"`
3. If not already directly saved in the corresponding folder -> Add your private SSH key to the ssh-agent and store your passphrase in the keychain: `ssh-add -K ~/.ssh/private/id_rsa`
4. Add a new SSH key to your account: `pbcopy < ~/.ssh/private/id_rsa.pub` and add to Github SSH keys
5. Make changes in the config file: `cd ~/.ssh` `touch config`
6. Adjust the file Copy and paste this text into the config file: 
    ```
    # Work2 GitHub account
        Host github.com-work2
        HostName github.com
        User git
        AddKeysToAgent yes
        UseKeychain yes
        IdentityFile ~/.ssh/private/id_rsa
    ```
7. Cd to repo_dir, then add new user locally: 
`git config --local user.name "Name Surname"`
`git config --local user.email "name.surname@company.com"`
8. Lastly, adjust the repositorys remote URLs: 
`git remote set-url origin git@work-github.com:account_name/repo_name.git`

Source:
- https://www.heady.io/blog/how-to-manage-multiple-github-accounts
- https://tommaso.pavese.me/2014/07/08/git-config-for-multiple-github-accounts/
