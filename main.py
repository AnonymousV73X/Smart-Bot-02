# Importing Essential Modules From Telebot and Python 
import time
import math
import telebot
import json
import re
import html
import random
from jokes import jokes
from telebot import types
import threading
from difflib import SequenceMatcher
from telebot.types import Message
from stickers import sticker_ids, not_found_stickers, hello_stickers, photos
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot import TeleBot, util

# Creating a Telebot instance(For The Telegram Server)
bot = telebot.TeleBot("5659036483:AAE9ggNsM0Hze3tR4j3vr7N2NkOtXRCBMmY")

# List to store users information
user_data = []


# Function to load user data from JSON file
def load_user_data():
    global user_data
    try:
        with open("user_data.json", "r", encoding="utf-8") as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = []


# Function to save user data to JSON file
def save_user_data():
    with open("user_data.json", "w") as file:
        json.dump(user_data, file)


# Load user data when the bot starts
load_user_data()


# Function to handle video messages
@bot.message_handler(content_types=["video"])
def handle_video(message):
    try:
        # Get video information
        video = message.video
        file_id = video.file_id
        file_name = video.file_name
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        mime_type = video.mime_type

        # Convert file size to human-readable format
        readable_size = convert_size(file_size)

        # Make duration human-readable
        readable_duration = format_duration(duration)

        # Prepare the video information message
        message_text = (
            f"📹 𝑽𝑰𝑫𝑬𝑶 𝑰𝑵𝑭𝑶𝑹𝑴𝑨𝑻𝑰𝑶𝑵\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n"
            f"|== Name: {file_name}\n"
            f"|== Size: {readable_size}\n"
            f"|== Duration: {readable_duration}\n"
            f"|== Width: {width}px\n"
            f"|== Height: {height}px\n"
            f"|== Mime Type: {mime_type}\n"
            f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖"
        )

        # Send the video back with the information as the caption
        bot.send_video(
            message.chat.id,
            file_id,
            caption=message_text,
            reply_to_message_id=message.message_id,
        )

    except Exception as e:
        # Handle errors as needed
        print(f"Error handling video: {e}")


# Function to make duration human-readable
def format_duration(duration):
    if duration is None:
        return "Not available"

    minutes, seconds = divmod(duration, 60)
    hours, minutes = divmod(minutes, 60)

    if hours > 0:
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    elif minutes > 0:
        return f"{int(minutes)}m {int(seconds)}s"
    else:
        return f"{int(seconds)}s"


# Function to convert file size to human-readable format
def convert_size(size_bytes):
    units = ["B", "KB", "MB", "GB", "TB"]
    unit_index = 0

    while size_bytes >= 1024 and unit_index < len(units) - 1:
        size_bytes /= 1024.0
        unit_index += 1

    return f"{size_bytes:.2f} {units[unit_index]}"


# List of admins user ids
admin_user_ids = [
    1816953935,
    1623281225,
    2143511704,
    1315053937,
    1209904298,
    1529546916,
]


# Initialising Important Variables & Dictionaries
MAX_BATCH_SIZE = 2
json_file = "file_data.json"
file_data = {}
update_mode_users = {}



# Handling The Start Command 
@bot.message_handler(commands=["start"])
def welcome(message):
    user = message.from_user
    user_id = user.id
    user_name = user.first_name

    # Check if the user is already registered
    if any(user_data_item["id"] == user_id for user_data_item in user_data):
        # If User is already registered in the users IDs JSON PASS
        pass
    else:
        # Assign a number based on the number of registered users
        user_number = len(user_data) + 1

        # Create a new entry for the user
        new_user = {"id": user_id, "name": user_name, "number": user_number}

        # Save user data in the list
        user_data.append(new_user)

        # Save user data to the JSON file
        save_user_data()

    photo_path = (
        "photo_2023-07-20_13-14-25.jpg"
    )
    photo_caption = f"Welcome to Smart Entertainment, {user.first_name}! 😊\n\nI'm a simple TV Series & Movies Search bot. Just send me the name of the Series or Movie you want, and I'll check my database for it.\n\n📝 Please Note: All files generated here have been forwarded from other telegram platforms."

    # Send the photo with caption
    bot.send_photo(
        chat_id=message.chat.id,
        photo=open(photo_path, "rb"),
        caption=photo_caption,
    )
    random_sticker_id = random.choice(hello_stickers)
    bot.send_sticker(chat_id=message.chat.id, sticker=random_sticker_id)


