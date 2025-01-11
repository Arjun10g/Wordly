import streamlit as st
import random
import nltk

# Download the NLTK word list
nltk.download("words")

# Load 6-letter words
word_list = [word.lower() for word in nltk.corpus.words.words() if len(word) == 6 and word.isalpha()]

# Function to generate feedback
def wordle_feedback(guess, target):
    feedback = ["X"] * 6  # Default to 'X' (Gray)
    target_count = {char: target.count(char) for char in set(target)}

    # First pass for 'G' (Green)
    for i in range(6):
        if guess[i] == target[i]:
            feedback[i] = "G"
            target_count[guess[i]] -= 1

    # Second pass for 'Y' (Yellow)
    for i in range(6):
        if feedback[i] == "X" and guess[i] in target and target_count[guess[i]] > 0:
            feedback[i] = "Y"
            target_count[guess[i]] -= 1

    return feedback

# CSS for Wordle-style tiles and keyboard
def inject_css():
    st.markdown(
        """
        <style>
        .tile-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .tile {
            width: 60px;
            height: 60px;
            margin: 5px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 24px;
            font-weight: bold;
            text-transform: uppercase;
            border: 2px solid #d3d6da;
            background-color: #ffffff;
            color: black;
        }
        .tile.green { background-color: #6aaa64; border-color: #6aaa64; color: white; }
        .tile.yellow { background-color: #c9b458; border-color: #c9b458; color: white; }
        .tile.gray { background-color: #787c7e; border-color: #787c7e; color: white; }
        .tile.empty { border-color: #d3d6da; }
        .keyboard {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            margin: 10px 0;
        }
        .key {
            width: 40px;
            height: 50px;
            margin: 3px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #d3d6da;
            background-color: #ffffff;
            color: black;
            text-transform: uppercase;
        }
        .key.green { background-color: #6aaa64; border-color: #6aaa64; color: white; }
        .key.yellow { background-color: #c9b458; border-color: #c9b458; color: white; }
        .key.gray { background-color: #787c7e; border-color: #787c7e; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Initialize session state
if "target_word" not in st.session_state:
    st.session_state.target_word = random.choice(word_list)
if "guesses" not in st.session_state:
    st.session_state.guesses = []
if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []
if "keyboard_state" not in st.session_state:
    st.session_state.keyboard_state = {letter: "unused" for letter in "abcdefghijklmnopqrstuvwxyz"}
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Inject CSS
inject_css()

# Title
st.title("6-Letter Wordle Game")

# Display previous guesses and feedback
st.header("Your Guesses")
for i in range(5):  # Show 5 rows for guesses
    if i < len(st.session_state.guesses):
        guess = st.session_state.guesses[i]
        feedback = st.session_state.feedbacks[i]
        tiles = "".join(
            f'<div class="tile { "green" if f == "G" else "yellow" if f == "Y" else "gray" }">{g}</div>'
            for g, f in zip(guess, feedback)
        )
    else:
        tiles = "".join('<div class="tile empty"></div>' for _ in range(6))
    st.markdown(f'<div class="tile-container">{tiles}</div>', unsafe_allow_html=True)

# Display keyboard
st.header("Keyboard")
keyboard_html = ""
for letter in "abcdefghijklmnopqrstuvwxyz":
    state = st.session_state.keyboard_state[letter]
    color_class = "green" if state == "green" else "yellow" if state == "yellow" else "gray" if state == "gray" else ""
    keyboard_html += f'<div class="key {color_class}">{letter}</div>'
st.markdown(f'<div class="keyboard">{keyboard_html}</div>', unsafe_allow_html=True)

# Input for new guess
if not st.session_state.game_over:
    st.header("Enter Your Guess")
    guess = st.text_input("Your guess (6 letters):", max_chars=6).lower()

    if st.button("Submit Guess"):
        if len(guess) != 6 or not guess.isalpha():
            st.error("Please enter a valid 6-letter word.")
        elif guess not in word_list:
            st.error("The word is not in the word list.")
        else:
            feedback = wordle_feedback(guess, st.session_state.target_word)
            st.session_state.guesses.append(guess)
            st.session_state.feedbacks.append(feedback)

            # Update keyboard state
            for g, f in zip(guess, feedback):
                if f == "G":
                    st.session_state.keyboard_state[g] = "green"
                elif f == "Y" and st.session_state.keyboard_state[g] != "green":
                    st.session_state.keyboard_state[g] = "yellow"
                elif f == "X" and st.session_state.keyboard_state[g] not in ["green", "yellow"]:
                    st.session_state.keyboard_state[g] = "gray"

            if guess == st.session_state.target_word:
                st.success(f"🎉 Congratulations! You guessed the word: {st.session_state.target_word.upper()}")
                st.session_state.game_over = True
            elif len(st.session_state.guesses) == 5:
                st.error(f"Game Over! The correct word was: {st.session_state.target_word.upper()}")
                st.session_state.game_over = True

# Restart the game
if st.session_state.game_over:
    if st.button("Restart Game"):
        st.session_state.target_word = random.choice(word_list)
        st.session_state.guesses = []
        st.session_state.feedbacks = []
        st.session_state.keyboard_state = {letter: "unused" for letter in "abcdefghijklmnopqrstuvwxyz"}
        st.session_state.game_over = False

# cd "/Users/arjunghumman/Downloads/VS Code Stuff/Python/Wordly"
# streamlit run wordly.py