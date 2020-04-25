import zss
import os
import re
import sqlite3
import hashlib
import json
from sqlite3 import Error
from graphviz import Digraph as Di


# Returns the children of the process
def get_the_child_processes(process_cursor, pid):
    process_id_query = '''
            SELECT id
            FROM processes
            WHERE parent = %s
            '''
    process_cursor.execute(process_id_query % pid)
    child_list = process_cursor.fetchall()
    chlst = []
    for child2 in child_list:
        chlst.append(child2[0])
    return chlst


# Returns the process name
def get_the_processes_name(executed_cursor, pid):
    process_name_query = '''
                SELECT name, argv
                FROM executed_files
                WHERE process = %s
                '''
    executed_cursor.execute(process_name_query % pid)
    process_name = executed_cursor.fetchall()
    if process_name != []:
        process_name = str(process_name[0][0]) #.split('/')[-1:][0]
    else:
        process_name = ""
    return process_name


# Returns all opened files (both W/R modes)
def get_opened_files_list(openfile_cursor, pid):
    opened_files_query = '''
            SELECT process, name, mode, id
            FROM opened_files
            WHERE process = %s AND mode <= 2
            '''
    openfile_cursor.execute(opened_files_query % pid)
    return openfile_cursor.fetchall()


def add_edge(graph_, from_, to_, mode):
    if mode == 'file':
        graph_.attr('edge', style='solid',color='black', penwidth='1')
    elif mode == 'ptree':
        graph_.attr('edge', style='dashed', color='grey', penwidth='1')
    graph_.edge(str(from_), str(to_))
    return graph_


def add_node(graph_, id, name, mode, color):
    # with graph_.subgraph(name='cluster_{}'.format(cluster)) as ngraph_:
    if mode == 'process':
        if color == 'red':
            if name == 'fslmaths':
                name = 'fsl\nmaths'
            if name == 'new_invwarp':
                name = 'new\ninvwarp'
            graph_.node(str(id), name.upper(), width='1.5', fontsize='16',fontname="Helvetica bold",
                        fontcolor='black', shape='circle',
                        style='filled', fillcolor='#EDB9B8', penwidth='1')
        elif color == 'green':
            graph_.node(str(id), name, width='1.5', penwidth='1', fontsize='16', shape='circle',
                        style='filled', fillcolor='#7FCDB1', fontname="Helvetica bold")
        elif color == 'subgreen':
            graph_.node(str(id), name, width='1.5', fontsize='16',fontname="Helvetica bold",
                        shape='circle', style='filled', fillcolor='#7FCDB1')
        elif color == 'white':
            graph_.node(str(id), name, width='1.5', shape='circle', style='filled', fontsize='16',
                        fontname="Helvetica bold", fillcolor='white')
    elif mode == 'file':
        if name != '':
            graph_.node(str(id), name, shape='box', style='filled', fillcolor=color, penwidth='1',
                        fontsize='16', fontname="Helvetica bold")
        else:
            graph_.node(str(id), name, shape='box', style='filled', fillcolor=color, penwidth='1')
    # graph_.node(str(id), name) 
    return graph_