# Defining the function to respond to the alive command
@bot.message_handler(commands=["alive"])
def alive(message):
    user = message.from_user
    # Randomly select a joke from the array
    joke = random.choice(jokes)

    caption = f"𝑶𝒇 𝑪𝒐𝒖𝒓𝒔𝒆 𝑰'𝒎 𝑨𝒍𝒊𝒗𝒆,\t {user.first_name} 😊\n\n {joke}\n\n 𝑶𝑲𝑨𝒀 𝑱𝑶𝑲𝑬𝑺 𝑨𝑺𝑰𝑫𝑬 😁\n 𝑾𝒉𝒂𝒕 𝑺𝒆𝒓𝒊𝒆𝒔 𝒄𝒂𝒏 𝑰 𝒈𝒆𝒕 𝒚𝒐𝒖 💁"
    photo_path = (
        "photo_2023-07-20_13-15-28.jpg"  # Replace with the actual path to your image
    )

    # Send the photo with caption (without the button)
    alive_message = bot.send_photo(
        chat_id=message.chat.id,
        photo=open(photo_path, "rb"),
        caption=caption,
    )

    # Function to delete messages after a certain delay
    def delete_message_after_delay(chat_id, message_id, delay):
        time.sleep(delay)
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except telebot.apihelper.ApiException:
            pass  

    # Create threads to delete messages after a certain delay
    thread_message = threading.Thread(
        target=delete_message_after_delay,
        args=(message.chat.id, message.message_id, 30),
    )
    thread_alive_message = threading.Thread(
        target=delete_message_after_delay,
        args=(message.chat.id, alive_message.message_id, 30),
    )

    # Start the threads
    thread_message.start()
    thread_alive_message.start()




# Declare data as a global variable
global data



