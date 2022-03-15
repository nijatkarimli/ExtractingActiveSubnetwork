

-> For successful run project, firstly run "readingPPI.py". this python file will read "PPI.sif" from "allData" folder and will create "ppiNodeList.txt" and "adjacency.json" files in "allData" folder

-> Secondly, you need to run "LastEnrichmentPhase.py". this file will automatically trigger to run "CreatingPopulationPhase.py" and "CrossoverAndMutationPhase.py".

-> If you want only create initial population you can only run "CreatingPopulationPhase.py". this python script will use "adjacency.json", "ppiNodeList.txt" and will create "initialPopulation.txt" file which contains initial population of our PPI network.