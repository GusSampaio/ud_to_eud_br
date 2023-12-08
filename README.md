# ud_to_eud_br

Comandos:
- eval $(opam env)
- Go to ./ud_to_eud
- Command: grew transform -config iwpt -grs grs/iwpt_UD_to_MIX.grs -strat ud_to_mix -i ../teste.conllu -o ../POS_ANOTACAO.conllu
- Always update grs/iwpt_UD_to_MIX.grs to conjunto_regras_oficial.grs

- grew count -request ADJ_NOUN_pre.req -request ADJ_NOUN_post.req -i Pre_Anotacao_Enhanced.conllu -tsv

Atualmente estou utilizando o arquivo UD_to_EUD_BR.grs para fazer o scrapping, porém o certo seria utilizar o arquivo conjunto_regras_oficial.grs.

Este último funciona se usar o grew na máquina, mas ele não pode ser inserido no site que faz o scrapping

Vendo com a magali se ela tem alguma sugestão do que fazer.