# Function To save The File IDs to The JSON
def save_files(message):
    
    global data  

    try:
        # Load existing data from JSON or create an empty dictionary
        with open(json_file, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    # Update the existing data with the new file details
    existing_data.update(file_data)

    # Write the updated data to the JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=4)

    # Load the data immediately after saving
    with open(json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Get the list of file names that have been updated
    updated_file_names = list(file_data.keys())

    # Clear the file_data dictionary
    file_data.clear()

    # Print the number of files remaining for the batch
    remaining_files = MAX_BATCH_SIZE - len(existing_data)

    # Prepare the list of updated files
    updated_files_list = []
    max_message_length = 3000

    for file_name in updated_file_names:
        file_name_html = (
            f"<pre><code class='language-text'><b>{file_name}</b></code></pre>"
        )
        if len("".join(updated_files_list)) + len(file_name_html) > max_message_length:
            # If adding the current file_name_html would exceed the max_message_length,
            # send the current message and start a new one
            message_text = "⚡<b>Here Are The Updated Files:</b>" + "".join(updated_files_list)
            bot.send_message(message.chat.id, message_text, parse_mode="HTML")
            updated_files_list = []

        updated_files_list.append(f"\n\n ✅\t{file_name_html}")

    # Send the remaining SPLITTED message
    if updated_files_list:
        message_text = "⚡<b>Here Are The Updated Files:</b>" + "".join(updated_files_list)
        bot.send_message(message.chat.id, message_text, parse_mode="HTML")
    else:
        bot.send_message(message.chat.id, f"{remaining_files} files sent to JSON.")




# Handling and setting user to the udate state 
@bot.message_handler(commands=["update"])
def handle_update_command(message):
    # Check if the user is an admin
    if message.from_user.id not in admin_user_ids:
        bot.send_message(
            message.chat.id, "❌ You are not authorized to perform this action. ❌"
        )
        return

    # Check if the user is already in update mode
    if message.from_user.id in update_mode_users:
        bot.send_message(message.chat.id, "⚠️ You are already in update mode. ⚠️")
        return

    # Put the user in update mode
    update_mode_users[message.from_user.id] = True
    bot.send_message(
        message.chat.id, "✅ You are now in update mode.\n🍀 You can send files to update."
    )

# Handler for file messages while in update mode
@bot.message_handler(
    content_types=["document"],
    func=lambda message: message.from_user.id in update_mode_users,
)
def handle_file_update_mode(message):
    # Get the file name, file ID, file size, and file caption (From The telegram Metadata)
    original_file_name = message.document.file_name
    file_id = message.document.file_id
    file_size = message.document.file_size
    caption = message.caption
    
    # Remove @JMDKH_Team_ and other @username patterns, as well as | from the caption
    if caption:
        if "@JMDKH_Team_" in caption:
            caption = caption.replace("@JMDKH_Team_", "")
        else:
            caption = re.sub(r'(@\w+|\|)', '', caption)



    # Split the file name for display purposes
    display_file_name = split_long_name(original_file_name)

    # Convert file size to human-readable format
    readable_size = convert_size(file_size)

    
    
    # If the File Name via the Caption is already present and captions are different, make it unique by appending a number
    # If the File Name via the Caption is already present and captions are different, make it unique by appending a number
    # If the File Name via the Caption is already present and captions are different, make it unique by appending a number
    # If the File Name via the Caption is already present and captions are different, make it unique by appending a number
    if display_file_name in file_data:
        existing_entries = file_data[display_file_name]

        # Check if any existing entry has a different caption
        if any(entry[2] != caption for entry in existing_entries):
            # Find the smallest available number to make the file name unique
            i = 1
            while f"{display_file_name}_{i}" in file_data:
                i += 1

            unique_display_file_name = f"{display_file_name}_{i}"

            # Set the original file name as the caption only if caption is None or empty
            file_data[unique_display_file_name] = [
                [
                    file_id,
                    readable_size,
                    original_file_name if caption is None or not caption.strip() else caption
                ]
            ]
        else:
            # If captions are the same for all existing entries, add a new entry with an incremented index only if caption is different
            i = 1
            while f"{display_file_name}_{i}" in file_data and any(entry[2] != caption for entry in file_data[f"{display_file_name}_{i}"]):
                i += 1

            unique_display_file_name = f"{display_file_name}_{i}"

            # Set the original file name as the caption only if caption is None or empty
            file_data[unique_display_file_name] = [
                [
                    file_id,
                    readable_size,
                    original_file_name if caption is None or not caption.strip() else caption
                ]
            ]
    else:
        # If the display file name is new, add it to the dictionary with the file details as a list
        # Set the original file name as the caption only if caption is None or empty
        file_data[display_file_name] = [
            [
                file_id,
                readable_size,
                original_file_name if caption is None or not caption.strip() else caption
            ]
        ]




    # Print the number of files remaining for the batch
    remaining_files = MAX_BATCH_SIZE - len(file_data)
    print(f"{remaining_files} files remaining...")

    # Check if the number of files reaches the batch size
    if len(file_data) >= MAX_BATCH_SIZE:
        # Ask the user if they want to send the files to JSON
        bot.send_message(
            message.chat.id,
            f"Do you want to send {len(file_data)} files to JSON? (yes👌or no👎) ⁉️",
        )


# Function to split longer names
def split_long_name(name, max_length=55):
    if len(name) > max_length:
        # Split the name and keep the first part
        return name[:max_length] + "..."
    else:
        return name


# Handler for responding to the confirmation to send files to JSON
@bot.message_handler(func=lambda message: message.text.lower() in ["yes", "no"])
def handle_confirmation(message):
    if message.text.lower() == "yes":
        if len(file_data) >= MAX_BATCH_SIZE:
            save_files(message)
    else:
        bot.send_message(
            message.chat.id,
            "❌ Files have not been sent to JSON. You can continue adding more files.",
        )


# Handler for exiting update mode
@bot.message_handler(commands=["exitupdate"])
def handle_exit_update_command(message):
    # Check if the user is an admin and in update mode
    if message.from_user.id not in admin_user_ids:
        bot.send_message(
            message.chat.id, "❌ You are not authorized to perform this action. ❌"
        )
        return

    if message.from_user.id in update_mode_users:
        # Remove the user from update mode
        del update_mode_users[message.from_user.id]
        bot.send_message(message.chat.id, "❌ You have exited update mode.")
    else:
        bot.send_message(message.chat.id, "❌ You are not in update mode.")


# Handler for /listfiles command to list files in the batch
@bot.message_handler(commands=["listfiles"])
def handle_list_files_command(message):
    # Check if the user is an admin
    if message.from_user.id not in admin_user_ids:
        bot.send_message(
            message.chat.id, "❌ You are not authorized to perform this action. ❌"
        )
        return

    # Get the list of file details in the batch
    file_details = [
        f"{index + 1}. File Name: {file_name} ({len(details)} files) \nFile Size: {', '.join(size for _, size, _ in details)}\nCaption: {', '.join(caption for _, _, caption in details)}"
        for index, (file_name, details) in enumerate(file_data.items())
    ]

    if not file_details:
        bot.send_message(message.chat.id, "❎ No files in the update batch.")
        return

    # Join file details into a single string
    formatted_file_details = "\n\n".join(file_details)

    # Split the message using telebot's split_message method
    chunks = telebot.util.split_string(
        formatted_file_details, 3000
    )  # Adjust the length as needed

    # Send each chunk as a separate message
    for chunk in chunks:
        bot.send_message(message.chat.id, f"✅ Files in the update batch:\n\n{chunk}")


###################################################################################
###################################################################################
################################### MAIN FUNCTION #################################
###################################################################################
###################################################################################



# Define a variable to store the number of results per page
RESULTS_PER_PAGE = 10

# User session data dictionary
user_sessions = {}


import unicodedata

# Function to clean text by removing special characters and normalizing
def clean_text(text):
    # Replace specified characters with nothing
    cleaned_text = re.sub(r"[()*^&%$#@!~`_\-+={}[\]:;\"',.]", " ", text)

    # Replace all years with nothing, considering multiple spaces
    cleaned_text = re.sub(
        r"\b(?:18[0-9]{2}|19[0-9]{2}|20[0-4][0-9]|2050)\b\s*", "", cleaned_text
    )

    # Normalize the text by removing diacritic marks
    cleaned_text = "".join(
        [
            c
            for c in unicodedata.normalize("NFKD", cleaned_text)
            if not unicodedata.combining(c)
        ]
    )

    # Remove extra spaces without using a separate regex
    cleaned_text = " ".join(cleaned_text.split())

    # Return the cleaned text in lowercase
    return cleaned_text.lower()


# Function to limit the search query length and clean it
def limit_search_query_length(search_query, max_length):
    if len(search_query) > max_length:
        limited_search_query = search_query[:max_length].rsplit(" ", 1)[0]
        return clean_text(limited_search_query)
    return clean_text(search_query)




# Function for custom sorting
def custom_sort(x):
    keywords_present_in_name = any(
        keyword.lower() in x[0].lower() for keyword in ["PSA", "psa", "x265", "10bit"]
    )
    modified_name = clean_text(x[0])

    if len(x) > 2 and isinstance(x[2], str):
        keywords_present_in_caption = any(
            keyword.lower() in x[2].lower() for keyword in ["PSA", "psa", "10bit"]
        )
        modified_caption = clean_text(x[2])
    else:
        keywords_present_in_caption = False
        modified_caption = ""

    # Invert the sorting order by using the reverse parameter in the tuple
    return (
        (1 if keywords_present_in_name else 0, 1 if keywords_present_in_caption else 0),
        modified_name,
        modified_caption,
    )[::-1]






# Load data from file_data.json once at the beginning
with open("file_data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    
    
# Handler for text messages
@bot.message_handler(func=lambda message: True)
def search_and_display_files(message):
    user_id = message.from_user.id

    # Retrieve or create user session context
    if user_id not in user_sessions:
        user_sessions[user_id] = {
            "total_pages": 0,
            "matching_files": {},
            "original_message": None,
        }

    user_context = user_sessions[user_id]

    # Clear previous user session data

    user_context["matching_files"] = {}
    user_context["original_message"] = None

    # Record the start time for measuring the duration
    start_time = time.time()
    
    user_query = limit_search_query_length(message.text.lower(), 50)

    # Search for the user's query in the file names and captions
    query_keywords = re.split(r'\s+', user_query.lower())
    matching_files = sorted(
        [
            (name, info)
            for name, info in data.items()
            if all(keyword in clean_text(name.lower()) for keyword in query_keywords)
            or (len(info[0]) > 2 and all(keyword in clean_text(info[0][2].lower()) for keyword in query_keywords))
        ],
        key=custom_sort,
    )

    # Calculate the time taken to find results
    duration = time.time() - start_time

    total_pages = math.ceil(len(matching_files) / RESULTS_PER_PAGE)

    if matching_files:
        # Initialize page to 1
        page = 1
        original_message = display_paginated_results(
            message.chat.id,
            matching_files,
            page,
            total_pages,
            original_message_id=user_context.get("original_message"),
            user_query=user_query,
            num_results=len(matching_files),
            duration=duration,
            user_first_name=message.from_user.first_name,
        )
    else:

        #  photo_2023-12-09_14-23-29.jpg is the path to your image file
        photo_path = "photo_2023-12-09_14-23-29.jpg"

        # Send the photo with the message
        response_message = bot.send_photo(
            chat_id=message.chat.id,
            photo=open(photo_path, "rb"),
            caption="🤔 Oopsie! I couldn't find that one. Maybe the movie or series is playing hide and seek with me. 😅\n\n"
            "Could you double-check the spelling. If you're absolutely certain, "
            "you can send your request to my creator, and we'll do our best to track it down together! 🚀✨"
        )

        # Delay for 5 seconds
        time.sleep(5)

        # Delete the message
        bot.delete_message(
            chat_id=message.chat.id, message_id=response_message.message_id
        )

    # Update user session context
    user_sessions[user_id] = {
        "total_pages": total_pages,
        "matching_files": matching_files,
        "original_message": original_message,
    }


# Function to send all files in the current page
def send_all_files_in_page(call, current_page, matching_files):
    start_index = (current_page - 1) * RESULTS_PER_PAGE
    end_index = start_index + RESULTS_PER_PAGE
    current_results = matching_files[start_index:end_index]

    for name, info in current_results:
        file_id, _, caption = info[0]
        bot.send_document(call.message.chat.id, file_id, caption=caption)

    # Update the user session context to reflect the changes
    user_id = call.from_user.id
    user_context = user_sessions.get(
        user_id,
        {
            "total_pages": 0,
            "matching_files": {},
            "original_message": None,
            "current_page": 1,
        },
    )

    # Remove the sent files from the matching_files list
    user_context["matching_files"] = user_context["matching_files"][RESULTS_PER_PAGE:]

    # If there are more files, send the "Send All Files" button
    if user_context["matching_files"]:
        send_all_button = types.InlineKeyboardButton(
            "⏮️ Continue ⏭️", callback_data="send_all2"
        )
        markup = types.InlineKeyboardMarkup().row(send_all_button)
        bot.send_message(
            call.message.chat.id,
            "Sending files has been paused. Click 'Continue' 👇 to send all remaining files.",
            reply_markup=markup,
        )
        # Update the current_page in the user session
        user_context["current_page"] += 1
    else:
        # If matching_files is empty, delete the results message and markup
        delete_results_message(
            call.message.chat.id, user_context.get("original_message")
        )
        send_random_sticker(call.message.chat.id, sticker_ids)



    # Update the user session context
    user_sessions[user_id] = user_context

# Send a sticker
def send_random_sticker(chat_id, sticker_ids):

    random_sticker_id = random.choice(sticker_ids)
    bot.send_sticker(chat_id, random_sticker_id)

# Function to delete the results message and markup
def delete_results_message(chat_id, message_id):
    try:
        bot.delete_message(chat_id=chat_id, message_id=message_id)
    except telebot.apihelper.ApiTelegramException as e:
        # Handle exceptions as needed
        print(f"Error deleting message: {e}")






# Function to display paginated results and return the original message ID
def display_paginated_results(
    chat_id,
    results,
    current_page,
    total_pages,
    original_message_id=None,
    user_query=None,
    num_results=None,
    duration=None,
    user_first_name=None
):
    # Custom sorting logic
    results = sorted(results, key=custom_sort)

    start_index = (current_page - 1) * RESULTS_PER_PAGE
    end_index = start_index + RESULTS_PER_PAGE
    current_results = results[start_index:end_index]

    markup = types.InlineKeyboardMarkup(row_width=3)

    for name, info in current_results:
        file_id, file_size, caption = info[0]
        callback_data = name
        button_text = f"[🗄️{file_size}] - {name}"
        button = types.InlineKeyboardButton(button_text, callback_data=callback_data)
        markup.add(button)

    # Add pagination buttons on the same row
    pagination_buttons = []

    if current_page > 1:
        prev_button = types.InlineKeyboardButton(
            "⏮️ Previous", callback_data=f"prev_{current_page}"
        )
        pagination_buttons.append(prev_button)

    page_number_button = types.InlineKeyboardButton(
        f"📝 Page {current_page}/{total_pages}", callback_data="page_number"
    )
    pagination_buttons.append(page_number_button)

    if current_page < total_pages:
        next_button = types.InlineKeyboardButton(
            "Next ⏭️", callback_data=f"next_{current_page}"
        )
        pagination_buttons.append(next_button)

    # Add a button to send all files in the current page
    send_all_button = types.InlineKeyboardButton(
        "🗃️ Send All Files 🗃️", callback_data="send_all")

    # Create a new row for the "Send All" button
    markup.row(send_all_button)

    # Add the pagination buttons in a new row
    markup.row(*pagination_buttons)

    try:
        if original_message_id is not None:
            # Try to edit the existing message
            bot.edit_message_reply_markup(
                chat_id=chat_id, message_id=original_message_id, reply_markup=markup
            )
        else:
            # Preparing the keyboard
            message_text = (
                f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                f"╭─❖✅ Requested: {user_query.title()}❖─╮\n"
                f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                f"╭─❖🔍 Results Found: {num_results}❖─╮\n"
                f"▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n"
                f"╭─❖⌚ Time Taken: {duration * 1000:.2f} ms ❖─╮\n"
                f"▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\n"
                f"╭─❖🍀 Requested By: {user_first_name} ❖─╮\n"
                f"▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱▱\n"
            )

            # Send a new message with updated information as a reply
            message = bot.send_message(
                chat_id,
                message_text,
                reply_markup=markup,
            )

            return message.message_id

    except telebot.apihelper.ApiTelegramException as e:
        if "message is not modified" in str(e):
            # Delete the existing message and send a new one
            if original_message_id is not None:
                bot.delete_message(chat_id=chat_id, message_id=original_message_id)
            message_text = f"File request: {user_query.title()}\nResults found: {num_results}\nTime taken: {duration * 1000:.2f} milliseconds"
            message = bot.send_message(chat_id, message_text, reply_markup=markup)
            return message.message_id
        else:
            # Log the error and handle it appropriately
            bot.send_message(
                chat_id,
                "⚠️ Please send the request again, I didn't quite catch that.",
            )
            # raise the exception or return an error message here
            raise



# Handler for inline keyboard button clicks
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    user_id = call.from_user.id

    # Load user session context
    user_context = user_sessions.get(
        user_id, {"total_pages": 0, "matching_files": {}, "original_message": None}
    )
    total_pages, matching_files, original_message = (
        user_context["total_pages"],
        user_context["matching_files"],
        user_context["original_message"],
    )

    # Load data from file_data.json
    with open("file_data.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    file_name = call.data
    file_info = data.get(file_name)

    # Handle file callbacks
    if file_info:
        file_id, _, caption = file_info[0]
        bot.send_document(call.message.chat.id, file_id, caption=caption)
    else:
        # Handle pagination button clicks
        if call.data.startswith("prev_") or call.data.startswith("next_"):
            handle_pagination_callback(call, user_context)
        elif call.data == "send_all":
            # Call the send_all_files_in_page function
            send_all_files_in_page(
                call, user_context.get("current_page", 1), matching_files
            )
        elif call.data == "send_all2":
            # Delete the current message
            try:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            except telebot.apihelper.ApiTelegramException as e:
                # Handle exceptions as needed
                pass

            # Call the send_all_files_in_page function
            send_all_files_in_page(
                call, user_context.get("current_page", 1), matching_files
            )

        else:
            pass

    # Update user session context
    user_sessions[user_id] = {
        "total_pages": total_pages,
        "matching_files": matching_files,
        "original_message": original_message,
    }


# Handler for pagination button clicks
def handle_pagination_callback(call, user_context):
    total_pages, matching_files, original_message = (
        user_context["total_pages"],
        user_context["matching_files"],
        user_context["original_message"],
    )
    current_page = int(call.data.split("_")[1])

    if call.data.startswith("prev_") and current_page > 1:
        page = current_page - 1
    elif call.data.startswith("next_") and current_page < total_pages:
        page = current_page + 1
    else:
        return

    # Check if original_message is not None before making the call
    if original_message is not None:
        original_message = display_paginated_results(
            call.message.chat.id, matching_files, page, total_pages, original_message
        )
    else:
        # Handle the case where original_message is not associated with a value
        # Send a message to the user saying that the search query couldn't be found
        search_query = user_context.get("user_query", "your search")
        error_message = "🤖 Oopsie! It seems I didn't quite catch that!\nPlease resend your request, and I'll do my best to understand this time. 🔄😊"

        bot.send_message(call.message.chat.id, error_message)

    # Update user session context
    user_context["total_pages"] = total_pages
    user_context["matching_files"] = matching_files
    user_context["original_message"] = original_message


# Run the bot
while True:
    try:
        bot.polling()
    except Exception as e:
        

        time.sleep(5)
