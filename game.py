import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import random
import streamlit as st
from questions import beginner, intermediate, advanced 

if 'stage' not in st.session_state:
    st.session_state.stage = 1  
if 'player_grid' not in st.session_state:
    st.session_state.player_grid = []
if 'computer_grid' not in st.session_state:
    st.session_state.computer_grid = []
if 'drawn_numbers' not in st.session_state:
    st.session_state.drawn_numbers = []
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'current_options' not in st.session_state:
    st.session_state.current_options = None
if 'current_answer' not in st.session_state:
    st.session_state.current_answer = None
if 'current_num' not in st.session_state:
    st.session_state.current_num = None
if 'turn' not in st.session_state:
    st.session_state.turn = "Player"  
if 'winner' not in st.session_state:
    st.session_state.winner = None  
if 'player_bingo_count' not in st.session_state:
    st.session_state.player_bingo_count = 0
if 'computer_bingo_count' not in st.session_state:
    st.session_state.computer_bingo_count = 0
if 'questions_answered' not in st.session_state:
    st.session_state.questions_answered = 0
if 'correct_answers' not in st.session_state:
    st.session_state.correct_answers = 0
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = None

def initialize_grids():
    numbers = random.sample(range(1, 26), 25)
    st.session_state.player_grid = [numbers[i * 5:(i + 1) * 5] for i in range(5)]
    st.session_state.computer_grid = [numbers[i * 5:(i + 1) * 5] for i in range(5)]

def draw_number():
    available_numbers = [num for row in st.session_state.player_grid for num in row if num != "X"]
    if available_numbers:
        drawn_number = random.choice(available_numbers)
        st.session_state.drawn_numbers.append(drawn_number)
        return drawn_number
    else:
        return None

def mark_number(grid, number):
    for row in grid:
        for i in range(len(row)):
            if row[i] == number:
                row[i] = "X"

def check_bingo(grid):
    bingo_count = 0
    for i in range(5):
        if all(cell == "X" for cell in grid[i]):  
            bingo_count += 1
        if all(row[i] == "X" for row in grid):  
            bingo_count += 1
            
    if all(grid[i][i] == "X" for i in range(5)):  
        bingo_count += 1
    if all(grid[i][4 - i] == "X" for i in range(5)):  
        bingo_count += 1
    
    return bingo_count

def ask_question(num):
    questions_dict = {
        "Beginner": beginner,
        "Intermediate": intermediate,
        "Advanced": advanced
    }
    
    current_questions = questions_dict[st.session_state.difficulty]
    st.session_state.current_question, st.session_state.current_options, st.session_state.current_answer = current_questions[num]

def computer_turn():
    drawn_number = random.randint(1, 25) 
    if drawn_number not in st.session_state.drawn_numbers:
        st.session_state.drawn_numbers.append(drawn_number)
        mark_number(st.session_state.player_grid, drawn_number)  
        mark_number(st.session_state.computer_grid, drawn_number)  
        st.write(f"Computer drew number {drawn_number}")
        
        st.session_state.computer_bingo_count = check_bingo(st.session_state.computer_grid)
        
        if st.session_state.computer_bingo_count >= 5:
            st.session_state.winner = "Computer"
            st.session_state.stage = 2  
        else:
            st.session_state.turn = "Player"   

def reset_game():
    st.session_state.stage = 1
    st.session_state.player_grid = []
    st.session_state.computer_grid = []
    st.session_state.drawn_numbers = []
    st.session_state.current_question = None
    st.session_state.current_options = None
    st.session_state.current_answer = None
    st.session_state.current_num = None
    st.session_state.turn = "Player"
    st.session_state.winner = None
    st.session_state.player_bingo_count = 0
    st.session_state.computer_bingo_count = 0
    st.session_state.questions_answered = 0
    st.session_state.correct_answers = 0

def highlight_bingo_lines(grid, winner):
    highlighted_grid = [row.copy() for row in grid]
    
    for i in range(5):
        if all(cell == "X" for cell in grid[i]):  
            for j in range(5):
                highlighted_grid[i][j] = f"{highlighted_grid[i][j]}"  
    
    for i in range(5):
        if all(row[i] == "X" for row in grid):  
            for j in range(5):
                highlighted_grid[j][i] = f"{highlighted_grid[j][i]}"  

    if all(grid[i][i] == "X" for i in range(5)):  
        for i in range(5):
            highlighted_grid[i][i] = f"{highlighted_grid[i][i]}"  
    if all(grid[i][4 - i] == "X" for i in range(5)):  
        for i in range(5):
            highlighted_grid[i][4 - i] = f"{highlighted_grid[i][4 - i]}"  

    return highlighted_grid

def highlight_cells(x):
    return ['background-color: yellow' if str(cell).startswith("") else '' for cell in x]

