#!/bin/bash
#date

if [ $# != 1 ]; then
    echo "Please provide particle species name: \"LowMassGammaGamma\" OR \"CohY1S\" OR \"CohY1S_0n0n\" OR \"CohY1S_0nXn\" OR \"CohY1S_XnXn\" OR \"InCohY1S\" OR \"CohY2S\" OR \"InCohY2S\" OR \"FeedDownY2S\"  !!!"
    exit
fi

if [ $1 != "LowMassGammaGamma" -a $1 != "CohY1S" -a $1 != "CohY1S_0n0n" -a $1 != "CohY1S_0nXn" -a $1 != "CohY1S_XnXn" -a $1 != "InCohY1S" -a $1 != "CohY2S" -a $1 != "InCohY2S" -a $1 != "FeedDownY2S" ]; then
    echo "The particle species name should be: \"LowMassGammaGamma\" OR \"CohY1S\" OR \"CohY1S_0n0n\" OR \"CohY1S_0nXn\" OR \"InCohY1S\" OR \"CohY2S\" OR \"InCohY2S\" OR \"InCohY2S\ OR \"FeedDownY2S\" !!!"
    exit
fi

dir=$1

lheFileDir="lheFiles"

if [ ! -d $dir/$lheFileDir ]; then
    mkdir -p $dir/$lheFileDir
fi

if [ "`ls -A $dir/$lheFileDir`" != "" ]; then
    rm -rf $dir/$lheFileDir/*
fi

cmsEnergyDiv2=2510

for inputFile in `ls $PWD/$dir/splitFiles/slight*`
do
    echo $inputFile

    baseFileName=`basename $inputFile`

    #outputFile=${baseFileName/.out/.lhe}
    if [[ $baseFileName =~ ".out" ]]; then
        outputFile=${baseFileName%.out}  # remove `.out`
    fi

    if [[ $baseFileName =~ ".tx" ]]; then
        outputFile=${baseFileName%.tx}  # remove `.tx`
    fi

    idx=${outputFile:$strLen-4}

    modIdx=$(echo $idx | sed 's/^0*//')  # remove leading zeroes
    #modIdx=$((10#$idx))  # remove leading zeroes

    modOutputFile=${outputFile/$idx/$modIdx}

    echo $outputFile
    #echo $modOutputFile
    #echo ""

    root -l -b << EOF
    .x convert_SL2LHE.C+("$inputFile","$dir/$lheFileDir/$outputFile",$cmsEnergyDiv2,$cmsEnergyDiv2)
    .q
EOF

done
