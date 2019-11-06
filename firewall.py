import policy

class Firewall():
    PROTOCOLS = ("udp", "tcp")
    DIRECTIONS = ("inbound","outbound")
    def __init__(self, rules_files):
        self._init_policy()
        self._load_policy(rules_files)

    def accept_packet(self, direction, protocol, port, ip_address_string):
        # Based on the direction and protocol, find the policy ids for the 
        # port and ip address, using the port and ip 
        # If there is a common policy id between these two sets,
        # then this packet is allowed by at least one rule
        # in the csv, and should be accepted
        ip_address = self._create_ip_address(ip_address_string)
        port_range = self.port_policies[(direction,protocol)] 
        ip_range = self.ip_policies[(direction,protocol)]
        ip_policies = ip_range.find_all(ip_address)
        port_policies = port_range.find_all(port)
       
        if len(ip_policies) < len(port_policies):
            return any(policy_id in port_policies for policy_id in ip_policies)
        else:
            return any(policy_id in ip_policies for policy_id in port_policies)

    
    def _load_policy(self, rules_files):
        with open(rules_files, 'r') as read_stream:
            for policy_id, line in enumerate(read_stream):
                direction, protocol, ports, ip_addresses = line.strip().split(',')
                ports = ports.split('-')
                ip_addresses = ip_addresses.split('-')
                ports = (int(ports[0]), int(ports[-1]))
                ip_addresses = (self._create_ip_address(ip_addresses[0]), self._create_ip_address(ip_addresses[-1]))
                self._update_policy(policy_id, direction,protocol,ports,ip_addresses)

    def _update_policy(self, policy_id, direction, protocol, ports, ip_addresses):
        # Based on the direction and protocol, find the corresponding
        # IP and Port ranges, and insert the new ip range and port range in them
        # This will create a new range of valid ip addresses in ip policy array, and a 
        # new range of valid ports in the port policy array 
        lower_port, higher_port = ports
        lower_address, higher_address = ip_addresses
        port_range = self.port_policies[(direction,protocol)] 
        port_range.insert_range(lower_port, higher_port, policy_id)
        ip_range = self.ip_policies[(direction,protocol)]
        ip_range.insert_range(lower_address, higher_address, policy_id)



    def _init_policy(self):
        # Create space for the Policy arrays for port and ip ranges, 
        # for every combination of direction and protocol, and initalize
        # a policy range
        self.port_policies = {}
        self.ip_policies = {}
        for direction in Firewall.DIRECTIONS:
            for protocol in Firewall.PROTOCOLS:
                self.port_policies[(direction,protocol)] = policy.PolicyRange()
                self.ip_policies[(direction,protocol)] = policy.PolicyRange()
    
    def _create_ip_address(self, ip_str):
        address = 0
        for i, octet in enumerate(reversed(ip_str.split("."))):
            address += int(octet) * 256**i
        return address





