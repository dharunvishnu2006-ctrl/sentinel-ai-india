import logging

logger = logging.getLogger(f"sentinel.{__name__}")


async def send(to_agent, message: dict):
    """Put a message into another agent's inbox."""
    await to_agent.inbox.put(message)


async def run_agent(agent):
    """Keep receiving and printing messages for one agent."""
    while True:
        msg = await agent.receive()
        logger.info(f"{agent.name} received: {msg}")
