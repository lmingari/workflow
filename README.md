# Load anaconda 
module load anaconda3/2021.05

# First time
python create_cases.py

# Day workflow

* ./get_wrf.sh
* python run_cases.py
* python plot_cases.py
* TODO: python upload_images.py

