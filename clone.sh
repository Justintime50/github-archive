mkdir -p $HOME/github-archive
cd $HOME/github-archive
CNTX={users}; NAME={Justintime50}; PAGE=1
curl "https://api.github.com/$CNTX/$NAME/repos?page=$PAGE&per_page=100" |
  grep -e 'git_url*' |
  cut -d \" -f 4 |
  xargs -L1 git clone 
