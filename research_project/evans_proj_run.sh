#! /bin/sh

# check that the relevant files are there (input data files (4))


if [ -e ./data/BMI565_ResearchProject_Data/H5N1_VN1203_DE_Probes.txt ]; then
    echo "DE Probes File exists"
else
    echo "DE Probes File does not exist"
    exit 1
fi

if [ -e ./data/BMI565_ResearchProject_Data/H5N1_VN1203_UNIVERSE_Probes.txt ]; then
    echo "UNIVERSE Probes File exists"
else
    echo "UNIVERSE probes File does not exist"
    exit 1
fi

if [ -e ./data/BMI565_ResearchProject_Data/KEGG_Pathway_Genes.txt ]; then
    echo "KEGG Pathway Genes File exists"
else
    echo "KEGG Pathway Genes File does not exist"
    exit 1
fi




# run part 1 




# check that part 1 executed properly 



# run part 2 

