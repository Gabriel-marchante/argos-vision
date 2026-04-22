import argparse
import sys
import threading
import uvicorn
from src.core.engine import ArgosEngine
from src.api.server import app
from dotenv import load_dotenv

def start_api():
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="warning")

def main():
    parser = argparse.ArgumentParser(description="ARGOS - Automated Recognition & Gathering Observation System")
    parser.add_argument("--provider", type=str, default="openai", choices=["openai", "anthropic"], 
                        help="AI provider for profiling (default: openai)")
    parser.add_argument("--no-ui", action="store_true", help="Disable the web dashboard")
    
    args = parser.parse_args()
    
    load_dotenv()
    
    print("--- ARGOS: El vigilante de los cien ojos ---")
    print(f"Initializing with {args.provider} provider...")
    
    try:
        engine = ArgosEngine(ai_provider=args.provider)
        
        # Start API in a separate thread
        if not args.no_ui:
            print("Starting Web Dashboard at http://localhost:8000")
            api_thread = threading.Thread(target=start_api, daemon=True)
            api_thread.start()

        engine.start()
        
        print("ARGOS is running. Press 'q' in the video window to stop.")
        
        # Keep main thread alive
        while engine.running:
            try:
                import time
                time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping ARGOS...")
                engine.stop()
                break
                
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
