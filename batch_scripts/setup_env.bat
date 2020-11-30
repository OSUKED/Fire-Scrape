call cd ..
call conda env create -f environment.yml
call conda activate FireScrape
call ipython kernel install --user --name=FireScrape
pause