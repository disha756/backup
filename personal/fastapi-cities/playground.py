# data = [10, "Python", True, 3.5, "Developer", False, 20]

# reports = {}
# numeric_sun = 0

# for a in data:
#     # print(a, "->", type(a))
#     if isinstance(a, bool):
#         reports[bool] = reports.get(bool, 0) + 1
#     elif isinstance(a, str):
#         reports[str] = reports.get(str, 0) + 1
#     elif isinstance(a, float):
#         reports[float] = reports.get(float, 0) + 1
#         numeric_sun += a
#     elif isinstance(a, int):
#         reports[int] = reports.get(int, 0) + 1
#         numeric_sun += a

# print(reports)
# print("int", reports.get(int, 0))
# print("numeric_sum", numeric_sun)

# from openai import OpenAI

# client = OpenAI()

# response = client.chat.completions.create(
#     model="gpt-5.4-mini",
#     messages=[
#         {
#             "role": "user",
#             "content": [{"type": "text", "text": "write a story about dinosou"}],
#         },
#         {
#             "role": "assistant",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "Once, in a valley surrounded by tall mountains and sparkling rivers, there lived a small dinosaur named Dinosou.\n\nDinosou was not the biggest dinosaur in the land. He was not the strongest, and he could not roar as loudly as the others. But Dinosou had one special talent: he was very kind. He helped baby dinosaurs find their way home, shared juicy berries with hungry friends, and always listened when someone felt sad.\n\nOne morning, Dinosou noticed that the river had dried up. The plants were drooping, and the dinosaurs were worried. “What can we do?” they asked.\n\nDinosou looked around and had an idea. “Let’s work together,” he said.\n\nHe led the other dinosaurs up the hill to the old rain cave, where water sometimes collected after storms. They dug little channels with their feet and tails, guiding the water back to the valley. It was hard work, but Dinosou never gave up. At last, the water began to flow again!\n\nThe plants stood tall, the river sparkled, and the valley came back to life. The dinosaurs cheered and lifted Dinosou onto their shoulders.\n\nFrom that day on, everyone knew the truth: Dinosou might have been small, but he had the biggest heart in the valley.\n\nAnd whenever the stars shone over the mountains, the dinosaurs would say, “Goodnight, Dinosou. Thank you for saving us.”\n\nIf you want, I can also write:\n- a funny dinosaur story\n- a scary dinosaur story\n- a bedtime dinosaur story for kids",
#                 }
#             ],
#         },
#     ],
#     response_format={"type": "text"},
#     verbosity="medium",
#     reasoning_effort="medium",
#     store=False,
# )

# print(response)


from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)