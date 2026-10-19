from functools import wraps

from pydantic_ai import Agent

from cost_tracker import capture_usage


def get_model_name(agent):
    model = agent.model
    if isinstance(model, str):
        return model
    return f'{model.system}:{model.model_name}'


def patch_agent_run():
    """Wrap Agent.run so every run, agent or judge, records its token usage."""
    original_run = Agent.run

    if getattr(original_run, '_cost_tracked', False):
        return

    @wraps(original_run)
    async def run_with_cost_tracking(self, *args, **kwargs):
        result = await original_run(self, *args, **kwargs)
        capture_usage(get_model_name(self), result)
        return result

    run_with_cost_tracking._cost_tracked = True
    Agent.run = run_with_cost_tracking
