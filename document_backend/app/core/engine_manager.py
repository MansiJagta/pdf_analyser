import os
import subprocess
import socket
import time
import logging

logger = logging.getLogger("uvicorn")

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("localhost", port)) == 0

def start_ollama_engine():
    """
    Locates the local Ollama binary in /engine and starts it in the background
    if port 11434 is not already taken.
    """
    # 1. Check if Ollama is already running
    if is_port_in_use(11434):
        logger.info("✅ Ollama is already running on port 11434.")
        return

    # 2. Locate the binary
    # Assumes 'engine' folder is in the project root (one level up from app/core if run from root)
    # Adjust path logic based on CWD being 'document_backend'
    base_dir = os.getcwd() # Should be document_backend
    engine_dir = os.path.join(base_dir, "engine")
    ollama_exe = os.path.join(engine_dir, "ollama.exe")
    models_dir = os.path.join(engine_dir, "models")

    if not os.path.exists(ollama_exe):
        logger.warning(f"⚠️  Ollama binary not found at {ollama_exe}. Assuming global install or manual start.")
        return

    # 3. Configure Environment
    # Ensure absolute paths
    models_dir = os.path.abspath(models_dir)
    env = os.environ.copy()
    env["OLLAMA_MODELS"] = models_dir
    # env["OLLAMA_HOST"] = "127.0.0.1:11434"

    logger.info(f"🚀 Starting Silent Ollama Engine from {ollama_exe}...")
    logger.info(f"📂 Model Path: {models_dir}")

    # 4. Start Process (Silent Mode)
    try:
        subprocess.Popen(
            [ollama_exe, "serve"],
            cwd=engine_dir,
            env=env,
            creationflags=0x08000000,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        # Give it a moment to bind the port
        time.sleep(5) # Increased wait time for safety
        
        if is_port_in_use(11434):
             logger.info("✅ Silent Ollama started successfully.")
             
             # 5. Verify Model Availability
             logger.info("🔍 Verifying 'llama3.2' model availability...")
             try:
                 # List models
                 result = subprocess.run(
                     [ollama_exe, "list"],
                     env=env,
                     capture_output=True,
                     text=True,
                     creationflags=0x08000000
                 )
                 
                 if "llama3.2" in result.stdout:
                     logger.info("✅ Model 'llama3.2' found in local registry.")
                 else:
                     logger.warning("⚠️  Model 'llama3.2' not found. Attempting to pull from local/remote...")
                     # Attempt pull (will use local models dir if correctly populated or fetch if online)
                     pull_process = subprocess.Popen(
                         [ollama_exe, "pull", "llama3.2"],
                         env=env,
                         creationflags=0x08000000,
                         stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL
                     )
                     pull_process.wait()
                     logger.info("✅ Model 'llama3.2' pull command completed.")
                     
             except Exception as e:
                 logger.error(f"❌ Model verification failed: {e}")

        else:
             logger.warning("⚠️  Ollama process started but port 11434 is not yet active.")
             
    except Exception as e:
        logger.error(f"❌ Failed to start Ollama silent engine: {e}")
