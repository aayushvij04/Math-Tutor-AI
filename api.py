from fastapi import FastAPI, Request
from pydantic import BaseModel
from tutor.rag import RAGPipeline
from tutor.flow_manager import TutorFlowManager
from tutor.confidence import ConfidenceChecker
from tutor.templates import get_templates
import os
from typing import Optional, List
from tutor.llm_rephrase import tutor_llm_response
import time
import random
import json

app = FastAPI()

# Initialize components
rag = RAGPipeline(qa_path=os.path.join(os.path.dirname(__file__), 'data/math_qa.json'))
flow = TutorFlowManager(personality=get_templates())
confidence = ConfidenceChecker()

class ChatRequest(BaseModel):
    user_input: str
    step_idx: int = 0
    last_steps: Optional[List[str]] = None
    last_question: Optional[str] = None
    asked_indices: Optional[List[int]] = None
    last_user_inputs: Optional[List[str]] = None
    last_tutor_outputs: Optional[List[str]] = None

@app.post("/chat")
async def chat(req: ChatRequest):
    user_input = req.user_input
    step_idx = req.step_idx
    last_steps = req.last_steps or []
    last_question = req.last_question
    asked_indices = req.asked_indices or []
    last_user_inputs = req.last_user_inputs or []
    last_tutor_outputs = req.last_tutor_outputs or []

    # If this is the first message, retrieve relevant Q&A and get initial response
    if not last_steps:
        retrieved = rag.retrieve(user_input, k=1)
        if not retrieved:
            return {"response": "Sorry, I couldn't find a relevant math problem.", "step_idx": 0, "last_steps": [], "last_question": None}
        question, answer, _ = retrieved[0]
        steps = flow.split_steps(answer)
        step = flow.get_step(steps, 0)
        return {
            "response": f"{flow.personality['greeting']}\n{step}\n{flow.get_prompt()}",
            "step_idx": 0,
            "last_steps": steps,
            "last_question": question
        }

    if user_input.strip().lower() == "exit":
        return {
            "response": flow.personality['farewell'],
            "step_idx": 0,
            "last_steps": [],
            "last_question": None,
            "asked_indices": []
        }

    # If user responded to a step with 'No' or 'n', use LLM to re-explain
    if user_input.strip().lower() in ["no", "n", "No", "nope", "nah", "not really", "no way", "no nahi", "nope.", "nah.", "no.", "not at all"]:
        previous_output = flow.get_step(last_steps, step_idx)
        print(f"Calling LLM to re-explain: previous_output='{previous_output}', question='{last_question}', user_input='{user_input}'")
        try:
            llm_response = tutor_llm_response(previous_output, last_question, user_input, last_user_inputs, last_tutor_outputs)
            print("LLM re-explanation output:", llm_response)
        except Exception as e:
            print("LLM re-explanation error:", e)
            llm_response = "Sorry, I couldn't rephrase that right now."
        return {
            "response": f"{llm_response}\n{flow.get_prompt()}",
            "step_idx": step_idx,
            "last_steps": last_steps,
            "last_question": last_question,
            "asked_indices": asked_indices
        }

    # If user responded 'Yes', go to next step or pick a new random question if done
    if user_input.strip().lower() in ["yes", "y"]:
        step_idx += 1
        if step_idx < len(last_steps):
            step = flow.get_step(last_steps, step_idx)
            return {
                "response": f"{step}\n{flow.get_prompt()}",
                "step_idx": step_idx,
                "last_steps": last_steps,
                "last_question": last_question,
                "asked_indices": asked_indices
            }
        else:
            # Pick a new random question, avoiding repeats
            with open(os.path.join(os.path.dirname(__file__), 'data/math_qa.json'), 'r') as f:
                data = json.load(f)
            available_indices = [i for i in range(len(data)) if i not in asked_indices]
            if not available_indices:
                # All questions asked, reset or inform user
                return {
                    "response": "You've completed all available questions! Great job!",
                    "step_idx": 0,
                    "last_steps": [],
                    "last_question": None,
                    "asked_indices": []
                }
            new_idx = random.choice(available_indices)
            new_qa = data[new_idx]
            new_question = new_qa['question']
            new_answer = new_qa['answer']
            new_steps = flow.split_steps(new_answer)
            new_step = flow.get_step(new_steps, 0)
            asked_indices.append(new_idx)
            return {
                "response": f"Here's a new question!\n{new_question}\n{new_step}\n{flow.get_prompt()}",
                "step_idx": 0,
                "last_steps": new_steps,
                "last_question": new_question,
                "asked_indices": asked_indices
            }

    # For all other inputs, send to LLM with context
    previous_output = flow.get_step(last_steps, step_idx)
    print(f"Calling LLM for unknown input: user_input='{user_input}', previous_output='{previous_output}', question='{last_question}'")
    try:
        llm_response = tutor_llm_response(previous_output, last_question, user_input, last_user_inputs, last_tutor_outputs)
        print("LLM unknown input output:", llm_response)
    except Exception as e:
        print("LLM unknown input error:", e)
        llm_response = "Sorry, I couldn't process your input right now."
    return {
        "response": f"{llm_response}\n{flow.get_prompt()}",
        "step_idx": step_idx,
        "last_steps": last_steps,
        "last_question": last_question,
        "asked_indices": asked_indices
    }
