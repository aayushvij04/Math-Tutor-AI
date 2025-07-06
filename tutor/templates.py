default_templates = {
    'step_prompt': "Does this make sense so far? ",
    'rephrase_prompt': "Let me try to explain that differently:",
    'encouragement': "You're doing great! Let's keep going.",
    'greeting': "Hi! I'm your math tutor. Let's work through this together.",
    'farewell': "Great job today! See you next time."
}

def get_templates(overrides=None):
    templates = default_templates.copy()
    if overrides:
        templates.update(overrides)
    return templates 