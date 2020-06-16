===============
Getting started
===============

This is where you describe how to get set up on a clean install, including the
commands necessary to get the raw data (using the `sync_data_from_s3` command,
for example), and then how to make the cleaned, final data sets.

Getting the raw data
--------------------
First, you need the Expanse books as an e-book format. Then you need to install Calibre so we can format the .epub / .mobi into a .txt file
without the additional crap, like ToC and Acknowledgement. I've made a couple of regex files for Calibres conversion programm.
You can find those in `/data/external`.

But I'm not sure which one I used in what order...

This needs to be updated obviously.

Once the book is converted into a clean .txt file, load each book into the corresponding `/data/raw` folder.