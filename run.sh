rm -rd pr*
tarTag=".tar.gz"
for tarFile in *.tar.gz;do
    tmpDir=${tarFile%"$tarTag"}
    python3 drawer.py $tmpDir
    #python3 parser.py $tmpDir
done