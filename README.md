# ud_to_eud_br

Comandos:
- eval $(opam env)
- Go to ./ud_to_eud
- Command: grew transform -config iwpt -grs grs/iwpt_UD_to_MIX.grs -strat ud_to_mix -i ../teste.conllu -o ../POS_ANOTACAO.conllu
- Always update grs/iwpt_UD_to_MIX.grs to teste.grs

- grew count -request ADJ_NOUN_pre.req -request ADJ_NOUN_post.req -i Pre_Anotacao_Enhanced.conllu -tsv