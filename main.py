#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author: TU

import argparse
import sic_lib 
import sic_instruction


SIC_RESULT = []
FUNC_MP = {}

class sic_line:
    def __init__(self):
        self.location = ""
        self.first = ""
        self.second = ""
        self.third = ""
        self.obj_code = ""
    
def main_func(input_file: str) -> list[sic_line]:
    start_location = 0
    with open(input_file, "r") as f:
        
        sic_source = f.read()
        
        for cnt, line in enumerate(sic_source.split("\n")):
            line = line.split()
            line = sic_lib.deal_comment(line)
            if len(line) == 0: continue
            curr_line_obj = sic_line()
            curr_line_obj.location = start_location
            next_add = 3
            
            if cnt == 0:
                
                if not(sic_lib.check_start(line)): 
                    print("Error START")
                    exit()
                else: 
                    start_location = int(line[-1], 16)
                curr_line_obj.third = line[-1]
                curr_line_obj.second = "START"
                curr_line_obj.location = start_location
                try:
                    curr_line_obj.first = line[-3]
                except: pass 
                next_add = 0
                
            
            else: 
                if len(line) == 1:
                    curr_line_obj.first = ""
                    curr_line_obj.second = line[0]
                    curr_line_obj.third = ""
                    curr_line_obj.obj_code = sic_instruction.instruction_convert[line[0]] + "0000"
                    
                else:
                    if line[-2] in sic_instruction.instruction_convert:
                        curr_line_obj.third = line[-1]
                        curr_line_obj.second = line[-2]
                        try:
                            curr_line_obj.first = line[-3]
                            FUNC_MP[curr_line_obj.first] = start_location
                        except: pass 
                        
                    else:
                        line_snd = line[-2]
                        if line_snd == "END":
                            curr_line_obj.third = line[-1]
                            curr_line_obj.second = line[-2]
                            next_add, curr_line_obj.obj_code = 0, ''
                        else:
                            curr_line_obj.third = line[-1]
                            curr_line_obj.second = line[-2]
                            curr_line_obj.first = line[-3]
                            FUNC_MP[curr_line_obj.first] = start_location
                            if line_snd == "BYTE":                        
                                next_add, curr_line_obj.obj_code =  sic_lib.deal_BYTE(line)                           
                            elif line_snd == "WORD":      
                                next_add, curr_line_obj.obj_code =  sic_lib.deal_WORD(int(curr_line_obj.third))
                            elif line_snd == "RESB":            
                                next_add, curr_line_obj.obj_code =  sic_lib.deal_RESB(int(curr_line_obj.third))
                            elif line_snd == "RESW":
                                next_add, curr_line_obj.obj_code =  sic_lib.deal_RESW(int(curr_line_obj.third))
                            
                        
                        
            SIC_RESULT.append(curr_line_obj)
            start_location += next_add    
        
        for obj in SIC_RESULT:
            if obj.second not in sic_instruction.pseudo_instruction and len(obj.obj_code) == 0:
                target_func = FUNC_MP[obj.third.split(",")[0]]
                if ",X" == obj.third[-2:]:
                    obj.obj_code = sic_instruction.instruction_convert[obj.second] + hex(target_func + int("8000", 16))[2:].upper().zfill(4)
                else:
                    obj.obj_code = sic_instruction.instruction_convert[obj.second] + hex(target_func)[2:].upper().zfill(4)
         


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", required=True, help="Input the file name you want to assemble here")
    parser.add_argument("-o", "--ouput", required=True, help="The file to store the assembly result")
    
    
    args = parser.parse_args()
    main_func(args.source)
    for i in range(len(SIC_RESULT)):
        print(f"{(i + 1) * 5:<7}  {hex(SIC_RESULT[i].location)[2:].upper():<15} {SIC_RESULT[i].first:<15} {SIC_RESULT[i].second:<15} {SIC_RESULT[i].third:<15}  {SIC_RESULT[i].obj_code:<15}")
    with open(args.ouput, "w") as f:
        for i in range(len(SIC_RESULT)):
            f.write(f"{(i + 1) * 5:<7}  {hex(SIC_RESULT[i].location)[2:].upper():<15} {SIC_RESULT[i].first:<15} {SIC_RESULT[i].second:<15} {SIC_RESULT[i].third:<15}  {SIC_RESULT[i].obj_code:<15}")
            f.write("\n")
            

                
            
                    