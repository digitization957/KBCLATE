"""One-off script: creates data/questions.xlsx with sample trivia so the
app runs out of the box. Replace/expand this file with real questions
later -- same column format: que, option1, option2, option3, option4,
answer, level (answer must exactly match one of option1-4; level is 1-4).
"""
import openpyxl

rows = [
    # Level 1
    ("Which planet is known as the Red Planet?", "Venus", "Mars", "Jupiter", "Saturn", "Mars", 1),
    ("How many continents are there on Earth?", "5", "6", "7", "8", "7", 1),
    ("What is the capital of India?", "Mumbai", "New Delhi", "Kolkata", "Chennai", "New Delhi", 1),
    ("Which animal is known as the King of the Jungle?", "Tiger", "Elephant", "Lion", "Leopard", "Lion", 1),
    ("How many days are there in a leap year?", "364", "365", "366", "367", "366", 1),
    ("Which is the largest ocean on Earth?", "Atlantic", "Indian", "Arctic", "Pacific", "Pacific", 1),
    ("What color do you get by mixing blue and yellow?", "Purple", "Green", "Orange", "Pink", "Green", 1),
    ("Which gas do plants absorb from the atmosphere?", "Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen", "Carbon Dioxide", 1),
    # Level 2
    ("Who wrote the Indian national anthem 'Jana Gana Mana'?", "Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi", "Rabindranath Tagore", 2),
    ("Which is the longest river in the world?", "Amazon", "Nile", "Ganga", "Yangtze", "Nile", 2),
    ("In which year did India gain independence?", "1945", "1946", "1947", "1948", "1947", 2),
    ("What is the chemical symbol for Gold?", "Ag", "Au", "Gd", "Go", "Au", 2),
    ("Which sport is associated with the term 'Checkmate'?", "Chess", "Carrom", "Badminton", "Billiards", "Chess", 2),
    ("Which Indian state is known as the 'Land of Five Rivers'?", "Punjab", "Kerala", "Rajasthan", "Bihar", "Punjab", 2),
    ("What is the smallest prime number?", "0", "1", "2", "3", "2", 2),
    ("Which organ in the human body produces insulin?", "Liver", "Pancreas", "Kidney", "Heart", "Pancreas", 2),
    # Level 3
    ("Who was the first Prime Minister of India?", "Sardar Patel", "Jawaharlal Nehru", "Lal Bahadur Shastri", "Rajendra Prasad", "Jawaharlal Nehru", 3),
    ("Which company developed the Windows operating system?", "Apple", "IBM", "Microsoft", "Google", "Microsoft", 3),
    ("What does 'www' stand for in a website address?", "World Wide Web", "World Web Wide", "Wide World Web", "Web World Wide", "World Wide Web", 3),
    ("Which planet has the most moons in our solar system?", "Jupiter", "Saturn", "Uranus", "Neptune", "Saturn", 3),
    ("Who painted the Mona Lisa?", "Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo", "Leonardo da Vinci", 3),
    ("Which is the smallest country in the world by area?", "Monaco", "San Marino", "Vatican City", "Liechtenstein", "Vatican City", 3),
    ("The Great Barrier Reef is located near which country?", "Brazil", "Australia", "South Africa", "Indonesia", "Australia", 3),
    ("Which Indian cricketer is known as 'The Wall'?", "Sachin Tendulkar", "Rahul Dravid", "Virender Sehwag", "Sourav Ganguly", "Rahul Dravid", 3),
    # Level 4
    ("Who was awarded the first Nobel Prize in Physics?", "Marie Curie", "Albert Einstein", "Wilhelm Rontgen", "Max Planck", "Wilhelm Rontgen", 4),
    ("What is the currency of Japan?", "Yuan", "Won", "Yen", "Ringgit", "Yen", 4),
    ("Which Mughal emperor built the Taj Mahal?", "Akbar", "Jahangir", "Shah Jahan", "Aurangzeb", "Shah Jahan", 4),
    ("What is the hardest natural substance on Earth?", "Gold", "Iron", "Diamond", "Platinum", "Diamond", 4),
    ("Which country hosted the first FIFA World Cup in 1930?", "Brazil", "Uruguay", "France", "Italy", "Uruguay", 4),
    ("Who is known as the 'Father of the Indian Constitution'?", "Mahatma Gandhi", "Jawaharlal Nehru", "B. R. Ambedkar", "Sardar Patel", "B. R. Ambedkar", 4),
    ("Which is the deepest point in the Earth's oceans?", "Mariana Trench", "Java Trench", "Tonga Trench", "Puerto Rico Trench", "Mariana Trench", 4),
    ("Which element has the atomic number 1?", "Helium", "Hydrogen", "Oxygen", "Carbon", "Hydrogen", 4),
]

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "questions"
ws.append(["que", "option1", "option2", "option3", "option4", "answer", "level"])
for row in rows:
    ws.append(row)

wb.save("D:/KBC/app/data/questions.xlsx")
print(f"wrote {len(rows)} sample questions to data/questions.xlsx")
