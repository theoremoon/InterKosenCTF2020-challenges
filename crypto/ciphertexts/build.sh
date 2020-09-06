rm -rf distfiles
mkdir -p distfiles
(cd challenge; python3 main.py > ../distfiles/output.txt)
cp challenge/main.py distfiles
