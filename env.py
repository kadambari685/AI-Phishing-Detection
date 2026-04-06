import openenv
from fastapi import FastAPI
from pydantic import BaseModel
from models import EmailObservation, PhishAction

# --- FAIL-SAFE IMPORT LOGIC ---
try:
    # Try importing the base class if it exists
    from openenv import OpenEnv
except ImportError:
    try:
        from openenv.core import OpenEnv
    except ImportError:
        # Fallback to object if library structure is different
        OpenEnv = object 

app = FastAPI()

class PhishGuardEnv(OpenEnv):
    def __init__(self):
        # 10 Levels: From basic spam to advanced BEC/Supply Chain attacks
        self.tasks = [
            {"id": "lv1", "data": {"sender": "win@lotto.net", "subject": "Claim $1M", "body": "Click now!", "links": ["http://bit.ly/123"], "has_attachments": False, "spf_record": "fail", "dmarc_record": "none", "urgency_level": "high"}, "correct_action": "MOVE_TO_SPAM"},
            {"id": "lv2", "data": {"sender": "support@googIe.com", "subject": "Security Alert", "body": "Verify account.", "links": ["http://googIe-verify.com"], "has_attachments": False, "spf_record": "pass", "dmarc_record": "pass", "urgency_level": "critical"}, "correct_action": "BLOCK_DOMAIN"},
            {"id": "lv3", "data": {"sender": "billing@office-supplies.co", "subject": "Invoice #88", "body": "Payment overdue.", "links": [], "has_attachments": True, "spf_record": "pass", "dmarc_record": "pass", "urgency_level": "medium"}, "correct_action": "QUARANTINE"},
            {"id": "lv4", "data": {"sender": "it@internal-help.com", "subject": "Update Patch", "body": "Run this file.", "links": ["http://internal-help.com/fix.exe"], "has_attachments": False, "spf_record": "softfail", "dmarc_record": "none", "urgency_level": "high"}, "correct_action": "BLOCK_DOMAIN"},
            {"id": "lv5", "data": {"sender": "hr@yourcompany.com", "subject": "Holiday List", "body": "Check portal.", "links": ["https://portal.yourcompany.com"], "has_attachments": False, "spf_record": "pass", "dmarc_record": "pass", "urgency_level": "low"}, "correct_action": "MARK_SAFE"},
            {"id": "lv6", "data": {"sender": "ceo@executive-mail.com", "subject": "Urgent Request", "body": "Wire $5000.", "links": [], "has_attachments": False, "spf_record": "softfail", "dmarc_record": "fail", "urgency_level": "high"}, "correct_action": "QUARANTINE"},
            {"id": "lv7", "data": {"sender": "notify@docs-share.net", "subject": "New File", "body": "View here.", "links": ["https://docs-verify.net/s/1"], "has_attachments": False, "spf_record": "pass", "dmarc_record": "none", "urgency_level": "medium"}, "correct_action": "BLOCK_DOMAIN"},
            {"id": "lv8", "data": {"sender": "payroll@hr-dept.net", "subject": "Update Bank", "body": "Form attached.", "links": [], "has_attachments": True, "spf_record": "fail", "dmarc_record": "none", "urgency_level": "critical"}, "correct_action": "QUARANTINE"},
            {"id": "lv9", "data": {"sender": "mfa@office365-auth.com", "subject": "MFA Update", "body": "Scan QR Code.", "links": [], "has_attachments": True, "spf_record": "pass", "dmarc_record": "pass", "urgency_level": "critical"}, "correct_action": "QUARANTINE"},
            {"id": "lv10", "data": {"sender": "partner@trusted-firm.com", "subject": "Project Specs", "body": "Check file.", "links": ["https://trusted-partner.com/files"], "has_attachments": False, "spf_record": "pass", "dmarc_record": "pass", "urgency_level": "medium"}, "correct_action": "BLOCK_DOMAIN"}
        ]
        self.current_task_idx = 0

    def reset(self):
        self.current_task_idx = 0
        return self.tasks[self.current_task_idx]["data"]

    def step(self, action_str: str):
        if self.current_task_idx >= len(self.tasks):
            return None, 0.0, True, {"info": "Finished"}
        
        current_task = self.tasks[self.current_task_idx]
        
        # Import grader inside function to avoid circular import issues
        try:
            from grader import grade_phishing_task
            reward = grade_phishing_task(action_str, current_task["correct_action"])
        except ImportError:
            # Fallback if grader is missing
            reward = 1.0 if action_str.upper() == current_task["correct_action"] else 0.0

        is_correct = (reward == 1.0) 
        
        if is_correct:
            self.current_task_idx += 1
            feedback = "Correct Decision."
        else:
            # Hardcore restart on any non-optimal action
            self.current_task_idx = 0 
            feedback = f"Action: {action_str} was not optimal. Resetting to Level 1."

        done = self.current_task_idx >= len(self.tasks)
        obs = self.tasks[self.current_task_idx]["data"] if not done else None
        
        return obs, reward, done, {
            "task_id": current_task["id"], 
            "is_correct": is_correct, 
            "feedback": feedback
        }

# Global Instance
env_instance = PhishGuardEnv()

@app.post("/reset")
async def reset():
    return {"observation": env_instance.reset()}

@app.post("/step")
async def step(action: PhishAction):
    obs, reward, done, info = env_instance.step(action.action)
    return {"observation": obs, "reward": reward, "done": done, "info": info}

@app.get("/state")
async def state():
    return {"current_task_idx": env_instance.current_task_idx}

if __name__ == "__main__":
    import uvicorn
    # Start server on 7860 (Hugging Face default)
    uvicorn.run(app, host="0.0.0.0", port=7860)