def create_provenance_graph(db_path, pid, graph_, pipe_list=[], multi_list={},
                            tmp_list=[], total_proc_diff=[], dag=False):
    try:
        db = sqlite3.connect(db_path)
    except Error as e:
        print(e)
    process_cursor = db.cursor()
    executed_cursor = db.cursor()
    openfile_cursor = db.cursor()
    # Get the list of child process from pid
    child_list = get_the_child_processes(process_cursor, pid)
    # Get the process name
    process_name = get_the_processes_name(executed_cursor, pid)

    short_name = {}
    short_name['ACPCAlignment.sh'] = 'ACPC-A'
    short_name['BrainExtraction_FNIRTbased.sh'] = 'BExt'
    short_name['AnatomicalAverage.sh'] = 'AAve'
    short_name['BiasFieldCorrection_sqrtT1wXT1w.sh'] = 'BFC'
    short_name['T2wToT1wDistortionCorrectAndReg.sh'] = 'DC'
    short_name['AtlasRegistrationToMNI152_FLIRTandFNIRT.sh'] = 'AR'

    filter_ = re.match('(/usr/bin/)|(/bin/)', process_name)
    exclude_list = [""]
    # exclude_list = ["", "imtest", "imcp", "remove_ext",
    #                 "fslval", "avscale", "fslhd"]
    if filter_ is None and process_name.split('/')[-1:][0] not in exclude_list:
        # Get the list of opened files (w/r) from pid
        flag_ = False
        process_ofiles = get_opened_files_list(openfile_cursor, pid)
        p_name = process_name.split('/')[-1:][0]
        if pid in total_proc_diff:
            graph_ = add_node(graph_, pid, p_name, 'process', 'red')
            flag_ = True
        elif total_proc_diff != []:
            graph_ = add_node(graph_, pid, p_name, 'process', 'green')
            if p_name in short_name.keys():
                graph_ = add_node(graph_, pid, short_name[p_name], 'process', 'subgreen')
        else:
            graph_ = add_node(graph_, pid, p_name, 'process', 'white')

        for file in process_ofiles:
            fname_ = str(os.path.basename(file[1]))
            file_code = str(file[1])
            if dag and fname_ in multi_list.keys():
                if file[2] == 2:
                    file_code = str(file[1]) + str(pid)
                else:
                    sorted_ = sorted(multi_list[fname_])
                    set_pid = pid
                    for pid_lst in sorted_:
                        if pid > pid_lst:
                            set_pid = pid_lst
                            continue
                    file_code = str(file[1]) + str(set_pid)

            hash_object = hashlib.sha1(file_code.encode('utf-8'))
            hex_dig_file = hash_object.hexdigest()
            # Read files
            if file[2] == 1 and str(hex_dig_file) in pipe_list:
                graph_ = add_edge(graph_, hex_dig_file, pid, 'file')

            # Write files
            elif file[2] == 2 and (fname_ in pipe_list or fname_ in tmp_list):
                if str(hex_dig_file) not in pipe_list:
                    pipe_list.append(str(hex_dig_file))
                color = 'white'
                if dag and (fname_ in tmp_list or fname_ in multi_list.keys()):
                    color = 'grey'
                elif fname_ in tmp_list or fname_ in multi_list.keys():
                    color = 'grey'
                if flag_:
                    graph_ = add_node(graph_, hex_dig_file, fname_, 'file', color)
                else:
                    graph_ = add_node(graph_, hex_dig_file, fname_, 'file', color)
                graph_ = add_edge(graph_, pid, hex_dig_file, 'file')

    for child in child_list:
        p_name_child = get_the_processes_name(executed_cursor, child)
        # find node in graph
        filter_ = re.match('(/usr/bin/)|(/bin/)', p_name_child)
        x_node = [True for v in graph_.body if '\t{} '.format(pid) in v]
        if filter_ is None and x_node and p_name_child.split('/')[-1:][0] not in exclude_list:
            graph_ = add_edge(graph_, pid, child, 'ptree')
        create_provenance_graph(db_path, child, graph_, pipe_list,
                                multi_list, tmp_list, total_proc_diff, dag)

def parse_transient(tr_file):
    try:
        with open(tr_file, 'r') as cfile:
            data = json.load(cfile)
            if "total_temp_proc" not in data:
                tmp_write = []
            else:
                tmp_write = []
                tmp_write_dic = data["total_temp_proc"]
                for key, file_ in tmp_write_dic.items():
                    for tmp in file_['files']:
                        # ntmp = tmp.encode('utf8', 'ignore') \
                        #           .replace('\x00', ' ').strip()
                        tmp_write.append(os.path.basename(tmp))

            if "total_multi_write_proc" not in data:
                multi_write = {}
            else:
                multi_write = {}
                multi_write_t = data["total_multi_write_proc"]
                for key, file_ in multi_write_t.items():
                    for mw in file_['files']:
                        fname = os.path.basename(mw)
                        # (mw.encode('utf8',
                        #                                    'ignore').strip())
                        if fname not in multi_write.keys():
                            multi_write[fname] = [file_['id']]
                        else:
                            tmp_list = multi_write[fname]
                            tmp_list.append(file_['id'])
                            multi_write[fname] = tmp_list
    except Exception:
        multi_write = {}
        tmp_write = []
    return multi_write, tmp_write


def parse_labelling(diff_processes):
    try:
        with open(diff_processes, 'r') as cfile:
            data = json.load(cfile)
            if "total_commands" not in data:
                list_p = []
            else:
                list_p = []
                tmp_write_dic = data["total_commands"]
                for key, file_ in tmp_write_dic.items():
                    list_p.append(file_['id'])

            if "total_commands_multi" in data:
                multi_write_t = data["total_commands_multi"]
                for key, file_ in multi_write_t.items():
                    list_p.append(file_['id'])

    except Exception:
        list_p = []
    return list_p


def main(args=None):
    input_folder = 'data/example/input'
    db_file = 'data/example/trace.sqlite3'
    diff_processes = 'data/example/nonreproducible_captured.json'
    tr_file = 'data/example/transient_captured.json'
    multi_list, tmp_list = parse_transient(tr_file)
    total_proc_diff = parse_labelling(diff_processes)

    # Get the list of output files
    lst_files = []
    for file in os.walk(input_folder):
        for elem in file[2]:
            lst_files.append(elem)
    # Create provenance graphs
    graph = Di('Graph',
               filename='figures/p-graph',
               format='pdf',
               strict=True)
    # graph.attr(compound=True)
    create_provenance_graph(db_file, 1, graph, lst_files, multi_list,
                            tmp_list, [], False)
    graph.render()

    graph = Di('Graph',
               filename='figures/p-graph-dag',
               format='pdf',
               strict=True)
    create_provenance_graph(db_file, 1, graph, lst_files, multi_list,
                            tmp_list, [], True)
    graph.render()

    graph = Di('Graph',
               filename='figures/p-graph-dag-labelled',
               format='pdf',
               strict=True)
    create_provenance_graph(db_file, 1, graph, lst_files, multi_list,
                            tmp_list, total_proc_diff, True)
    graph.render()

    


if __name__ == '__main__':
    main()
