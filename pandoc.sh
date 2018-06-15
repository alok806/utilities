#!/bin/bash

# General purpose script to perform tasks while going to each of nested
# directories (single level)
# In this example, we use pandoc to convert our markdown files to
# either HTML, PDF or DOCX

file_format=docx

case $1 in
    pdf) file_format=pdf
        ;;
    docx) file_format=docx
        ;;
    html) file_format=html
        ;;
    *) 
        echo $"Usage: $0 {pdf|docx|html}"
        exit 1
esac

# Set your working directory (directory called 'archive' in this case)

pushd archive

for dir in ./*
do
    echo "Entering directory $dir"
    pushd $dir

    for file in ./*.md
    do
        basefile=$(echo `basename "$file"` | cut -f1 -d '.')
        echo "Deleting existing $file_format files in `pwd`"
        find `pwd` -name "*.$file_format" -type f -delete
        echo "Converting $file"
        pandoc -s -V geometry:margin=1in -o "${basefile}.${file_format}" $file
    done

    popd
done
