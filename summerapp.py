from flask import Flask, render_template, request
import pandas as pd
import numpy as np

# +
app = Flask(__name__)
school_data = pd.read_csv("projectdata.csv")
school_data.replace('NA', np.nan, inplace=True)
school_data['Overall Scoring Trend'] = pd.Categorical(
    school_data['Overall Scoring Trend'],
    categories = ['Up', 'Neutral', 'Down'],
    ordered = True)

neighbor_map = {
            "Ada-Borup-West": ["Ada-Borup-West", "Climax-Shelly", "Fertile-Beltrami", "Norman County East", "Ulen-Hitterdal", "Dilworth-Glyndon-Felton", "Moorhead"],
            "Adrian": ["Adrian", "Edgerton", "Murray County Central", "Fulda", "Worthington", "Ellsworth", "Luverne"],
            "Aitkin": ["Aitkin", "Hill City", "McGregor", "Isle", "Onamia", "Brainerd", "Crosby-Ironton"],
            "Albany": ["Albany", "Upsala", "Holdingford", "St. Cloud", "Rocori", "Paynesville", "Melrose"],
            "Albert Lea": ["Albert Lea", "Alden-Conger", "NRHEG", "Blooming Prairie", "Austin", "Glenville-Emmons"],
            "Alden-Conger": ["Alden-Conger", "United South Central", "Albert Lea", 'Glenville-Emmons'],
            "Alexandria": ["Alexandria", "Parkers Prairie", "Browerville", "Osakis", "Minnewaska", "West Central Area", "Brandon-Evansville"],
            "Annandale": ["Annandale", "Kimball", "St. Cloud", "Monticello", "Maple Lake", "Howard Lake-Waverly-Winsted", "Dassel-Cokato", "Litchfield"],
            "Anoka-Hennepin": ["Anoka-Hennepin", "Elk River", "St. Francis", "Forest Lake", "Osseo", "Brooklyn Center", "Columbia Heights", "Fridley", "Spring Lake Park", "Centennial"],
            "Ashby": ["Ashby", "Fergus Falls", "Underwood", "Battle Lake", "Brandon-Evansville", "West Central"],
            "Atwater-Cosmos-Grove City (A.C.G.C.)": ["A.C.G.C.", "New London-Spicer", "Paynesville", "Eden Valley-Watkins", "Litchfield", "Hutchinson", "Buffalo Lake-Hector-Stewart", "Bird Island-Olivia-Lake Lillian", "Willmar"],
            "Austin": ["Austin", "Blooming Prairie", "Hayfield", "Southland", "Lyle", "Glenville-Emmons", "Albert Lea"],
            "Badger": ["Badger", "Roseau", "Greenbush-Middle River"],
            "Bagley": ["Bagley", "Clearbrook Gonvick", "Bemidji", "Park Rapids", "Waubun-Ogema-White Earth", "Mahnomen", "Fosston"],
            "Barnesville": ["Barnesville", "Moorhead", "Dilworth-Glyndon-Felton", "Hawley", "Pelican Rapids", "Rothsay", "Breckenridge"],
            "Barnum": ["Barnum", "McGregor", "Cromwell-Wright", "Carlton", "Wrenshall", "Moose Lake"],
            "Battle Lake": ["Battle Lake", "Underwood", "Perham-Dent", "Henning", "Parkers Prairie", "Brandon-Evansville", "Ashby"],
            "Becker": ["Becker", "St. Cloud", "Foley", "Princeton", "Big Lake", "Monticello"],
            "Belgrade-Brooten-Elrosa": ["Belgrade-Brooten-Elrosa", "Minnewaska", "Sauk Centre", "Melrose", "Paynesville", "New London-Spicer", "Kerkhoven-Murdock-Sunburg", "Benson"],
            "Belle Plaine": ["Belle Plaine", "Central", "Sibley East", "Le Sueur-Henderson", "New Prague Area", "Waconia", "Jordan", "Eastern Carver County"],
            "Bemidji": ["Bemidji", "Red Lake", "Blackduck", "Cass Lake-Bena", "Laporte", "Park Rapids", "Bagley", "Clearbrook Gonvick"],
            "Benson": ["Benson", "Hancock", "Minnewaska", "Belgrade-Brooten-Elrosa", "Kerkhoven-Murdock-Sunburg", "MACCRAY", "Montevideo", "Lac qui Parle Valley"],
            "Bertha-Hewitt": ["Bertha-Hewitt", "Wadena-Deer Creek", "Verndale", "Staples-Motley", "Browerville", "Parkers Prairie", "Henning"],
            "Big Lake": ["Big Lake", "Becker", "Princeton", "Elk River", "Monticello"],
            "Bird Island-Olivia-Lake Lillian": ["Bird Island-Olivia-Lake Lillian", "Willmar", "A.C.G.C.", "Buffalo Lake-Hector-Stewart", "GFW", "Cedar Mountain", "Redwood Area", "Renville County West"],
            "Blackduck": ["Blackduck", "Kelliher", "South Koochiching", "Grand Rapids", "Cass Lake-Bena", "Bemidji", "Red Lake"],
            "Blooming Prairie": ["Blooming Prairie", "Owatonna", "Triton", "Hayfield", "Austin", "Albert Lea", "NRHEG"],
            "Bloomington": ["Bloomington", "Burnsville", "Eden Prairie", "Edina", "Richfield", "West St. Paul-Mendota Hts.-Eagan"],
            "Blue Earth Area": ["Blue Earth Area", "Granada Huntley East Chain", "Truman", "Maple River", "United South Central"],
            "Braham": ["Braham", "Ogilvie", "Mora", "Pine City", "Rush City", "Cambridge-Isanti"],
            "Brainerd": ["Brainerd", "Pine River Backus", "Pequot Lakes", "Crosby-Ironton", "Aitkin", "Onamia", "Pierz", "Little Falls", "Pillager"],
            "Brandon-Evansville": ["Brandon-Evansville", "Ashby", "Battle Lake", "Parkers Prairie", "Alexandria", "West Central Area"],
            "Breckenridge": ["Breckenridge", "Barnesville", "Rothsay", "Fergus Falls", "Campbell-Tintah"],
            "Brooklyn Center": ["Brooklyn Center", "Fridley", "Columbia Heights", "Minneapolis", "Robbinsdale", "Osseo", "Anoka-Hennepin"],
            "Browerville": ["Browerville", "Bertha-Hewitt", "Staples-Motley", "Little Falls", "Swanville", "Long Prairie-Grey Eagle", "Osakis", "Alexandria", "Parkers Prairie"],
            "Browns Valley": ["Browns Valley", "Wheaton Area", "Clinton-Graceville-Beardsley"],
            "Buffalo-Hanover-Montrose": ["Buffalo-Hanover-Montrose", "Maple Lake", "Monticello", "St. Michael-Albertville", "Osseo", "Elk River", "Rockford", "Delano", "Watertown-Mayer", "Howard Lake-Waverly-Winsted"],
            "Buffalo Lake-Hector-Stewart": ["Buffalo Lake-Hector-Stewart", "A.C.G.C.", "Hutchinson", "Glencoe-Silver Lake", "GFW", "Cedar Mountain", "Bird Island-Olivia-Lake Lillian"],
            "Burnsville-Eagan-Savage": ["None"],
            "Butterfield": ["Butterfield", "Comfrey", "St. James", "Martin County West", "Mountain Lake"],
            "Byron": ["Byron", "Pine Island", "Rochester", "Stewartville", "Hayfield", "Kasson-Mantorville"],
            "Caledonia": ["Caledonia", "Spring Grove", "Houston", "La Crescent-Hokah"],
            "Cambridge-Isanti": ["Cambridge-Isanti", "Ogilvie", "Braham", "Rush City", "North Branch", "Forest Lake", "St. Francis", "Princeton"],
            "Campbell-Tintah": ["Campbell-Tintah", "Breckenridge", "Fergus Falls", "West Central Area", "Herman-Norcross", "Wheaton Area"],
            "Canby": ["Canby", "Lac qui Parle Valley", "Dawson-Boyd", "Yellow Medicine East", "Minneota", "Ivanhoe", "Hendricks"],
            "Cannon Falls": ["Cannon Falls", "Red Wing", "Goodhue", "Kenyon-Wanamingo", "Northfield", "Randolph", "Hastings"],
            "Carlton": ["Carlton", "Barnum", "Cromwell-Wright", "Cloquet", "Wrenshall", "Esko"],
            "Cass Lake-Bena": ["Cass Lake-Bena", "Bemidji", "Blackduck", "Grand Rapids", "Deer River", "Northland Community", "Walker-Hackensack-Akeley", "Laporte"],
            "Cedar Mountain": ["Cedar Mountain", "Redwood Area", "Bird Island-Olivia-Lake Lillian", "Buffalo Lake-Hector-Stewart", "GFW", "Sleepy Eye", "Springfield", "Wabasso"],
            "Centennial": ["Centennial", "Spring Lake Park", "Mounds View", "White Bear Lake", "Anoka-Hennepin", "Forest Lake"],
            "Central": ["Central", "Glencoe-Silver Lake", "Lester Prairie", "Waconia", "Belle Plaine", "Sibley East"],
            "Chatfield": ["Chatfield", "Rochester", "Dover-Eyota", "St. Charles", "Rushford-Peterson", "Lanesboro", "Fillmore Central", "Kingsland", "Stewartville"],
            "Chisago Lakes": ["Chisago Lakes", "North Branch", "Forest Lake", "Franconia"],
            "Chisholm": ["Chisholm", "St. Louis County", "Mountain Iron-Buhl", "Hibbing"],
            "Chokio-Alberta": ["Chokio-Alberta", "Clinton-Graceville-Beardsley", "Wheaton Area", "Herman-Norcross", "Morris Area", "Lac qui Parle Valley", "Ortonville"],
            "Clearbrook-Gonvick": ["Clearbrook-Gonvick", "Red Lake County Central", "Red Lake", "Bemidji", "Bagley", "Fosston", "Win E Mac"],
            "Cleveland": ["Cleveland", "La Sueur Henderson", "Tri-City United", "Waterville-Elysian-Morristown", "Mankato", "St. Peter"],
            "Climax-Shelly": ["Climax-Shelly", "Fisher", "Crookston", "Fertile-Beltrami", "Ada-Borup-West"],
            "Clinton-Graceville-Beardsley": ["Clinton-Graceville-Beardsley", "Browns Valley", "Wheaton Area", "Herman-Norcross", "Chokio-Alberta", "Ortonville"],
            "Cloquet": ["Cloquet", "Esko", "Carlton", "Cromwell-Wright", "St. Louis County", "Proctor"],
            "Columbia Heights": ["Columbia Heights", "Fridley", "Mounds View", "St. Anthony-New Brighton", "Minneapolis", "Brooklyn Center"],
            "Comfrey": ["Comfrey", "Springfield", "Sleepy Eye", "St. James", "Butterfield", "Mountain Lake", "Red Rock Central"],
            "Cook County": ["Cook County", "Lake Superior"],
            "Cromwell-Wright": ["Cromwell-Wright", "McGregor", "Floodwood", "St. Louis County", "Cloquet", "Carlton", "Barnum"],
            "Crookston": ["Crookston", "Fisher", "East Grand Forks", "Warren-Alvarado-Oslo", "Thief River Falls", "Red Lake Falls", "Fertile-Beltrami", "Climax-Shelly"],
            "Crosby-Ironton": ["Crosby-Ironton", "Pequot Lakes", "Pine River Backus", "Northland Community", "Aitkin", "Brainerd"],
            "Dassel-Cokato": ["Dassel-Cokato", "Litchfield", "Kimball", "Annandale", "Howard Lake-Waverly-Winsted", "Glencoe-Silver Lake", "Hutchinson"],
            "Dawson-Boyd": ["Dawson-Boyd", "Lac qui Parle Valley", "Montevideo", "Yellow Medicine East", "Minneota", "Canby"],
            "Deer River": ["Deer River", "Grand Rapids", "Northland Community", "Cass Lake-Bena"],
            "Delano": ["Delano", "Buffalo-Hanover-Montrose", "Rockford", "Howard Lake-Waverly-Winsted", "Watertown-Mayer", "Orono"],
            "Detroit Lakes": ["Detroit Lakes", "Waubun-Ogema-White Earth", "Park Rapids", "Frazee-Vergas", "Perham-Dent", "Pelican Rapids", "Lake Park Audubon"],
            "Dilworth-Glyndon-Felton": ["Dilworth-Glyndon-Felton", "Moorhead", "Ada-Borup-West", "Ulen-Hitterdal", "Hawley", "Barnesville"],
            "Dover-Eyota": ["Dover-Eyota", "St. Charles", "Chatfield", "Rochester", "Plainview-Elgin-Millville"],
            "Duluth": ["Duluth", "St. Louis County", "Mesabi East", "Lake Superior", "Hermantown"],
            "East Central": ["East Central", "Wrenshall", "Moose Lake", "Willow River", "McGregor", "Mora", "Hinckley-Finlayson"],
            "Eastern Carver County": ["Eastern Carver County", "Westonka", "Minnetonka", "Eden Prairie", "Shakopee", "Jordan", "Belle Plaine", "Waconia"],
            "East Grand Forks": ["East Grand Forks", "Warren-Alvarado-Oslo", "Crookston", "Fisher"],
            "Eden Prairie": ["Eden Prairie", "Burnsville", "Shakopee", "Eastern Carver County", "Minnetonka", "Hopkins", "Edina", "Bloomington"],
            "Eden Valley-Watkins": ["Eden Valley-Watkins", "Paynesville", "Rocori", "Kimball", "Litchfield", "A.C.G.C."],
            "Edgerton": ["Edgerton", "Pipestone Area", "Murray County Central", "Adrian", "Luverne"],
            "Edina": ["Edina", "St. Louis Park", "Minneapolis", "Richfield", "Bloomington", "Eden Prairie", "Hopkins"],
            "Elk River": ["Elk River", "Big Lake", "Princeton", "St. Francis", "Anoka-Hennepin", "Osseo", "Buffalo-Hanover-Montrose", "St. Michael-Albertville", "Monticello"],
            "Ellsworth": ["Ellsworth", "Luverne", "Adrian", "Worthington"],
            "Ely": ["Ely", "St. Louis County", "Lake Superior"],
            "Esko": ["Esko", "Proctor", "Hermantown", "Wrenshall", "Carlton", "Cloquet"],
            "Fairmont Area": ["Fairmont Area", "Martin County West", "Truman", "Granada Huntley East Chain"],
            "Faribault": ["Faribault", "Northfield", "Kenyon-Wanamingo", "Medford", "Waterville-Elysian-Morristown", "Tri-City United"],
            "Farmington": ["Farmington", "Lakeville", "Randolph", "Rosemount-Apple Valley-Eagan", "Northfield"],
            "Fergus Falls": ["Fergus Falls", "Rothsay", "Pelican Rapids", "Underwood", "Ashby", "West Central Area", "Campbell-Tintah", "Breckenridge"],
            "Fertile-Beltrami": ["Fertile-Beltrami", "Climax-Shelly", "Crookston", "Red Lake Falls", "Win E Mac", "Mahnomen", "Norman County East", "Ada-Borup-West"],
            "Fillmore Central": ["Fillmore Central", "LeRoy-Ostrander", "Kingsland", "Chatfield", "Lanesboro", "Mabel-Canton"],
            "Fisher": ["Fisher", "East Grand Forks", "Crookston", "Climax-Shelly"],
            "Floodwood": ["Floodwood", "Cromwell-Wright", "McGregor", "Hill City", "Grand Rapids", "Nashwauk-Keewatin", "Hibbing", "St. Louis County"],
            "Foley": ["Foley", "Pierz", "Milaca", "Princeton", "Becker", "St. Cloud", "Sauk Rapids-Rice"],
            "Forest Lake": ["Forest Lake", "Franconia", "Chisago Lakes", "North Branch", "Cambridge-Isanti", "St. Francis", "Anoka-Hennepin", "Centennial", "White Bear Lake", "Mahtomedi", "Stillwater Area"],
            "Fosston": ["Fosston", "Win E Mac", "Clearbrook-Gonvick", "Bagley", "Mahnomen"],
            "Frazee-Vergas": ["Frazee-Vergas", "Detroit Lakes", "Park Rapids", "Pine Point", "Menahga", "New York Mills", "Perham-Dent", "Pelican Rapids"],
            "Fridley": ["Fridley", "Spring Lake Park", "Mounds View", "Columbia Heights", "Brooklyn Center", "Anoka-Hennepin"],
            "Fulda": ["Fulda", "Murray County Central", "Westbrook-Walnut Grove", "Heron Lake-Okabena", "Round Lake-Brewster", "Worthington", "Adrian"],
            "GFW": ["GFW", "Buffalo Lake-Hector-Stewart", "Glencoe-Silver Lake", "Sibley East", "New Ulm", "Sleepy Eye", "Cedar Mountain", "Bird Island-Olivia-Lake Lillian"],
            "Glencoe-Silver Lake": ["Glencoe-Silver Lake", "Hutchinson", "Dassel-Cokato", "Howard Lake-Waverly-Winsted", "Lester Prairie", "Central", "Sibley East", "GFW", "Buffalo Lake-Hector-Stewart"],
            "Glenville-Emmons": ["Glenville-Emmons", "United South Central", "Alden-Conger", "Albert Lea", "Austin", "Lyle"],
            "Goodhue": ["Goodhue", "Cannon Falls", "Red Wing", "Lake City", "Zumbrota Mazeppa", "Kenyon-Wanamingo"],
            "Goodridge": ["Goodridge", "Greenbush-Middle River", "Grygla", "Red Lake", "Red Lake County Central", "Thief River Falls"],
            "Granada Huntley East Chain": ["Granada Huntley East Chain", "Fairmont Area", "Truman", "Blue Earth Area"],
            "Grand Meadow": ["Grand Meadow", "Hayfield", "Stewartville", "Kingsland", "LeRoy-Ostrander", "Southland"],
            "Grand Rapids": ["Grand Rapids", "Blackduck", "Kelliher", "South Koochiching", "St. Louis County", "Hibbing", "Nashwauk-Keewatin", "Greenway", "Floodwood", "Hill City", "Northland Community", "Deer River", "Cass Lake-Bena"],
            "Greenbush-Middle River": ["Greenbush-Middle River", "Lancaster", "Tri-County", "Marshall County Central", "Thief River Falls", "Goodridge", "Grygla", "Roseau", "Badger"],
            "Greenway": ["Greenway", "Grand Rapids", "Nashwauk-Keewatin"],
            "Grygla": ["Grygla", "Greenbush-Middle River", "Roseau", "Lake of the Woods", "Kelliher", "Red Lake", "Goodridge"],
            "Hancock": ["Hancock", "Morris Area", "Minnewaska", "Benson", "Lac qui Parle Valley"],
            "Hastings": ["Hastings", "Randolph", "Farmington", "Rosemount-Apple Valley-Eagan", "South Washington County", "Stillwater Area", "Red Wing", "Cannon Falls"],
            "Hawley": ["Hawley", "Dilworth-Glyndon-Felton", "Ulen-Hitterdal", "Lake Park Audubon", "Pelican Rapids", "Barnesville"],
            "Hayfield": ["Hayfield", "Triton", "Kasson-Mantorville", "Byron", "Stewartville", "Grand Meadow", "Southland", "Austin", "Blooming Prairie"],
            "Hendricks": ["Hendricks", "Canby", "Ivanhoe", "Lake Benton"],
            "Henning": ["Henning", "Perham-Dent", "New York Mills", "Wadena-Deer Creek", "Bertha-Hewitt", "Parkers Prairie", "Battle Lake"],
            "Herman-Norcross": ["Herman-Norcross", "Wheaton Area", "Campbell-Tintah", "West Central Area", "Morris Area", "Chokio-Alberta", "Clinton-Graceville-Beardsley"],
            "Hermantown": ["Hermantown", "Proctor", "St. Louis County", "Duluth", "Esko"],
            "Heron Lake-Okabena": ["Heron Lake-Okabena", "Westbrook-Walnut Grove", "Red Rock Central", "Windom", "Jackson County Central", "Round Lake-Brewster", "Fulda"],
            "Hibbing": ["Hibbing", "Floodwood", "Grand Rapids", "Nashwauk-Keewatin", "St. Louis County", "Chisholm", "Mountain Iron-Buhl"],
            "Hill City": ["Hill City", "Aitkin", "McGregor", "Floodwood", "Grand Rapids", "Northland Community", "Crosby-Ironton"],
            "Hills-Beaver Creek": ["Hills-Beaver Creek", "Pipestone Area", "Luverne"],
            "Hinckley-Finlayson": ["Hinckley-Finlayson", "Pine City", "Mora", "East Central"],
            "Holdingford": ["Holdingford", "Upsala", "Royalton", "Sauk Rapids-Rice", "Sartell-St. Stephen", "St. Cloud", "Albany"],
            "Hopkins": ["Hopkins", "Wayzata", "Robbinsdale", "Minneapolis", "St. Louis Park", "Edina", "Eden Prairie", "Minnetonka"],
            "Houston": ["Houston", "Winona Area", "La Crescent-Hokah", "Caledonia", "Spring Grove", "Mabel-Canton", "Rushford Peterson"],
            "Howard Lake-Waverly-Winsted": ["Howard Lake-Waverly-Winsted", "Dassel-Cokato", "Annandale", "Maple Lake", "Buffalo-Hanover-Montrose", "Watertown-Mayer", "Lester Prairie", "Glencoe-Silver Lake"],
            "Hutchinson": ["Hutchinson", "A.C.G.C.", "Litchfield", "Dassel-Cokato", "Glencoe-Silver Lake", "Buffalo Lake-Hector Stewart"],
            "International Falls": ["International Falls", "Littlefork-Big Falls", "Nett Lake", "St. Louis County"],
            "Inver Grove Heights": ["Inver Grove Heights", "South St. Paul", "South Washington County", "Rosemount-Apple Valley-Eagan", "West St. Paul-Mendota Hts.-Eagan"],
            "Isle": ["Isle", "Aitkin", "McGregor", "Mora", "Ogilvie", "Onamia"],
            "Ivanhoe": ["Ivanhoe", "Hendricks", "Canby", "Minneota", "RTR", "Lake Benton"],
            "Jackson County Central": ["Jackson County Central", "Round Lake-Brewster", "Heron Lake-Okabena", "Windom", "Mountain Lake", "Martin County West"],
            "Janesville-Waldorf-Pemberton": ["Janesville-Waldorf-Pemberton", "St. Clair", "Mankato", "Waterville-Elysian-Morristown", "Waseca", "NRHEG", "United South Central", "Maple River"],
            "Jordan": ["Jordan", "New Prague", "Belle Plaine", "Lakeville", "Prior Lake-Savage", "Shakopee", "Eastern Carver County"],
            "Kasson-Mantorville": ["Kasson-Mantorville", "Triton", "Pine Island", "Byron", "Stewartville", "Hayfield"],
            "Kelliher": ["Kelliher", "Lake of the Woods", "South Koochiching", "Grand Rapids", "Blackduck", "Red Lake", "Grygla"],
            "Kenyon-Wanamingo": ["Kenyon-Wanamingo", "Northfield", "Cannon Falls", "Goodhue", "Zumbrota-Mazeppa", "Pine Island", "Triton", "Owatonna", "Medford", "Faribault"],
            "Kerkhoven-Murdock-Sunburg": ["Kerkhoven-Murdock-Sunburg", "Benson", "Belgrade-Brooten-Elrosa", "New London-Spicer", "Willmar", "MACCRAY"],
            "Kimball": ["Kimball", "Rocori", "St. Cloud", "Annandale", "Dassel-Cokato", "Litchfield", "Eden Valley-Watkins"],
            "Kingsland": ["Kingsland", "Stewartville", "Chatfield", "Fillmore Central", "LeRoy-Ostrander", "Grand Meadow"],
            "Kittson Central": ["Kittson Central", "Lancaster", "Tri County", "Stephen-Argyle Central"],
            "Lac qui Parle Valley": ["Lac qui Parle Valley", "Ortonville", "Chokio-Alberta", "Morris Area", "Hancock", "Benson", "Montevideo", "Dawson-Boyd", "Canby"],
            "La Crescent-Hokah": ["La Crescent-Hokah", "Winona Area", "Houston", "Caledonia"],
            "Lake Benton": ["Lake Benton", "Handricks", "Ivanhoe", "RTR", "Pipestone Area"],
            "Lake City": ["Lake City", "Red Wing", "Goodhue", "Zumbrota-Mazeppa", "Rochester", "Plainview-Elgin-Millville", "Wabasha-Kellogg"],
            "Lake Crystal-Wellcome Memorial": ["Lake Crystal-Wellcome Memorial", "Nicolett", "Mankato", "St. Clair", "Maple River", "Madelia", "New Ulm"],
            "Lake of the Woods": ["Lake of the Woods", "South Koochiching", "Kelliher", "Grygla", "Roseau", "Warroad"],
            "Lake Park Audubon": ["Lake Park Audubon", "Ulen-Hitterdal", "Waubun-Ogema-White Earth", "Detroit Lakes", "Pelican Rapids", "Hawley"],
            "Lake Superior": ["Lake Superior", "Cook County", "St. Louis County", "Ely", "Mesabi East", "Duluth"],
            "Lakeview": ["Lakeview", "Yellow Medicine East", "Milroy", "Marshall", "Minneota"],
            "Lakeville": ["Lakeville", "Prior Lake-Savage", "Burnsville", "Rosemount-Apple Valley-Eagan", "Farmington", "New Prague", "Northfield"],
            "Lancaster": ["Lancaster", "Kittson Central", "Tri County", "Greenbush-Middle River"],
            "Lanesboro": ["Lanesboro", "Mabel-Canton", "Fillmore Central", "Chatfield", "St. Charles", "Rushford-Peterson"],
            "Laporte": ["Laporte", "Bemidji", "Cass Lake-Bena", "Walker-Hackensack-Akeley", "Nevis", "Park Rapids"],
            "LeRoy-Ostrander": ["LeRoy-Ostrander", "Southland", "Grand Meadow", "Kingsland", "Fillmore Central"],
            "Lester Prairie": ["Lester Prairie", "Howard Lake-Waverly Winsted", "Watertown-Mayer", "Waconia", "Central", "Glencoe-Silver Lake"],
            "Le Sueur-Henderson": ["Le Sueur-Henderson", "Sibley East", "Belle Plaine", "New Prague Area", "Tri-City United", "Cleveland", "St. Peter"],
            "Lewiston-Altura": ["Lewiston-Altura", "Plainview-Elgin-Millville", "Winona Area", "Rushford-Peterson", "St. Charles"],
            "Litchfield": ["Litchfield", "Eden Valley-Watkins", "Kimball", "Annandale", "Dassel-Cokato", "Hutchinson", "A.C.G.C."],
            "Little Falls": ["Little Falls", "Pillager", "Brainerd", "Pierz", "Royalton", "Upsala", "Swanville", "Browerville", "Staples Motley"],
            "Littlefork-Big Falls": ["Littlefork-Big Falls", "South Koochiching", "St. Louis County", "Nett Lake", "International Falls"],
            "Long Prairie-Grey Eagle": ["Long Prairie-Grey Eagle", "Browerville", "Swanville", "Upsala", "Melrose", "Sauk Centre", "Osakis"],
            "Luverne": ["None"],
            "Lyle": ["None"],
            "Lynd": ["None"],
            "Mankato": ["Mankato", "St. Peter", "Cleveland", "Waterville-Elysian-Morristown", "Janesville-Waldorf-Pemberton", "Maple River", "St. Clair", "Lake Crystal-Wellcome Memorial", "Nicollet"],
            "Redwood Area": ["Redwood Area", "Yellow Medicine East", "Renville County West", "Bird Island-Olivia-Lake Lillian", "Cedar Mountain", "Wabasso"],
            "Southland": ["Southland", "Lyle", "Austin", "Hayfield", "Grand Meadow", "LeRoy-Ostrander"],
            "Stephen-Argyle Central": ["Stephen-Argyle Central", "Kittson Central", "Tri-County", "Marshall County Central", "Warren-Alvarado-Oslo"],
            "St. Michael-Albertville": ["St. Michael-Albertville", "Monticello", "Big Lake", "Elk River", "Buffalo-Hanover-Montrose"],
            "Tracy Area": ["Tracy Area", "Lynd", "Marshall", "Milroy", "Westbrook-Walnut Grove", "Murray County Central", "RTR"]
        }

