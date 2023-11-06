import discord
import responses
import asyncio
import requests
import random

async def send_message(message, user_message, is_private): #sends regular messages
    try:
        response = responses.get_response(user_message)
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

#setting up embeds
def create_embed(title, description):
    embed = discord.Embed(title=title, description=description, color=discord.Color.green())
    return embed

def send_embed(channel, embed):
    coroutine = channel.send(embed=embed)
    asyncio.ensure_future(coroutine)

#Filtering JSON files
def find_celestial_by_english_name(json_url, target_name): #for celestial api
    response = requests.get(json_url)
    if response.status_code == 200:
        data = response.json()
        bodies = data['bodies']
        for body in bodies:
            if body.get('englishName') == target_name:
                return body
    return None

def get_random_photo(json_url): #for mars api
    photo_data = requests.get(json_url)
    if photo_data.status_code == 200:
        photo_list = photo_data.json()["photos"]
        if photo_list:
            return random.choice(photo_list)
    return None

def get_curious(json_url): #for mars curiousity api
    photo_data = requests.get(json_url)
    if photo_data.status_code == 200:
        photo_list = photo_data.json()["photos"]
        if photo_list:
            curiosity = random.choice(photo_list)
            while curiosity['rover']['name'] != "Curiosity":
                curiosity = random.choice(photo_list)
            return curiosity
    return None

def get_opportunity(json_url): #for mars opportunity api
    photo_data = requests.get(json_url)
    if photo_data.status_code == 200:
        photo_list = photo_data.json()["photos"]
        if photo_list:
            opportunity = random.choice(photo_list)
            while opportunity['rover']['name'] != "Opportunity":
                opportunity = random.choice(photo_list)
            return opportunity
    return None

def get_apod(json_url): #fetches apod data
    response = requests.get(json_url)
    response.raise_for_status()  
    data_dict = response.json()
    hdurl = data_dict.get("hdurl")
    date = data_dict.get('date')
    title = data_dict.get('title')
    if hdurl and date and title:
        return hdurl, date, title
    else:
        return "No Data Available."

def get_astronauts(json_url):
    response = requests.get(json_url)
    response_data = response.json()
    
    if "people" in response_data:
        astronauts = response_data["people"]
        number = response_data["number"]
        return astronauts, number
    
    return None

def asteroid(json_url):
    response = requests.get(json_url)
    response = response.json()
    
    if "near_earth_objects" in response:
        dates = list(response["near_earth_objects"].keys())  # Get all available dates
        random_date = random.choice(dates)  # Select a random date
        
        asteroids_on_date = response["near_earth_objects"][random_date]
        random_asteroid = random.choice(asteroids_on_date)  # Select a random asteroid
        
        asteroid_info = {
            "name": random_asteroid["name"],
            "max_diameter_miles": random_asteroid["estimated_diameter"]["miles"]["estimated_diameter_max"],
            "relative_velocity_mph": random_asteroid["close_approach_data"][0]["relative_velocity"]["miles_per_hour"],
            "is_potentially_hazardous": random_asteroid["is_potentially_hazardous_asteroid"],
            "close_approach_date": random_asteroid["close_approach_data"][0]["close_approach_date"]
        }
        
        return asteroid_info
    else:
        return None

