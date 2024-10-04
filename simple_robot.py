from autogen import ConversableAgent, UserProxyAgent, config_list_from_json

config_list = config_list_from_json(env_or_file="OAI_CONFIG_LIST")
robot = ConversableAgent(
  "robot",
  system_message="""You are an autonomous robot and you are part of a swarm of robots just like you.
  You have sensors and actuators.
  You have the following movement capabilities:
  - Move forward x meters
  - Move backward x meters
  - Turn left x degrees
  - Turn right x degrees
  You have the following sensors:
  - Position sensor
  - Four proximity sensors, one in front, one in back, one on the left, one on the right
  - A temperature sensor
  - A light sensor
  After executing a movement, you will receive a message from the environment with the following information:
  - Your current position
  - Whether there is an object in front, back, left, and right
  - The temperature at your current position
  - The light level at your current position
  """,
  llm_config={"config_list": config_list},
  human_input_mode="NEVER"
)
environment = UserProxyAgent("environment", code_execution_config=False)
robot.initiate_chat(environment, message="Try to find the closest hot object.")