def score_qualities(read, math, science, attend, care, suspend, NW, ELL, SE, FRL, preschool, STratio, para, license, advanced, fed, trend, data):
    
        from sklearn.preprocessing import MinMaxScaler
        
        display_data = data.copy()
        data = data.copy()
        data['Overall Scoring Trend'] = data['Overall Scoring Trend'].cat.codes
        data['Overall Scoring Trend'] = data['Overall Scoring Trend'].replace(-1, 3)
        #data['Overall Scoring Trend'] = 2 - data['Overall Scoring Trend']
        
        numeric_cols = [col for col in data.columns if col not in ['District', 'Name', 'Overall Scoring Trend']]
        scale = MinMaxScaler()
        data[numeric_cols] = scale.fit_transform(data[numeric_cols])
        
        user_preferences = {
            'Reading Performance': read,
            'Math Performance': math,
            'Science Performance': science,
            'Attendance': attend,
            'Parent Opinion': care,
            'Suspension Rate': suspend,
            'Non-White Percentage': NW,
            'ELL Percentage': ELL,
            'Special Ed Percentage': SE,
            'Free-Reduced Lunch Percentage': FRL,
            'Preschool Attendance': preschool,
            'Student-Teacher Ratio': STratio,
            'Para Percentage': para,
            'Licensed Percentage': license,
            'Advanced Degree Percentage': advanced,
            'Federal Funding': fed,
            'Overall Trend': trend
        }
        
        howto_sort = {
        'Reading Performance': ('Meets Read Standards', False),
        'Math Performance': ('Meets Math Standards', False),
        'Science Performance': ('Meets Science Standards', False),
        'Attendance': ('Consistent Attendance Rate', False),
        'Parent Opinion': ('Caring Teachers', False),
        'Suspension Rate': ('Suspension Rate', True),
        'Non-White Percentage': ('Non-White Percentage', False),
        'ELL Percentage': ('ELL Percentage', False),
        'Special Ed Percentage': ('SE Percentage', False),
        'Free-Reduced Lunch Percentage': ('FRL Percentage', False),
        'Preschool Attendance': ('Preschool Attendance', False),
        'Student-Teacher Ratio': ('Student-Teacher Ratio', True),
        'Para Percentage': ('Percent Paras', False),
        'Licensed Percentage': ('Licensed Teachers', False),
        'Advanced Degree Percentage': ('Advanced Degree Teachers', False),
        'Federal Funding': ('Percent Federal Funds', False),
        'Overall Trend': ('Overall Scoring Trend', True),
        }
        useful_qualities = [(quality, rank) for quality,rank in user_preferences.items() if rank not in (0, None)]
        if not useful_qualities:
            return "You have not selected any qualities to rank by!"
        
        bottom_ranked = max(rank for _, rank in useful_qualities)
        weights = {quality: bottom_ranked - rank + 1 for quality, rank in useful_qualities}

        # Compute weighted score for each school
        score_series = pd.Series(0, index=data.index)
        for quality, weight in weights.items():
            col, higher_is_better = howto_sort[quality]

            if not higher_is_better:
                score_series += data[col] * weight
            else:
                score_series += (1 - data[col]) * weight  # invert if lower is better

        display_data["Final Score"] = score_series

        # Sort descending (best schools first)
        return display_data.sort_values("Final Score", ascending=False).drop(columns=["Final Score"])
        
