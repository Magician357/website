echo Starting Commit...
echo What should the message be?
read comment
git add main.py
cd html
git add *
git commit -m "$comment"
git push
