from  argparse import ArgumentParser
from subprocess import run
from json import load as json_load
from yaml import safe_load as yaml_safe_load

def parse_args():
    parser = ArgumentParser(description = "Process and move files")
    parser.add_argument('-f', '--filename', required = True, help = "zipped genome filepath")
    parser.add_argument('-s', '--species', required = True, help = "species name")
    return parser.parse_args()

def main():
    args = parse_args()
    filename, species = args.filename, args.species
    
    # unzip the file and auto input 'no' to replace README prompt
    run(f'echo "n" | unzip {filename}', shell = True)
    with open('ncbi_dataset/data/dataset_catalog.json') as dataset_catalog, open(f'configs/config_{species}.yaml') as config_file: 
        parsed_dataset = json_load(dataset_catalog)
        config_file = yaml_safe_load(config_file)
    
    data_dir = config_file['data_directory']
    fa_filepath = f"ncbi_dataset/data/{parsed_dataset['assemblies'][2]['files'][0]['filePath']}"
    run(
        f"""
        cp {fa_filepath} {data_dir}/{species}/{species}.fa
        echo "File has been moved and renamed to {species}.fa"
        rm -r ncbi_dataset
        cd {data_dir}/{species}
        samtools faidx {species}.fa
        bwa index -p {species} {species}.fa
        """, shell = True
    )

    ## tried using subprocess.run instead of os.system for all bash commands. it was more hassle than needed. 
    ## doesn't work well with f"" and multiple commands
    ## maybe if i moved the multiline commands into a seperate bash script and called the script using subprocess.run

if __name__ == "__main__":
    main()