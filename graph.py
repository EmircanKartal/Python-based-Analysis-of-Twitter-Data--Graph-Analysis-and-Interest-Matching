import tkinter
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, ttk, StringVar, Canvas, Scrollbar, Frame
import json
import tkinter as tk
from tkinter import ttk
import spacy
from collections import Counter
from tkinter import ttk, StringVar
from ttkthemes import ThemedTk
from ttkthemes import ThemedStyle
from ttkwidgets.autocomplete import AutocompleteCombobox
from PIL import Image, ImageTk
import random

interests_map= {}

class Follower:
    def __init__(self, username):
        self.username = username
        self.region = None
        self.top_interest = None

class Following:
    def __init__(self, username):
        self.username = username
        self.region = None
        self.top_interest = None
        
class Person:
    def __init__(self, username, name="", followers_count=0, following_count=0, language="", region="", tweets=None,
                 followers=None, following=None):
        self.username = username
        self.name = name
        self.followers_count = followers_count
        self.following_count = following_count
        self.language = language
        self.region = region
        self.tweets = tweets if tweets else []
        self.followers_usernames = followers if followers else []  # Store follower usernames
        self.following_usernames = following if following else []  # Store following usernames
        self.followers = []  # Initialize empty list for follower Person instances
        self.following = []  # Initialize empty list for following Person instances
        self.interests = []  # Added field for storing interests

    def share_tweet(self, tweet):
        self.tweets.append(tweet)

    def follow(self, person):
        # For simplicity, this function is not implemented for this example
        pass

    def get_person_info(self):
    # Top Interests
        top_interests = self.get_interests_from_tweetsReturn(nlp_en, top_n=3)
        top_interests_info = f"Top Interests: {', '.join(top_interests)}" if top_interests else "Top Interests: None"

    # Tweet Analysis
        tweet_analysis_info = "----- Tweet Analysis -----\n"
        for i, tweet in enumerate(self.tweets, start=1):
            tweet_analysis_info += f"Tweet {i}: {tweet}\n"

        info = f"Username: {self.username}\n" \
           f"Name: {self.name}\n" \
           f"Followers: {self.followers_count}\n" \
           f"Following: {self.following_count}\n" \
           f"Language: {self.language}\n" \
           f"Region: {self.region}\n" \
           f"{top_interests_info}\n" \
           f"{tweet_analysis_info}"

        return info



    def get_interests_from_tweetsReturn(self, language_model, top_n=1):
        doc = language_model(" ".join(self.tweets))
        words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

        # Count the occurrences of each word
        word_counts = Counter(words)

        # Get the top N most common words
        top_words = [word for word, _ in word_counts.most_common(top_n)]

        # Assign interests to the person
        self.interests = top_words

        # Print person's name and top interests
        #print(f"{self.name}'s top interests: {', '.join(top_words)}")

        return top_words

    def get_interests_from_tweets(self, language_model, top_n=1):
        doc = language_model(" ".join(self.tweets))
        words = [token.text.lower() for token in doc if token.is_alpha and not token.is_stop]

        # Count the occurrences of each word
        word_counts = Counter(words)

        # Get the top N most common words
        top_words = [word for word, _ in word_counts.most_common(top_n)]

        # Assign interests to the person
        self.interests = top_words

        # Print person's name and top interests
        #print(f"{self.name}'s top interests: {', '.join(top_words)}")

    def __str__(self):
        return f"{self.name}"
    
    def get_interests_count_in_tweets(self, top_interests):
        interests_count = Counter()

        for tweet in self.tweets:
            words = tweet.split()
            for interest in top_interests:
                interests_count[interest] += words.count(interest.lower())

        return interests_count

# Load the dataset from JSON
# Load the dataset from JSON
with open('english_dataset.json') as f:
    data = json.load(f)

# Create instances of Person and store them in a hash map
persons = {user['username']: Person(**user) for user in data}

