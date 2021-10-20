#!/usr/bin/env python
# -*- conding:utf-8 -*-
# @AUTHOR: Gui-Yan Xie
# @CONTACT: xieguiyan.at.hust.edu.cn
# @DATE: 2021-09-03 15:29:17
# @DESCRIPTION:


import json
from pathlib import Path

current_path = Path(__file__).parent


class Config(object):
    def __init__(self, configfile: Path = current_path / "../resource/configure.json"):
        self.configfile = Path(configfile)
        self.config = self.read_config()
        self.mature_miRNA, self.hairpin_info = self.deal_mir_info()

    def read_config(self):
        try:
            with open(self.configfile, "r") as f:
                return json.load(f)
        except IOError:
            print(f"{self.configfile} not exists.")

    def deal_mir_info(self):
        mature_miRNA = {}
        hairpin_info = {}
        with open(self.config["mirbase"], "r") as f:
            for i in f:
                line = i.strip().split("\t")
                hairpin_seq = line[4]
                mir_seq = line[3]
                miRNA_start = hairpin_seq.find(mir_seq)
                if miRNA_start == -1:
                    continue
                miRNA_len = len(mir_seq)
                hairpin_len = len(hairpin_seq)
                arm = "5p" if hairpin_len > 2 * miRNA_start + miRNA_len - 1 else "3p"
                mature_miRNA.setdefault(line[1], {})[arm] = [line[0], miRNA_start, miRNA_len, mir_seq, hairpin_seq]
                if line[1] in hairpin_info:
                    continue
                hairpin_info[line[1]] = [hairpin_seq, hairpin_len]
        return (mature_miRNA, hairpin_info)
