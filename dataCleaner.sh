# clear out all data
rm -rd pr* data
tarTag=".tar.gz"
for tarFile in *.tar.gz;do
    tmpDir=${tarFile%"$tarTag"}
    echo $tmpDir
    rm -rd $tmpDir
done

# unzip
for tarFile in *.tar.gz;do
    tmpDir=${tarFile%"$tarTag"}
    echo $tmpDir
    tar -zxvf $tarFile
    mv data $tmpDir
done