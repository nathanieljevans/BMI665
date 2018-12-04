#! /bin/sh

# check that the relevant files are there (input data files (4)) --------------

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

# run part 1 -----------------------------------------------------------------

echo ""
python evans_project-part1.py 
echo "" 

# check that part 1 executed properly ----------------------------------------

if [ -e ./outputs/chosen_pathway.pkl ]; then
    echo "Part 1 Script Executed Appropriately"
else
    echo "Part 1 did not execute properly. Exiting."
    exit 1
fi

# run part 2 -----------------------------------------------------------------

echo ""
python evans_project-part2.py
echo ""
 