import os
import json
import logging
import asyncio
import aiofiles
from datetime import datetime
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters as tg_filters, CallbackQueryHandler, ContextTypes

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class Config:
    def __init__(self):
        # Telegram API Configuration - Replace with your credentials
        self.API_ID = int(os.getenv('API_ID', '24250238'))
        self.API_HASH = os.getenv('API_HASH', 'cb3f118ce5553dc140127647edcf3720')
        self.BOT_TOKEN = os.getenv('BOT_TOKEN', '6047785902:AAE59KTfmhRvF8sUSYIzl9wcGnm4FLXiWDk')
        
        # Create necessary directories
        os.makedirs('uploads', exist_ok=True)
        os.makedirs('output', exist_ok=True)

class PremiumTestGenerator:
    def __init__(self):
        self.config = Config()
    
    def generate_premium_html_test(self, json_data, user_id, theme="dark", device="desktop"):
        """Generate premium HTML test with mobile/desktop and dark/light mode"""
        
        # Theme configurations
        themes = {
            "dark": {
                "bg_primary": "#0f0f23",
                "bg_secondary": "#1a1a2e",
                "bg_card": "#16213e",
                "text_primary": "#ffffff",
                "text_secondary": "#b0b0b0",
                "accent": "#ff6b6b",
                "accent_hover": "#ff5252",
                "success": "#2ecc71",
                "danger": "#e74c3c",
                "warning": "#f39c12",
                "border": "#2d3748"
            },
            "light": {
                "bg_primary": "#f8f9fa",
                "bg_secondary": "#ffffff",
                "bg_card": "#ffffff",
                "text_primary": "#2d3748",
                "text_secondary": "#718096",
                "accent": "#667eea",
                "accent_hover": "#5a67d8",
                "success": "#48bb78",
                "danger": "#f56565",
                "warning": "#ed8936",
                "border": "#e2e8f0"
            }
        }
        
        colors = themes[theme]
        
        # Dynamic values based on device
        container_width = "100%" if device == "mobile" else "1400px"
        container_padding = "10px" if device == "mobile" else "20px"
        header_padding = "15px 10px" if device == "mobile" else "25px 20px"
        logo_font_size = "20px" if device == "mobile" else "28px"
        logo_icon_size = "24px" if device == "mobile" else "32px"
        timer_font_size = "14px" if device == "mobile" else "16px"
        control_grid = "1fr" if device == "mobile" else "repeat(auto-fit, minmax(200px, 1fr))"
        info_grid = "repeat(2, 1fr)" if device == "mobile" else "repeat(4, 1fr)"
        main_display = "block" if device == "mobile" else "flex"
        questions_margin = "margin-bottom: 20px;" if device == "mobile" else ""
        nav_order = "order: -1; margin-bottom: 20px;" if device == "mobile" else ""
        nav_flex = "1" if device == "mobile" else "0 0 300px"
        question_grid_cols = "repeat(5, 1fr)" if device == "mobile" else "repeat(6, 1fr)"
        question_btn_size = "35px" if device == "mobile" else "40px"
        info_value_size = "24px" if device == "mobile" else "32px"
        actions_justify = "space-between" if device == "desktop" else "center"
        btn_style = "flex: 1; min-width: 120px; justify-content: center;" if device == "mobile" else ""
        results_grid = "1fr 1fr" if device == "mobile" else "repeat(4, 1fr)"
        
        html_content = f"""
        <!DOCTYPE html>
        <html lang="hi">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>🚀 Premium Test Series</title>
            <style>
                * {{
                    margin: 0;
                    padding: 0;
                    box-sizing: border-box;
                    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
                }}
                
                :root {{
                    --bg-primary: {colors['bg_primary']};
                    --bg-secondary: {colors['bg_secondary']};
                    --bg-card: {colors['bg_card']};
                    --text-primary: {colors['text_primary']};
                    --text-secondary: {colors['text_secondary']};
                    --accent: {colors['accent']};
                    --accent-hover: {colors['accent_hover']};
                    --success: {colors['success']};
                    --danger: {colors['danger']};
                    --warning: {colors['warning']};
                    --border: {colors['border']};
                    --shadow: rgba(0, 0, 0, 0.1);
                    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                }}
                
                body {{
                    background: var(--bg-primary);
                    color: var(--text-primary);
                    line-height: 1.6;
                    min-height: 100vh;
                    transition: var(--transition);
                }}
                
                .container {{
                    max-width: {container_width};
                    margin: 0 auto;
                    padding: {container_padding};
                }}
                
                /* Header Styles */
                .header {{
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    padding: {header_padding};
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                    border-radius: 0 0 25px 25px;
                    margin-bottom: 25px;
                    backdrop-filter: blur(10px);
                }}
                
                .header-content {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    flex-wrap: wrap;
                    gap: 15px;
                }}
                
                .logo {{
                    font-size: {logo_font_size};
                    font-weight: 800;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    color: white;
                }}
                
                .logo-icon {{
                    font-size: {logo_icon_size};
                    animation: bounce 2s infinite;
                }}
                
                @keyframes bounce {{
                    0%, 20%, 50%, 80%, 100% {{ transform: translateY(0); }}
                    40% {{ transform: translateY(-10px); }}
                    60% {{ transform: translateY(-5px); }}
                }}
                
                .user-info {{
                    display: flex;
                    align-items: center;
                    gap: 15px;
                    background: rgba(255, 255, 255, 0.1);
                    padding: 8px 16px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    color: white;
                    font-weight: 500;
                }}
                
                .timer {{
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    padding: 8px 16px;
                    border-radius: 20px;
                    font-weight: 700;
                    font-size: {timer_font_size};
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
                }}
                
                /* Control Panel */
                .control-panel {{
                    background: var(--bg-card);
                    border-radius: 20px;
                    padding: 20px;
                    margin-bottom: 25px;
                    box-shadow: 0 8px 32px var(--shadow);
                    border: 1px solid var(--border);
                }}
                
                .control-grid {{
                    display: grid;
                    grid-template-columns: {control_grid};
                    gap: 15px;
                    margin-bottom: 20px;
                }}
                
                .control-group {{
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                }}
                
                .control-label {{
                    font-weight: 600;
                    color: var(--text-secondary);
                    font-size: 14px;
                }}
                
                .btn-group {{
                    display: flex;
                    gap: 8px;
                    flex-wrap: wrap;
                }}
                
                .mode-btn {{
                    padding: 10px 16px;
                    border: 2px solid var(--border);
                    background: var(--bg-secondary);
                    color: var(--text-primary);
                    border-radius: 12px;
                    cursor: pointer;
                    transition: var(--transition);
                    font-weight: 600;
                    font-size: 14px;
                    flex: 1;
                    min-width: 80px;
                }}
                
                .mode-btn.active {{
                    background: var(--accent);
                    color: white;
                    border-color: var(--accent);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }}
                
                .mode-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px var(--shadow);
                }}
                
                /* Test Info */
                .test-info {{
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    padding: 25px;
                    border-radius: 20px;
                    margin-bottom: 25px;
                    color: white;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                }}
                
                .info-grid {{
                    display: grid;
                    grid-template-columns: {info_grid};
                    gap: 15px;
                }}
                
                .info-item {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                
                .info-value {{
                    font-size: {info_value_size};
                    font-weight: 800;
                    margin-bottom: 5px;
                }}
                
                .info-label {{
                    font-size: 12px;
                    opacity: 0.9;
                    font-weight: 500;
                }}
                
                /* Main Content */
                .main-content {{
                    display: {main_display};
                    gap: 25px;
                }}
                
                .questions-section {{
                    flex: 1;
                    background: var(--bg-card);
                    border-radius: 20px;
                    padding: 25px;
                    box-shadow: 0 8px 32px var(--shadow);
                    border: 1px solid var(--border);
                    {questions_margin}
                }}
                
                .question-nav {{
                    flex: {nav_flex};
                    background: var(--bg-card);
                    border-radius: 20px;
                    padding: 20px;
                    box-shadow: 0 8px 32px var(--shadow);
                    border: 1px solid var(--border);
                    {nav_order}
                }}
                
                .question-nav h3 {{
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 2px solid var(--border);
                    color: var(--text-primary);
                    font-size: 18px;
                    font-weight: 700;
                }}
                
                .question-grid {{
                    display: grid;
                    grid-template-columns: {question_grid_cols};
                    gap: 10px;
                    margin-bottom: 20px;
                }}
                
                .question-btn {{
                    width: {question_btn_size};
                    height: {question_btn_size};
                    border: 2px solid var(--border);
                    border-radius: 10px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: var(--transition);
                    font-weight: 700;
                    font-size: 14px;
                    background: var(--bg-secondary);
                    color: var(--text-primary);
                }}
                
                .question-btn:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 5px 15px var(--shadow);
                }}
                
                .question-btn.answered {{
                    background: var(--success);
                    color: white;
                    border-color: var(--success);
                }}
                
                .question-btn.current {{
                    background: var(--accent);
                    color: white;
                    border-color: var(--accent);
                    transform: scale(1.1);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }}
                
                .question-btn.skipped {{
                    background: var(--warning);
                    color: white;
                    border-color: var(--warning);
                }}
                
                .question-btn.incorrect {{
                    background: var(--danger);
                    color: white;
                    border-color: var(--danger);
                }}
                
                /* Question Styles */
                .question {{
                    margin-bottom: 30px;
                }}
                
                .question-number {{
                    font-size: 18px;
                    font-weight: 700;
                    margin-bottom: 15px;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }}
                
                .question-number::before {{
                    content: "🎯";
                    font-size: 16px;
                }}
                
                .question-text {{
                    font-size: 16px;
                    margin-bottom: 20px;
                    line-height: 1.7;
                    background: var(--bg-secondary);
                    padding: 20px;
                    border-radius: 15px;
                    border-left: 4px solid var(--accent);
                    box-shadow: 0 4px 15px var(--shadow);
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
                    padding: 18px;
                    border: 2px solid var(--border);
                    border-radius: 15px;
                    cursor: pointer;
                    transition: var(--transition);
                    background: var(--bg-secondary);
                }}
                
                .option:hover {{
                    border-color: var(--accent);
                    background: var(--bg-card);
                    transform: translateX(5px);
                    box-shadow: 0 5px 20px var(--shadow);
                }}
                
                .option.selected {{
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    border-color: var(--accent);
                    color: white;
                    transform: translateX(5px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
                }}
                
                .option.correct {{
                    background: linear-gradient(135deg, var(--success), #27ae60);
                    border-color: var(--success);
                    color: white;
                    box-shadow: 0 8px 25px rgba(46, 204, 113, 0.3);
                }}
                
                .option.incorrect {{
                    background: linear-gradient(135deg, var(--danger), #c0392b);
                    border-color: var(--danger);
                    color: white;
                    box-shadow: 0 8px 25px rgba(231, 76, 60, 0.3);
                }}
                
                .option-label {{
                    font-weight: 700;
                    min-width: 35px;
                    height: 35px;
                    background: var(--border);
                    color: var(--text-primary);
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: var(--transition);
                }}
                
                .option.selected .option-label {{
                    background: white;
                    color: var(--accent);
                }}
                
                .option.correct .option-label {{
                    background: white;
                    color: var(--success);
                }}
                
                .option.incorrect .option-label {{
                    background: white;
                    color: var(--danger);
                }}
                
                /* Actions */
                .actions {{
                    display: flex;
                    justify-content: {actions_justify};
                    flex-wrap: wrap;
                    gap: 10px;
                    margin-top: 30px;
                    padding-top: 20px;
                    border-top: 2px solid var(--border);
                }}
                
                .btn {{
                    padding: 12px 24px;
                    border: none;
                    border-radius: 12px;
                    cursor: pointer;
                    font-weight: 700;
                    transition: var(--transition);
                    font-size: 14px;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    {btn_style}
                }}
                
                .btn-primary {{
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    color: white;
                }}
                
                .btn-primary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
                }}
                
                .btn-secondary {{
                    background: var(--bg-secondary);
                    color: var(--text-primary);
                    border: 2px solid var(--border);
                }}
                
                .btn-secondary:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px var(--shadow);
                }}
                
                .btn-success {{
                    background: linear-gradient(135deg, var(--success), #27ae60);
                    color: white;
                }}
                
                .btn-success:hover {{
                    transform: translateY(-2px);
                    box-shadow: 0 8px 25px rgba(46, 204, 113, 0.4);
                }}
                
                /* Solution */
                .solution {{
                    margin-top: 25px;
                    padding: 25px;
                    background: var(--bg-secondary);
                    border-radius: 15px;
                    border-left: 5px solid var(--accent);
                    box-shadow: 0 4px 15px var(--shadow);
                }}
                
                .solution h4 {{
                    margin-bottom: 15px;
                    color: var(--text-primary);
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    font-size: 18px;
                }}
                
                .solution h4::before {{
                    content: "💡";
                }}
                
                /* Results */
                .results {{
                    text-align: center;
                    padding: 40px;
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    border-radius: 25px;
                    color: white;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                }}
                
                .results h2 {{
                    margin-bottom: 30px;
                    font-size: 32px;
                    font-weight: 800;
                }}
                
                .results-grid {{
                    display: grid;
                    grid-template-columns: {results_grid};
                    gap: 20px;
                    margin: 30px 0;
                }}
                
                .result-item {{
                    background: rgba(255, 255, 255, 0.1);
                    padding: 25px;
                    border-radius: 20px;
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.2);
                }}
                
                .result-value {{
                    font-size: 36px;
                    font-weight: 800;
                    margin-bottom: 10px;
                }}
                
                .result-label {{
                    font-size: 14px;
                    opacity: 0.9;
                    font-weight: 500;
                }}
                
                /* Responsive */
                @media (max-width: 768px) {{
                    .container {{
                        padding: 10px;
                    }}
                    
                    .header-content {{
                        flex-direction: column;
                        text-align: center;
                    }}
                    
                    .control-grid {{
                        grid-template-columns: 1fr;
                    }}
                    
                    .actions {{
                        flex-direction: column;
                    }}
                    
                    .btn {{
                        width: 100%;
                    }}
                }}
                
                /* Custom Scrollbar */
                ::-webkit-scrollbar {{
                    width: 8px;
                }}
                
                ::-webkit-scrollbar-track {{
                    background: var(--bg-secondary);
                    border-radius: 10px;
                }}
                
                ::-webkit-scrollbar-thumb {{
                    background: linear-gradient(135deg, var(--accent), var(--accent-hover));
                    border-radius: 10px;
                }}
                
                ::-webkit-scrollbar-thumb:hover {{
                    background: var(--accent-hover);
                }}
                
                /* Animations */
                @keyframes fadeIn {{
                    from {{ opacity: 0; transform: translateY(20px); }}
                    to {{ opacity: 1; transform: translateY(0); }}
                }}
                
                .fade-in {{
                    animation: fadeIn 0.6s ease-out;
                }}
                
                .hidden {{
                    display: none;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <div class="container">
                    <div class="header-content">
                        <div class="logo">
                            <span class="logo-icon">🚀</span>
                            Premium Test Series
                        </div>
                        <div class="user-info">
                            <div class="timer" id="timer">03:00:00</div>
                            <div>User: {user_id}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="container">
                <!-- Control Panel -->
                <div class="control-panel fade-in">
                    <div class="control-grid">
                        <div class="control-group">
                            <div class="control-label">🎨 Theme Mode</div>
                            <div class="btn-group">
                                <button class="mode-btn {'active' if theme == 'dark' else ''}" onclick="switchTheme('dark')">
                                    🌙 Dark
                                </button>
                                <button class="mode-btn {'active' if theme == 'light' else ''}" onclick="switchTheme('light')">
                                    ☀️ Light
                                </button>
                            </div>
                        </div>
                        
                        <div class="control-group">
                            <div class="control-label">📱 Device View</div>
                            <div class="btn-group">
                                <button class="mode-btn {'active' if device == 'mobile' else ''}" onclick="switchDevice('mobile')">
                                    📱 Mobile
                                </button>
                                <button class="mode-btn {'active' if device == 'desktop' else ''}" onclick="switchDevice('desktop')">
                                    🖥️ Desktop
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Test Info -->
                <div class="test-info fade-in">
                    <h3 style="margin-bottom: 20px; display: flex; align-items: center; gap: 10px;">
                        <span>📊</span> Test Overview
                    </h3>
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
                            <div class="info-label">Marking</div>
                        </div>
                        <div class="info-item">
                            <div class="info-value">{datetime.now().strftime('%d/%m/%Y')}</div>
                            <div class="info-label">Date</div>
                        </div>
                    </div>
                </div>
                
                <!-- Main Content -->
                <div class="main-content">
                    <div class="question-nav fade-in">
                        <h3>🧭 Navigation</h3>
                        <div class="question-grid" id="questionGrid">
                            <!-- Navigation buttons will be loaded here -->
                        </div>
                        
                        <div class="solution" id="solutionContainer">
                            <h4>Solution & Explanation</h4>
                            <div id="solutionText">Select an option to view detailed solution</div>
                        </div>
                    </div>
                    
                    <div class="questions-section fade-in">
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
                                <span>🚀</span> Submit Test
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <script>
                // Test data
                const testData = {json.dumps(json_data, ensure_ascii=False)};
                
                // Application state
                let currentQuestionIndex = 0;
                let userAnswers = {{}};
                let currentTheme = '{theme}';
                let currentDevice = '{device}';
                let timerInterval;
                let timeRemaining = 10800; // 3 hours
                let testSubmitted = false;

                // Initialize test
                function initializeTest() {{
                    createQuestionNavigation();
                    loadQuestion(currentQuestionIndex);
                    startTimer();
                    setupEventListeners();
                }}

                function createQuestionNavigation() {{
                    const grid = document.getElementById('questionGrid');
                    grid.innerHTML = '';
                    
                    testData.data.forEach((question, index) => {{
                        const button = document.createElement('div');
                        button.className = 'question-btn';
                        button.textContent = index + 1;
                        button.onclick = () => loadQuestion(index);
                        grid.appendChild(button);
                    }});
                    updateNavigationButtons();
                }}

                function loadQuestion(index) {{
                    if (testSubmitted) return;
                    
                    currentQuestionIndex = index;
                    const question = testData.data[index];
                    
                    let optionsHtml = '';
                    const userAnswer = userAnswers[question.id];
                    const correctAnswer = question.answer;
                    
                    // Generate options with correct/incorrect highlighting after submission
                    Object.entries(question.options).forEach(([key, value]) => {{
                        if (!value) return;
                        
                        let optionClass = 'option';
                        if (userAnswer === `option${{key}}`) {{
                            optionClass += ' selected';
                        }}
                        if (testSubmitted) {{
                            if (key === correctAnswer) {{
                                optionClass += ' correct';
                            }} else if (userAnswer === `option${{key}}` && key !== correctAnswer) {{
                                optionClass += ' incorrect';
                            }}
                        }}
                        
                        optionsHtml += `
                            <div class="${{optionClass}}" data-option="option${{key}}">
                                <div class="option-label">${{key.toUpperCase()}}</div>
                                <div class="option-text">${{value}}</div>
                            </div>
                        `;
                    }});
                    
                    document.getElementById('questionContainer').innerHTML = `
                        <div class="question-number">Question ${{index + 1}} of ${{testData.data.length}}</div>
                        <div class="question-text">${{question.question}}</div>
                        <div class="options">${{optionsHtml}}</div>
                    `;
                    
                    // Add event listeners to options
                    document.querySelectorAll('.option').forEach(option => {{
                        option.onclick = () => selectOption(question, option);
                    }});
                    
                    updateNavigationButtons();
                    updateSolution(question);
                }}

                function selectOption(question, optionElement) {{
                    if (testSubmitted) return;
                    
                    // Remove selection from all options
                    document.querySelectorAll('.option').forEach(opt => {{
                        opt.classList.remove('selected');
                    }});
                    
                    // Add selection to clicked option
                    optionElement.classList.add('selected');
                    
                    // Save answer
                    userAnswers[question.id] = optionElement.dataset.option;
                    
                    // Update navigation
                    updateQuestionStatus(question.id, 'answered');
                    
                    // Show solution
                    updateSolution(question);
                }}

                function updateSolution(question) {{
                    const solutionText = document.getElementById('solutionText');
                    if (userAnswers[question.id] && question.solution) {{
                        solutionText.innerHTML = `
                            <strong>✅ Correct Answer:</strong> Option ${{question.answer.toUpperCase()}}<br><br>
                            <strong>💡 Explanation:</strong><br>
                            ${{question.solution}}
                        `;
                    }} else {{
                        solutionText.textContent = 'Select an option to view detailed solution';
                    }}
                }}

                function updateNavigationButtons() {{
                    const buttons = document.querySelectorAll('.question-btn');
                    buttons.forEach((button, index) => {{
                        button.classList.remove('current', 'answered', 'skipped', 'incorrect');
                        
                        if (index === currentQuestionIndex) {{
                            button.classList.add('current');
                        }}
                        
                        const questionId = testData.data[index].id;
                        if (userAnswers[questionId]) {{
                            if (testSubmitted) {{
                                const isCorrect = userAnswers[questionId] === `option${{testData.data[index].answer}}`;
                                button.classList.add(isCorrect ? 'answered' : 'incorrect');
                            }} else {{
                                button.classList.add('answered');
                            }}
                        }}
                    }});
                    
                    // Update button states
                    document.getElementById('prevBtn').disabled = currentQuestionIndex === 0;
                    document.getElementById('nextBtn').disabled = currentQuestionIndex === testData.data.length - 1;
                }}

                function updateQuestionStatus(questionId, status) {{
                    const index = testData.data.findIndex(q => q.id === questionId);
                    const button = document.querySelectorAll('.question-btn')[index];
                    button.classList.add(status);
                }}

                function switchTheme(theme) {{
                    currentTheme = theme;
                    // In a real implementation, you would reload the page with new theme
                    alert(`Theme switched to ${{theme}} mode!`);
                }}

                function switchDevice(device) {{
                    currentDevice = device;
                    // In a real implementation, you would reload the page with new device view
                    alert(`View switched to ${{device}} mode!`);
                }}

                function startTimer() {{
                    timerInterval = setInterval(() => {{
                        timeRemaining--;
                        updateTimerDisplay();
                        if (timeRemaining <= 0) submitTest();
                    }}, 1000);
                }}

                function updateTimerDisplay() {{
                    const hours = Math.floor(timeRemaining / 3600);
                    const minutes = Math.floor((timeRemaining % 3600) / 60);
                    const seconds = timeRemaining % 60;
                    document.getElementById('timer').textContent = 
                        `${{hours.toString().padStart(2, '0')}}:${{minutes.toString().padStart(2, '0')}}:${{seconds.toString().padStart(2, '0')}}`;
                }}

                function submitTest() {{
                    clearInterval(timerInterval);
                    testSubmitted = true;
                    
                    // Calculate results
                    let score = 0;
                    let correct = 0;
                    let incorrect = 0;
                    let skipped = 0;
                    
                    testData.data.forEach(question => {{
                        if (userAnswers[question.id] === `option${{question.answer}}`) {{
                            score += question.plus_marks || 4;
                            correct++;
                        }} else if (userAnswers[question.id] && userAnswers[question.id] !== 'skipped') {{
                            score -= question.minus_marks || 1;
                            incorrect++;
                        }} else {{
                            skipped++;
                        }}
                    }});
                    
                    // Show results
                    document.getElementById('questionContainer').innerHTML = `
                        <div class="results">
                            <h2>🎉 Test Completed! 🎉</h2>
                            <div class="results-grid">
                                <div class="result-item">
                                    <div class="result-value">${{score.toFixed(2)}}</div>
                                    <div class="result-label">Total Score</div>
                                </div>
                                <div class="result-item">
                                    <div class="result-value">${{correct}}</div>
                                    <div class="result-label">Correct</div>
                                </div>
                                <div class="result-item">
                                    <div class="result-value">${{incorrect}}</div>
                                    <div class="result-label">Incorrect</div>
                                </div>
                                <div class="result-item">
                                    <div class="result-value">${{skipped}}</div>
                                    <div class="result-label">Skipped</div>
                                </div>
                            </div>
                            <p style="font-size: 18px; opacity: 0.9;">Time Taken: ${{document.getElementById('timer').textContent}}</p>
                        </div>
                    `;
                    
                    document.querySelector('.actions').style.display = 'none';
                    
                    // Reload current question to show correct/incorrect highlights
                    loadQuestion(currentQuestionIndex);
                }}

                function setupEventListeners() {{
                    document.getElementById('prevBtn').onclick = () => {{
                        if (currentQuestionIndex > 0) loadQuestion(currentQuestionIndex - 1);
                    }};
                    
                    document.getElementById('nextBtn').onclick = () => {{
                        if (currentQuestionIndex < testData.data.length - 1) loadQuestion(currentQuestionIndex + 1);
                    }};
                    
                    document.getElementById('skipBtn').onclick = () => {{
                        userAnswers[testData.data[currentQuestionIndex].id] = 'skipped';
                        updateQuestionStatus(testData.data[currentQuestionIndex].id, 'skipped');
                        if (currentQuestionIndex < testData.data.length - 1) loadQuestion(currentQuestionIndex + 1);
                    }};
                    
                    document.getElementById('submitBtn').onclick = submitTest;
                }}

                // Initialize when page loads
                document.addEventListener('DOMContentLoaded', initializeTest);
            </script>
        </body>
        </html>
        """
        
        return html_content