# Build the relationships between followers and followings as Person objects
for person in persons.values():
    # Ensure that the follower's username is in the persons dictionary
    person.followers = [persons.get(follower, None) for follower in person.followers_usernames]
    person.followers = [follower for follower in person.followers if follower is not None]

    # Ensure that the following's username is in the persons dictionary
    person.following = [persons.get(following, None) for following in person.following_usernames]
    person.following = [following for following in person.following if following is not None]

    # Update followers' followers lists
    for follower in person.followers:
        if person not in follower.following:
            follower.following.append(person)

    # Update following's following lists
    for following_person in person.following:
        if person not in following_person.followers:
            following_person.followers.append(person)

# Print information for debugging
for person in persons.values():
    print(f"{person.username}'s Followers: {[follower.username for follower in person.followers]}")
    print(f"{person.username}'s Following: {[following.username for following in person.following]}")

def on_canvas_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def on_info_configure(event):
    canvas_info.configure(scrollregion=canvas_info.bbox("all"))

def show_info_popup(info):
    global canvas, canvas_info  # Declare as global variables

    popup = Tk()
    popup.title("Information")
    popup.geometry("400x300")
    popup.configure(bg="#2A2F4F")

    frame = ttk.Frame(popup, style='TFrame')
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Create a Canvas with a Scrollbar for the main content
    canvas = Canvas(
        frame,
        bg="#2A2F4F",
        height=100,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Place the Canvas and Scrollbar for the main content
    canvas.pack(side="top", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bind the Canvas configure event to update the scroll region
    canvas.bind("<Configure>", on_canvas_configure)

    # Create a Canvas with a Scrollbar for the information label
    canvas_info = Canvas(
        frame,
        bg="#2A2F4F",
        height=50,
        width=400,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    scrollbar_info = Scrollbar(frame, orient="vertical", command=canvas_info.yview)
    canvas_info.configure(yscrollcommand=scrollbar_info.set)

    # Place the Canvas and Scrollbar for the information label
    canvas_info.pack(side="top", fill="both", expand=True)
    scrollbar_info.pack(side="right", fill="y")

    # Bind the Canvas configure event to update the scroll region
    canvas_info.bind("<Configure>", on_info_configure)

    style = ttk.Style(popup)
    style.configure('TFrame', background='#2A2F4F')
    style.configure('TLabel', font=('Arial', 12, 'bold'), foreground='#FFDD54', background='#2A2F4F')  # Adjusted font, size, and color
    style.configure('TButton.Modern.TButton', background='#ADA5C1', foreground='#2A2F4F', font=('Helvetica', 14, 'bold'))

    # "Information" text in white bold font
    info_label = ttk.Label(canvas, text="Information", style='TLabel')
    info_label.pack(pady=5)

    # Information text below in white with a smaller font
    label = ttk.Label(canvas, text=info, style='TLabel')
    label.pack(pady=10)

     # Modern style for the "Close" button with bold font and ADA5C1 background
    button = ttk.Button(frame, text="Close", command=popup.destroy, style='TButton.Modern.TButton')
    button.pack(pady=15)

    popup.mainloop()

# Function to update the graph based on the selected person
def update_graph(selected_person, all_persons, language_model):
    plt.clf()  # Clear the existing plot

    # Extract interests from selected person's tweets
    selected_person.get_interests_from_tweets(language_model)

    # Create a subgraph based on the selected person and their interests
    subgraph = nx.Graph()
    subgraph.add_node(selected_person)

    for following_person in all_persons.values():
        # Extract interests from following person's tweets
        following_person.get_interests_from_tweets(language_model)

        # Find common interests
        common_interests = set(selected_person.interests) & set(following_person.interests)

        if common_interests:
            subgraph.add_node(following_person)
            subgraph.add_edge(selected_person, following_person, interests=common_interests)

    pos = nx.spring_layout(subgraph)

    # Draw the graph with labels
    nx.draw(subgraph, pos, labels={person: str(person) for person in subgraph.nodes},
            with_labels=True, font_size=12, font_weight='bold')

    # Add information as node attributes
    node_attributes = {person: {"info": person.get_person_info()} for person in subgraph.nodes}
    nx.set_node_attributes(subgraph, node_attributes)

    # Add information as edge attributes
    edge_attributes = nx.get_edge_attributes(subgraph, 'interests')

    # Draw smaller edge labels
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels=edge_attributes, font_size=8)

    # Handle click events on nodes
    def on_node_click(event):
        if event.inaxes is not None:
            for node, (x, y) in pos.items():
                if x - 0.05 < event.xdata < x + 0.05 and y - 0.05 < event.ydata < y + 0.05:
                    show_info_popup(subgraph.nodes[node]["info"])

    # Handle click events on edges
    def on_edge_click(event):
        if event.inaxes is not None:
            for edge, (x, y) in pos.items():
                if x - 0.05 < event.xdata < x + 0.05 and y - 0.05 < event.ydata < y + 0.05:
                    show_info_popup(edge_attributes[edge])

    # Connect click events
    fig = plt.gcf()
    fig.canvas.mpl_connect('button_press_event', on_node_click)
    fig.canvas.mpl_connect('button_press_event', on_edge_click)
    
    # Set the title of the Matplotlib figure window to "Graph"
    fig.canvas.manager.set_window_title("Graph")
    
    # Show the plot
    plt.title("Twitter Data Analysis")
    plt.show()

# Function to update the follower/following graph based on the selected person
def update_following_graph(selected_person, all_persons):
    """
    Update and display the following graph based on the selected person.

    Parameters:
    - selected_person (Person): The selected Person object.
    - all_persons (dict): A dictionary of all Person objects.

    Returns:
    - None
    """
    # Create a directed graph
    following_graph = nx.DiGraph()

    # Add nodes for the selected person and their followers/following
    following_graph.add_node(selected_person.username, color='red')  # Color the selected person differently

    # Add followers as nodes and edges
    for follower_username in selected_person.followers_usernames:
        if follower_username in all_persons:
            following_graph.add_node(follower_username)
            following_graph.add_edge(follower_username, selected_person.username, relationship="follower")

    # Add following as nodes and edges
    for following_username in selected_person.following_usernames:
        if following_username in all_persons:
            following_graph.add_node(following_username)
            following_graph.add_edge(selected_person.username, following_username, relationship="following")

    # Add information as node attributes
    node_attributes = {person: {"info": all_persons[person].get_person_info()} for person in following_graph.nodes}
    nx.set_node_attributes(following_graph, node_attributes)

    # Visualization (optional, you can skip this part if not needed)
    pos = nx.spring_layout(following_graph)
    labels = nx.get_edge_attributes(following_graph, 'relationship')

    # Draw nodes
    nx.draw(following_graph, pos, with_labels=True, font_weight='bold', arrowsize=10, node_color='lightblue', node_size=800)

    # Draw edge labels
    nx.draw_networkx_edge_labels(following_graph, pos, edge_labels=labels)

    # Handle click events on nodes
    def on_node_click(event):
        if event.inaxes is not None:
            for node, (x, y) in pos.items():
                if x - 0.05 < event.xdata < x + 0.05 and y - 0.05 < event.ydata < y + 0.05:
                    show_info_popup(following_graph.nodes[node]["info"])

    # Handle click events on edges
    def on_edge_click(event):
        if event.inaxes is not None:
            for edge, (x, y) in pos.items():
                if x - 0.05 < event.xdata < x + 0.05 and y - 0.05 < event.ydata < y + 0.05:
                    show_info_popup(labels[edge])

    # Connect the click events
    plt.gcf().canvas.mpl_connect('button_press_event', on_node_click)
    plt.gcf().canvas.mpl_connect('button_press_event', on_edge_click)

    plt.title("Following Graph")
    plt.show()
    
# Update the show_interests_column_chart function
def show_interests_column_chart(selected_person):
    # Get the top interests for the selected person
    top_interests = selected_person.get_interests_from_tweetsReturn(nlp_en, top_n=3)

    # Get the count of each top interest in the person's tweets
    interests_count = selected_person.get_interests_count_in_tweets(top_interests)

    # Create a new Tkinter window for the column chart
    chart_window = Tk()
    chart_window.title(f"Interest Counts for {selected_person.name}")
    chart_window.geometry("600x400")

    # Create a canvas to draw the column chart
    canvas = Canvas(chart_window, bg="#2A2F4F", width=600, height=400)
    canvas.pack()

    # Check if the person has any interests
    if not interests_count:
        info_label = ttk.Label(canvas, text=f"{selected_person.name} has no recorded interests in tweets.", style='TLabel')
        info_label.pack(pady=10)
        return

    # Sort interests based on counts
    sorted_interests = sorted(interests_count.items(), key=lambda x: x[1], reverse=True)

    # Extract top interests and their counts for plotting
    top_interests, counts = zip(*sorted_interests)

    # Plot the column chart
    bar_width = 50
    x_offset = 65
    column_height_factor = 55  # Increase the factor to make columns taller

    for i, (interest, count) in enumerate(zip(top_interests, counts), start=1):
        column_height = count * column_height_factor
        canvas.create_rectangle(i * x_offset, 400 - column_height, i * x_offset + bar_width, 400, fill='#45B39D')
        canvas.create_text(i * x_offset + bar_width / 2, 400 - column_height - 15, text=f"{count}", fill='white', font=('Arial', 10))
        canvas.create_text(i * x_offset + bar_width / 2, 400 - column_height + 45, text=f"{interest}", fill='white', font=('Arial', 13, 'bold'), angle=30)
    # Display the chart window
    chart_window.mainloop()

# Function to handle list users dropdown selection
def on_list_users_dropdown_select(selected_person_str):
    # Display information about the selected user
    selected_person = persons[selected_person_str]

    # Show the column chart of most used interests for the selected person
    show_interests_column_chart(selected_person)

# Function to handle follower/following dropdown selection
def on_following_dropdown_select(selected_person_str):
    selected_person = persons[selected_person_str]
    update_following_graph(selected_person, persons)


# Function to handle dropdown selection
def on_dropdown_select(selected_person_str):
    selected_person = persons[selected_person_str]
    update_graph(selected_person, persons, nlp_en)

# Function to clear text when dropdown is clicked
def on_dropdown_click(combobox):
    combobox.set("")

# Function to update dropdown options based on user input
def on_search(event):
    search_term = dropdown_var.get().lower()
    filtered_values = [person for person in persons.keys() if search_term in person.lower()]
    dropdown['values'] = filtered_values

    # Insert filtered values
    for value in filtered_values:
        dropdown.insert("", "end", values=(value,))

# Function to get interests from a sentence using spaCy
def get_interests(sentence, language_model):
    doc = language_model(sentence)
    interests = [token.text.lower() for token in doc if token.pos_ == "NOUN"]
    return interests

# Function to classify sentences into groups based on interests
def classify_sentences_into_groups(sentences, language_model):
    groups = {}

    for sentence in sentences:
        interests = get_interests(sentence, language_model)

        found_group = None
        for group_interests in groups.keys():
            if set(interests) & set(group_interests):
                found_group = group_interests
                break

        if found_group is not None:
            groups[found_group].append(sentence)
        else:
            groups[tuple(interests)] = [sentence]

    return groups

# Load the spaCy English model
nlp_en = spacy.load("en_core_web_sm")

interest_list = []

for i in persons.keys():
    temp = persons[i].get_interests_from_tweetsReturn(nlp_en)
    print(temp)
    
    # Add interests to the redesigned list
    interest_list.extend(temp)

    for interest in temp:
        if interest not in interests_map:
            interests_map[interest] = [persons[i]]
        else:
            interests_map[interest].append(persons[i])

# Print the redesigned interest list
print("Redesigned Interest List:", interest_list)

for interest, persons_list in interests_map.items():
    print(f"Interest: {interest}")
    for person in persons_list:
        print(f"    {person.name}")

region_interests_map = {}

# Calculate interests for each person and update the region_interests_map
for person in persons.values():
    interests = person.get_interests_from_tweetsReturn(nlp_en, top_n=3)  # Adjust top_n as needed

    # Update the region_interests_map
    if person.region not in region_interests_map:
        region_interests_map[person.region] = interests
    else:
        region_interests_map[person.region].extend(interests)

# Function to analyze and print the frequency of each top interest in tweets
def analyze_top_interest_frequency(persons, top_interest, interest_list):
    print(f"Analyzing frequency of top interest: {top_interest}")
    
    # Counter to store the frequency of the top interest for each person

    
# Assuming 'stock' is one of the top interests
top_interests_to_analyze = list(interests_map.keys())

# Analyze and print the frequency of each top interest in tweets
for top_interest in top_interests_to_analyze:
    analyze_top_interest_frequency(persons, top_interest, interest_list)

# Print region_interests_map for debugging
region_list = list()
for region, interests in region_interests_map.items():
    region_list.append(region)
    print(f"Region: {region}, Top Interests: {interests}")

with open('person_analysis_results.txt', 'w') as file:
    # Analyze each person and write results to the file
    for person in persons.values():
        file.write(f"Username: {person.username}\n")
        file.write(f"Name: {person.name}\n")
        file.write(f"Followers Count: {person.followers_count}\n")
        file.write(f"Following Count: {person.following_count}\n")
        file.write(f"Language: {person.language}\n")
        file.write(f"Region: {person.region}\n")

        # 2. Top Interests
        top_interests = person.get_interests_from_tweetsReturn(nlp_en, top_n=3)
        file.write(f"Top Interests: {', '.join(top_interests)}\n")

        # 4. Tweet Analysis
        file.write("----- Tweet Analysis -----\n")
        for i, tweet in enumerate(person.tweets, start=1):
            file.write(f"Tweet {i}: {tweet}\n")

        # 5. Region-based Analysis
        file.write("----- Region-based Analysis -----\n")
        file.write(f"Region: {person.region}\n")
        file.write(f"Followers: {[follower.name for follower in person.followers]}\n")
        file.write(f"Following: {[following.name for following in person.following]}\n")

        # Add a separator between each person's analysis
        file.write("\n" + "=" * 50 + "\n\n")

def assign_random_attributes_to_followers():
    for person in persons.values():
        for follower_username in person.followers_usernames:
            # Check if the follower belongs to the user in the english_dataset.json
            if follower_username in persons:
                follower = Follower(username=follower_username)
            else:
                follower = Following(username=follower_username)

            # Assign random values to region and top_interest
            follower.region = random.choice(region_list)
            follower.top_interest = random.choice(interest_list)

            # Add the follower to the self.followers list of the person
            person.followers.append(follower)

def assign_random_attributes_to_following():
    for person in persons.values():
        for following_username in person.following_usernames:
            # Decide whether to use Follower or Following class
            if following_username in person.followers_usernames:
                following = Follower(username=following_username)
            else:
                following = Following(username=following_username)

            # Assign random values to region and top_interest
            following.region = random.choice(region_list)
            following.top_interest = random.choice(interest_list)
assign_random_attributes_to_followers()
assign_random_attributes_to_following()

for person in persons.values():
    print(person.username)
    for follower in person.followers:
        print(f"    {follower.username}")
        #print(f"        Top Interest: {follower.top_interest}")
        #print(f"        Region: {follower.region}")

# Create a network graph
#G = tk.Canvas(width=600, height=400)

# Create a ThemedTk window with 'equilux' theme
window = ThemedTk(theme="equilux")
window.title("Network Graph Visualization")
window.geometry("600x400")  # Increase window size

# Define colors
color1 = "#efe9d1"
color2 = "#09ad78"
color3 = "#12171f"

# Load and display the background image for the canvas
image_path_bg = r"C:\\Users\\User\\OneDrive\\Belgeler\\Python Scripts\\Images\\WorldMap.jpg"
pil_bg = Image.open(image_path_bg)
bg_image = ImageTk.PhotoImage(pil_bg)

# Create a canvas with the background image
canvas = tk.Canvas(window, width=600, height=400, bg="#12171f")  # Use a solid color as a fallback
canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)
canvas.pack()

# Create rectangles with different colors on the canvas
rectangle1 = canvas.create_rectangle(25, 30, 185, 370, fill=color1)
rectangle2 = canvas.create_rectangle(215, 30, 375, 370, fill=color2)
rectangle3 = canvas.create_rectangle(405, 30, 565, 370, fill=color1)

# Add title text to each rectangle
title_font = ('Eugello Bold', 18, 'bold')  # Choose a Times New Roman font with size 18 and bold style
text_font = (('Eugello Regular', 11))
canvas.create_text(105, 90, text="Person", font=title_font, fill='black')

# Add description text below the title
canvas.create_text(105, 140, text="Matching Person with\nthe ones having the\nsame interest", font=text_font, fill='black')

canvas.create_text(295, 90, text="Follow", font=title_font, fill='white')
canvas.create_text(295, 140, text="Displaying Person \nwith the followings\nand followers", font=text_font, fill='white')

canvas.create_text(485, 90, text="Frequency", font=title_font, fill='black')
canvas.create_text(485, 150, text="A chart based\non the frequency of\ninterests in a\nperson's tweets", font=text_font, fill='black')

# Load and display the image
image_path_globe = r"C:\\Users\\User\\OneDrive\\Belgeler\\Python Scripts\\Images\\globe.png"
image_path_node = r"C:\\Users\\User\\OneDrive\\Belgeler\\Python Scripts\\Images\\node.png"
image_path_wave = r"C:\\Users\\User\\OneDrive\\Belgeler\\Python Scripts\\Images\\wave.png"

# Load and display the image using Pillow
pil_image1 = Image.open(image_path_globe)
network_image = ImageTk.PhotoImage(pil_image1)
canvas.create_image(285, 290, anchor=tk.CENTER, image=network_image)

pil_image2 = Image.open(image_path_node)
node_image = ImageTk.PhotoImage(pil_image2)
canvas.create_image(104, 238, anchor=tk.CENTER, image=node_image)

pil_image3 = Image.open(image_path_wave)
wave_image = ImageTk.PhotoImage(pil_image3)
canvas.create_image(490, 240, anchor=tk.CENTER, image=wave_image)

# Configure background color and font
window.configure(background="#12171f")  # Dark background color
style = ThemedStyle(window)
style.configure('TButton', background='#45B39D', font=('Helvetica', 12))
style.configure('TCombobox', font=('Arial', 12, 'bold'), foreground='white', fieldbackground='#2E3B4E')  # Change font and colors

# Create an AutocompleteCombobox with custom styling for person-interest graph
dropdown_var = tk.StringVar()
dropdown = AutocompleteCombobox(
    window,
    textvariable=dropdown_var,
    style='TCombobox',  # Apply the custom style
)
dropdown['values'] = list(persons.keys())
dropdown.set("Person")
dropdown.bind('<Button-1>', lambda event: on_dropdown_click(dropdown))
dropdown.bind('<<ComboboxSelected>>', lambda event: on_dropdown_select(dropdown_var.get()))
dropdown.bind('<KeyRelease>', on_search)
dropdown_window = canvas.create_window(105, 319, window=dropdown)  # Place dropdown in the first rectangle

# Create a new AutocompleteCombobox for follower/following graph
following_dropdown_var = tk.StringVar()
following_dropdown = AutocompleteCombobox(
    window,
    textvariable=following_dropdown_var,
    style='TCombobox',  # Apply the custom style
)
following_dropdown['values'] = list(persons.keys())
following_dropdown.set("Follow")
following_dropdown.bind('<Button-1>', lambda event: on_dropdown_click(following_dropdown))
following_dropdown.bind('<<ComboboxSelected>>', lambda event: on_following_dropdown_select(following_dropdown_var.get()))
following_dropdown.bind('<KeyRelease>', on_search)
following_dropdown_window = canvas.create_window(295, 200, window=following_dropdown)  # Place dropdown in the second rectangle

# Create a new AutocompleteCombobox for listing users
list_users_dropdown_var = tk.StringVar()
list_users_dropdown = AutocompleteCombobox(
    window,
    textvariable=list_users_dropdown_var,
    style='TCombobox',  # Apply the custom style
)
list_users_dropdown['values'] = list(persons.keys())
list_users_dropdown.set("Frequency")
list_users_dropdown.bind('<Button-1>', lambda event: on_dropdown_click(list_users_dropdown))
list_users_dropdown.bind('<<ComboboxSelected>>', lambda event: on_list_users_dropdown_select(list_users_dropdown_var.get()))
list_users_dropdown.bind('<KeyRelease>', on_search)
list_users_dropdown_window = canvas.create_window(485, 319, window=list_users_dropdown)  # Place dropdown in the third rectangle

# Lift the dropdown widgets to the top to make them visible
canvas.tag_raise(dropdown_window)
canvas.tag_raise(following_dropdown_window)
canvas.tag_raise(list_users_dropdown_window)

# Run the Tkinter main loop
window.mainloop()