def filter_single(quality, asc, data):
    try:
        data2 = data.sort_values(by=quality, ascending=asc, na_position='last')
        return data2
    except:
        return "Sorting was unsuccessful! The quality to sort by was invalid or another error occured."
        
def geographic_filter(districts, data):
    matching_schools = []
    for district in districts:
        for _, school in data.iterrows():
            if school['District'] == district:
                matching_schools.append(school)
    matching_schools = pd.DataFrame(matching_schools) 
    return matching_schools



# -

@app.route('/')
def home():
    return render_template('homepage.html')  

@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/results', methods=['POST'])
def results():
    read = int(request.form['read'])
    math = int(request.form['math'])
    science = int(request.form['science'])
    attend = int(request.form['attend'])
    care = int(request.form['care'])
    suspend = int(request.form['suspend'])
    NW = int(request.form['NW'])
    ELL = int(request.form['ELL'])
    SE = int(request.form['SE'])
    FRL = int(request.form['FRL'])
    preschool = int(request.form['preschool'])
    STratio = int(request.form['STratio'])
    para = int(request.form['para'])
    license = int(request.form['license'])
    advanced = int(request.form['advanced'])
    fed = int(request.form['fed'])
    trend = int(request.form['trend'])
    
    sorted_data = score_qualities(read, math, science, attend, care, suspend, NW, ELL, SE, FRL, preschool, STratio, para, license, advanced, fed, trend, school_data)
    
    selected = request.form.get("geography")   # same name as in your <select> in HTML
    if selected:
        included = neighbor_map.get(selected, [selected])
        sorted_data = geographic_filter(included, sorted_data)
    
    renamed_data = sorted_data.rename(columns={
    "Meets Read Standards": "% of Students Proficient in Reading",
    "Meets Math Standards": "% of Students Proficient in Math",
    "Meets Science Standards": "% of Students Proficient in Science",
    "Consistent Attendance Rate": "% of Students Consistently Attending Class",
    "Caring Teachers": "% of Students That Believe Teachers Care",
    "Suspension Rate": "% of Students That Receive Suspensions",
    "Non-White Percentage": "% of Students That Are Non-White",
    "ELL Percentage": "% of Students That Are English Language Learners",
    "SE Percentage": "% of Students Enrolled in Special Education",
    "FRL Percentage": "% of Students That Receive Free/Reduced Lunch",
    "Preschool Attendance": "% of Students That Attended Preschool",
    "Student-Teacher Ratio": "# of Students Per Teacher",
    "Percent Paras": "% of Staff That Are Paraprofessionals",
    "Licensed Teachers": "% of Staff That Are Licensed",
    "Advanced Degree Teachers": "% of Staff With Advanced Degrees",
    "Percent Federal Funds": "% of Funding from Federal Government"
    })
    
    cols_to_round = [
    "% of Students Proficient in Reading",
    "% of Students Proficient in Math",
    "% of Students Proficient in Science",
    "% of Students Consistently Attending Class",
    "% of Students That Believe Teachers Care",
    "% of Students That Are Non-White",
    "% of Students That Are English Language Learners",
    "% of Students Enrolled in Special Education",
    "% of Students That Receive Free/Reduced Lunch",
    "% of Students That Attended Preschool",
    "# of Students Per Teacher",
    "% of Staff That Are Paraprofessionals",
    "% of Staff That Are Licensed",
    "% of Staff With Advanced Degrees",
    "% of Funding from Federal Government",
    "Final Score"
    ]

    for col in cols_to_round:
        if col in renamed_data.columns:
            renamed_data[col] = renamed_data[col].round(0).astype("Int64")
            
    return render_template('results.html', table=renamed_data.to_html(classes='data', index=False, border=2))


