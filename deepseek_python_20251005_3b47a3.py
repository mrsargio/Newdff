import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import html
import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TestSeriesGenerator:
    def __init__(self):
        self.users_data = {}
    
    def generate_html_test(self, json_data, user_id):
        """Generate professional HTML test series from JSON data"""
        
        test_html = f"""
        <!DOCTYPE html>
        <html lang="hi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Test Series - प्रश्नोत्तरी</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                
                body {{
                    background-color: #f5f5f5;
                    color: #333;
                    line-height: 1.6;
                }}
                
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                
                header {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px 0;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                    border-radius: 0 0 20px 20px;
                }}
                
                .header-content {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                }}
                
                .logo {{
                    font-size: 28px;
                    font-weight: bold;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .logo-icon {{
                    font-size: 32px;
                }}
                
                .user-info {{
                    display: flex;
                    align-items: center;
                    gap: 20px;
                    background: rgba(255,255,255,0.1);
                    padding: 10px 20px;
                    border-radius: 25px;
                    backdrop-filter: blur(10px);
                }}
                
                .timer {{
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: bold;
                    box-shadow: 0 4px 15px rgba(255,107,107,0.3);
                }}
                
                .main-content {{
                    display: flex;
                    gap: 25px;
                    margin-top: 30px;
                }}
                
                .questions-section {{
                    flex: 1;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                    padding: 25px;
                    max-height: 80vh;
                    overflow-y: auto;
                }}
                
                .question-nav {{
                    flex: 0 0 280px;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 8px 25px rgba(0,0,0,0.1);
                    padding: 20px;
                    max-height: 80vh;
                    overflow-y: auto;
                }}
                
                .question-nav h3 {{
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid #f0f0f0;
                    color: #2c3e50;
                    font-size: 20px;
                }}
                
                .question-grid {{
                    display: grid;
                    grid-template-columns: repeat(5, 1fr);
                    gap: 12px;
                    margin-bottom: 20px;
                }}
                
                .question-btn {{
                    width: 45px;
                    height: 45px;
                    border: 2px solid #e0e0e0;
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: bold;
                    font-size: 14px;
                }}
                
                .question-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
                }}
                
                .question-btn.answered {{
                    background: linear-gradient(135deg, #2ecc71, #27ae60);
                    color: white;
                    border-color: #27ae60;
                }}
                
                .question-btn.current {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    color: white;
                    border-color: #2980b9;
                    transform: scale(1.1);
                }}
                
                .question-btn.skipped {{
                    background: linear-gradient(135deg, #e74c3c, #c0392b);
                    color: white;
                    border-color: #c0392b;
                }}
                
                .question {{
                    margin-bottom: 30px;
                }}
                
                .question-number {{
                    font-size: 20px;
                    font-weight: bold;
                    margin-bottom: 15px;
                    color: #2c3e50;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .question-number::before {{
                    content: "📌";
                    font-size: 18px;
                }}
                
                .question-text {{
                    font-size: 17px;
                    margin-bottom: 20px;
                    line-height: 1.6;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                    border-left: 4px solid #3498db;
                }}
                
                .options {{
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }}
                
                .option {{
                    display: flex;
                    align-items: flex-start;
                    gap: 15px;
                    padding: 15px;
                    border: 2px solid #e9ecef;
                    border-radius: 10px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                }}
                
                .option:hover {{
                    border-color: #3498db;
                    background: #f8f9ff;
                    transform: translateX(5px);
                }}
                
                .option.selected {{
                    background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
                    border-color: #4fc3f7;
                    box-shadow: 0 5px 15px rgba(79,195,247,0.2);
                }}
                
                .option-label {{
                    font-weight: bold;
                    min-width: 35px;
                    height: 35px;
                    background: #3498db;
                    color: white;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                
                .option.selected .option-label {{
                    background: #e74c3c;
                }}
                
                .actions {{
                    display: flex;
                    justify-content: space-between;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid #f0f0f0;
                }}
                
                .btn {{
                    padding: 12px 25px;
                    border: none;
                    border-radius: 25px;
                    cursor: pointer;
                    font-weight: bold;
                    transition: all 0.3s ease;
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                }}
                
                .btn-primary {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    color: white;
                }}
                
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(52,152,219,0.3);
                }}
                
                .btn-secondary {{
                    background: linear-gradient(135deg, #95a5a6, #7f8c8d);
                    color: white;
                }}
                
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(149,165,166,0.3);
                }}
                
                .btn-success {{
                    background: linear-gradient(135deg, #2ecc71, #27ae60);
                    color: white;
                }}
                
                .btn-success:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(46,204,113,0.3);
                }}
                
                .language-toggle {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 20px;
                    background: #f8f9fa;
                    padding: 15px;
                    border-radius: 10px;
                }}
                
                .lang-btn {{
                    padding: 10px 20px;
                    border: 2px solid #e0e0e0;
                    background: white;
                    border-radius: 25px;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    font-weight: bold;
                }}
                
                .lang-btn.active {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    color: white;
                    border-color: #2980b9;
                }}
                
                .question-status {{
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 15px;
                    margin-bottom: 20px;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 10px;
                }}
                
                .status-item {{
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .status-color {{
                    width: 20px;
                    height: 20px;
                    border-radius: 50%;
                }}
                
                .answered-color {{
                    background: linear-gradient(135deg, #2ecc71, #27ae60);
                }}
                
                .current-color {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                }}
                
                .skipped-color {{
                    background: linear-gradient(135deg, #e74c3c, #c0392b);
                }}
                
                .unattempted-color {{
                    background: #f0f0f0;
                    border: 2px solid #ddd;
                }}
                
                .solution {{
                    margin-top: 25px;
                    padding: 20px;
                    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
                    border-radius: 10px;
                    border-left: 5px solid #ff9800;
                }}
                
                .solution h4 {{
                    margin-bottom: 15px;
                    color: #e65100;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .solution h4::before {{
                    content: "💡";
                }}
                
                .hidden {{
                    display: none;
                }}
                
                .test-info {{
                    background: linear-gradient(135deg, #fff3e0, #ffe0b2);
                    padding: 20px;
                    border-radius: 15px;
                    margin-bottom: 25px;
                    border-left: 5px solid #ff9800;
                }}
                
                .test-info h3 {{
                    color: #e65100;
                    margin-bottom: 15px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .test-info h3::before {{
                    content: "📊";
                }}
                
                .info-grid {{
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 15px;
                }}
                
                .info-item {{
                    background: white;
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    box-shadow: 0 3px 10px rgba(0,0,0,0.1);
                }}
                
                .info-value {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #3498db;
                    margin-bottom: 5px;
                }}
                
                .info-label {{
                    font-size: 14px;
                    color: #7f8c8d;
                }}
                
                @media (max-width: 768px) {{
                    .main-content {{
                        flex-direction: column;
                    }}
                    
                    .question-nav {{
                        order: -1;
                    }}
                    
                    .question-grid {{
                        grid-template-columns: repeat(8, 1fr);
                    }}
                    
                    .actions {{
                        flex-direction: column;
                        gap: 10px;
                    }}
                    
                    .btn {{
                        width: 100%;
                        justify-content: center;
                    }}
                    
                    .question-status {{
                        grid-template-columns: 1fr;
                    }}
                }}
                
                /* Custom scrollbar */
                ::-webkit-scrollbar {{
                    width: 8px;
                }}
                
                ::-webkit-scrollbar-track {{
                    background: #f1f1f1;
                    border-radius: 10px;
                }}
                
                ::-webkit-scrollbar-thumb {{
                    background: linear-gradient(135deg, #3498db, #2980b9);
                    border-radius: 10px;
                }}
                
                ::-webkit-scrollbar-thumb:hover {{
                    background: linear-gradient(135deg, #2980b9, #1f618d);
                }}
            </style>
        </head>
        <body>
            <header>
                <div class="container">
                    <div class="header-content">
                        <div class="logo">
                            <span class="logo-icon">📚</span>
                            Premium Test Series
                        </div>
                        <div class="user-info">
                            <div class="timer" id="timer">03:00:00</div>
                            <div>User ID: {user_id}</div>
                        </div>
                    </div>
                </div>
            </header>
            
            <div class="container">
                <div class="test-info">
                    <h3>Test Overview</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <div class="info-value">{len(json_data['data'])}</div>
                            <div class="info-label">Total Questions</div>
                        </div>
                        <div class="info-item">
                            <div class="info-value">180</div>
                            <div class="info-label">Minutes</div>
                        </div>
                        <div class="info-item">
                            <div class="info-value">+4/-1</div>
                            <div class="info-label">Marking Scheme</div>
                        </div>
                        <div class="info-item">
                            <div class="info-value">{datetime.datetime.now().strftime('%d/%m/%Y')}</div>
                            <div class="info-label">Test Date</div>
                        </div>
                    </div>
                </div>
                
                <div class="language-toggle">
                    <button class="lang-btn active" id="hindiBtn">हिन्दी 🇮🇳</button>
                    <button class="lang-btn" id="englishBtn">English 🇺🇸</button>
                </div>
                
                <div class="question-status">
                    <div class="status-item">
                        <div class="status-color answered-color"></div>
                        <span>Answered</span>
                    </div>
                    <div class="status-item">
                        <div class="status-color current-color"></div>
                        <span>Current</span>
                    </div>
                    <div class="status-item">
                        <div class="status-color skipped-color"></div>
                        <span>Skipped</span>
                    </div>
                    <div class="status-item">
                        <div class="status-color unattempted-color"></div>
                        <span>Unattempted</span>
                    </div>
                </div>
                
                <div class="main-content">
                    <div class="questions-section">
                        <div class="question" id="questionContainer">
                            <!-- Question content will be loaded here -->
                        </div>
                        
                        <div class="actions">
                            <button class="btn btn-secondary" id="prevBtn">
                                <span>⬅️</span> Previous
                            </button>
                            <button class="btn btn-secondary" id="skipBtn">
                                <span>⏭️</span> Skip
                            </button>
                            <button class="btn btn-primary" id="nextBtn">
                                Next <span>➡️</span>
                            </button>
                            <button class="btn btn-success" id="submitBtn">
                                <span>📤</span> Submit Test
                            </button>
                        </div>
                    </div>
                    
                    <div class="question-nav">
                        <h3>Questions Navigation</h3>
                        <div class="question-grid" id="questionGrid">
                            <!-- Question navigation buttons will be loaded here -->
                        </div>
                        
                        <div class="solution" id="solutionContainer">
                            <h4>Solution & Explanation</h4>
                            <div id="solutionText">Select an option to view detailed solution</div>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                // Sample test data
                const testData = {json.dumps(json_data, ensure_ascii=False)};
                
                // Application state
                let currentQuestionIndex = 0;
                let userAnswers = {{}};
                let currentLanguage = 'hindi';
                let timerInterval;
                let timeRemaining = 10800; // 3 hours in seconds

                // DOM elements
                const questionContainer = document.getElementById('questionContainer');
                const questionGrid = document.getElementById('questionGrid');
                const prevBtn = document.getElementById('prevBtn');
                const nextBtn = document.getElementById('nextBtn');
                const skipBtn = document.getElementById('skipBtn');
                const submitBtn = document.getElementById('submitBtn');
                const hindiBtn = document.getElementById('hindiBtn');
                const englishBtn = document.getElementById('englishBtn');
                const timerElement = document.getElementById('timer');
                const solutionContainer = document.getElementById('solutionContainer');
                const solutionText = document.getElementById('solutionText');

                // Initialize the test
                function initializeTest() {{
                    createQuestionNavigation();
                    loadQuestion(currentQuestionIndex);
                    startTimer();
                    
                    // Set up event listeners
                    prevBtn.addEventListener('click', goToPreviousQuestion);
                    nextBtn.addEventListener('click', goToNextQuestion);
                    skipBtn.addEventListener('click', skipQuestion);
                    submitBtn.addEventListener('click', submitTest);
                    hindiBtn.addEventListener('click', () => switchLanguage('hindi'));
                    englishBtn.addEventListener('click', () => switchLanguage('english'));
                }}

                // Create question navigation buttons
                function createQuestionNavigation() {{
                    questionGrid.innerHTML = '';
                    
                    testData.data.forEach((question, index) => {{
                        const button = document.createElement('div');
                        button.className = 'question-btn';
                        button.textContent = index + 1;
                        button.addEventListener('click', () => loadQuestion(index));
                        
                        if (index === currentQuestionIndex) {{
                            button.classList.add('current');
                        }}
                        
                        questionGrid.appendChild(button);
                    }});
                }}

                // Load a specific question
                function loadQuestion(index) {{
                    currentQuestionIndex = index;
                    const question = testData.data[index];
                    
                    // Update navigation buttons
                    updateNavigationButtons();
                    
                    // Display question
                    if (currentLanguage === 'hindi') {{
                        questionContainer.innerHTML = `
                            <div class="question-number">प्रश्न {{{{index + 1}}}} of {{{{testData.data.length}}}}</div>
                            <div class="question-text">${{question['question']}}</div>
                            <div class="options">
                                ${{Object.entries(question['options']).map(([key, value]) => 
                                    value ? `
                                <div class="option ${{userAnswers[question.id] === `option${{key}}` ? 'selected' : ''}}" data-option="option${{key}}">
                                    <div class="option-label">${{key.toUpperCase()}}</div>
                                    <div class="option-text">${{value}}</div>
                                </div>
                                ` : ''
                                ).join('')}}
                            </div>
                        `;
                    }} else {{
                        questionContainer.innerHTML = `
                            <div class="question-number">Question {{{{index + 1}}}} of {{{{testData.data.length}}}}</div>
                            <div class="question-text">${{question['question_eng']}}</div>
                            <div class="options">
                                ${{Object.entries(question['options_eng']).map(([key, value]) => 
                                    value ? `
                                <div class="option ${{userAnswers[question.id] === `option${{key}}` ? 'selected' : ''}}" data-option="option${{key}}">
                                    <div class="option-label">${{key.toUpperCase()}}</div>
                                    <div class="option-text">${{value}}</div>
                                </div>
                                ` : ''
                                ).join('')}}
                            </div>
                        `;
                    }}
                    
                    // Add event listeners to options
                    const options = questionContainer.querySelectorAll('.option');
                    options.forEach(option => {{
                        option.addEventListener('click', () => {{
                            // Remove selected class from all options
                            options.forEach(opt => opt.classList.remove('selected'));
                            
                            // Add selected class to clicked option
                            option.classList.add('selected');
                            
                            // Save user's answer
                            userAnswers[question.id] = option.dataset.option;
                            
                            // Update navigation button
                            updateQuestionStatus(question.id, 'answered');
                            
                            // Show solution
                            showSolution(question);
                        }});
                    }});
                    
                    // Show solution if already answered
                    if (userAnswers[question.id]) {{
                        showSolution(question);
                    }} else {{
                        solutionText.textContent = currentLanguage === 'hindi' 
                            ? 'विस्तृत समाधान देखने के लिए कोई विकल्प चुनें' 
                            : 'Select an option to view detailed solution';
                    }}
                }}

                // Update navigation buttons
                function updateNavigationButtons() {{
                    const buttons = questionGrid.querySelectorAll('.question-btn');
                    
                    buttons.forEach((button, index) => {{
                        button.classList.remove('current', 'answered', 'skipped');
                        
                        if (index === currentQuestionIndex) {{
                            button.classList.add('current');
                        }}
                        
                        const questionId = testData.data[index].id;
                        if (userAnswers[questionId]) {{
                            button.classList.add('answered');
                        }}
                    }});
                    
                    // Enable/disable navigation buttons
                    prevBtn.disabled = currentQuestionIndex === 0;
                    nextBtn.disabled = currentQuestionIndex === testData.data.length - 1;
                }}

                // Update question status in navigation
                function updateQuestionStatus(questionId, status) {{
                    const questionIndex = testData.data.findIndex(q => q.id === questionId);
                    const button = questionGrid.querySelectorAll('.question-btn')[questionIndex];
                    
                    button.classList.remove('answered', 'skipped');
                    button.classList.add(status);
                }}

                // Show solution for current question
                function showSolution(question) {{
                    if (question.solution) {{
                        solutionText.innerHTML = `
                            <strong>Correct Answer:</strong> Option ${{question.answer.toUpperCase()}}<br><br>
                            <strong>Explanation:</strong><br>
                            ${{question.solution}}
                        `;
                    }} else {{
                        solutionText.textContent = currentLanguage === 'hindi'
                            ? 'इस प्रश्न के लिए कोई समाधान उपलब्ध नहीं है'
                            : 'No solution available for this question';
                    }}
                }}

                // Navigate to previous question
                function goToPreviousQuestion() {{
                    if (currentQuestionIndex > 0) {{
                        loadQuestion(currentQuestionIndex - 1);
                    }}
                }}

                // Navigate to next question
                function goToNextQuestion() {{
                    if (currentQuestionIndex < testData.data.length - 1) {{
                        loadQuestion(currentQuestionIndex + 1);
                    }}
                }}

                // Skip current question
                function skipQuestion() {{
                    const questionId = testData.data[currentQuestionIndex].id;
                    userAnswers[questionId] = 'skipped';
                    updateQuestionStatus(questionId, 'skipped');
                    
                    if (currentQuestionIndex < testData.data.length - 1) {{
                        loadQuestion(currentQuestionIndex + 1);
                    }}
                }}

                // Switch language
                function switchLanguage(language) {{
                    currentLanguage = language;
                    
                    if (language === 'hindi') {{
                        hindiBtn.classList.add('active');
                        englishBtn.classList.remove('active');
                    }} else {{
                        englishBtn.classList.add('active');
                        hindiBtn.classList.remove('active');
                    }}
                    
                    // Reload current question with new language
                    loadQuestion(currentQuestionIndex);
                }}

                // Start timer
                function startTimer() {{
                    timerInterval = setInterval(() => {{
                        timeRemaining--;
                        updateTimerDisplay();
                        
                        if (timeRemaining <= 0) {{
                            submitTest();
                        }}
                    }}, 1000);
                }}

                // Update timer display
                function updateTimerDisplay() {{
                    const hours = Math.floor(timeRemaining / 3600);
                    const minutes = Math.floor((timeRemaining % 3600) / 60);
                    const seconds = timeRemaining % 60;
                    
                    timerElement.textContent = 
                        `${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                }}

                // Submit test
                function submitTest() {{
                    clearInterval(timerInterval);
                    
                    // Calculate score
                    let score = 0;
                    let correct = 0;
                    let incorrect = 0;
                    let skipped = 0;
                    
                    testData.data.forEach(question => {{
                        if (userAnswers[question.id] === `option${{question.answer}}`) {{
                            score += question.plus_marks;
                            correct++;
                        }} else if (userAnswers[question.id] && userAnswers[question.id] !== 'skipped') {{
                            score -= question.minus_marks;
                            incorrect++;
                        }} else {{
                            skipped++;
                        }}
                    }});
                    
                    // Show results
                    const resultHTML = `
                        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-radius: 20px;">
                            <h2 style="margin-bottom: 20px; font-size: 32px;">🎉 Test Completed! 🎉</h2>
                            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin: 30px 0;">
                                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                                    <div style="font-size: 42px; font-weight: bold;">${{score.toFixed(2)}}</div>
                                    <div>Total Score</div>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                                    <div style="font-size: 42px; font-weight: bold;">${{correct}}</div>
                                    <div>Correct Answers</div>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                                    <div style="font-size: 42px; font-weight: bold;">${{incorrect}}</div>
                                    <div>Incorrect Answers</div>
                                </div>
                                <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; backdrop-filter: blur(10px);">
                                    <div style="font-size: 42px; font-weight: bold;">${{skipped}}</div>
                                    <div>Skipped Questions</div>
                                </div>
                            </div>
                            <p style="font-size: 18px; opacity: 0.9;">Time Taken: ${{timerElement.textContent}}</p>
                        </div>
                    `;
                    
                    questionContainer.innerHTML = resultHTML;
                    document.querySelector('.actions').style.display = 'none';
                }}

                // Initialize the test when the page loads
                document.addEventListener('DOMContentLoaded', initializeTest);
            </script>
        </body>
        </html>
        """
        
        return test_html

