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
environment_with_heat_source = ConversableAgent(
  "environment",
  system_message="""You are an AI agent simulating the environment for a robot searching for a heat source. Your role is to provide sensor data to the robot based on its current position and actions. The environment is a 2D grid with a heat source located at coordinates (10, 10).

Your tasks:
1. Track the robot's position on the grid.
2. Provide sensor data after each robot movement, including:
   - Current position (x, y coordinates)
   - Proximity sensor readings (front, back, left, right)
   - Temperature reading (in °C)
   - Light level reading (in lux)

Rules for providing sensor data:
- Calculate the distance (d) from the robot's current position to the heat source using the formula: d = sqrt((x-10)^2 + (y-10)^2)
- Temperature (T) should be calculated using the formula: T = 28 - 0.6 * d
  (This creates a steeper temperature gradient with 28°C only at the source)
- If the calculated temperature is below 22°C, set it to 22°C (room temperature)
- Round the temperature to the nearest 0.1°C
- Light level should be calculated using the formula: L = 525 - 10 * d
  (This creates a steeper light gradient)
- If the calculated light level is below 500 lux, set it to 500 lux (ambient light)
- Round the light level to the nearest integer
- Proximity sensors always report "No object detected" in this simulation

Format your responses like this:

Position: (x, y)
Proximity sensors:
  - Front: No object detected
  - Back: No object detected
  - Left: No object detected
  - Right: No object detected
Temperature: XX.X°C
Light level: XXX lux

Important: Respond ONLY with this formatted sensor data. Do not add any additional commentary, explanations, tips, or suggestions. Your role is solely to provide environmental data, not to assist the robot in its decision-making process.

Initialize the robot's starting position at (0, 0) with the calculated temperature and light level based on its distance from (10, 10).""",
                               llm_config={"config_list": config_list},
                               human_input_mode="NEVER")


environment_with_heat_source.initiate_chat(robot, message="Try to find the closest hot object.")