@app.route('/total', methods=['GET', 'POST'])
def total():
    
    renamed_data = school_data.rename(columns={
    "Meets Read Standards": "% of Students Proficient in Reading",
    "Meets Math Standards": "% of Students Proficient in Math",
    "Meets Science Standards": "% of Students Proficient in Science",
    "Consistent Attendance Rate": "% of Students Consistently Attending Class",
    "Caring Teachers": "% of Students That Believe Teachers Care",
    "Suspension Rate": "% of Students That Receive Suspensions",
    "Non-White Percentage": "% of Students That Are Non-White",
    "ELL Percentage": "% of Students That Are English Language Learners",
    "SE Percentage": "% of Students Enrolled in Special Education",
    "FRL Percentage": "% of Students That Receive Free/Reduced Lunch",
    "Preschool Attendance": "% of Students That Attended Preschool",
    "Student-Teacher Ratio": "# of Students Per Teacher",
    "Percent Paras": "% of Staff That Are Paraprofessionals",
    "Licensed Teachers": "% of Staff That Are Licensed",
    "Advanced Degree Teachers": "% of Staff With Advanced Degrees",
    "Percent Federal Funds": "% of Funding from Federal Government"
    })
    
    cols_to_round = [
    "% of Students Proficient in Reading",
    "% of Students Proficient in Math",
    "% of Students Proficient in Science",
    "% of Students Consistently Attending Class",
    "% of Students That Believe Teachers Care",
    "% of Students That Are Non-White",
    "% of Students That Are English Language Learners",
    "% of Students Enrolled in Special Education",
    "% of Students That Receive Free/Reduced Lunch",
    "% of Students That Attended Preschool",
    "# of Students Per Teacher",
    "% of Staff That Are Paraprofessionals",
    "% of Staff That Are Licensed",
    "% of Staff With Advanced Degrees",
    "% of Funding from Federal Government",
    "Final Score"
    ]

    for col in cols_to_round:
        if col in renamed_data.columns:
            renamed_data[col] = renamed_data[col].round(0).astype("Int64")
            
    if request.method == 'POST':
        selected = request.form['geography']
        if selected:
            included = neighbor_map.get(selected, [selected])
            filtered_geog = geographic_filter(included, renamed_data)
            filtered_df = pd.DataFrame(filtered_geog)
            total_table = filtered_df.to_html(classes='data', index=False, border=2)
        else: 
            total_table = renamed_data.to_html(classes='data', index=False, border=2)
    else:
        total_table = renamed_data.to_html(classes='data', index=False, border=2)
    return render_template('total.html', table=total_table)


