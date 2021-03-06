from FB_ideology import base
from FB_ideology import read
from FB_ideology import write
import os.path



class incorrect_input(Exception):
    pass



class overwriting_file(Exception):
    pass



#build a dicitonary to assign oders to different work.
input_dict = {"user_like" : 0, "page_page_matrix" : 1, "page_score" : 2}
output_dict = {"page_page_matrix" : 0, "page_score" : 1, "user_score" :2}



def fb_score(input_format, output_format, input_path, output_path, 
            page_info_path = "", user_like_path = "", overwrite_file = False, 
            clinton_on_the_left = False, page_id_column_index = 0):
    """Combine base, read, write modules in Python package "FB_ideology"
    
    This function reads the file from input_path and processes data by the 
    specified input_format and output_format, and will write the results as
    a csv file located at the given output_path.

    Args:
        input_format: A string being "user_like", "page_page_matrix", or 
            "page_score" to specify inputed data being in what stage of
            FB_ideology score computation.
        output_format: A string being "page_page_matrix", "page_score", 
            or "user_score" to sepcify data processing should be ended 
            and written in what stage of FB_ideology score computation.
        input_path: A string indicating path of input data.
        output_path: A string indicating path of output data.
        page_info_path: A string indicating path of page information data,
            used only when generating page score data.
        user_like_path: A string indicating path of user like page data,
            used only when generating user score data.
        clinton_on_the_left: A boolean expression indicating whether the 
            function ensures Hillary Clinton's computed ideology score being
            negative to make ideology score increases as the person being 
            more conservative. Which is used only when generating 
            page score data.
        page_id_column_index: An integer as the index to the 
            column: "page_id". Which is used only when reading 
            page score data.
    Returns: 
        Differ as input_format and output_format specified, same as 
            returns in base module.
    Raise: 
        incorrect_input: Happens when input_format or output_formated entered
            does not exists. Or file indicated by input_path does not exist.
        overwriting_file: Happens when the function is overwriting a file without
            entering "True" in the "overwrite_file" argument.
    """    
    
    try:
        input_order = input_dict[input_format]
    except KeyError:
        raise incorrect_input("input_format could only be 'user_like', ",
                            "'page_page_matrix' or 'page_score'")
    try:
        output_order = output_dict[output_format]
    except KeyError:
        raise incorrect_input("output_format could only be 'page_page_matrix',",
                            " 'page_score' or 'user_like'")

    if( output_order < input_order):
        raise incorrect_input("you can't generate", output_format,
                            "from", input_format)
    if( not os.path.isfile(input_path)):
        raise incorrect_input("input file doesn't exist")
    if(os.path.isfile(output_path) and overwrite_file == False):
        raise overwriting_file("You are overwriting an existing file, set " 
                            "overwrite_file = True in the funciton if you ",
                            "want to overwrite")

    if(page_info_path != ""):
        page_info_data = read.read_page_info_data(page_info_path,
                                                 page_id_column_index)
    if(user_like_path != ""):
        user_like_page_data = read.read_us_user_like_page_pd_df(user_like_path)

    if(input_order == 0):
        print("start reading user like page_data")
        user_like = read.read_us_user_like_page(input_path)
        print("start turning user_like to page_page_matrix")
        page_page_df = base.us_user_page_to_page_page_matrix(user_like)
        if(output_order == 0):
            write.write_page_page_matrix(page_page_df,  output_path, overwrite_file)
            return(page_page_df)
        elif(output_order == 1):
            ("start turning  page_page_matrix to page_score")
            page_score_df = base.page_page_matrix_to_page_score(page_page_df, page_info_data, 
                                    clinton_on_the_left)
            write.write_page_score_data(page_score_df,  output_path, overwrite_file)
            return(page_score_df)
        elif(output_order == 2):
            print("start turning  page_page_matrix to page_score")
            page_score_df = base.page_page_matrix_to_page_score(page_page_df, page_info_data, 
                                    clinton_on_the_left)
            print("start turning page_score to user_score")
            user_score_df = base.page_score_to_user_score(page_score_df, user_like_page_data)
            write.write_user_score_data(user_score_df,  output_path, overwrite_file)
            return(user_score_df)

    elif(input_order == 1):
        print("start reading page page matrix")
        page_page_df = read.read_page_page_matrix(input_path)
        print("start turning  page_page_matrix to page_score")
        page_score_df = base.page_page_matrix_to_page_score(page_page_df, page_info_data, 
                                    clinton_on_the_left)
        if(output_order == 1):
            write.write_page_score_data(page_score_df,  output_path, overwrite_file)
            return(page_score_df)           
        elif(output_order == 2):
            print("start turning page_score to user_score")
            user_score_df = base.page_score_to_user_score(page_score_df, user_like_page_data)
            write.write_user_score_data(user_score_df,  output_path, overwrite_file)
            return(user_score_df)

    elif(input_order == 2):
        print("start reading page score data")
        page_score_df = read.read_page_score_data(input_path)
        print("start turning page_score to user_score")
        user_score_df = base.page_score_to_user_score(page_score_df, user_like_page_data)
        write.write_user_score_data(user_score_df,  output_path, overwrite_file)
        return(user_score_df)



