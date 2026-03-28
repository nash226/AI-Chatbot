





while user_input != "exit":

    history += [{"role": "user", "content": user_input}]
    response = llm_response(history, tools)
    history += response.output

    # Gather an array of all function calls within response.
    # This will be None if there are no function calls:
    tool_calls = [obj for obj in response.output \
        if getattr(obj, "type", None) == "function_call"]
    
    while tool_calls: ## the "agent loop"
        for tool_call in tool_calls:
            function_name = tool_call.name
            args = json.loads(tool_call.arguments)

            if function_name == "multiply":
                result = {"multiply": multiply(**args)}
                history += [{"type": "function_call_output",
                            "call_id": tool_call.call_id,
                            "output": json.dumps(result)}]
                response = llm_response(history, tools)
                history += response.output
                tool_calls = [obj for obj in response.output \
                    if getattr(obj, "type", None) == "function_call"]
                
    print(f"\nAssistant: {response.output_text}\n")
    history += [
        {"role": "assistant", "content": response.output_text},
    ]
    user_input = input("User: ")