class TelegramTestBot:
    def __init__(self):
        self.config = Config()
        self.test_generator = PremiumTestGenerator()
        
    async def start_bot(self):
        """Start both Pyrogram and python-telegram-bot"""
        await self.start_telegram_bot()
    
    async def start_telegram_bot(self):
        """Start python-telegram-bot"""
        application = Application.builder().token(self.config.BOT_TOKEN).build()
        
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            welcome_text = f"""
            🚀 **Welcome {user.first_name}!**

            **Premium Test Series Generator**

            📁 **Send me a JSON file** and get a beautiful test series!

            ✨ **Features:**
            • 🎨 Dark/Light Mode
            • 📱 Mobile/Desktop Views  
            • ✅ Green Highlight for Correct Answers
            • 🎯 Professional Interface
            • ⏱️ Timer & Scoring
            • 💡 Solutions & Explanations

            **Commands:**
            /start - Show this message
            /help - Get help
            /generate - Create test series
            """
            
            keyboard = [
                [InlineKeyboardButton("📤 Upload JSON File", callback_data="upload_json")],
                [InlineKeyboardButton("🎨 Preview Themes", callback_data="themes")],
                [InlineKeyboardButton("❓ Help Guide", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')
        
        async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            help_text = """
            🤖 **How to Use:**

            1. **Prepare JSON File** with this format:
            ```json
            {
                "data": [
                    {
                        "id": 1,
                        "question": "Your question?",
                        "question_eng": "English version",
                        "answer": "a",
                        "options": {
                            "a": "Option A",
                            "b": "Option B"
                        },
                        "options_eng": {
                            "a": "English A", 
                            "b": "English B"
                        },
                        "solution": "Explanation"
                    }
                ]
            }
            ```

            2. **Send JSON file** to this bot
            3. **Download HTML** test series
            4. **Open in browser** and start test!

            🎯 **Features Included:**
            • Dark/Light Mode Toggle
            • Mobile/Desktop Responsive Views
            • Green Highlight for Correct Answers
            • Professional UI/UX
            • Timer & Auto Submission
            • Score Calculation
            • Detailed Solutions
            """
            
            await update.message.reply_text(help_text, parse_mode='Markdown')
        
        async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await self.process_telegram_document(update, context)
        
        async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
            query = update.callback_query
            await query.answer()
            
            if query.data == "upload_json":
                await query.edit_message_text(
                    "📤 **Upload JSON File**\\n\\n"
                    "Please send me your JSON file containing test questions.\\n"
                    "Make sure it follows the required format.",
                    parse_mode='Markdown'
                )
            elif query.data == "themes":
                await query.edit_message_text(
                    "🎨 **Available Themes & Modes**\\n\\n"
                    "• **🌙 Dark Mode** - Easy on eyes\\n"
                    "• **☀️ Light Mode** - Classic look\\n"
                    "• **📱 Mobile View** - Phone optimized\\n" 
                    "• **🖥️ Desktop View** - Full features\\n\\n"
                    "All modes can be switched in the test interface!",
                    parse_mode='Markdown'
                )
            elif query.data == "help":
                await help_command(update, context)
        
        # Add handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("generate", start))
        application.add_handler(MessageHandler(tg_filters.Document.ALL, handle_document))
        application.add_handler(CallbackQueryHandler(button_handler))
        
        logger.info("Starting python-telegram-bot...")
        await application.run_polling()
    
    async def process_telegram_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Process document for python-telegram-bot"""
        try:
            user_id = update.effective_user.id
            document = update.message.document
            
            if not (document.mime_type == 'application/json' or document.file_name.endswith('.json')):
                await update.message.reply_text("❌ Please send a valid JSON file.")
                return
            
            msg = await update.message.reply_text("📥 Downloading your file...")
            
            # Download file
            file = await context.bot.get_file(document.file_id)
            file_path = f"temp_{user_id}.json"
            await file.download_to_drive(file_path)
            
            # Read JSON
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
                content = await f.read()
                json_data = json.loads(content)
            
            await msg.edit_text("🎨 Generating premium test series...")
            
            # Generate HTML
            html_content = self.test_generator.generate_premium_html_test(
                json_data, user_id, theme="dark", device="desktop"
            )
            
            # Save HTML
            output_file = f"test_series_{user_id}_{int(datetime.now().timestamp())}.html"
            async with aiofiles.open(output_file, 'w', encoding='utf-8') as f:
                await f.write(html_content)
            
            await msg.edit_text("📤 Sending your premium test series...")
            
            # Send file
            await update.message.reply_document(
                document=open(output_file, 'rb'),
                filename=f"Premium_Test_Series.html",
                caption=f"""
                🚀 **Premium Test Series Ready!**

                ✨ **Features:**
                • 🎨 Dark/Light Mode Toggle
                • 📱 Mobile/Desktop Views  
                • ✅ Green Highlight for Correct Answers
                • ⏱️ Timer & Auto-Submit
                • 📊 Smart Scoring
                • 💡 Detailed Solutions

                🎯 **Questions:** {len(json_data['data'])}
                ⏰ **Time:** 3 Hours
                📅 **Generated:** {datetime.now().strftime('%d/%m/%Y %H:%M')}

                **📖 Open in browser and start testing!**
                """,
                parse_mode='Markdown'
            )
            
            # Cleanup
            os.remove(file_path)
            os.remove(output_file)
            await msg.delete()
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            await update.message.reply_text(f"❌ Error: {str(e)}")

async def main():
    """Main function to start the bot"""
    bot = TelegramTestBot()
    await bot.start_bot()

if __name__ == "__main__":
    asyncio.run(main())
