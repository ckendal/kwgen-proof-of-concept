# KWGen (KeyWord Generator): Proof of Concept Web Application
- Author: Chris Kendall

Tools used:
- Python
- HTML/CSS

### Dependencies
- See 'requirements.txt'

### Description
- Takes input of a CSV file and iteratively generates a list of ordered keywords (ordered by location of input columns)

### Instructions:
Input a CSV published to the web (from Google Sheets). Upon successful import, the download will begin shortly. Otherwise, you will recieve an error message.
The input file may have up to 10 columns of text data, not counting the Campaign Name column. The input file must have a column 'Campaign Name' with its first row populated.
However, the location of the 'Campaign Name' column in the input file does not matter.

### Release Notes:
- July 17, 2020:
-- Initial release

- July 23, 2020
-- Added support for entry of campaign name via the import file.

### Upcoming features
To Do:
- Add support for a single input column
- Add support for optional user input of Final URL
- Resolve encoding issues for uploading local files
- write formal documentation
- more code comments
- spruce up the appearance with CSS

Wishlist:
- Add feature to email results
- add user login/profiles
- add database functionality (requires secure login)
- add a link to the demo input sheet
- Impose rules for keyword restrictions (exclude special characters, enforce keyword length limits)
- Add support for phrase-match keywords

