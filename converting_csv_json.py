import json
import csv

import argparse

# Create a Secrets Manager client


create_rich_menu_desc = "sample_create_rich_menu.jsonの作成の説明です。"

parser = argparse.ArgumentParser(
    description=create_rich_menu_desc,
)
args = parser.parse_args()


def json_to_csv(json_file):
    """
    jsonファイルから、csvファイルの書き込みをするメソッド
    :param json_file:
    :return:
    """
    try:
        with open(json_file, "r") as f:
            json_data = json.load(f)

        areas_action_label_lis = [i["action"]["label"] for i in json_data["areas"]]
        areas_action_type_lis = [i["action"]["type"] for i in json_data["areas"]]
        area_action_content_lis = []

        for num, action_type in enumerate(areas_action_type_lis):
            if action_type == "uri":
                area_action_content_lis.append(
                    json_data["areas"][num]["action"][action_type]
                )
            elif action_type == "message":
                area_action_content_lis.append(
                    json_data["areas"][num]["action"]["text"]
                )
            else:
                raise ValueError("area_action_content_lisが正しくありません")

        areas_bounds_height = [i["bounds"]["height"] for i in json_data["areas"]]
        areas_bounds_width = [i["bounds"]["width"] for i in json_data["areas"]]
        areas_bounds_x = [i["bounds"]["x"] for i in json_data["areas"]]
        areas_bounds_y = [i["bounds"]["y"] for i in json_data["areas"]]
        chat_bar_text_lis = [json_data["chatBarText"]]
        areas_name = [json_data["name"]]
        selected_lis = [json_data["selected"]]
        size_height_lis = [json_data["size"]["height"]]
        size_width_lis = [json_data["size"]["width"]]
        csv_column = [
            "areas/action/label",
            "areas/action/type",
            "areas/action/content",
            "areas/bounds/height",
            "areas/bounds/width",
            "areas/bounds/x",
            "areas/bounds/y",
            "chatBarText",
            "name",
            "selected",
            "size/height",
            "size/width",
        ]

        csv_data_lis = [
            areas_action_label_lis,
            areas_action_type_lis,
            area_action_content_lis,
            areas_bounds_height,
            areas_bounds_width,
            areas_bounds_x,
            areas_bounds_y,
            chat_bar_text_lis,
            areas_name,
            selected_lis,
            size_height_lis,
            size_width_lis,
        ]

        with open("sample_create_rich_menu.csv", "w", newline="") as f:
            csv_write = csv.writer(
                f, delimiter=",", quotechar='"', quoting=csv.QUOTE_NONNUMERIC
            )
            csv_write.writerow(csv_column)

            for n in range(len(json_data["areas"])):
                csv_data_row_n = []
                for csv_data in csv_data_lis:
                    if len(csv_data) > n:
                        csv_data_row_n.append(csv_data[n])
                    else:
                        csv_data_row_n.append("")
                csv_write.writerow(csv_data_row_n)
    except Exception:
        raise Exception("json_fileが正しくありません")


def csv_to_json(csv_path):
    """
    csvファイルから、jsonデータを作成するメソッド
    :param csv_path:
    :return:
    """
    try:
        with open(csv_path, "r") as f:
            csv_data = csv.reader(f)
            csv_raw_data = []
            for i in csv_data:
                csv_raw_data.append(i)

            del csv_raw_data[0]
            action_data_lis = []
            for i in csv_raw_data:
                action_data = {
                    "action": {"label": i[0], "type": i[1], "uri": i[2]},
                    "bounds": {"height": int(i[3]), "width": int(i[4]), "x": int(i[5]), "y": int(i[6])},
                }
                action_data_lis.append(action_data)
            json_data = {
                "areas": [action_data],
                "chatBarText": csv_raw_data[0][7],
                "name": csv_raw_data[0][8],
                "selected": bool(csv_raw_data[0][9]),
                "size": {"height": int(csv_raw_data[0][10]), "width": int(csv_raw_data[0][11])},
            }
            return json_data

    except Exception:
        raise Exception("正しいcsvファイルを設置してください")
