from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from pytz import timezone
import re
# Get dates
today = datetime.now()

# Get tomorrow's date by adding one day to today's date
tomorrow = today + timedelta(days=1)


print("Here are the upcoming CS2 Pro matches:\n")

url = "https://liquipedia.net/counterstrike/Liquipedia:Matches"

# Updated HTML content
response = requests.get(url)
html_content = response.text

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')
# Find the specific div with data-toggle-area-content="2"
div_content = soup.find('div', {'data-toggle-area-content': '2'})

# If the div is found, proceed to extract information
if div_content:
    # Find all tables with the specified class within the div
    tables = div_content.find_all('table', class_='wikitable wikitable-striped infobox_matches_content')

    # Iterate through each table
    for table in tables:
        # Find all rows in the table
        rows = table.find_all('tr')
        # Iterate through each row
        # Extract data from each table row (assuming there are multiple rows)
        for row in table.find_all('tr'):
            # Extract team names from first row cells with 'team-left' and 'team-right' classes
            if len(row.find_all('td', class_='team-left')) > 0 and len(row.find_all('td', class_='team-right')) > 0:
                team_left_cell = row.find('td', class_='team-left')
                team_right_cell = row.find('td', class_='team-right')
                
                # Extract all text content within the cell (may include extra spaces or newlines)
                team_left_name = team_left_cell.get_text(strip=True)  # Improved line
                team_right_name = team_right_cell.get_text(strip=True)  # Improved line
             
                            
            # Extract match details from the second row (assuming it has 'match-filler' class)
            if len(row.find_all('td', class_='match-filler')) > 0:
                match_details_cell = row.find('td', class_='match-filler')


                # Extract the ongoing match status (assuming it's within 'timer-object-countdown-live' class)
                match_status = match_details_cell.find('span', class_='timer-object-countdown-live')
                
                
                # Extract the league name from the anchor tag within 'league-icon-small-image' class
                league_details = match_details_cell.find('a', class_=None)  # Find anchor tag without a class
                

                # Find countdown element and extract date INSIDE the loop for each row
                countdown_span = row.find('span', class_='timer-object-countdown-only')
                if countdown_span:
                    timestamp = countdown_span['data-timestamp']
                    dt_object = datetime.fromtimestamp(int(timestamp))
                    if today <= dt_object <= tomorrow:
                        print(f"Match: {team_left_name} vs. {team_right_name}")
                        league_details = match_details_cell.find('a', class_=None)  # Find anchor tag without a class
                        if league_details:
                            print(f"League: {league_details.text.strip()}")
                        print(f"Date and Time (EST): {dt_object.strftime('%A, %m/%d/%Y, %I:%M %p')}")
                        # Get CEST 
                        dt_object_cest = dt_object.astimezone(timezone('CET'))
                        print(f"Date and Time (CET): {dt_object_cest.strftime('%A, %m/%d/%Y, %I:%M %p')}")
                        # Check if Twitch stream link exists in data-stream-twitch attribute
                        twitch_stream_link = None
                        if countdown_span.has_attr('data-stream-twitch'):
                            twitch_stream_link = countdown_span['data-stream-twitch']
                        else:
                            # If not found in data-stream-twitch attribute, try to extract from the href of the <a> tag
                            twitch_stream_link_tag = match_details_cell.find('a', href=re.compile(r"/counterstrike/Special:Stream/twitch/"))
                            if twitch_stream_link_tag:
                                twitch_stream_link = twitch_stream_link_tag['href']

                        if twitch_stream_link:
                            print(f"Twitch Stream Link: https://liquipedia.net/counterstrike/Special:Stream/twitch/{twitch_stream_link}")
                        else:
                            print("Twitch stream link not found for this match.")
                    else: 
                        break
                else:
                    print("Timestamp not found.")
                                
                # You can extract other details from the 'match-details_cell' element based on your needs
                print("---\n")