def moon_phase(month, day, year): #for moonphase command
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]
    description = ["new (totally dark)",
      "waxing crescent (increasing to full)",
      "in its first quarter (increasing to full)",
      "waxing gibbous (increasing to full)",
      "full (full light)",
      "waning gibbous (decreasing from full)",
      "in its last/third quarter (decreasing from full)",
      "waning crescent (decreasing from full)"]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    if day == 31:
        day = 1
    days_into_phase = int((ages[(year + 1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16/59.0)
    #print(index)  # test
    if index > 7:
        index = 7
    status = description[index]
    if status == description[0]:
        image = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/New_Moon.jpg/300px-New_Moon.jpg"
    elif status == description[1]:
        image = "https://www.surfertoday.com/images/stories/waxing-crescent-moon.jpg"
    elif status == description[2]:
        image = "https://www.surfertoday.com/images/stories/first-quarter-moon.jpg"
    elif status == description[3]:
        image = "https://www.surfertoday.com/images/stories/waxing-gibbous-moon.jpg"
    elif status == description[4]:
        image = "https://www.surfertoday.com/images/stories/full-moon.jpg"
    elif status == description[5]:
        image = "https://www.surfertoday.com/images/stories/waning-gibbous-moon.jpg"
    elif status == description[6]:
        image = "https://www.surfertoday.com/images/stories/third-quarter-moon.jpg"
    else:
        image = "https://www.surfertoday.com/images/stories/waning-crescent-moon.jpg"
    
    
    # light should be 100% 15 days into phase
    light = int(2 * days_into_phase * 100/29)
    if light > 100:
        light = abs(light - 200);
    date = "%d%s%d" % (day, months[month-1], year)

    return date, status, light, image

def epic(json_url): #EPIC API
    data = requests.get(json_url)
    data = data.json()
    random_item = random.choice(data)
    identifier = random_item['image']
    caption = random_item['caption']
    date = random_item['date']
    centroid_coordinates = random_item['centroid_coordinates']
    lat = centroid_coordinates['lat'] 
    lon = centroid_coordinates['lon'] 
        
    return identifier, caption, date, lat, lon
    
def image_grabber(name): #image api function
    image_data = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&titles={name}&prop=pageimages&format=json&pithumbsize=500")
    image_data = image_data.json()

    pages = image_data['query']['pages']
    
    # Loop through the page IDs
    for page_id, page_info in pages.items():
        if 'thumbnail' in page_info:
            photo = page_info['thumbnail']['source']
            return photo  # Return the first image source found

    return None

def rocket_launches(json_url): #rocket launches api function
    rocket_data = requests.get(json_url)
    rocket_data = rocket_data.json()
    rocket_name = []
    rocket_state = []
    rocket_country = []
    rocket_launch_description = []

    for rocket in rocket_data["result"]:
        rocket_name.append(rocket["name"])
        rocket_state.append(rocket["pad"]["location"]["state"])
        rocket_country.append(rocket["pad"]["location"]["country"])
        rocket_launch_description.append(rocket["launch_description"])
    
    rockets_info={
        "Rocket Name": rocket_name,
        "State": rocket_state,
        "Country": rocket_country,
        "Launch Description": rocket_launch_description,
    }
    return rockets_info

#Helping with uppercase sensitivity
def capitalize_first_character(input_string):
    if not input_string:  # Check if the string is empty
        return input_string
    return input_string[0].upper() + input_string[1:]


#running the actual bot
def run_discord_bot():
    TOKEN = "MTEwOTY3NDY2NzcwNDMyNDEzNg.GqYP5U.C7edEVXGYdlFabSGVMkOCs44KymRcH_X2O8RRk"
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        user_message = user_message.lower()
        print(f'{username} said: {user_message} in {channel}')

        #space related embeds
        if user_message == "k!iss" or user_message == "pk!iss":
            issresponse = requests.get("https://api.wheretheiss.at/v1/satellites/25544%22")
            iss = issresponse.json()
            altitude = str(round(iss['altitude'], 2))
            velocity = str(round(iss['velocity'], 2))
            footprint = str(round(iss['footprint'], 2))
            latitude = str(round(iss['latitude'], 2))
            longitude = str(round(iss['longitude'], 2))
            embed = create_embed('International Space Station 🚀', (f"The ISS is at {latitude} latitude and {longitude} longitude!"))
            embed.set_image(url='https://www.esa.int/var/esa/storage/images/esa_multimedia/images/2021/11/cosmic_pearl/23822292-1-eng-GB/Cosmic_pearl_pillars.jpg')
            embed.add_field(name='Altitude', value = (altitude), inline=False)
            embed.add_field(name='Velocity', value = (f"{velocity} m/s"), inline=False)
            embed.add_field(name='Visibility', value = (iss['visibility']), inline=False)
            embed.add_field(name='Footprint', value = (footprint), inline=False)
            send_embed(message.channel, embed) if user_message == "k!iss" else send_embed(message.author, embed)
        
        elif user_message == "k!tesla" or user_message == "pk!tesla":
            teslaresponse = requests.get("https://api.spacexdata.com/v4/roadster")
            tesla = teslaresponse.json()
            speed = str(round(tesla['speed_kph'], 2))
            earth_distance = str(round(tesla['earth_distance_km'], 2))
            mars_distance = str(round(tesla['mars_distance_km'], 2))
            embed = create_embed("Elon Musk's Tesla Roadster", (f"{tesla['details']}"))
            embed.add_field(name= "Speed", value = (f"{speed} km/h"), inline=True)
            embed.add_field(name = "Launch Mass", value = f"{tesla['launch_mass_kg']} kg", inline = True)
            embed.add_field(name = "Orbit Type", value = tesla['orbit_type'], inline = True)
            embed.add_field(name= "Distance From Earth", value = (f"{earth_distance} km"), inline=True)
            embed.add_field(name= "Distance From Mars", value = (f"{mars_distance} km"), inline=True)
            embed.set_image(url="https://cdn.uanews.arizona.edu/s3fs-public/styles/uaqs_large/public/story-images/Elon_Musk's_Tesla_Roadster_(40143096241).jpg?itok=Qx4r6c0V")
            embed.set_footer(text="Data from: SpaceX")
            send_embed(message.channel, embed) if user_message == "k!tesla" else send_embed(message.author, embed)
        
        elif user_message.startswith("k!celestial") or user_message.startswith("pk!celestial"):
            celestial_response = "test"
            if user_message.startswith("k!celestial"):
                user_command = user_message[:11]
                celestial_response = user_message[12:] 
            else:
                user_command = user_message[:12]
                celestial_response = celestial_response[13:]
            celestial_response = capitalize_first_character(celestial_response)
            celestial = find_celestial_by_english_name("https://api.le-systeme-solaire.net/rest/bodies", celestial_response)
            if celestial:
                embed = create_embed(celestial_response, (f"Here's some information about " + celestial_response + ":"))
                founder = celestial["discoveredBy"]
                alt_name = celestial['alternativeName']
                discovery = celestial['discoveryDate']
                if founder == '':
                    founder = "N/A"
                if alt_name == '':
                    alt_name = "None"
                if discovery == '':
                    discovery = "N/A"
                if celestial_response == "Jupiter":
                    image = "https://s.abcnews.com/images/Technology/jupiter-webb-telescope-01-ht-iwb-220822_1661177358675_hpMain_16x9_1600.jpg"
                elif celestial_response == "Moon":
                    image = "https://www.rmg.co.uk/sites/default/files/styles/full_width_1440/public/ROG_AMAT_Moon.jpg?itok=KIKB_93o"
                elif celestial_response== "Earth":
                    image = "https://static.toiimg.com/thumb/msid-100436479,width-1280,height-720,resizemode-4/.jpg"
                elif celestial_response == "Saturn":
                    image = "https://starwalk.space/gallery/images/saturn-planet-guide/1920x1080.jpg"
                elif celestial_response == "Neptune":
                    image = "https://imageio.forbes.com/specials-images/imageserve/648792456/Neptune/960x0.jpg?format=jpg&width=960"
                elif celestial_response == "Venus":
                    image = "https://s7d1.scene7.com/is/image/CENODS/09911-feature3-venus-social?$twitter$"
                elif celestial_response == "Uranus":
                    image = "https://ychef.files.bbci.co.uk/1280x720/p0257vk5.jpg"
                elif celestial_response == "Pluto":
                    image = "https://cdn.mos.cms.futurecdn.net/DoZSMXF87kCuzbymsuEFHo.jpg"
                elif celestial_response == "Mercury":
                    image = "https://www.farmersalmanac.com/wp-content/uploads/2010/08/Mercury-planet-as_102739845-1050x630.jpeg"
                elif celestial_response == "Sun":
                    image = "https://d2r55xnwy6nx47.cloudfront.net/uploads/2018/07/SolarFull_SeanDoran_2880FullwidthLede.jpg"
                elif celestial_response == "Mars":
                    image = "https://cdn.mos.cms.futurecdn.net/BiH44Z2Wd9PS55wXBuQK8H.jpg"
                else:
                    image = "https://i.natgeofe.com/n/e484088d-3334-4ab6-9b75-623f7b8505c9/1086_2x1.jpg"

                embed.add_field(name = "Is it A planet?", value = celestial['isPlanet'], inline = True)
                embed.add_field(name = "Gravity", value = celestial['gravity'], inline = True)
                embed.add_field(name = "Body Type", value = celestial['bodyType'], inline = True)
                embed.add_field(name = "Discovered By", value = founder, inline = True)
                embed.add_field(name = "Discovery Date", value = discovery, inline = False)
                embed.add_field(name = "Alternative Name", value = alt_name, inline = False)
                if image =="https://i.natgeofe.com/n/e484088d-3334-4ab6-9b75-623f7b8505c9/1086_2x1.jpg":
                    embed.set_footer(text = f"(Image not dipicting {celestial_response})\nData from: https://api.le-systeme-solaire.net")
                else:
                    embed.set_footer(text = "Data from: https://api.le-systeme-solaire.net")
                embed.set_image(url = image)
                send_embed(message.channel, embed) if user_command == "k!celestial" else send_embed(message.author, embed)
            else:
                return "No Data Found."
        
        elif user_message == "k!kepler22b" or user_message == "pk!kepler22b":
            embed = create_embed('Kepler-22b', "Kepler-22b is a planet discovered by NASA's Kepler Telescope. It's in a star's habitible zone, leaving it oddly close to Earth.")
            embed.add_field(name = "Size", value = '2.4 times the size of Earth', inline = True)
            embed.add_field(name = "Discovery Date", value = 'December 5, 2011', inline = True)
            embed.add_field(name = "Distance", value = '635 light years', inline = True)
            embed.add_field(name = "Planet Type", value = 'Super Earth', inline = True)
            embed.add_field(name = "Mass", value = '9.1 x Earth', inline = True)
            embed.add_field(name = "Orbital Period", value = '289.9 Days', inline = True)
            embed.set_image(url = 'https://www.nasa.gov/sites/default/files/images/607694main_Kepler22bArtwork_full.jpg')
            embed.set_footer(text='Data from: NASA')
            send_embed(message.channel, embed) if user_message == "k!kepler22b" else send_embed(message.author, embed)
        
        elif user_message == "k!spirit" or user_message == "pk!spirit":
            embed = create_embed('Mars Images', "Photos taken by the Spirit Rover on Mars, as well as its information.")
            mars_photo = get_random_photo('https://api.nasa.gov/mars-photos/api/v1/rovers/spirit/photos?api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T&sol=1000')
            embed.set_image(url = mars_photo['img_src'])
            embed.add_field(name = f"{mars_photo['rover']['name']} Launch Date", value = mars_photo['rover']['launch_date'], inline = True)
            embed.add_field(name = "Rover", value = mars_photo['rover']['name'], inline = True)
            embed.add_field(name = "Status", value = mars_photo["rover"]["status"], inline = True)
            embed.add_field(name = "Camera", value = mars_photo["camera"]["full_name"], inline = True)
            embed.add_field(name = "Date Taken", value = mars_photo['earth_date'], inline = True)
            embed.set_footer(text='Data from: NASA')
            send_embed(message.channel, embed) if user_message =="k!spirit" else send_embed(message.author, embed)
        
        elif user_message.startswith('k!apod') or user_message.startswith('pk!apod'):
            if user_message.startswith("k!"):
                date = user_message[7:]
            else:
                date = user_message[8:]
            link ='https://api.nasa.gov/planetary/apod?api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T&date='
            hdurl, date, title = get_apod(link)
            embed = create_embed("Astronomy Picture of the Day (APOD)", title)
            embed.add_field(name = 'Date', value = date, inline = True)
            embed.set_image(url = hdurl)
            embed.set_footer(text = 'Data from: NASA')
            send_embed(message.channel, embed) if user_message.startswith('k!apod') else send_embed(message.author, embed)

        elif user_message == "k!in space" or user_message == "pk!in space":
            astronauts, number = get_astronauts('http://api.open-notify.org/astros.json')
            embed = create_embed("Who's in Space?", f"There are {number} people in space right now!")
            names_list = "\n".join([astronaut["name"] for astronaut in astronauts])
            embed.add_field(name="Names", value=names_list, inline=False)
            embed.set_footer(text = f"Requested by {message.author}")
            send_embed(message.channel, embed) if user_message == 'k!in space' else send_embed(message.author, embed)

        elif user_message == "k!asteroid" or user_message == "pk!asteroid":
            asteroid_info = asteroid("https://api.nasa.gov/neo/rest/v1/feed?start_date=2020-09-07&api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T")
            embed = create_embed("Near-Earth Astroids", "Track a random astroid.")
            embed.add_field(name = "Name", value = asteroid_info["name"], inline = True)
            embed.add_field(name = "Max Diameter", value = f'{asteroid_info["max_diameter_miles"]} miles' , inline = True)
            embed.add_field(name = "Velocity", value = f'{asteroid_info["relative_velocity_mph"]} mph', inline = True)
            embed.add_field(name = "Possibly Hazardous?", value = asteroid_info["is_potentially_hazardous"], inline = True)
            embed.add_field(name = "Close Approach Date", value = asteroid_info["close_approach_date"], inline = False)
            embed.set_image(url = "https://media-cldnry.s-nbcnews.com/image/upload/t_focal-1000x563,f_auto,q_auto:eco,dpr_2.0/mpx/2704722219/2023_06/1686744985925_tdy_news_8a_nasa_massive_asteroid_earth_230614_1920x1080-mqdfo4.jpg")
            embed.set_footer(text = "Data from: NASA")
            send_embed(message.channel, embed) if user_message == "k!asteroid" else send_embed(message.author, embed)

        elif user_message == "k!curiosity" or user_message == "pk!curiosity":
            data = get_curious("https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T&sol=1000")
            embed = create_embed("Curiosity Rover", "Photos taken by the *Curiosity* rover on Mars, along with information.")
            embed.set_image(url = data['img_src'])
            embed.add_field(name = f"{data['rover']['name']} Launch Date", value = data['rover']['launch_date'], inline = True)
            embed.add_field(name = "Curiousity Land Date", value = data['rover']['landing_date'])
            embed.add_field(name = "Status", value = data['rover']['status'], inline = True)
            embed.add_field(name = "Camera", value = data['camera']['full_name'], inline = True)
            embed.add_field(name = "Date Taken", value = data['earth_date'], inline = True)
            embed.set_footer(text = "Data from: NASA")
            send_embed(message.channel, embed) if user_message == "k!curiosity" else send_embed(message.author, embed)

        elif user_message == "k!jkepler" or user_message == "pk!jkepler":
            embed = create_embed("Johannes Kepler", "Johannes Kepler is a German astronomer from the 15th century. He came from a poor family, but he was able to go to University of Tübingen to study for the Lutheran Ministry. He was then introduced to Copernicus and science, and began to create astronomy works and revolutionize the industry. He dicovered many unknown topics at the time, such as eyeglass designing for nearsightedness and farsightedness and how telescopes work.")
            embed.add_field(name = "Kepler's Laws of Planetary Motion", value = "1: Planets move in ellipses with the Sun at one focus.\n2: The radius vector describes equal areas in equal times.\n3: The squares of the periodic times are to each other as the cubes of the mean distances.", inline = False)
            embed.add_field(name = "Birthday", value = "1 PM on December 27, 1571", inline = False)
            embed.add_field(name = "Origin", value = "Weil der Stadt, Württemberg, Holy Roman Empire (Germany)", inline = True)
            embed.set_image(url = "https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcQlbgqJpVT75pSKW-r0e05PxnCsQPvJvDLfOYC0Yh7tMqMne40-vjsmOuX_iDxpV6f4MWLnUur00AQYZDA")
            embed.set_footer(text = "Data from: NASA")
            send_embed(message.channel, embed) if user_message == "k!jkepler" else send_embed(message.author, embed)
        
        elif user_message.startswith("k!moon phase") or user_message.startswith("pk!moon phase"):
            if user_message == "k!moon phase" or user_message == "pk!moon phase":
                return "Invalid format: type the command with a date in yyyy-mm-dd format\nExample: k!moon phase 2023-08-13"
            if user_message.startswith("k!moon phase"):
                year = int(user_message[13:17])
                month = int(user_message[18:20])
                day = int(user_message[21:])
            else:
                year = int(user_message[14:18])
                month = int(user_message[19:21])
                day = int(user_message[22:])
            date, status, light, image = moon_phase(month, day, year)
            embed = create_embed("Moon Phase", "The moon phase on %s was %s" % (date, status))
            embed.add_field(name="Light", value="%d%s" % (light, '%'), inline=False)
            embed.set_image(url = image)
            send_embed(message.channel, embed) if user_message.startswith("k!moon phase") else send_embed(message.author, embed)

        elif user_message.startswith("k!epic") or user_message.startswith("pk!epic"):
            if user_message.startswith("k!epic"):
                date = user_message[7:]
            else:
                date = user_message[8:]
            year = date[:4]
            month = date[5:7]
            day = date[8:]
            random_image, random_caption, random_date, lat, lon = epic(f"https://api.nasa.gov/EPIC/api/natural/date/{date}?api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T")
            lat = round(int(lat), 2)
            lon = round(int(lon), 2)
            embed = create_embed("Earth Polychromatic Imaging Camera (EPIC)", random_caption)
            embed.add_field(name = "Date & Time", value = random_date, inline = False)
            embed.add_field(name = "Latitude", value = lat, inline = False)
            embed.add_field(name = "Longitude", value = lon, inline = False)
            embed.set_image(url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/jpg/{random_image}.jpg" )
            embed.set_footer(text = "Data from: NASA")
            send_embed(message.channel, embed) if user_message.startswith('k!epic') else send_embed(message.author, embed)

        elif user_message == "k!opportunity" or user_message == "pk!opportunity":
            data = get_opportunity("https://api.nasa.gov/mars-photos/api/v1/rovers/opportunity/photos?api_key=q2XOEZwSdDnlNJMAm1ILf5DCBokzDTw5AmNvki2T&sol=1000")
            embed = create_embed("Opportunity Rover", "Photos taken by the *Opportunity* rover on Mars, along with information.")
            embed.set_image(url = data['img_src'])
            embed.add_field(name = f"{data['rover']['name']} Launch Date", value = data['rover']['launch_date'], inline = True)
            embed.add_field(name = "Opportunity Land Date", value = data['rover']['landing_date'])
            embed.add_field(name = "Status", value = data['rover']['status'], inline = True)
            embed.add_field(name = "Camera", value = data['camera']['full_name'], inline = True)
            embed.add_field(name = "Date Taken", value = data['earth_date'], inline = True)
            embed.set_footer(text = "Data from: NASA")
            send_embed(message.channel, embed) if user_message == "k!opportunity" else send_embed(message.author, embed)

        elif user_message =="k!rocket" or user_message == "pk!rocket":
            rocket_info = rocket_launches("https://fdo.rocketlaunch.live/json/launches/next/5")
            embed = create_embed("Next 5 Rocket Launches", "The one of the upcoming 5 rocket launches:")
            index = random.randint(0,4)
            r_name = rocket_info["Rocket Name"][index]
            r_state = rocket_info["State"][index]
            r_country= rocket_info["Country"][index]
            r_launch = rocket_info["Launch Description"][index]
            if r_name.startswith("Starlink"):
                r_url = "https://apicms.thestar.com.my/uploads/images/2023/03/16/1981338.jpg"
            else:
                r_url = "https://i.natgeofe.com/n/88420695-3555-4f84-90be-8f7903a1a57e/01_58_51a_remotesite-2-frame-8_4x3.jpg"
            embed.add_field(name = "Rocket Name", value = r_name, inline = False)
            embed.add_field(name = "State", value = r_state, inline = True)
            embed.add_field(name = "Country", value = r_country, inline = True)
            embed.add_field(name = "Description", value = r_launch, inline = False)
            embed.set_image(url = r_url)
            embed.set_footer(text = "Data from: RocketLaunch.live/api")
            send_embed(message.channel, embed) if user_message == "k!rocket" else send_embed(message.author, embed) 
        
        
        
        
        #non-space embeds below vvv
        elif user_message == "k!help" or user_message == "pk!help":
            embed = create_embed('ProjectKepler Commands 🪐', "A list of every command I use!\n*(Pro Tip: If you want a private message by me, replace 'k!' with 'pk!')*")
            embed.add_field(name = 'Astronomy Commands', value = "`k!iss:` Returns the coordinates of the ISS and additional information.\n`k!tesla:` Gives you an intro into the tesla roadster in space, with current updates.\n`k!celestial [text]:` Displays information about a given celestial.\n`k!kepler22b:` Information about me!\n`k!jkepler:` Facts about Johannes Kepler.\n`k!spirit:` Returns a random image taken by the Spirit rover, along with basic information.\n`k!curiosity:` A random Mars photo from specifically the Curiosity rover, along with information.\n`k!opportunity:` An image from the opportunity Mars rover, along with information.\n`k!apod [yyyy-mm-dd]:` Shows the chosen Astronomy picture of the day.\n`k!in space:` Gives a list of who's currently in space.\n`k!asteroid:` Gives a random close asteroid\n`k!moon phase [yyyy-mm-dd]:` Displays the moon phase and light %.\n`k!epic [yyyy-mm-dd]:` Get a random image of Earth taken on that date.\n`k!rocket:` Gives one of the 5 most upcoming rocket launches.", inline = True)
            embed.add_field(name = "Basic Commands", value = '`k!8ball [text]:` Returns a randomly-generated 8ball answer.\n`k!roll:` Gives a number 1-6 inclusive, simulating dice.\n`k!dog:` Generates a random dog image.\n`k!fortune:` Fortune cookie advice.\n`k!rps [choice here]:` Play rock paper scissors with a computer.\n`k!image [name]:` Returns image of choice. ', inline = False)
            embed.set_image(url ='https://exoplanets.nasa.gov/rails/active_storage/blobs/eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaHBBbWtEIiwiZXhwIjpudWxsLCJwdXIiOiJibG9iX2lkIn19--56aca35757a25dfcb00e2307006fd2fc7ceb8a76/Kepler22b.jpg?disposition=inline')
            embed.set_footer(text = f"Requested by {message.author}.")
            send_embed(message.channel, embed) if user_message == "k!help" else send_embed(message.author, embed)
        
        elif user_message == "k!dog" or user_message == "pk!dog":
            link = 'https://dog.ceo/api/breeds/image/random'
            response = requests.get(link)
            response = response.json()
            dog_message = response['message']
            embed = create_embed('Random Dog', 'Woof!')
            embed.set_image(url = dog_message)
            embed.set_footer(text = f'resquested by {message.author}.')
            send_embed(message.channel, embed) if user_message == 'k!dog' else send_embed(message.author, embed)
        
        elif user_message.startswith("k!rps") or user_message.startswith("pk!rps"):
            choices = ["Rock", "Paper", "Scissors"]
            player_choice = user_message[6:]
            player_choice = capitalize_first_character(player_choice)
            if player_choice == "Scissor":
                player_choice == player_choice + "s"
            comp_choice = random.choice(choices)

            if comp_choice == player_choice:
                answer = f"It was a draw! I chose {comp_choice}"
            elif comp_choice == "Rock" and player_choice == "Paper":
                answer = "You won! I chose rock🪨"
            elif comp_choice == "Rock" and player_choice == "Scissors":
                answer = "You lost! I chose rock🪨"
            elif comp_choice == "Paper" and player_choice == "Scissors":
                answer = "You won! I chose paper📄"
            elif comp_choice == "Paper" and player_choice == "Rock":
                answer = "You lost! I chose paper📄"
            elif comp_choice == "Scissors" and player_choice == "Rock":
                answer = "You won! I chose scissors ✂"
            elif comp_choice == "Scissors" and player_choice == "Paper":
                answer = "You lost! I chose scissors ✂"
            embed = create_embed("Rock, Paper, Scissors... Shoot!", answer)
            embed.set_footer(text = f"Requested by: {message.author}")
            send_embed(message.channel, embed) if user_message.startswith('k!rps') else send_embed(message.author, embed)
                
        elif user_message[0] == "p": #checks if message is private
            user_message = user_message[1:]
            await send_message(message, user_message, is_private = True)
        else:
            await send_message(message, user_message, is_private = False) #sends regular messages to responses.py
            
    client.run(TOKEN)