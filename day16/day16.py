import math

# pylint: disable=too-many-locals,too-many-statements,too-many-branches
h2b = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111",
}


def hex_to_bin(c):
    return h2b[c]


def bin_to_int(b):
    return int(b, 2)


def parse_packet(packet, ptr=0):
    version = packet[ptr : ptr + 3]
    ptr += 3
    version = bin_to_int(version)
    type_id = packet[ptr : ptr + 3]
    ptr += 3
    type_id = bin_to_int(type_id)

    if type_id == 4:
        number = ""
        while True:
            is_last = packet[ptr] == "0"
            number += packet[ptr + 1 : ptr + 5]
            ptr += 5
            if is_last:
                break

        number = bin_to_int(number)
        return version, number, ptr

    length_type_id = packet[ptr]
    ptr += 1
    if length_type_id == "0":
        sub_packet_length = bin_to_int(packet[ptr : ptr + 15])
        ptr += 15
        sub_packet = packet[ptr : ptr + sub_packet_length]
        ptr += sub_packet_length
        sub_packets = []
        sub_ptr = 0
        while sub_ptr < sub_packet_length:
            v1, n1, sub_ptr = parse_packet(sub_packet, sub_ptr)
            sub_packets.append((v1, n1))

    else:
        number_of_sub_packets = bin_to_int(packet[ptr : ptr + 11])
        ptr += 11
        sub_packets = []
        for _ in range(number_of_sub_packets):
            v, n, ptr = parse_packet(packet, ptr)
            sub_packets.append((v, n))

    nums = [n for _, n in sub_packets]
    if type_id == 0:
        value = sum(nums)
    elif type_id == 1:
        value = math.prod(nums)
    elif type_id == 2:
        value = min(nums)
    elif type_id == 3:
        value = max(nums)
    elif type_id == 5:
        assert len(nums) == 2
        value = 1 if nums[0] > nums[1] else 0
    elif type_id == 6:
        assert len(nums) == 2
        value = 1 if nums[0] < nums[1] else 0
    elif type_id == 7:
        assert len(nums) == 2
        value = 1 if nums[0] == nums[1] else 0

    sub_version_sum = sum(v for v, n in sub_packets)
    return version + sub_version_sum, value, ptr


def part1(packet):
    bin_packet = "".join(hex_to_bin(c) for c in packet)
    version, _, _ = parse_packet(bin_packet)
    return version


def part2(packet):
    bin_packet = "".join(hex_to_bin(c) for c in packet)
    _, value, _ = parse_packet(bin_packet)
    return value


def main():
    hex_packet = input().strip()
    print(part1(hex_packet))
    print(part2(hex_packet))


if __name__ == "__main__":
    main()
