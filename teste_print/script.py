import subprocess

#atencao para case_add
pacotes = ['root','deep_features','null_nodes_head','null_nodes_dep','orphan_default','rel_pron','deep_subj_ud','coord_gov','null_subject','coord_dep_left','coord_dep_left_aux','coord_dep_left_cop','coord_dep_left_case','coord_dep_left_mark','coord_dep_left_subj','coord_dep_right','deep_subj_ud','rel_pron','case_mwe_specific','case_mwe','case_mark','case_info','case_add','cc_mark','cc_info','copy_basic_enhanced','cleaning_feat']

print(len(pacotes))
comando = "echo 'Ola, mundo'"

res = subprocess.run(comando, shell=True, capture_output=True)

print(res.stderr)