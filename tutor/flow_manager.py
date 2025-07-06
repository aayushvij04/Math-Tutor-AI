from typing import List, Optional

class TutorFlowManager:
    def __init__(self, personality: Optional[dict] = None):
        self.personality = personality or {
            'step_prompt': "Does this make sense so far? (Yes/No)",
            'rephrase_prompt': "Let me try to explain that differently:",
            'encouragement': "You're doing great! Let's keep going."
        }

    def split_steps(self, answer: str) -> List[str]:
        # Split answer into steps by 'Step' or numbered steps
        steps = []
        for part in answer.split('Step '):
            part = part.strip()
            if part:
                if not part.startswith('Step'):
                    steps.append('Step ' + part if len(steps) > 0 else part)
                else:
                    steps.append(part)
        return steps

    def get_step(self, steps: List[str], idx: int) -> str:
        if idx < len(steps):
            return steps[idx]
        return ""

    def get_prompt(self) -> str:
        return self.personality['step_prompt']

    def get_rephrase(self, step: str) -> str:
        return f"{self.personality['rephrase_prompt']} {step}"

    def get_encouragement(self) -> str:
        return self.personality['encouragement'] 