def show_performance_report():
    metrics = {
        'Questions Answered': st.session_state.questions_answered,
        'Correct Answers': st.session_state.correct_answers,
        'Player Bingo Count': st.session_state.player_bingo_count,
        'Computer Bingo Count': st.session_state.computer_bingo_count,
        'Accuracy (%)': st.session_state.correct_answers / st.session_state.questions_answered * 100 if st.session_state.questions_answered > 0 else 0,
        'Drawn Numbers': len(st.session_state.drawn_numbers)
    }

    df = pd.DataFrame(metrics.items(), columns=['Metric', 'Value'])

    fig, axes = plt.subplots(3, 2, figsize=(14, 12))
    axes = axes.flatten()  

    sns.barplot(x='Metric', y='Value', data=df, ax=axes[0])
    axes[0].set_title('Game Performance Metrics')

    sns.lineplot(x='Metric', y='Value', data=df, ax=axes[1], marker='o')
    axes[1].set_title('Performance Over Time')

    sns.histplot(df['Value'], bins=10, ax=axes[2], kde=True)
    axes[2].set_title('Distribution of Game Metrics')

    axes[3].pie(df['Value'], labels=df['Metric'], autopct='%1.1f%%')
    axes[3].set_title('Proportion of Game Metrics')

    additional_data = [random.randint(1, 10) for _ in range(5)]
    axes[4].bar(range(1, 6), additional_data)
    axes[4].set_title('Additional Metric 1')

    additional_data2 = [random.randint(1, 10) for _ in range(5)]
    axes[5].bar(range(1, 6), additional_data2)
    axes[5].set_title('Additional Metric 2')

    plt.tight_layout()
    st.write("### Player's Performance Report")
    st.pyplot(fig)

    st.write("### Winning Bingo Grid:")
    winning_grid = highlight_bingo_lines(st.session_state.player_grid, st.session_state.winner)
    winning_grid_df = pd.DataFrame(winning_grid)
    
    styled_winning_grid = winning_grid_df.style.apply(highlight_cells, axis=1)
    st.dataframe(styled_winning_grid)

    st.write("### How Bingo was Achieved:")
    st.write(f"The player marked the following numbers on their grid: {', '.join(map(str, st.session_state.drawn_numbers))}.")
    st.write("The lines highlighted in yellow indicate the winning Bingo lines!")

st.title("Pandas Bingo Game:")

st.sidebar.subheader("Select Difficulty Level")
difficulty = st.sidebar.radio("Choose your level:", ("Beginner", "Intermediate", "Advanced"))
st.session_state.difficulty = difficulty

if st.session_state.difficulty == "Beginner":
    st.sidebar.write("Welcome, Beginner!")
    st.sidebar.write("- Welcome to the Bingo Quiz for Beginners! Click a number on your Bingo card to answer a trivia question. If you're correct, mark it off. Aim to mark 5 numbers in a row—horizontally, vertically, or diagonally—while competing against the computer. Enjoy the game!.")
    st.sidebar.write("- Don’t worry if you’re new; hints are available! Enjoy a playful way to enhance your knowledge and enjoy the thrill of Bingo!")


elif st.session_state.difficulty == "Intermediate":
    st.sidebar.write("Welcome, Intermediate Player!")
    st.sidebar.write("- Welcome to the Intermediate Bingo Quiz! Start with a Bingo card filled with numbers and challenging trivia questions. Click a number to answer; if correct, mark it on your card. Compete against the computer and aim for 5 marked numbers in a row. Enjoy this exciting blend of strategy and trivia!")
    st.sidebar.write("- Get ready to elevate your knowledge and skills while playing!")
    

elif st.session_state.difficulty == "Advanced":
    st.sidebar.write("Welcome, Advanced Player!")
    st.sidebar.write("- Welcome to the Advanced Bingo Quiz! This level is designed for trivia enthusiasts seeking a challenge. Receive a Bingo card with numbers linked to intricate questions. Click a number to answer; if correct, mark it. Compete against a smart computer opponent and aim for 5 marked numbers in a row!")
    st.sidebar.write("- Ready to showcase your knowledge and strategic thinking? Jump into the Advanced Bingo Quiz and aim for victory!")

if st.session_state.stage == 1:
    st.write("Welcome to the Pandas Bingo Game, where fun meets knowledge! This interactive game combines the classic Bingo experience with trivia challenges tailored to different skill levels: Beginner, Intermediate, and Advanced. Players will draw numbers, mark their Bingo grids, and answer corresponding questions to earn their spots on the grid. Compete against the computer to achieve Bingo first, while tracking your performance through insightful metrics. Perfect for honing your skills in a playful setting, this game promises an engaging blend of luck and learning. Let the games begin!.")
    st.write("Choose your Difficulty level and press 'Start Game' to begin.")
    if st.button("Start Game"):
        st.session_state.stage = 2  
        initialize_grids()

elif st.session_state.stage == 2:
    if st.session_state.winner:
        st.success(f"🎉 Congratulations {st.session_state.winner}! 🎉 You won the game!")
        show_performance_report()
        if st.button("Back to Home"):
            reset_game()
    else:
        st.subheader("Player's Card")
        cols = st.columns(5)
        for row_idx, row in enumerate(st.session_state.player_grid):
            for col_idx, num in enumerate(row):
                if cols[col_idx].button(f"{num}", key=f"player-{row_idx}-{col_idx}"):
                    ask_question(num)
                    st.session_state.current_num = num
                    st.session_state.stage = 3
        
        st.write(f"Your Bingo Progress: {st.session_state.player_bingo_count} / 5")
        if st.session_state.turn == "Computer":
            computer_turn()

elif st.session_state.stage == 3:
    st.subheader(f"Question for Number {st.session_state.current_num}:")
    question_text, options, answer = st.session_state.current_question, st.session_state.current_options, st.session_state.current_answer
    st.write(question_text)
    player_answer = st.radio("Select your answer:", options, index=None)  
    
    if st.button("Submit Answer"):
        st.session_state.questions_answered += 1
        if player_answer == answer:
            st.success("Correct! You can now mark the number.")
            st.session_state.correct_answers += 1
            mark_number(st.session_state.player_grid, st.session_state.current_num)
            st.session_state.player_bingo_count = check_bingo(st.session_state.player_grid)
            if st.session_state.player_bingo_count >= 5:
                st.session_state.winner = "Player"
                st.session_state.stage = 2  
            else:
                st.session_state.turn = "Computer"
        else:
            st.error("Incorrect answer! The computer will now take its turn.")
            st.session_state.turn = "Computer"
        
        st.session_state.stage = 2  