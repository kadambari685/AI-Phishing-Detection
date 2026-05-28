import asyncio
import os
import json
import textwrap
from openai import OpenAI
from env import env_instance # Importing from your env.py
from models import PhishAction

# Env Config
API_KEY = os.getenv("HF_TOKEN") or os.getenv("API_KEY")
API_BASE_URL = os.getenv("API_BASE_URL") or "https://router.huggingface.co/v1"
MODEL_NAME = os.getenv("MODEL_NAME") or "Qwen/Qwen2.5-72B-Instruct"

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)
SYSTEM_PROMPT = "You are a SOC Analyst. Analyze email. Respond ONLY with JSON: {\"action\": \"MARK_SAFE|MOVE_TO_SPAM|QUARANTINE|BLOCK_DOMAIN\", \"reasoning\": \"...\"}"

async def main():
    rewards = []
    steps = 0
    success = False
    
    print(f"[START] task=phishing_triage env=phishguard_v1 model={MODEL_NAME}", flush=True)

    try:
        obs = env_instance.reset()
        done = False
        
        while not done and steps < 30:
            steps += 1
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": str(obs)}],
                response_format={"type": "json_object"}
            )
            
            res = json.loads(completion.choices[0].message.content)
            action_str = res.get("action", "MARK_SAFE")
            
            obs, reward, done, info = env_instance.step(action_str)
            rewards.append(reward)
            
            print(f"[STEP] step={steps} action={action_str} reward={reward:.2f} done={str(done).lower()} error=null", flush=True)
            if done: break
            
        score = sum(rewards) / 10.0
        success = score >= 0.7

    finally:
        rewards_str = ",".join(f"{r:.2f}" for r in rewards)
        print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)

if __name__ == "__main__":
    asyncio.run(main())