from typing import Any

class BasicParser:

    def parse_prompt_response(self, model_out_text) -> Any:
        """Parse model out text to prompt define response.

        Args:
            model_out_text: The output of an LLM call.

        Returns:
            Any: The parsed output of an LLM call.
        """
        cleaned_output = model_out_text.rstrip()
        if "```json" in cleaned_output:
            _, cleaned_output = cleaned_output.split("```json")
        # if "```" in cleaned_output:
        #     cleaned_output, _ = cleaned_output.split("```")
        if cleaned_output.startswith("```json"):
            cleaned_output = cleaned_output[len("```json") :]
        if cleaned_output.startswith("```"):
            cleaned_output = cleaned_output[len("```") :]
        if cleaned_output.endswith("```"):
            cleaned_output = cleaned_output[: -len("```")]
        cleaned_output = cleaned_output.strip()
        if not cleaned_output.startswith("{") or not cleaned_output.endswith("}"):
            cleaned_output = self.extract_json(cleaned_output)

        if not cleaned_output or len(cleaned_output) <= 0:
            return model_out_text

        cleaned_output = (
            cleaned_output.strip()
            .replace("\\n", " ")
            .replace("\n", " ")
            .replace("\\", " ")
            .replace("\\_", "_")
        )
        cleaned_output = self.illegal_json_ends(cleaned_output)
        return cleaned_output

    #防止一些生成错误，规范格式
    def illegal_json_ends(self, s):
        temp_json = s
        illegal_json_ends_1 = [", }", ",}"]
        illegal_json_ends_2 = ", ]", ",]"
        for illegal_json_end in illegal_json_ends_1:
            temp_json = temp_json.replace(illegal_json_end, " }")
        for illegal_json_end in illegal_json_ends_2:
            temp_json = temp_json.replace(illegal_json_end, " ]")
        return temp_json

    #如果去除一些特殊符号后的答案仍然不是json格式，则要提取其中的json格式
    def extract_json(self, s):
        try:
            temp_json_simple = self.json_interception(s)
            temp_json_array = self.json_interception(s, True)
            if len(temp_json_simple) > len(temp_json_array):
                temp_json = temp_json_simple
            else:
                temp_json = temp_json_array

            if not temp_json:
                temp_json = self.json_interception(s)

            temp_json = self.illegal_json_ends(temp_json)
            return temp_json
        except Exception:
            raise ValueError("Failed to find a valid json in LLM response！" + temp_json)


    #提取对象
    def json_interception(self, s, is_json_array: bool = False):
        try:
            if is_json_array:
                i = s.find("[")
                if i < 0:
                    return ""
                count = 1
                for j, c in enumerate(s[i + 1 :], start=i + 1):
                    if c == "]":
                        count -= 1
                    elif c == "[":
                        count += 1
                    if count == 0:
                        break
                return s[i : j + 1]
            else:
                i = s.find("{")
                if i < 0:
                    return ""
                count = 1
                for j, c in enumerate(s[i + 1 :], start=i + 1):
                    if c == "}":
                        count -= 1
                    elif c == "{":
                        count += 1
                    if count == 0:
                        break
                return s[i : j + 1]
        except Exception:
            return ""