# Create bot instance
test_generator = TestSeriesGenerator()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send welcome message when the command /start is issued."""
    user = update.effective_user
    welcome_text = f"""
    🎉 Welcome {user.first_name}! 🎉

    📚 *Premium Test Series Generator Bot*

    I can create professional test series from your JSON data!

    🚀 *Available Commands:*
    /start - Show this welcome message
    /help - Get help information
    /generate - Generate test series from JSON file

    📤 Just send me a JSON file with test questions, and I'll create a beautiful HTML test series for you!
    """
    
    keyboard = [
        [InlineKeyboardButton("📤 Upload JSON File", callback_data="upload_json")],
        [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send help message when the command /help is issued."""
    help_text = """
    🤖 *How to Use This Bot:*

    1. 📤 *Upload JSON File*: Send me a JSON file containing your test questions
    2. 🎨 *Auto Generation*: I'll create a professional HTML test series
    3. 📄 *Download*: Get your beautiful test series HTML file

    📋 *JSON Format Required:*
    ```json
    {
        "data": [
            {
                "id": 1,
                "question": "Your question here?",
                "question_eng": "English version",
                "answer": "a",
                "options": {
                    "a": "Option A",
                    "b": "Option B",
                    ...
                },
                "options_eng": {
                    "a": "English Option A",
                    ...
                },
                "solution": "Detailed solution"
            }
        ]
    }
    ```

    🎯 *Features:*
    • Bilingual support (Hindi/English)
    • Professional UI/UX
    • Timer functionality
    • Score calculation
    • Responsive design
    • Solution explanations
    """
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming document (JSON file)."""
    user_id = update.effective_user.id
    document = update.message.document
    
    # Check if it's a JSON file
    if document.mime_type == 'application/json' or document.file_name.endswith('.json'):
        await update.message.reply_text("📥 Downloading your JSON file...")
        
        try:
            # Download the file
            file = await context.bot.get_file(document.file_id)
            file_path = f"temp_{user_id}.json"
            await file.download_to_drive(file_path)
            
            # Read and parse JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Validate JSON structure
            if 'data' in json_data and isinstance(json_data['data'], list):
                await update.message.reply_text("✅ JSON file validated! Generating your test series...")
                
                # Generate HTML test
                html_content = test_generator.generate_html_test(json_data, user_id)
                
                # Save HTML file
                output_file = f"test_series_{user_id}.html"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Send HTML file to user
                await update.message.reply_document(
                    document=open(output_file, 'rb'),
                    filename=f"Premium_Test_Series_{datetime.datetime.now().strftime('%Y%m%d')}.html",
                    caption="🎉 Your Premium Test Series is Ready!\n\nDownload and open in any browser to start your test! 🚀"
                )
                
                # Clean up temporary files
                os.remove(file_path)
                os.remove(output_file)
                
            else:
                await update.message.reply_text("❌ Invalid JSON format. Please check the structure and try again.")
                
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing file: {str(e)}")
            
    else:
        await update.message.reply_text("❌ Please send a valid JSON file.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button callbacks."""
    query = update.callback_query
    await query.answer()
    
    if query.data == "upload_json":
        await query.edit_message_text("📤 Please upload your JSON file containing test questions.")
    elif query.data == "help":
        help_text = """
        📋 *JSON Format Example:*
        ```json
        {
            "data": [
                {
                    "id": 1,
                    "question": "Sample question?",
                    "question_eng": "English question",
                    "answer": "a",
                    "options": {"a": "Option A", "b": "Option B"},
                    "options_eng": {"a": "Eng Option A", "b": "Eng Option B"},
                    "solution": "Explanation"
                }
            ]
        }
        ```
        """
        await query.edit_message_text(help_text, parse_mode='Markdown')

def main() -> None:
    """Start the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    TOKEN = "YOUR_BOT_TOKEN_HERE"
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Start the bot
    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()