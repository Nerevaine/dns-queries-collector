import pandas as pd


def print_statistics(dataframe: pd.DataFrame,head: int = 5) -> None:
    """
    Displays DNS query statistics, showing the total records and rankings of
    client IPs and queried hosts.

    Args: dataframe (pd.DataFrame): DataFrame containing DNS query data with
    columns "client_ip" and "host_queried". head (int): Number of top entries
    to display for both client IPs and hosts. Defaults to 5.
    """
    num_rows = dataframe.shape[0]
    client_ips_rank = dataframe["client_ip"].value_counts().head(head)
    host_rank = dataframe["host_queried"].value_counts().head(head)

    print(f"Total Records: {num_rows}\n")

    print("Client IPs Rank")
    print("------------------ --- -----")
    for ip,count in client_ips_rank.items():
        percentage = (count / num_rows) * 100
        print(f"{ip:<18} {count:<3} {percentage:.2f}%")
    print("------------------ --- -----\n")

    print("Host Rank")
    print("-------------------------------------------- ---- -----")
    for host,count in host_rank.items():
        percentage = (count / num_rows) * 100
        print(f"{host:<44} {count:<3} {percentage:.2f}%")
    print("-------------------------------------------- ---- -----")