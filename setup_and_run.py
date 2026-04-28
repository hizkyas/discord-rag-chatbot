import subprocess
import sys
import os
from loguru import logger

def install_dependencies():
    logger.info("Installing dependencies from requirements.txt...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def check_env():
    if not os.path.exists(".env"):
        logger.warning(".env file not found!")
        if os.path.exists(".env.example"):
            logger.info("Creating .env from .env.example. Please populate it with your keys.")
            with open(".env.example", "r") as f_ex, open(".env", "w") as f_env:
                f_env.write(f_ex.read())
        return False
    return True

def run_backend():
    logger.info("Starting FastAPI backend...")
    return subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app.main:app", "--reload"])

def run_bot():
    logger.info("Starting Discord bot...")
    return subprocess.Popen([sys.executable, "bot/bot.py"])

if __name__ == "__main__":
    install_dependencies()
    if not check_env():
        logger.error("Please configure your .env file and restart.")
        sys.exit(1)
        
    logger.info("System initialized. Starting services...")
    # These would normally run in separate terminals or in the background
    # For now, we just inform the user.
    print("""
    Setup complete! To run the system, you should open two terminals:
    
    Terminal 1 (Backend):
    python -m uvicorn backend.app.main:app --reload
    
    Terminal 2 (Bot):
    python bot/bot.py
    
    Make sure your .env file is fully populated!
    """)
