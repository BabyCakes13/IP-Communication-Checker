"""Module which given two IP's, it checks whether the first IP
 can communicate with the second IP."""
import sys


def initialise():
    """Gets the given arguments.
    Constructs the range: [network, broadcast].
    Checks if the first IP can communicate with the second IP."""

    ip1 = sys.argv[1]
    ip2 = sys.argv[2]

    network, broadcast = construct_interval(ip1)
    ip2 = split_ip(ip2)

    print("\nIP2: ", ip2,
          "\nNetwork: ", network,
          "\nBroadcast: ",
          broadcast, "\n")

    if check_communication(network, broadcast, ip2) is True:
        print("The first ip can communicate with the second ip.")
    else:
        print("The first ip cannot communicate with the second ip.")


def check_communication(network, broadcast, ip_argument):
    """Checks if the second IP is in range [network, broadcast]."""

    can_communicate = True

    for i in range(0, len(ip_argument)):
        if (ip_argument[i] > broadcast[i]) or (ip_argument[i] < network[i]):
            can_communicate = False
            break

    return can_communicate


def split_ip(ip_argument):
    """Splits the octets of the IP and the broadcast mask."""

    separated = list(ip_argument.split('.'))
    mask = list(separated[3].split('/'))

    separated.append(mask[0])

    del mask[0]
    del separated[3]

    for i in range(0, len(separated)):
        separated[i] = int(separated[i])

    return separated


def construct_interval(ip_argument):
    """Using the generated binary IP and mask,
    the netmask and broadcast are created."""

    mask, first_ip = get_binary(ip_argument, 0)
    netmask = get_binary(get_netmask(int(mask[0])), 1)
    network = get_network(netmask, first_ip)
    broadcast = get_broadcast(int(mask[0]), first_ip)

    return network, broadcast


def get_netmask(mask):
    """Creates the subnets mask which will be the lower bound
    in the range in which the second IP should be in order to
    communicate."""

    mask = int(mask)
    mask_string = ""

    for i in range(0, 32):
        if i in (8, 16, 24):
            mask_string += "."
        if i < mask:
            mask_string += "1"
        else:
            mask_string += "0"

    binary_mask_list = mask_string.split('.')
    int_mask_list = []

    for byte in binary_mask_list:
        int_mask_list.append(int(byte, 2))

    return int_mask_list


def get_binary(ip_argument, is_subnet):
    """Converts the IP from decimal to binary."""

    separated_bytes_binary_ip = []

    if is_subnet is 1:

        separated_bytes_int_ip = ip_argument

        for byte in separated_bytes_int_ip:
            separated_bytes_binary_ip.append('{0:08b}'.format(int(byte)))

        return separated_bytes_binary_ip

    separated_bytes_int_ip = list(ip_argument.split('.'))

    mask = list(separated_bytes_int_ip[3].split('/'))

    separated_bytes_int_ip.append(mask[0])

    del mask[0]
    del separated_bytes_int_ip[3]

    if is_subnet == 0:
        for byte in separated_bytes_int_ip:
            separated_bytes_binary_ip.append('{0:08b}'.format(int(byte)))

    return mask, separated_bytes_binary_ip


def get_network(subnet, ip_argument):
    """Creates the network."""

    network = []

    for i in range(0, len(subnet)):
        network_byte = ''
        for j in range(0, len(subnet[i])):
            if (subnet[i][j] == ip_argument[i][j]) and (subnet[i][j] == '1'):
                network_byte += '1'
            else:
                network_byte += '0'
        network.append(network_byte)

    for i in range(0, len(network)):
        network[i] = int(network[i], 2)

    return network


def get_broadcast(mask, ip_argument):
    """Creates the broadcast."""

    cidr = 32 - mask
    broadcast_mask = get_netmask(cidr)
    broadcast_mask = get_binary(broadcast_mask, 1)

    for i in range(0, 3):
        broadcast_mask[i] = broadcast_mask[i][::-1]

    broadcast_mask.reverse()

    broadcast = []

    for i in range(0, len(broadcast_mask)):
        broadcast_byte = ''
        for j in range(0, len(broadcast_mask[i])):
            if (ip_argument[i][j] == '1') or (broadcast_mask[i][j] == '1'):
                broadcast_byte += '1'
            else:
                broadcast_byte += '0'
        broadcast.append(broadcast_byte)

    for i in range(0, len(broadcast)):
        broadcast[i] = int(broadcast[i], 2)

    return broadcast


initialise()
