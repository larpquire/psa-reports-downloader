## psa-reports-downloader
If you work closely with Philippine data, you probably know that the Philippine Statistics Authority (PSA) provides highlights/key points on periodic statistical releases (such as monthly inflation, trade performance, etc) on its website at http://psa.gov.ph/. These summaries are usually accompanied by downloadable attachments (such as PDF or Excel files) containing the data used to generate the report. Sometimes, accessing and downloading these attachments can become excruciatingly tedious, especially if you're trying to gather data for longer time horizons and you need files from dozens or even hundreds of summary reports.

You can use this  Python script to quickly and conveniently download all attachments associated with a given report simply by providing the link to the report's page. Plus, this script allows you to specify multiple reports, so that you can download everything you need in one sitting.

## Requirements
This script runs on Python 2.7 and uses the following packages:

1. `requests` (`pip install requests`)
2. `lxml` (`pip install lxml`)

## Usage Instructions
To start downloading the data files, please install the above requirements and then go through the following steps:

1. Open the file `links.txt` in this project's root directory and make sure that the file is empty.
2. Paste the PSA report's link on a blank line. If you're going to download attachments from more than one report, paste each link on a separate line. For example, let's say you want  to download the attachments for two PSA summary reports: "Highlights of the Philippine Population 2015 Census of Population" and the "Monthly Integrated Survey of Selected Industries : May 2016". Then the contents of the `links.txt` file should look something like this:
    ```
    https://psa.gov.ph/content/highlights-philippine-population-2015-census-population
    https://www.psa.gov.ph/content/monthly-integrated-survey-selected-industries-may-2016
    ```
3. Save and close `links.txt`. *Important*: Make sure that `links.txt` has been closed before proceeding.
4. On the command line, `cd` to this project's root directory and run:
    ```
    $ python downloader.py
    ```
5. Wait for the download to finish.

## Output/Downloaded Files
Each PSA report included in the `links.txt` file will have its own directory where its attachments will be saved. To illustrate, the example used in the Usage Instructions above produces the following directory structure:
```
psa-reports-downloader
¦   .gitignore
¦   downloader.py
¦   LICENSE
¦   links.txt
¦   README.md
¦   requirements.txt
¦   
+---Downloads
    +---2016-07-14
        +---11.17.52
            +---001
            ¦       2015 population counts Summary.xlsx
            ¦       ARMM.xlsx
            ¦       CAR.xlsx
            ¦       Caraga.xlsx
            ¦       NCR.xlsx
            ¦       NIR.xlsx
            ¦       R01.xlsx
            ¦       R02.xlsx
            ¦       R03.xlsx
            ¦       R04A.xlsx
            ¦       R04B.xlsx
            ¦       R05.xlsx
            ¦       R06.xlsx
            ¦       R07.xlsx
            ¦       R08.xlsx
            ¦       R09.xlsx
            ¦       R10.xlsx
            ¦       R11.xlsx
            ¦       R12.xlsx
            ¦       
            +---002
                    sk160501.pdf
                    sk160502.pdf
                    sk160503.pdf
                    sk160504.pdf
                    sk160505.pdf
                    sk160506.pdf
                    sk160507.pdf
                    sk160508.pdf
```
The above directory tree shows that downloads are organized according to the date of download, then by the time of download, and then by the associated summary report. Here, the folder `001` contains downloaded attachments of the "Highlights of the Philippine Population 2015 Census of Population" while the folder `002` contains the downloaded attachments of the "Monthly Integrated Survey of Selected Industries : May 2016" report. The numberings of the reports folder are based on the `links.txt` file. The filenames of the attachments are kept as they appear on the PSA's servers.
                    
## Contributing
As always, please feel free to comment or suggest improvements.

## Disclaimer
The author is not affiliated in any way with the Philippine Statistics Authority.