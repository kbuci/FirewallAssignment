from firewall import Firewall

if __name__ == "__main__":
    fw = Firewall("prompt_input.csv")
    print(fw.port_policies)
    print(fw.ip_policies)
    assert(fw.accept_packet("inbound", "tcp", 80, "192.168.1.2")) # matches first rule
    assert(fw.accept_packet("inbound", "udp", 53, "192.168.2.1")) # matches third rule
    assert(fw.accept_packet("outbound", "tcp", 10234, "192.168.10.11")) # matches second rule true
    assert(not fw.accept_packet("inbound", "tcp", 81, "192.168.1.2"))
    assert(not fw.accept_packet("inbound", "udp", 24, "52.12.48.92"))
    fw = Firewall("overlap_ranges_input.csv")
    # test for case of overlapping intervals 
    assert(fw.accept_packet("outbound","tcp",14000, "192.168.10.12"))
    assert(fw.accept_packet("outbound","tcp",14000, "192.168.10.11"))
    assert(not fw.accept_packet("outbound","tcp",10000, "192.168.10.12"))
    assert(not fw.accept_packet("outbound","tcp",13000, "192.168.10.16"))
    assert(fw.accept_packet("outbound","tcp",15000, "192.168.10.16"))