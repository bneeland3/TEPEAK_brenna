#!/bin/bash

# Variables for filename and species name
FILENAME=""
SPECIES=""

# Process command line flags
while getopts "f:s:" opt; do
  case $opt in
    f)
      FILENAME=$OPTARG
      ;;
    s)
      SPECIES=$OPTARG
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# Check if both required parameters are provided
if [[ -z $FILENAME || -z $SPECIES ]]; then
    echo "Both filename (-f) and species (-s) flags are required."
    exit 1
fi

# Unzip the file
echo "n" | unzip "${FILENAME}"

# Extract the base name from the filename (i.e., without .zip extension)
BASENAME=$(basename "${FILENAME%.*}")
DIR_PATH=$(dirname "${FILENAME}")

# Move the only file from the specified path to the current directory and rename
mv ncbi_dataset/data/${BASENAME}/$(ls ncbi_dataset/data/${BASENAME}/ | head -n 1) ${SPECIES}.fa

rm -r ncbi_dataset/
mv ${SPECIES}.fa "${DIR_PATH}/"

echo "File has been moved and renamed as ${SPECIES}.fa"
cd "${DIR_PATH}/"
samtools faidx ${SPECIES}.fa

bwa index -p ${SPECIES} ${SPECIES}.fa
