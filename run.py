# Custom modules
from lures import LureNotifier
from data_loading import load_graph_data, load_domains


def main():
    domains = load_domains()
    supervisors_to_members = load_graph_data()
    potential_lures = LureNotifier.identify_lures(domains)
    print(potential_lures)

if __name__ == '__main__':
    main()