@app.route("/sources")
def sources():
    return render_template("sources.html")


@app.route("/filter")
def filter():
    return render_template("filter.html")


@app.route("/submit", methods=["POST"])
def submit():
    filter_qual = request.form["quality"]
    selected = request.form.get("geography")
    quality_map = {
        "reading": ("Meets Read Standards", False),
        "math": ("Meets Math Standards", False),
        "science": ("Meets Science Standards", False),
        "attendance": ("Consistent Attendance Rate", False),
        "opinion": ("Caring Teachers", False),
        "suspension": ("Suspension Rate", True),
        "diversity": ("Non-White Percentage", False),
        "language": ("ELL Percentage", False),
        "economic": ("FRL Percentage", False),
        "preschool": ("Preschool Attendance", False),
        "ratio": ("Student-Teacher Ratio", True),
        "para": ("Percent Paras", False),
        "licensed": ("Licensed Teachers", False),
        "advanced": ("Advanced Degree Teachers", False),
        "federal": ("Percent Federal Funds", False),
        "trend": ("Overall Scoring Trend", True)
    }
    data = school_data.copy()
    if filter_qual in quality_map:
        column, sort = quality_map[filter_qual]
        data = filter_single(column, sort, school_data)
    if selected:
        included = neighbor_map.get(selected, [selected])
        data = geographic_filter(included, data)
    renamed_data = data.rename(columns={
    "Meets Read Standards": "% of Students Proficient in Reading",
    "Meets Math Standards": "% of Students Proficient in Math",
    "Meets Science Standards": "% of Students Proficient in Science",
    "Consistent Attendance Rate": "% of Students Consistently Attending Class",
    "Caring Teachers": "% of Students That Believe Teachers Care",
    "Suspension Rate": "% of Students That Receive Suspensions",
    "Non-White Percentage": "% of Students That Are Non-White",
    "ELL Percentage": "% of Students That Are English Language Learners",
    "SE Percentage": "% of Students Enrolled in Special Education",
    "FRL Percentage": "% of Students That Receive Free/Reduced Lunch",
    "Preschool Attendance": "% of Students That Attended Preschool",
    "Student-Teacher Ratio": "# of Students Per Teacher",
    "Percent Paras": "% of Staff That Are Paraprofessionals",
    "Licensed Teachers": "% of Staff That Are Licensed",
    "Advanced Degree Teachers": "% of Staff With Advanced Degrees",
    "Percent Federal Funds": "% of Funding from Federal Government"
    })
    
    cols_to_round = [
    "% of Students Proficient in Reading",
    "% of Students Proficient in Math",
    "% of Students Proficient in Science",
    "% of Students Consistently Attending Class",
    "% of Students That Believe Teachers Care",
    "% of Students That Are Non-White",
    "% of Students That Are English Language Learners",
    "% of Students Enrolled in Special Education",
    "% of Students That Receive Free/Reduced Lunch",
    "% of Students That Attended Preschool",
    "# of Students Per Teacher",
    "% of Staff That Are Paraprofessionals",
    "% of Staff That Are Licensed",
    "% of Staff With Advanced Degrees",
    "% of Funding from Federal Government",
    "Final Score"
    ]

    for col in cols_to_round:
        if col in renamed_data.columns:
            renamed_data[col] = renamed_data[col].round(0).astype("Int64")
            
    return render_template('results.html', table=renamed_data.to_html(classes='data', index=False, border=2))


if __name__ == '__main__':
    app.run(debug=True)
