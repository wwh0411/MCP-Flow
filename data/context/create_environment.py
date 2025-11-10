
from import get_text
num_samples = 5

# file keyi exsisting

def create_context(mcp):
    
    category = prompt1(server)
    if category == "#CTX-File":

    # create context, files
        with open("data/tools/{}.json".format(server), "r", encoding="utf-8") as f:
            tool_list = json.load(f)
        # get the tool to write
        for tool in tool_list:
            # judge tool is write
            if prompt2(tool) == "#WRITE":
                for i in range(num_samples):
                    text = get_context()
                    write_request = get_query(text)

                    final_text = await run_interaction(
                        user_query=write_request,
                        model_name=chosen_model_name,
                        provider_config_path=config_path,
                        # mcp_server_config={"server_choice": mcp},
                        mcp_server_config_path="data/mcp_config/{}.json".format(mcp),
                        quiet_mode=quiet_mode,
                        log_messages_path="data/trajectory/{}.json".format(mcp)
                    )
                    print(final_text)
    
    elif category == "#CTX-Software"

    
    
    # use exsisting context, files, softwares

    