class Node:
    def __init__(self):
        self.marker = False      # Marker to check if this is the end of a prefix
        self.children = {}       # Dictionary to store children nodes
        self.data = None         # To store additional data like network address and mask


class Trie:
    def __init__(self):
        self.root = Node()

    def insert(self, binary_network_address, prefix_length, data):
        """Insert a binary network address with its prefix length into the Trie."""
        current = self.root
        for i in range(len(binary_network_address)):
            bit = binary_network_address[i]
            if bit not in current.children:
                current.children[bit] = Node()
            current = current.children[bit]
            # Store data at the end of the prefix
            if i == prefix_length - 1:
                current.marker = True
                current.data = data  # Store the corresponding data

    def find_exact_match(self, binary_ip_address):
        """Find the exact matching network address for the given binary IP address."""
        current = self.root
        for bit in binary_ip_address:
            if bit in current.children:
                current = current.children[bit]
            else:
                return None  # No match found
        return current.data if current.marker else None  # Return data only if it's an end of a word

    def convert_to_binary(self, address):
        """Converts a dotted-decimal IP address to a binary representation."""
        return [int(bit) for bit in ''.join(format(int(part), '08b') for part in address.split('.'))]

    def prefix_matching(self, binary_ip_address):
        """Return all prefixes that match the given binary IP address."""
        current = self.root
        matches = []
        for bit in binary_ip_address:
            if bit in current.children:
                current = current.children[bit]
                # If current is a marker, store the corresponding data
                if current.marker:
                    matches.append(current.data)
            else:
                break  # No further matches
        return matches


def load_test_cases(file_path):
    """Load test cases from a file."""
    networks = []
    ip_addresses = []
    
    with open(file_path, 'r') as file:
        section = None
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                continue  # Skip comments
            if line == "":
                continue  # Skip empty lines
            
            if "Network addresses" in line:
                section = "networks"
                continue
            elif "IP addresses" in line:
                section = "ips"
                continue
            
            if section == "networks":
                networks.append(tuple(line.split()))
            elif section == "ips":
                ip_addresses.append(line)
    
    return networks, ip_addresses


def main():
    trie = Trie()

    # Load test cases from file
    networks, ip_addresses = load_test_cases('test_cases.txt')

    # Insert predefined network addresses into the Trie
    for net_add, net_mask in networks:
        binary_net_add = trie.convert_to_binary(net_add)
        binary_net_mask = trie.convert_to_binary(net_mask)
        prefix_length = sum(binary_net_mask)
        trie.insert(binary_net_add, prefix_length, (net_add, net_mask))

    # Check each IP address against the Trie
    for ip in ip_addresses:
        binary_ip_addr = trie.convert_to_binary(ip)

        # Find the exact matching network address in the Trie
        exact_match = trie.find_exact_match(binary_ip_addr)
        if exact_match:
            print(f"{ip} matches {exact_match[0]} with mask {exact_match[1]}")
        else:
            print(f"{ip} not found")

        # Find all matching prefixes
        matches = trie.prefix_matching(binary_ip_addr)
        if matches:
            for match in matches:
                print(f"{ip} matches prefix {match[0]} with mask {match[1]}")
        else:
            print(f"No matching prefixes for {ip}")


if __name__ == "__main__":
    main()
