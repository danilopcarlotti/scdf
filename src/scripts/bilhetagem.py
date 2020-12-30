import sys

import matplotlib.pyplot as plt
import networkx as nx

from pathlib import Path

PATH_ROOT = Path().absolute().parent.parent
sys.path.append(str(PATH_ROOT))

from scdf.src.scripts.networkx_graphs import networkx_graphs


def processar_interceptacao_telefonica(
    filepath, id_inv, path_inicial, colunaOrig="Origem/IMEI", colunaDest="Destino/IMEI"
):
    nt = networkx_graphs(file_path=filepath)
    nt.df_dir_graph(colunaOrig, colunaDest, excelf=True)
    nx.draw_circular(nt.graph, with_labels=True, edge_color="b")
    plt.savefig(
        path_inicial
        + filepath.split("/")[-1].split(".")[0]
        + "_"
        + str(id_inv)
        + ".png"
    )
    relatorio = open(
        path_inicial + "relatório_bilhetagem_investigacao_%s.txt" % (str(id_inv),), "w"
    )
    relatorio.write("Nome do arquivo analisado: " + filepath.split("/")[-1])
    relatorio.write("\nEstes são os números que fazem ou recebem ligações\n")
    for i in nt.graph.nodes:
        relatorio.write(str(i) + "\n")
    relatorio.write(
        "\nAnálise de ciclos fechados - números que fazem e que recebem ligações mutuamente\n"
    )
    relatorio.write(str(nt.simple_cycles()))
    relatorio.write("\nNúmeros que se falam\n")
    relatorio.write(str(nt.degree_edges()))
    relatorio.write("\nQuantidade de ligações entre números\n")
    relatorio.write(str(nt.get_edge_attributes(sorted_tuples=True)))
    relatorio.close()


if __name__ == "__main__":
    if len(sys.argv) == 4:
        processar_interceptacao_telefonica(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3],
            colunaOrig="Origem/IMEI",
            colunaDest="Destino/IMEI",
        )
    elif len(sys.argv) == 6:
        processar_interceptacao_telefonica(
            sys.argv[1],
            sys.argv[2],
            sys.argv[3],
            colunaOrig=sys.argv[4],
            colunaDest=sys.argv[5],
        )
